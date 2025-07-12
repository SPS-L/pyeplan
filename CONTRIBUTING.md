# Contributing to PyEPlan

Thank you for your interest in contributing to PyEPlan! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Guidelines](#documentation-guidelines)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

- Use the GitHub issue tracker
- Include a clear and descriptive title
- Provide detailed steps to reproduce the bug
- Include system information (OS, Python version, etc.)
- Attach relevant files or error messages

### Suggesting Enhancements

- Use the GitHub issue tracker with the "enhancement" label
- Describe the feature and its benefits
- Provide use cases and examples
- Consider implementation complexity

### Code Contributions

- Fork the repository
- Create a feature branch
- Make your changes
- Add tests for new functionality
- Ensure all tests pass
- Submit a pull request

## Development Setup

### Prerequisites

- Python 3.7 or higher
- Git
- pip

### Local Development Installation

```bash
# Clone the repository
git clone https://github.com/SPS-L/pyeplan.git
cd pyeplan

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e .
pip install -r requirements.txt

# Install additional development tools
pip install pytest pytest-cov black flake8 mypy
```

### Development Dependencies

The following tools are recommended for development:

- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **black**: Code formatting
- **flake8**: Linting
- **mypy**: Type checking

## Code Style Guidelines

### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use 4 spaces for indentation
- Maximum line length of 88 characters (Black default)
- Use meaningful variable and function names
- Add type hints where appropriate

### Code Formatting

We use [Black](https://black.readthedocs.io/) for automatic code formatting:

```bash
# Format all Python files
black pyeplan/ tests/

# Check formatting without making changes
black --check pyeplan/ tests/
```

### Linting

We use [flake8](https://flake8.pycqa.org/) for linting:

```bash
# Run flake8
flake8 pyeplan/ tests/

# Configuration in setup.cfg or pyproject.toml
```

### Type Checking

We use [mypy](http://mypy-lang.org/) for static type checking:

```bash
# Run type checking
mypy pyeplan/
```

## Testing Guidelines

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=pyeplan

# Run specific test file
pytest tests/test_dataproc.py

# Run tests with verbose output
pytest tests/ -v
```

### Writing Tests

- Write tests for all new functionality
- Use descriptive test names
- Follow the existing test structure
- Mock external dependencies (APIs, solvers)
- Test both success and failure cases
- Aim for high test coverage

### Test Structure

```python
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import os

class TestNewFeature(unittest.TestCase):
    """Test cases for new feature."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_basic_functionality(self):
        """Test basic functionality of new feature."""
        # Test implementation
        pass
    
    @patch('pyeplan.external_api.call')
    def test_with_mocked_dependency(self, mock_api):
        """Test with mocked external dependency."""
        mock_api.return_value = {'result': 'success'}
        # Test implementation
        pass
```

## Documentation Guidelines

### Code Documentation

- Use docstrings for all public functions and classes
- Follow [Google docstring style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Include parameter types and return types
- Provide usage examples for complex functions

### Example Docstring

```python
def optimize_microgrid(input_folder: str, solver: str = 'glpk') -> dict:
    """Optimize microgrid investment and operation.
    
    This function formulates and solves a mixed-integer linear programming
    problem for microgrid planning.
    
    Args:
        input_folder: Path to folder containing input data files
        solver: Optimization solver to use ('glpk', 'cbc', 'gurobi')
    
    Returns:
        Dictionary containing optimization results
        
    Raises:
        FileNotFoundError: If input files are missing
        ValueError: If solver is not supported
        
    Example:
        >>> results = optimize_microgrid("examples/5_bus/", solver='glpk')
        >>> print(results['total_cost'])
        125000.0
    """
    pass
```

### Documentation Updates

- Update README.md for new features
- Update API documentation in docs/
- Add examples for new functionality
- Update installation instructions if needed

## Pull Request Process

### Before Submitting

1. **Ensure tests pass**: Run the full test suite
2. **Check code style**: Run Black and flake8
3. **Update documentation**: Add/update relevant docs
4. **Add tests**: Include tests for new functionality
5. **Update examples**: Add examples if applicable

### Pull Request Guidelines

1. **Clear title**: Descriptive title for the PR
2. **Detailed description**: Explain what and why, not how
3. **Reference issues**: Link to related issues
4. **Screenshots**: Include for UI changes
5. **Test results**: Show that tests pass

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Test addition
- [ ] Other (please describe)

## Testing
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes
```

## Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

1. **Update version**: Update version in `__init__.py`
2. **Update changelog**: Document changes in README or CHANGELOG
3. **Run full test suite**: Ensure all tests pass
4. **Update documentation**: Ensure docs are current
5. **Create release**: Tag and create GitHub release
6. **Publish to PyPI**: Upload to Python Package Index

### Release Commands

```bash
# Update version
# Edit pyeplan/__init__.py and pyproject.toml

# Run tests
pytest tests/ --cov=pyeplan

# Build package
python -m build

```

## Getting Help

- **GitHub Issues**: For bug reports and feature requests
- **Email**: s.dehghan@ieee.org
- **Documentation**: https://pyeplan.sps-lab.org/

## Acknowledgments

Thank you to all contributors who have helped make PyEPlan better!

## License

By contributing to PyEPlan, you agree that your contributions will be licensed under the Apache Software License. 