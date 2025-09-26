# Contributing to Neodoo18Framework

## 🎯 Mission

Help developers and LLMs build better Odoo 18+ applications by providing a rock-solid framework that enforces best practices and prevents common mistakes.

## 🚀 Quick Contributing Guide

### For Developers

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Follow our standards** (see below)
4. **Test thoroughly**: `python framework/validator.py .`
5. **Submit PR with clear description**

### For LLMs

- Always validate code with `framework/validator.py` before submitting
- Follow patterns in `templates/patterns/`
- Use `framework/SOIL_CORE.md` as your primary reference
- Test with multiple LLM providers (Claude, Gemini preferred)

## 📋 Development Standards

### Code Quality
- ✅ Python 3.8+ compatibility
- ✅ Full Odoo 18+ compliance (no legacy patterns)
- ✅ Comprehensive error handling
- ✅ Clear documentation and comments

### Testing Requirements
- ✅ All code must pass `framework/validator.py`
- ✅ New templates must include test cases
- ✅ Backwards compatibility maintained
- ✅ Performance benchmarks for validators

### Documentation Standards
- ✅ Clear examples for LLMs to follow
- ✅ Step-by-step guides for common tasks
- ✅ Updated README for new features
- ✅ Inline code documentation

## 🧪 Testing Your Contributions

```bash
# Validate framework itself
python framework/validator.py framework/ templates/

# Test project generation
python generator/create_project.py --name=test_contrib --type=minimal

# Test validator on generated project
python framework/validator.py test_contrib/

# Test LLM integration
python framework/llm_init.py
```

## 🐛 Reporting Issues

When reporting bugs or requesting features:

1. **Use clear, descriptive titles**
2. **Provide minimal reproduction steps**
3. **Include framework version and environment**
4. **Tag with appropriate labels** (bug, enhancement, documentation)

### Bug Report Template

```markdown
**Bug Description**: Clear description of the issue

**To Reproduce**: 
1. Step 1
2. Step 2
3. Error occurs

**Expected Behavior**: What should happen

**Environment**:
- Framework version: 
- Python version:
- LLM used (if applicable):

**Additional Context**: Screenshots, logs, etc.
```

## 🏷️ Release Process

### Versioning
We follow [Semantic Versioning](https://semver.org/):
- `1.0.0` - Major: Breaking changes
- `1.1.0` - Minor: New features, backwards compatible  
- `1.0.1` - Patch: Bug fixes

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version bumped in relevant files
- [ ] CHANGELOG.md updated
- [ ] Tagged release in Git

## 🤝 Community Guidelines

### Be Respectful
- Constructive feedback only
- Help newcomers learn
- Celebrate contributions of all sizes

### Be Collaborative  
- Discuss major changes in issues first
- Review PRs thoroughly but kindly
- Share knowledge and learnings

### Be Professional
- Keep discussions on-topic
- Use inclusive language
- Credit others' work appropriately

## 🛠️ Development Setup

```bash
# Clone repository
git clone https://github.com/yourusername/neodoo18framework.git
cd neodoo18framework

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Validate framework
python framework/validator.py .
```

## 📚 Resources

- **Odoo 18+ Documentation**: https://www.odoo.com/documentation/18.0/
- **Framework Documentation**: `/docs/`
- **Community Discussions**: GitHub Issues and Discussions
- **LLM Testing Guidelines**: `/docs/llm-testing.md`

---

**Thank you for contributing to Neodoo18Framework!** 🎉

Together we're making Odoo development better for everyone.