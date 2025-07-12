# PyEPlan Unit Tests

This directory contains comprehensive unit tests for the PyEPlan package. The tests cover all major functionality including data processing, network routing, and investment/operation optimization.

## Test Structure

### Test Files

- **`test_dataproc.py`**: Tests for the data processing module (`datsys`)
  - PVGIS API integration
  - Time series clustering
  - Data preprocessing and file generation
  - Power factor calculations
  - Timezone handling

- **`test_routing.py`**: Tests for the network routing module (`rousys`)
  - Minimum spanning tree algorithm
  - Geographic distance calculations
  - Cable parameter calculations
  - Network topology generation
  - File output validation

- **`test_investoper.py`**: Tests for the investment/operation optimization module (`inosys`)
  - Model initialization and data loading
  - Optimization problem formulation
  - Solver integration
  - Result processing and output generation
  - Utility functions

- **`test_pyeplan_integration.py`**: Integration tests for complete workflows
  - End-to-end data processing, routing, and optimization
  - Integration between all modules
  - Real-world example scenarios
  - Error handling and edge cases

### Test Categories

1. **Unit Tests**: Test individual functions and methods in isolation
2. **Integration Tests**: Test interactions between modules
3. **Workflow Tests**: Test complete end-to-end workflows
4. **Error Handling Tests**: Test error conditions and edge cases

## Running Tests

### Prerequisites

- Python 3.7 or higher
- All PyEPlan dependencies installed
- Example data files (optional, for integration tests)

### Running All Tests

```bash
# From the project root directory
python tests/run_tests.py

# With verbose output
python tests/run_tests.py --verbose

# Run specific test module
python tests/run_tests.py --module test_dataproc

# List available test modules
python tests/run_tests.py --list
```

### Using unittest directly

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_dataproc

# Run specific test class
python -m unittest tests.test_dataproc.TestDatsys

# Run specific test method
python -m unittest tests.test_dataproc.TestDatsys.test_init_basic_parameters
```

### Using pytest (if installed)

```bash
# Install pytest
pip install pytest

# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_dataproc.py

# Run tests matching pattern
pytest tests/ -k "test_init"
```

## Test Coverage

### Data Processing Module (`datsys`)

- ✅ Initialization with various parameters
- ✅ PVGIS API integration (mocked)
- ✅ Time series data extraction
- ✅ K-means clustering
- ✅ File generation and output validation
- ✅ Timezone detection
- ✅ Power factor calculations
- ✅ Error handling for invalid inputs

### Network Routing Module (`rousys`)

- ✅ Initialization with various parameters
- ✅ Cable parameter calculations
- ✅ Base value calculations
- ✅ Minimum spanning tree generation
- ✅ Geographic distance calculations
- ✅ Network topology validation
- ✅ File output validation
- ✅ Error handling for invalid inputs

### Investment/Operation Module (`inosys`)

- ✅ Initialization with various parameters
- ✅ Data loading and validation
- ✅ Component counting
- ✅ Power conversion to per-unit
- ✅ Optimization problem formulation (mocked)
- ✅ Result processing
- ✅ Error handling for missing files
- ✅ Utility functions

### Integration Tests

- ✅ Complete workflow testing
- ✅ Module interaction testing
- ✅ Real example data processing
- ✅ Error handling and edge cases
- ✅ Import and attribute validation

## Mocking Strategy

The tests use mocking to isolate units and avoid external dependencies:

- **PVGIS API**: Mocked to avoid network calls during testing
- **Optimization Solvers**: Mocked to avoid requiring solver installations
- **File System**: Uses temporary directories for file operations
- **Network Operations**: Mocked where appropriate

## Test Data

### Synthetic Test Data

The tests create minimal synthetic datasets that cover all required file formats and data structures. This ensures tests can run independently without external data dependencies.

### Real Example Data

Integration tests use real example data from the `examples/` directory when available. These tests are skipped if the example data is not present.

## Continuous Integration

The tests are designed to work in CI/CD environments:

- No external network dependencies (all APIs are mocked)
- No external solver dependencies (optimization is mocked)
- Fast execution (minimal data processing)
- Clear pass/fail criteria
- Comprehensive error reporting

## Adding New Tests

When adding new functionality to PyEPlan, follow these guidelines:

1. **Create unit tests** for new functions and methods
2. **Add integration tests** for new workflows
3. **Test error conditions** and edge cases
4. **Use descriptive test names** that explain what is being tested
5. **Include docstrings** explaining the test purpose
6. **Mock external dependencies** to keep tests fast and reliable

### Example Test Structure

```python
def test_new_feature_basic_functionality(self):
    """Test basic functionality of new feature."""
    # Arrange
    test_data = create_test_data()
    
    # Act
    result = new_feature(test_data)
    
    # Assert
    self.assertIsNotNone(result)
    self.assertEqual(result.expected_attribute, expected_value)

def test_new_feature_error_handling(self):
    """Test error handling for new feature."""
    # Arrange
    invalid_data = create_invalid_data()
    
    # Act & Assert
    with self.assertRaises(ValueError):
        new_feature(invalid_data)
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure PyEPlan is installed or the project root is in the Python path
2. **Missing Dependencies**: Install all required packages from `requirements.txt`
3. **File Permission Errors**: Ensure write permissions in the test directory
4. **Timeout Errors**: Some tests may take longer on slower systems

### Debug Mode

Run tests with verbose output to see detailed information:

```bash
python tests/run_tests.py --verbose
```

### Running Individual Tests

To debug a specific test, run it individually:

```bash
python -m unittest tests.test_dataproc.TestDatsys.test_init_basic_parameters -v
```

## Contributing

When contributing to PyEPlan:

1. **Write tests** for new functionality
2. **Ensure all tests pass** before submitting
3. **Add tests** for bug fixes
4. **Update tests** when changing existing functionality
5. **Follow the existing test patterns** and conventions 