#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Neodoo18Framework Project Generator
Creates new Odoo 18+ modules with proper structure and compliance
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime

class ProjectGenerator:
    """Generate new Odoo 18+ modules from templates"""
    
    def __init__(self):
        self.framework_root = Path(__file__).parent.parent.parent
        self.templates_dir = self.framework_root / 'templates'
        
    def create_project(self, name: str, project_type: str = 'minimal', output_dir: str = None, 
                      author: str = None, company: str = None, email: str = None, 
                      description: str = None, all_placeholders: bool = True, dry_run: bool = False):
        """Create a new module from template"""
        
        # Validate inputs
        if not name.replace('_', '').replace('-', '').isalnum():
            raise ValueError(f"Invalid module name: {name}. Use only letters, numbers, underscore and hyphens.")
            
        # Prefer direct template directory (e.g., templates/minimal) when it exists.
        # Fall back to "-project" variant (e.g., templates/minimal-project) when only that exists.
        direct_template = self.templates_dir / project_type
        project_variant = self.templates_dir / f"{project_type}-project"

        if direct_template.exists():
            template_path = direct_template
        elif project_variant.exists():
            template_path = project_variant
        else:
            # Build a de-duplicated list of available template names
            names = set()
            for d in self.templates_dir.iterdir():
                if not d.is_dir():
                    continue
                n = d.name
                if n.endswith('-project'):
                    n = n[:-8]
                names.add(n)
            available = sorted(names)
            raise ValueError(f"Template '{project_type}' not found. Available: {', '.join(available)}")
        
        # Determine output directory
        if output_dir is None:
            output_dir = Path.cwd() / name
        else:
            output_dir = Path(output_dir) / name
            
        if output_dir.exists():
            raise ValueError(f"Directory already exists: {output_dir}")
        
        print(f"🚀 Creating module '{name}' using '{project_type}' template...")
        
        # Copy template
        shutil.copytree(template_path, output_dir)
        
        # Customize project with additional parameters
        self._customize_project(
            output_dir,
            name,
            project_type,
            author,
            company,
            email,
            description,
            all_placeholders,
            dry_run,
        )
        
        print(f"✅ Project created successfully!")
        print(f"📁 Location: {output_dir}")
        print(f"\n🔄 Next steps:")
        print(f"   cd {output_dir}")
        print(f"   ./init_project.sh")
        print(f"   python -m framework.validator .")
        
        return output_dir
    
    def _customize_project(self, project_dir: Path, name: str, project_type: str, 
                          author: str = None, company: str = None, email: str = None, 
                          description: str = None, all_placeholders: bool = True, dry_run: bool = False):
        """Customize the copied template with project-specific values"""
        
        # Derive sane defaults for model-related placeholders
        def to_camel(s: str) -> str:
            parts = re.split(r'[^a-zA-Z0-9]+', s)
            return ''.join(p.capitalize() for p in parts if p)

        import re
        module_class_prefix = to_camel(name)
        default_model_name = 'record'
        default_model_description = f"{name.replace('_', ' ')} record"

        replacements = {
            '{{PROJECT_NAME}}': name,
            '{{MODULE_NAME}}': name.replace('_', ' ').title(),
            '{{MODULE_TECHNICAL_NAME}}': name,
            '{{PROJECT_TYPE}}': project_type,
            '{{CREATION_DATE}}': datetime.now().strftime('%Y-%m-%d'),
            '{{FRAMEWORK_VERSION}}': '1.0.0',
            '{{AUTHOR}}': author or 'Your Name',
            '{{COMPANY}}': company or 'Your Company', 
            '{{WEBSITE}}': f'https://{company.lower().replace(" ", "")}.com' if company else 'https://yourwebsite.com',
            '{{EMAIL}}': email or 'your.email@example.com',
            '{{DESCRIPTION}}': description or f'Module for managing {name.replace("_", " ")}',
            '{{CATEGORY}}': 'Operations',
            '{{SUMMARY}}': description or f'{name.replace("_", " ").title()} management module',
            '{{IS_APPLICATION}}': 'True',
            # Model-related placeholders used by some templates
            '{{MODEL_NAME}}': default_model_name,
            '{{MODULE_CLASS}}': f'{module_class_prefix}Record',
            '{{MODEL_DESCRIPTION}}': default_model_description,
        }
        
        if all_placeholders:
            # Process most text-like files across the project
            exts = {'.py', '.xml', '.csv', '.md', '.rst', '.txt'}
            for path in project_dir.rglob('*'):
                if path.is_file() and path.suffix in exts:
                    try:
                        content = path.read_text(encoding='utf-8')
                    except Exception:
                        continue
                    new_content = content
                    for placeholder, replacement in replacements.items():
                        new_content = new_content.replace(placeholder, replacement)
                    if new_content != content:
                        if dry_run:
                            print(f"DRY-RUN: would replace placeholders in {path.relative_to(project_dir)}")
                        else:
                            path.write_text(new_content, encoding='utf-8')
        else:
            # Backward-compatible minimal replacements
            files_to_process = [
                'README.md',
                '__manifest__.py',
                'models/__init__.py'
            ]
            for file_rel_path in files_to_process:
                file_path = project_dir / file_rel_path
                if file_path.exists():
                    content = file_path.read_text(encoding='utf-8')
                    for placeholder, replacement in replacements.items():
                        content = content.replace(placeholder, replacement)
                    file_path.write_text(content, encoding='utf-8')
        
        # After content replacement, rename files and directories containing placeholders in their names
        self._rename_paths_with_placeholders(project_dir, replacements, dry_run)

        # Make scripts executable
        for script in ['init_project.sh', 'validate_odoo18.sh']:
            script_path = project_dir / script
            if script_path.exists():
                os.chmod(script_path, 0o755)

    def _rename_paths_with_placeholders(self, project_dir: Path, replacements: dict, dry_run: bool = False):
        """Rename files and directories whose names contain known placeholders.

        We traverse depth-first (deepest paths first) to avoid conflicts during renames.
        """
        # Collect all paths and sort by depth descending so children are renamed before parents
        paths = list(project_dir.rglob('*'))
        paths.sort(key=lambda p: len(p.relative_to(project_dir).parts), reverse=True)

        for path in paths:
            old_name = path.name
            new_name = old_name
            for placeholder, replacement in replacements.items():
                new_name = new_name.replace(placeholder, replacement)
            if new_name != old_name:
                new_path = path.with_name(new_name)
                if dry_run:
                    print(f"DRY-RUN: would rename {path.relative_to(project_dir)} -> {new_path.relative_to(project_dir)}")
                else:
                    path.rename(new_path)
    
    def list_templates(self):
        """List available project templates (deduplicated).

        Preference order for description/path: direct template dir > -project variant.
        """
        # Map template name -> directory path to prefer
        preferred: dict[str, Path] = {}

        # First collect direct templates (preferred)
        for d in self.templates_dir.iterdir():
            if d.is_dir() and not d.name.endswith('-project'):
                preferred[d.name] = d

        # Then add -project variants only if direct not present
        for d in self.templates_dir.glob('*-project'):
            name = d.name[:-8]
            preferred.setdefault(name, d)

        templates = []
        for name in sorted(preferred.keys()):
            template_dir = preferred[name]
            # Read template info if available
            info_file = template_dir / 'TEMPLATE_INFO.md'
            description = "No description available"
            if info_file.exists():
                content = info_file.read_text(encoding='utf-8')
                lines = content.split('\n')
                if lines and lines[0].startswith('# '):
                    description = lines[0][2:].strip()
            templates.append({
                'name': name,
                'description': description,
                'path': template_dir,
            })

        return templates

def main():
    """CLI interface for project generator"""
    parser = argparse.ArgumentParser(
        description="Neodoo18Framework Project Generator",
        epilog="Example: python create_project.py --name=my_crm --type=minimal"
    )
    
    parser.add_argument('--name', required=True, help='Project name (must be valid Python identifier)')
    parser.add_argument('--type', default='minimal', help='Project template type (default: minimal)')
    parser.add_argument('--output', help='Output directory (default: current directory)')
    parser.add_argument('--author', help='Author name')
    parser.add_argument('--company', help='Company name') 
    parser.add_argument('--email', help='Author email')
    parser.add_argument('--description', help='Module description')
    parser.add_argument('--list-templates', action='store_true', help='List available templates')
    parser.add_argument('--all-placeholders', dest='all_placeholders', action='store_true', default=True, help='Replace placeholders across all supported files (default)')
    parser.add_argument('--no-all-placeholders', dest='all_placeholders', action='store_false', help='Limit replacements to core files only')
    parser.add_argument('--dry-run', action='store_true', help='Preview placeholder replacements without writing changes')
    
    args = parser.parse_args()
    
    generator = ProjectGenerator()
    
    if args.list_templates:
        print("📦 Available Project Templates:")
        print("=" * 50)
        
        templates = generator.list_templates()
        
        for template in templates:
            print(f"• {template['name']}: {template['description']}")
        
        return
    
    try:
        project_dir = generator.create_project(
            name=args.name,
            project_type=args.type,
            output_dir=args.output,
            author=args.author,
            company=args.company,
            email=args.email,
            description=args.description,
            all_placeholders=args.all_placeholders,
            dry_run=args.dry_run
        )
        
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ Error creating project: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()