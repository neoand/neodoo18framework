#!/usr/bin/env python3
"""
OCA Watcher (v0.1)

- Summary mode (default): prints configured repos from .neodoo/oca_watch.yml
- Update mode (--update): uses GITHUB_TOKEN to fetch new releases/commits since last state,
  appends entries to docs/oca-digests/<repo>.md, and updates .neodoo/oca_state.json

Safety:
- First run initializes state to current tip without creating digests (avoids large first PR)
"""
from __future__ import annotations

import sys
import os
import json
import time
import urllib.parse
from datetime import datetime, timezone
from fnmatch import fnmatch
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover
    yaml = None
try:
    import requests  # type: ignore
except Exception:  # pragma: no cover
    requests = None

ROOT = Path(__file__).resolve().parents[1]
WATCH = ROOT / ".neodoo" / "oca_watch.yml"
STATE = ROOT / ".neodoo" / "oca_state.json"
DIGESTS_DIR = ROOT / "docs" / "oca-digests"


def load_yaml(path: Path) -> Dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML is not installed.")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def load_state(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {"keys": {}, "updated_at": None}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {"keys": {}, "updated_at": None}


def save_state(path: Path, state: Dict[str, Any]) -> None:
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def repo_key(repo: str, branch: str, monitor: str) -> str:
    return f"{repo}@{branch}::{monitor}"


def ensure_digests_dir() -> None:
    DIGESTS_DIR.mkdir(parents=True, exist_ok=True)


def digest_file_for_repo(repo: str) -> Path:
    safe = repo.replace("/", "-")
    return DIGESTS_DIR / f"{safe}.md"


def http_get(url: str, token: Optional[str], params: Optional[Dict[str, Any]] = None):
    if requests is None:  # type: ignore
        raise RuntimeError("requests not installed")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=20)
        if resp.status_code == 200:
            return resp
        else:
            print(f"WARN: GET {url} -> {resp.status_code} {resp.text[:200]}")
            return None
    except Exception as e:  # pragma: no cover
        print(f"ERROR: GET {url} failed: {e}")
        return None


def list_releases(repo: str, per_page: int = 10, token: Optional[str] = None) -> List[Dict[str, Any]]:
    url = f"https://api.github.com/repos/{repo}/releases"
    resp = http_get(url, token, params={"per_page": per_page})
    return resp.json() if resp else []


def list_commits(repo: str, branch: str, per_page: int = 10, token: Optional[str] = None) -> List[Dict[str, Any]]:
    url = f"https://api.github.com/repos/{repo}/commits"
    resp = http_get(url, token, params={"sha": branch, "per_page": per_page})
    return resp.json() if resp else []


def get_commit(repo: str, sha: str, token: Optional[str]) -> Optional[Dict[str, Any]]:
    url = f"https://api.github.com/repos/{repo}/commits/{urllib.parse.quote(sha)}"
    resp = http_get(url, token)
    return resp.json() if resp else None


def filter_commit_by_paths(commit_json: Dict[str, Any], include_globs: List[str]) -> bool:
    if not include_globs:
        return True
    files = commit_json.get("files", [])
    for f in files:
        filename = f.get("filename", "")
        if any(fnmatch(filename, g) for g in include_globs):
            return True
    return False


def append_digest(repo: str, lines: List[str]) -> None:
    ensure_digests_dir()
    df = digest_file_for_repo(repo)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    header = f"## {ts}\n\n"
    content = "\n".join(lines).rstrip() + "\n\n"
    if df.exists():
        prev = df.read_text(encoding="utf-8")
        new_text = prev + header + content
    else:
        title = f"# OCA Digest for {repo}\n\n"
        new_text = title + header + content
    df.write_text(new_text, encoding="utf-8")


def run_update(data: Dict[str, Any], state: Dict[str, Any], token: Optional[str], bootstrap: bool = False) -> bool:
    changed = False
    repos = data.get("repos", [])
    defaults = data.get("defaults", {})
    for r in repos:
        repo = r.get("repo")
        branch = r.get("branch") or defaults.get("branch", "main")
        monitor = r.get("monitor") or defaults.get("monitor", "commits")
        include_paths = r.get("include_paths") or []
        key = repo_key(repo, branch, monitor)
        last = state.get("keys", {}).get(key)

        print(f"Repo {repo} [{branch}] via {monitor}")
        if monitor == "releases":
            items = list_releases(repo, per_page=10, token=token)
            if not items:
                print("  No releases found or API error")
                continue
            latest = items[0]
            latest_id = str(latest.get("id"))
            if not last:
                state.setdefault("keys", {})[key] = latest_id
                if bootstrap:
                    new = items[:3]
                    if new:
                        lines = []
                        for it in reversed(new):
                            name = it.get("name") or it.get("tag_name")
                            url = it.get("html_url")
                            ts = it.get("published_at") or it.get("created_at")
                            lines.append(f"- Release {name} ({ts}) → {url}")
                        append_digest(repo, lines)
                        changed_here = True
                        print(f"  Bootstrapped {len(new)} release(s)")
                    else:
                        changed_here = False
                        print("  Initialized at latest release (no bootstrap items)")
                else:
                    print("  Initialized at latest release")
                    changed_here = False
            else:
                new = []
                for it in items:
                    if str(it.get("id")) == last:
                        break
                    new.append(it)
                if new:
                    lines = []
                    for it in reversed(new):
                        name = it.get("name") or it.get("tag_name")
                        url = it.get("html_url")
                        ts = it.get("published_at") or it.get("created_at")
                        lines.append(f"- Release {name} ({ts}) → {url}")
                    append_digest(repo, lines)
                    state["keys"][key] = latest_id
                    changed_here = True
                    print(f"  + {len(new)} release(s) captured")
                else:
                    changed_here = False
                    print("  Up-to-date")
        else:
            items = list_commits(repo, branch, per_page=10, token=token)
            if not items:
                print("  No commits found or API error")
                continue
            latest_sha = items[0].get("sha")
            if not last:
                state.setdefault("keys", {})[key] = latest_sha
                if bootstrap:
                    to_check = items[:5]
                    lines = []
                    kept = 0
                    for it in reversed(to_check):
                        sha = it.get("sha")
                        msg = (it.get("commit", {}) or {}).get("message", "").split("\n")[0]
                        url = it.get("html_url")
                        ok = True
                        if include_paths:
                            detail = get_commit(repo, sha, token)
                            ok = bool(detail and filter_commit_by_paths(detail, include_paths))
                            time.sleep(0.2)
                        if ok:
                            kept += 1
                            lines.append(f"- Commit {sha[:7]}: {msg} → {url}")
                    if lines:
                        append_digest(repo, lines)
                        changed_here = True
                        print(f"  Bootstrapped {kept} commit(s)")
                    else:
                        changed_here = False
                        print("  Initialized at tip commit (no bootstrap items)")
                else:
                    print("  Initialized at tip commit")
                    changed_here = False
            else:
                new = []
                for it in items:
                    if it.get("sha") == last:
                        break
                    new.append(it)
                if new:
                    lines = []
                    to_check = new[:5]
                    kept = 0
                    for it in reversed(to_check):
                        sha = it.get("sha")
                        msg = (it.get("commit", {}) or {}).get("message", "").split("\n")[0]
                        url = it.get("html_url")
                        ok = True
                        if include_paths:
                            detail = get_commit(repo, sha, token)
                            ok = bool(detail and filter_commit_by_paths(detail, include_paths))
                            time.sleep(0.2)
                        if ok:
                            kept += 1
                            lines.append(f"- Commit {sha[:7]}: {msg} → {url}")
                    if lines:
                        append_digest(repo, lines)
                        state["keys"][key] = latest_sha
                        changed_here = True
                        print(f"  + {kept} commit(s) captured")
                    else:
                        state["keys"][key] = latest_sha
                        changed_here = False
                        print("  No relevant commits by include_paths; advanced pointer")
                else:
                    changed_here = False
                    print("  Up-to-date")

        changed = changed or changed_here

    save_state(STATE, state)
    return changed


def main() -> int:
    if not WATCH.exists():
        print(f"Watchlist not found: {WATCH}")
        return 1
    try:
        data = load_yaml(WATCH)
    except Exception as e:
        print(f"YAML error: {e}")
        return 2

    if len(sys.argv) == 1:
        repos = data.get("repos", [])
        print(f"OCA watchlist: {len(repos)} repos configured")
        for r in repos:
            repo = r.get("repo")
            branch = r.get("branch") or data.get("defaults", {}).get("branch", "main")
            monitor = r.get("monitor") or data.get("defaults", {}).get("monitor", "commits")
            areas = ",".join(r.get("areas", [])) or "-"
            print(f"- {repo} [{branch}] via {monitor} | areas: {areas}")
        return 0

    if "--update" in sys.argv:
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            print("GITHUB_TOKEN not found; cannot query GitHub API.")
            return 3
        bootstrap = "--bootstrap" in sys.argv or os.getenv("OCA_BOOTSTRAP") == "true"
        state = load_state(STATE)
        changed = run_update(data, state, token, bootstrap=bootstrap)
        print("Digest/state updated." if changed else "No changes found (state updated if initialized).")
        return 0

    print("Usage: oca_watch.py [--update] [--bootstrap]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
