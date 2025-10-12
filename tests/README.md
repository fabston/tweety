# Tweety Library Tests

This directory contains comprehensive tests for the tweety Twitter scraping library.

## Quick Start

From the project root directory:

```bash
# List all available tests
python run_tests.py --list

# Run basic functionality tests
python run_tests.py test_basic

# Run the interactive demo
python run_tests.py demo

# Run all tests
python run_tests.py --all
```

## Test Files

### 🧪 Core Tests

- **`test_basic.py`** - Tests core functionality without authentication
- **`test_authenticated.py`** - Tests features requiring Twitter login
- **`test_comprehensive.py`** - Complete test suite with detailed reporting
- **`test_profile_images.py`** - Tests profile image URL functionality

### 🎮 Demos

- **`demo.py`** - Interactive demonstration of library features

### 📖 Documentation

- **`TESTING.md`** - Comprehensive testing guide and documentation

## Running Tests

### From Project Root (Recommended)

```bash
# Test runner with options
python run_tests.py <test_name>     # Run specific test
python run_tests.py --all           # Run all tests
python run_tests.py --list          # List available tests
```

### Direct Execution

```bash
# Run tests directly from this directory
python test_basic.py
python demo.py
```

## Test Results

- ✅ **PASS** - Test completed successfully
- ❌ **FAIL** - Test failed (check output for details)
- ⚠️ **WARNING** - Test completed with limitations

## Requirements

- Python 3.7+
- Virtual environment with tweety library installed
- Internet connection for API tests
- Optional: Twitter credentials for authenticated tests

## Session Files

Test session files (containing user data) are automatically ignored by git:
- `*.session`
- `test_*.session`
- `demo_*.session`

## Test Reports

Some tests generate detailed JSON reports:
- `test_report_*.json` - Comprehensive test results
- `debug_*.json` - Debug information (temporary)

These files are also ignored by git to keep the repository clean.

## Contributing

When adding new tests:

1. Follow the naming convention: `test_*.py` for tests, `demo*.py` for demos
2. Add proper imports with path handling for the new directory structure
3. Update this README if adding new test categories
4. Ensure tests work both from project root and directly from tests directory

## Troubleshooting

If tests fail to import the tweety library:

1. Make sure you're in the project root directory
2. Ensure the virtual environment is activated
3. Verify the library is installed: `pip install -e .`
4. Check that the path imports are correct in the test files

For more detailed troubleshooting, see `TESTING.md`.
