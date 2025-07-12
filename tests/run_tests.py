#!/usr/bin/env python3
"""
Test runner for PyEPlan unit tests.

This script runs all unit tests for the PyEPlan package and provides
a comprehensive test report.
"""

import unittest
import sys
import os
import argparse
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def run_all_tests(verbose=False, pattern=None):
    """
    Run all PyEPlan unit tests.
    
    Args:
        verbose (bool): Enable verbose output
        pattern (str): Pattern to match test files
    
    Returns:
        unittest.TestResult: Test results
    """
    # Discover and run tests
    loader = unittest.TestLoader()
    
    if pattern:
        loader.testNamePatterns = [pattern]
    
    # Start from the tests directory
    start_dir = os.path.join(project_root, 'tests')
    
    # Discover tests
    suite = loader.discover(
        start_dir=start_dir,
        pattern='test_*.py',
        top_level_dir=project_root
    )
    
    # Run tests
    runner = unittest.TextTestRunner(
        verbosity=2 if verbose else 1,
        stream=sys.stdout
    )
    
    result = runner.run(suite)
    return result

def run_specific_test(test_module, verbose=False):
    """
    Run a specific test module.
    
    Args:
        test_module (str): Name of the test module to run
        verbose (bool): Enable verbose output
    
    Returns:
        unittest.TestResult: Test results
    """
    # Import the test module
    test_module_path = f"tests.{test_module}"
    
    try:
        module = __import__(test_module_path, fromlist=[''])
    except ImportError as e:
        print(f"Error importing test module {test_module}: {e}")
        return None
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(module)
    
    # Run tests
    runner = unittest.TextTestRunner(
        verbosity=2 if verbose else 1,
        stream=sys.stdout
    )
    
    result = runner.run(suite)
    return result

def print_test_summary(result):
    """
    Print a summary of test results.
    
    Args:
        result (unittest.TestResult): Test results
    """
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED")
    
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Exception:')[-1].strip()}")

def main():
    """Main function to run tests."""
    parser = argparse.ArgumentParser(description='Run PyEPlan unit tests')
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--module', '-m',
        type=str,
        help='Run tests from a specific module (e.g., test_dataproc)'
    )
    parser.add_argument(
        '--pattern', '-p',
        type=str,
        help='Pattern to match test names'
    )
    parser.add_argument(
        '--list', '-l',
        action='store_true',
        help='List available test modules'
    )
    
    args = parser.parse_args()
    
    # List available test modules
    if args.list:
        test_dir = os.path.join(project_root, 'tests')
        test_files = [f for f in os.listdir(test_dir) if f.startswith('test_') and f.endswith('.py')]
        
        print("Available test modules:")
        for test_file in sorted(test_files):
            module_name = test_file[:-3]  # Remove .py extension
            print(f"  - {module_name}")
        return
    
    # Run specific module
    if args.module:
        print(f"Running tests from module: {args.module}")
        result = run_specific_test(args.module, args.verbose)
        if result:
            print_test_summary(result)
            sys.exit(0 if result.wasSuccessful() else 1)
        else:
            sys.exit(1)
    
    # Run all tests
    print("Running all PyEPlan unit tests...")
    result = run_all_tests(args.verbose, args.pattern)
    print_test_summary(result)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)

if __name__ == '__main__':
    main() 