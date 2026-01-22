# Utils Module

Utility functions for logging, validation, and helper operations.

## Contents

- **`logging_utils.py`**: Centralized logging configuration
- **`validators.py`**: Data validation functions

---

## Logging Utils (`logging_utils.py`)

Centralized logging configuration for consistent logging across the pipeline.

### Functions

#### `setup_logging(log_file=None, level='INFO')`

Configure logging for the application.

**Parameters**:
- `log_file` (str, optional): Path to log file
- `level` (str): Logging level (DEBUG, INFO, WARNING, ERROR)

**Example**:
```python
from src.utils import setup_logging

setup_logging(log_file='logs/my_script.log', level='INFO')
```

#### `get_logger(name)`

Get a logger instance.

**Example**:
```python
from src.utils import get_logger

logger = get_logger(__name__)
logger.info("Processing started")
```

#### `log_exception(logger, message, exc_info=True)`

Log an exception with context.

**Example**:
```python
try:
    risky_operation()
except Exception as e:
    log_exception(logger, "Operation failed", exc_info=True)
```

---

## Validators (`validators.py`)

Comprehensive validation functions for pipeline data.

### CIK and Year Validation

#### `validate_cik(cik)` → `(is_valid, formatted_cik)`

Validate and format CIK.

```python
from src.utils import validate_cik

is_valid, formatted = validate_cik("1750")
# Returns: (True, "0000001750")
```

#### `validate_year(year, min_year=1994, max_year=None)` → `bool`

Validate fiscal year.

```python
from src.utils import validate_year

assert validate_year(2020) == True
assert validate_year(1990) == False  # Before SEC EDGAR
```

### File Validation

#### `validate_10k_file(filepath, min_size=1000)` → `(is_valid, message)`

Validate a downloaded 10-K file.

```python
from src.utils import validate_10k_file

is_valid, message = validate_10k_file('data/raw/10k/0000001750_2020_10K.html')
if is_valid:
    print("File is valid")
else:
    print(f"Validation failed: {message}")
```

#### `validate_filename(filename)` → `(is_valid, cik, year)`

Validate filename format.

```python
from src.utils import validate_filename

is_valid, cik, year = validate_filename('0000001750_2020_10K.html')
# Returns: (True, '0000001750', 2020)
```

### Text Validation

#### `validate_extracted_text(text, min_length=1000, min_words=100)` → `(is_valid, message)`

Validate extracted text quality.

```python
from src.utils import validate_extracted_text

is_valid, message = validate_extracted_text(extracted_text)
```

### Batch Validation

#### `validate_firm_list(df)` → `(is_valid, errors)`

Validate firm-year DataFrame.

```python
import pandas as pd
from src.utils import validate_firm_list

df = pd.read_csv('firm_list.csv')
is_valid, errors = validate_firm_list(df)

if not is_valid:
    for error in errors:
        print(f"Error: {error}")
```

#### `validate_download_directory(directory)` → `(is_valid, stats)`

Validate a directory of downloaded files.

```python
from src.utils import validate_download_directory

is_valid, stats = validate_download_directory('data/raw/10k')
print(f"Valid files: {stats['valid_files']}/{stats['total_files']}")
```

#### `validate_batch_results(results_df, expected_count=None)` → `(is_valid, summary)`

Validate batch processing results.

```python
from src.utils import validate_batch_results

is_valid, summary = validate_batch_results(results_df)
print(f"Success rate: {summary['success_rate']:.1f}%")
```

### Helper Functions

#### `get_missing_downloads(firm_years, download_dir)` → `pd.DataFrame`

Find firm-years that haven't been downloaded.

```python
from src.utils import get_missing_downloads

missing = get_missing_downloads(firm_list, 'data/raw/10k')
print(f"Missing {len(missing)} downloads")
```

#### `validate_pipeline_data(firm_list_path, download_dir, parsed_dir=None)` → `dict`

Validate entire pipeline data.

```python
from src.utils import validate_pipeline_data

results = validate_pipeline_data(
    firm_list_path='data/firm_lists/target_firm_years.csv',
    download_dir='data/raw/10k',
    parsed_dir='data/processed/cleaned'
)

for stage, result in results.items():
    print(f"{stage}: {'PASS' if result['valid'] else 'FAIL'}")
```

---

## Usage Examples

### Complete Validation Workflow

```python
from src.utils import *
import pandas as pd

# Setup logging
setup_logging('logs/validation.log', level='INFO')
logger = get_logger(__name__)

# Load and validate firm list
firm_list = pd.read_csv('data/firm_lists/target_firm_years.csv')
is_valid, errors = validate_firm_list(firm_list)

if not is_valid:
    logger.error(f"Firm list validation failed: {errors}")
    exit(1)

# Validate downloads
is_valid, stats = validate_download_directory('data/raw/10k')
logger.info(f"Download validation: {stats['valid_files']}/{stats['total_files']} files valid")

# Find missing downloads
missing = get_missing_downloads(firm_list, 'data/raw/10k')
if len(missing) > 0:
    logger.warning(f"Missing {len(missing)} downloads")
    missing.to_csv('missing_downloads.csv', index=False)

# Validate all pipeline data
results = validate_pipeline_data(
    firm_list_path='data/firm_lists/target_firm_years.csv',
    download_dir='data/raw/10k',
    parsed_dir='data/processed/cleaned'
)

logger.info("Pipeline validation complete")
```

---

## Command-Line Usage

Use validators via the validation script:

```bash
# Validate all pipeline data
python scripts/validate_data.py

# Validate only downloads
python scripts/validate_data.py --stage downloads

# Generate detailed report
python scripts/validate_data.py --report
```

---

## Testing

```bash
# Run utils tests
pytest tests/test_utils.py -v
```

---

**Last Updated**: 2026-01-21
**Version**: 1.0
