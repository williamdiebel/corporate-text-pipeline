# Tests Directory

Unit and integration tests for the corporate text pipeline.

## Test Files

- `test_downloaders.py` - Tests for SEC and CSR downloaders
- `test_processors.py` - Tests for parser and text cleaner
- `test_utils.py` - Tests for validators and utilities

---

## Running Tests

### Run All Tests

```bash
# Run entire test suite
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Run Specific Test Files

```bash
# Test downloaders only
pytest tests/test_downloaders.py -v

# Test processors only
pytest tests/test_processors.py -v

# Test utils only
pytest tests/test_utils.py -v
```

### Run Specific Test Classes or Functions

```bash
# Test specific class
pytest tests/test_downloaders.py::TestSECDownloader -v

# Test specific function
pytest tests/test_downloaders.py::TestSECDownloader::test_initialization -v
```

---

## Test Markers

Tests are organized with pytest markers:

### Available Markers

- `@pytest.mark.integration` - Integration tests (require internet)
- `@pytest.mark.slow` - Slow-running tests
- `@pytest.mark.unit` - Fast unit tests

### Run Tests by Marker

```bash
# Run only unit tests (fast)
pytest tests/ -m "not integration and not slow"

# Run integration tests
pytest tests/ -m integration

# Skip slow tests
pytest tests/ -m "not slow"
```

---

## Test Coverage

### Current Coverage

- **Downloaders**: ~75%
  - Core download logic
  - CIK validation
  - Filename generation
  - Integration tests (optional)

- **Processors**: ~80%
  - Text parsing
  - Text cleaning
  - Metadata extraction

- **Utils**: ~85%
  - All validation functions
  - Logging setup

### Coverage Goals

- Target: 80%+ coverage for all modules
- Critical paths: 100% coverage

### Generate Coverage Report

```bash
# Generate HTML coverage report
pytest tests/ --cov=src --cov-report=html --cov-report=term

# View in browser
open htmlcov/index.html

# Generate text report
pytest tests/ --cov=src --cov-report=term-missing
```

---

## Writing Tests

### Test Structure

```python
"""
Tests for module_name.
"""

import pytest
from src.module import ClassToTest

class TestClassName:
    """Tests for ClassName."""

    def setup_method(self):
        """Setup test fixtures before each test."""
        # Initialize test data
        pass

    def teardown_method(self):
        """Cleanup after each test."""
        # Clean up temporary files, etc.
        pass

    def test_functionality(self):
        """Test specific functionality."""
        # Arrange
        input_data = "test"

        # Act
        result = function_to_test(input_data)

        # Assert
        assert result == expected_output
```

### Test Fixtures

Use pytest fixtures for shared test data:

```python
@pytest.fixture
def sample_firm_list():
    """Sample firm list for testing."""
    return pd.DataFrame({
        'cik': ['1750', '320193'],
        'year': [2020, 2021]
    })

def test_with_fixture(sample_firm_list):
    """Test using fixture."""
    assert len(sample_firm_list) == 2
```

### Temporary Files

Use `tempfile` for test files:

```python
import tempfile
from pathlib import Path

def test_file_processing():
    """Test file processing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = Path(temp_dir) / "test.txt"
        test_file.write_text("test content")

        # Run tests
        result = process_file(test_file)

        # Assertions
        assert result is not None
        # temp_dir automatically cleaned up
```

---

## Integration Tests

Integration tests require internet access and may be rate-limited.

### Running Integration Tests

```bash
# Run integration tests (may be slow)
pytest tests/ -m integration -v

# Run with longer timeout
pytest tests/ -m integration -v --timeout=300
```

### Integration Test Guidelines

1. Mark with `@pytest.mark.integration`
2. Use real but small data samples
3. Handle rate limiting gracefully
4. Allow tests to be skipped if offline

Example:
```python
@pytest.mark.integration
@pytest.mark.slow
def test_download_real_filing(self):
    """Test downloading real 10-K filing."""
    downloader = SECDownloader(user_agent="test@test.com", ...)

    # Use known CIK with small filing
    success, filepath = downloader.download_10k(cik="1750", year=2020)

    if success:  # May fail due to network/rate limiting
        assert filepath.exists()
```

---

## Continuous Integration

### GitHub Actions

Tests run automatically on push/PR:

```yaml
# .github/workflows/tests.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - run: pip install -r requirements.txt
      - run: pytest tests/ --cov=src -m "not integration"
```

### Pre-commit Hooks

Run tests before committing:

```bash
# Install pre-commit
pip install pre-commit

# Setup hooks
pre-commit install

# Tests run automatically on git commit
```

---

## Test Data

### Sample Files

Create minimal test files in `tests/fixtures/`:

```
tests/fixtures/
├── sample_10k.html           # Minimal 10-K HTML
├── sample_firm_list.csv      # Test firm list
└── sample_extracted.txt      # Sample extracted text
```

### Using Test Data

```python
from pathlib import Path

def get_test_data_path(filename):
    """Get path to test data file."""
    return Path(__file__).parent / "fixtures" / filename

def test_with_sample_file():
    """Test using sample file."""
    sample_file = get_test_data_path("sample_10k.html")
    result = parse_10k(sample_file)
    assert result is not None
```

---

## Debugging Tests

### Run Tests with Debug Output

```bash
# Show print statements
pytest tests/ -v -s

# Show local variables on failure
pytest tests/ -v -l

# Stop on first failure
pytest tests/ -v -x

# Drop into debugger on failure
pytest tests/ -v --pdb
```

### Debug Specific Test

```python
def test_debug_example():
    """Test with debugging."""
    import pdb; pdb.set_trace()  # Set breakpoint

    result = function_to_test()
    assert result == expected
```

---

## Performance Testing

### Benchmark Tests

```python
import time

def test_performance():
    """Test performance."""
    start = time.time()

    # Run operation
    result = expensive_operation()

    elapsed = time.time() - start

    assert elapsed < 5.0  # Should complete in 5 seconds
    assert result is not None
```

### Memory Testing

```python
import tracemalloc

def test_memory_usage():
    """Test memory usage."""
    tracemalloc.start()

    # Run operation
    result = memory_intensive_operation()

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Assert memory usage is reasonable
    assert peak < 100 * 1024 * 1024  # Less than 100MB
```

---

## Mocking

Use mocks for external dependencies:

```python
from unittest.mock import Mock, patch

def test_with_mock():
    """Test with mocked dependency."""
    with patch('requests.get') as mock_get:
        # Configure mock
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "<html>Test</html>"

        # Run test
        result = download_function()

        # Verify mock was called
        mock_get.assert_called_once()
        assert result is not None
```

---

## Test Best Practices

### Do's

✅ Test one thing per test function
✅ Use descriptive test names
✅ Use arrange-act-assert pattern
✅ Test edge cases and error conditions
✅ Keep tests independent
✅ Use fixtures for shared setup
✅ Mock external dependencies
✅ Test both success and failure paths

### Don'ts

❌ Don't test implementation details
❌ Don't make tests dependent on each other
❌ Don't use real credentials/API keys in tests
❌ Don't commit test outputs
❌ Don't skip test cleanup
❌ Don't make tests too slow

---

## Common Test Patterns

### Testing Exceptions

```python
def test_raises_exception():
    """Test that function raises expected exception."""
    with pytest.raises(ValueError, match="Invalid CIK"):
        validate_cik("invalid")
```

### Testing File Operations

```python
def test_file_creation(tmp_path):
    """Test file creation using tmp_path fixture."""
    output_file = tmp_path / "output.txt"

    write_file(output_file, "content")

    assert output_file.exists()
    assert output_file.read_text() == "content"
```

### Parametrized Tests

```python
@pytest.mark.parametrize("cik,expected", [
    ("1750", "0000001750"),
    ("320193", "0000320193"),
    ("12345", "0000012345"),
])
def test_cik_formatting(cik, expected):
    """Test CIK formatting with multiple inputs."""
    _, formatted = validate_cik(cik)
    assert formatted == expected
```

---

## Troubleshooting

### Tests Pass Locally But Fail in CI

- Check Python version compatibility
- Verify all dependencies in requirements.txt
- Ensure test data files are committed
- Check for environment-specific paths

### Flaky Tests

- Use pytest-timeout to catch hanging tests
- Fix tests that depend on external state
- Use mocks for external services
- Avoid time-dependent tests

### Slow Tests

- Use markers to skip slow tests: `@pytest.mark.slow`
- Mock expensive operations
- Use smaller test datasets
- Run slow tests separately in CI

---

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [Mocking Guide](https://docs.python.org/3/library/unittest.mock.html)

---

**Last Updated**: 2026-01-21
**Version**: 1.0
