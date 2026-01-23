# tests/ - Automated Tests

**Tests to verify the pipeline works correctly**

---

## 🎯 For Students & Research Assistants

**You probably won't need to look here often.** These are automated tests that check if the code works correctly. Will uses these during development.

---

## 📚 What's in This Folder?

```
tests/
├── test_downloaders.py     # Tests for downloading functionality
├── test_processors.py      # Tests for text processing
└── test_utils.py           # Tests for validation utilities
```

---

## 🔬 Running Tests

### Basic Test Commands

**Run all tests**:
```bash
pytest tests/
```

**What you'll see**:
```
==================== test session starts ====================
collected 45 items

tests/test_downloaders.py ........    [  20%]
tests/test_processors.py ..........   [  50%]
tests/test_utils.py ...............   [ 100%]

==================== 45 passed in 12.34s ====================
```

**If all tests pass**: ✅ Everything works!

**If tests fail**: ❌ Something is broken - tell Will

---

## 📋 When to Run Tests

### Before Major Work

Run tests to make sure everything starts working:
```bash
pytest tests/
```

### After Will Updates Code

When Will updates the code, run tests to verify:
```bash
# Pull latest changes
git pull origin main

# Run tests
pytest tests/
```

### If Something Seems Broken

Run tests to help identify the problem:
```bash
pytest tests/ -v
```

The `-v` flag shows more details about what's being tested.

---

## 💡 Understanding Test Output

### All Tests Pass ✅

```
==================== 45 passed in 12.34s ====================
```

**Meaning**: Everything works correctly. You're good to go!

### Some Tests Fail ❌

```
==================== FAILURES ====================
___ test_download_10k ___
    assert result == True
    E assert False == True
==================== 1 failed, 44 passed ====================
```

**Meaning**: Something is broken. Copy the error message and send it to Will.

### Tests Skipped ⏭️

```
==================== 40 passed, 5 skipped ====================
```

**Meaning**: Some tests were skipped (usually slow internet tests). This is normal.

---

## 🎓 Advanced: Test Types

### Unit Tests (Fast)

Test individual functions in isolation:
```bash
# Run only unit tests (takes ~5 seconds)
pytest tests/ -m "not integration and not slow"
```

### Integration Tests (Slow)

Test with real internet connections:
```bash
# Run integration tests (takes ~1-2 minutes)
pytest tests/ -m integration
```

**Note**: Integration tests require internet and may be rate-limited by SEC.

---

## 📊 Test Coverage

**What is test coverage?** It shows how much of the code has tests.

**Check coverage**:
```bash
pytest tests/ --cov=src --cov-report=term
```

**Example output**:
```
Name                          Stmts   Miss  Cover
-------------------------------------------------
src/downloaders/sec.py          120      8    93%
src/processors/parser.py        150     12    92%
src/utils/validators.py          80      5    94%
-------------------------------------------------
TOTAL                           350     25    93%
```

**Goal**: >80% coverage for all modules

---

## 🔍 Detailed Test Output

### Show More Information

```bash
# Verbose output (shows each test name)
pytest tests/ -v

# Show print statements
pytest tests/ -v -s

# Stop on first failure
pytest tests/ -x
```

### Test Specific Module

```bash
# Test only downloaders
pytest tests/test_downloaders.py -v

# Test only processors
pytest tests/test_processors.py -v

# Test only validators
pytest tests/test_utils.py -v
```

---

## 🐛 If Tests Fail

### Step 1: Read the Error

The error message tells you what broke:

```
FAILED tests/test_downloaders.py::test_download_10k
    assert success == True
```

This means the `test_download_10k` test failed.

### Step 2: Copy the Full Error

Run with verbose mode to get details:
```bash
pytest tests/test_downloaders.py::test_download_10k -v
```

### Step 3: Tell Will

Send Will:
1. The command you ran
2. The full error message
3. When it started failing (after update? after you changed something?)

---

## 🔧 When Will Asks You to Run Specific Tests

Sometimes Will might ask:

**"Run the downloader tests"**:
```bash
pytest tests/test_downloaders.py -v
```

**"Run tests and send me the coverage"**:
```bash
pytest tests/ --cov=src --cov-report=term > test_results.txt
cat test_results.txt
```

**"Skip the slow tests"**:
```bash
pytest tests/ -m "not slow"
```

---

## 🚫 What NOT to Do

### ❌ Don't Edit Test Files

Unless Will asks you to, don't modify files in `tests/`.

### ❌ Don't Worry If Some Tests Skip

Some tests are marked to skip (like slow internet tests). This is normal:
```
==================== 40 passed, 5 skipped ====================
```

### ❌ Don't Panic If Tests Fail After Git Pull

If tests fail after pulling Will's changes:
1. Try running them again
2. Make sure your virtual environment is activated
3. Send Will the error message

---

## 🎓 For Curious Students

### What Do Tests Actually Do?

Tests verify that code works correctly by:

1. **Running functions** with sample inputs
2. **Checking outputs** match expected results
3. **Reporting failures** when something breaks

**Example**: A test might download 1 filing and verify:
- ✅ The file was created
- ✅ The file is not empty
- ✅ The file is valid HTML

### Why Are Tests Important?

- **Catch bugs early**: Before they affect your data
- **Verify changes**: Make sure updates don't break things
- **Document behavior**: Show how code should work

### Learning More

If you're interested in testing:
- [Pytest Documentation](https://docs.pytest.org/)
- Tests in this project show examples of good testing practices

---

## 🔍 Main Documentation

For complete details, see:

- **[Main README](../README.md)** - Project overview
- **[Setup Guide](../docs/SETUP.md)** - Installation instructions
- **[Scripts README](../scripts/README.md)** - How to run scripts

---

**Last Updated**: January 2026
**Version**: 1.0
