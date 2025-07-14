# Contributing to PyEPlan

## Version Management

### Current Version
PyEPlan follows semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR**: Breaking changes, incompatible API changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### Version Bumping

#### Using bump2version (Recommended)
```bash
# Install bump2version
pip install bump2version

# Bump versions
bump2version patch  # 1.1.1 → 1.1.2 (bug fixes)
bump2version minor  # 1.1.1 → 1.2.0 (new features)
bump2version major  # 1.1.1 → 2.0.0 (breaking changes)
```

#### Using Custom Script
```bash
# Bump to specific version
python scripts/bump_version.py 1.1.2
```

#### Manual Version Update
1. Update `pyeplan/__init__.py` line 67:
   ```python
   __version__ = '1.1.2'
   ```
2. Update `.bumpversion.cfg`:
   ```ini
   current_version = 1.1.2
   ```

### Release Process
1. Bump version using one of the methods above
2. Update CHANGELOG.md with release notes
3. Create git tag: `git tag v1.1.2`
4. Push changes and tag: `git push origin main --tags`
5. Create GitHub release with release notes

### Development Versions
For development builds, use suffixes:
- `1.1.1.dev0` - Development version
- `1.1.1a1` - Alpha release
- `1.1.1b1` - Beta release
- `1.1.1rc1` - Release candidate

## Development Setup

### Prerequisites
- Python 3.7+
- Git

### Installation
```bash
# Clone repository
git clone https://github.com/SPS-L/pyeplan.git
cd pyeplan

# Install in development mode
pip install -e .

# Install development dependencies
pip install -r requirements.txt
```

### Testing
```bash
# Run tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_dataproc.py
```

### Code Quality
```bash
# Format code
black pyeplan/ tests/

# Lint code
flake8 pyeplan/ tests/

# Type checking (if using mypy)
mypy pyeplan/
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Update documentation if needed
7. Commit your changes: `git commit -m 'Add amazing feature'`
8. Push to your fork: `git push origin feature/amazing-feature`
9. Create a Pull Request

### Commit Message Guidelines
- Use present tense: "Add feature" not "Added feature"
- Use imperative mood: "Move cursor to..." not "Moves cursor to..."
- Limit first line to 72 characters
- Reference issues and pull requests after first line

Example:
```
Add solar irradiance data fetching from PVGIS API

- Implement PVGIS API client
- Add data validation and error handling
- Include unit tests for API integration

Fixes #123
```

## Code Style

### Python
- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for all public functions and classes
- Keep functions focused and under 50 lines when possible

### Documentation
- Update docstrings for any changed functions
- Add examples in docstrings
- Update README.md for new features
- Update user guide for significant changes

## Reporting Issues

When reporting bugs, please include:
- Python version
- Operating system
- PyEPlan version
- Minimal example to reproduce the issue
- Expected vs actual behavior
- Error messages and stack traces

## License

By contributing to PyEPlan, you agree that your contributions will be licensed under the Apache Software License. 