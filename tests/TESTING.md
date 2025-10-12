# Testing the Tweety Library

This document explains how to test the tweety library to ensure it's working correctly.

## Quick Start

### 1. Install Dependencies

First, make sure you have the library installed in a virtual environment:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the library
pip install -e .
```

### 2. Run Basic Tests

Test the core functionality without authentication:

```bash
# From project root
python run_tests.py test_basic

# Or directly from tests directory
python tests/test_basic.py
```

This will test:
- ✅ Library import and initialization
- ✅ Public user information retrieval
- ✅ Public tweets retrieval
- ✅ Basic class properties and methods

### 3. Run Demo

See the library in action with a simple demo:

```bash
# From project root
python run_tests.py demo

# Or directly from tests directory
python tests/demo.py
```

This interactive demo shows:
- 🌐 Public features (no authentication required)
- 🔐 Authenticated features (optional, requires credentials)
- 🔄 Synchronous vs asynchronous usage

## Test Runner

The project includes a convenient test runner script that allows you to run tests from the project root:

```bash
# List all available tests
python run_tests.py --list

# Run a specific test
python run_tests.py test_basic

# Run all tests
python run_tests.py --all

# Run the demo
python run_tests.py demo
```

## Test Scripts Overview

### `test_basic.py`
**Purpose**: Test core functionality without authentication
**Requirements**: None
**What it tests**:
- Library import and initialization
- Public user information retrieval
- Public tweets retrieval
- Class properties and methods
- Error handling

**Expected Results**: All tests should pass ✅

### `test_authenticated.py`
**Purpose**: Test features that require Twitter authentication
**Requirements**: Valid Twitter credentials
**What it tests**:
- User authentication
- Trends retrieval
- Search functionality
- User followers/followings
- Advanced features (GIF search, place search, etc.)

**Usage**:
```bash
# From project root
python run_tests.py test_authenticated

# Or directly from tests directory
python tests/test_authenticated.py
```

### `test_comprehensive.py`
**Purpose**: Complete test suite covering all major features
**Requirements**: Optional authentication for full testing
**What it tests**:
- All basic functionality
- All authenticated features
- Error handling
- Advanced features
- Generates detailed JSON report

**Usage**:
```bash
# From project root
python run_tests.py test_comprehensive

# Or directly from tests directory
python tests/test_comprehensive.py
```

### `demo.py`
**Purpose**: Interactive demonstration of library features
**Requirements**: Optional authentication for full demo
**What it shows**:
- Real-world usage examples
- Public vs authenticated features
- Synchronous vs asynchronous usage

## Test Results Interpretation

### ✅ PASS
The test completed successfully and the feature is working as expected.

### ❌ FAIL
The test failed. This could be due to:
- Network connectivity issues
- Twitter API changes
- Invalid credentials (for authenticated tests)
- Rate limiting

### ⚠️ WARNING
The test completed but with limitations (e.g., private account data not accessible).

## Common Issues and Solutions

### 1. Import Errors
**Error**: `ModuleNotFoundError: No module named 'tweety'`
**Solution**: Make sure you're in the virtual environment and the library is installed:
```bash
source venv/bin/activate
pip install -e .
```

### 2. Authentication Failures
**Error**: Login failed or authentication errors
**Solutions**:
- Verify your Twitter credentials are correct
- Check if your account has 2FA enabled (may need app password)
- Ensure your account is not suspended or restricted

### 3. Rate Limiting
**Error**: Too many requests or rate limit exceeded
**Solutions**:
- Wait before retrying
- Use smaller page counts in tests
- Implement delays between requests

### 4. Network Issues
**Error**: Connection timeouts or network errors
**Solutions**:
- Check your internet connection
- Try again later
- Use a VPN if Twitter is blocked in your region

## Testing Best Practices

### 1. Start with Basic Tests
Always run `test_basic.py` first to ensure the core functionality works.

### 2. Use Small Page Counts
When testing, use `pages=1` to avoid hitting rate limits:
```python
tweets = await app.get_tweets("username", pages=1)
```

### 3. Handle Errors Gracefully
The library may raise exceptions for various reasons. Always wrap calls in try-catch blocks:
```python
try:
    user = await app.get_user_info("username")
    if user:
        print(f"User: @{user.username}")
except Exception as e:
    print(f"Error: {e}")
```

### 4. Respect Rate Limits
Twitter has rate limits. The library includes built-in delays, but be mindful of:
- Making too many requests in a short time
- Testing with large page counts
- Running multiple test scripts simultaneously

## Advanced Testing

### Custom Test Scenarios

You can create custom test scenarios by modifying the existing test scripts or creating new ones:

```python
import asyncio
from tweety import TwitterAsync

async def custom_test():
    app = TwitterAsync("test_session")
    
    # Test specific functionality
    try:
        user = await app.get_user_info("your_test_username")
        print(f"User found: @{user.username}")
    except Exception as e:
        print(f"Test failed: {e}")

# Run the test
asyncio.run(custom_test())
```

### Performance Testing

To test performance, you can measure execution times:

```python
import time

start_time = time.time()
tweets = await app.get_tweets("username", pages=1)
end_time = time.time()

print(f"Retrieved {len(tweets)} tweets in {end_time - start_time:.2f} seconds")
```

## Troubleshooting

### Check Library Version
```python
import tweety
print(f"Tweety version: {tweety.__version__}")
```

### Check Dependencies
```bash
pip list | grep -E "(httpx|beautifulsoup4|openpyxl)"
```

### Debug Mode
Enable debug logging to see detailed request/response information:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Support

If you encounter issues:

1. Check this testing guide
2. Review the test output for specific error messages
3. Check the [main documentation](https://mahrtayyab.github.io/tweety_docs/)
4. Report issues on the [GitHub repository](https://github.com/mahrtayyab/tweety)

## Test Data

The tests use public accounts like `@elonmusk` for demonstration. You can modify the test scripts to use different usernames or test with your own data.

Remember: Always respect Twitter's Terms of Service and rate limits when testing or using the library.
