# src/ - Pipeline Library

**Reusable modules for downloading, processing, and validating 10-K filings**

---

## 📚 What's in This Folder?

```
src/
├── downloaders/     # Download 10-K filings from SEC EDGAR
├── processors/      # Parse and clean extracted text
├── utils/           # Validation and logging utilities
└── config.py        # Configuration loader
```

---

## 🎯 For Students & Research Assistants

**You typically DON'T need to look in this folder!**

These are the "under the hood" modules that make the scripts work. You'll use the scripts in the `scripts/` folder instead.

### When to Look Here

- ✅ You're curious how the downloader works
- ✅ You need to understand what a function does
- ✅ Will asks you to check something in the source code

### When NOT to Look Here

- ❌ You just want to download files → Use `scripts/download_10k.py`
- ❌ You want to process files → Use `scripts/process_batch.py`
- ❌ You want to validate data → Use `scripts/validate_data.py`

---

## 📖 Quick Reference

### Using the Library (For Advanced Users)

If you want to use these modules in your own Python code:

```python
from src.downloaders import SECDownloader
from src.processors import TenKParser, TextCleaner

# Download a specific filing
downloader = SECDownloader(user_agent="your@email.com", output_dir="data/raw/10k")
success, filepath, was_skipped = downloader.download_10k(cik="1750", year=2020)

# Parse it
parser = TenKParser()
sections = parser.parse_file(filepath)

# Clean the text
cleaner = TextCleaner()
clean_text = cleaner.clean(sections['item_1a'])
```

---

## 📋 Module Documentation

### Downloaders

**What it does**: Downloads 10-K filings from SEC EDGAR

**Key class**: `SECDownloader`

**Used by**: `download_10k.py` script

### Processors

**What it does**: Extracts and cleans text from 10-K files

**Key classes**: `TenKParser`, `TextCleaner`

**Used by**: `process_batch.py` script

### Utils

**What it does**: Validates data and sets up logging

**Key functions**: `validate_10k_file()`, `validate_firm_list()`, `setup_logging()`

**Used by**: All scripts

---

## 🔍 Main Documentation

For comprehensive project documentation, see:

- **[Main README](../README.md)** - Project overview and quick start
- **[Setup Guide](../docs/SETUP.md)** - Installation instructions
- **[Scripts README](../scripts/README.md)** - How to run scripts

---

## 💡 Understanding src/ vs scripts/

**Think of it this way:**

- **`src/`** = Toolbox (individual tools you can combine)
- **`scripts/`** = Pre-built solutions (ready-to-use programs)

**Example:**

- **src/downloaders/sec_downloader.py** = A screwdriver (tool)
- **scripts/download_10k.py** = A pre-assembled shelf (solution)

You usually want the pre-assembled shelf, not individual tools!

---

**Last Updated**: January 2026

## Modules Overview

### `config.py`
**Purpose**: Load and manage configuration settings from `config.yaml`

**Key Functions**:
- `load_config(config_path)` - Load configuration from YAML file
- `get_api_key(provider)` - Get API keys from environment
- `get_sec_user_agent()` - Get SEC EDGAR user agent
- `load_firm_list()` - Load target firm-year list

**Usage**:
```python
from src.config import load_config

config = load_config('config.yaml')
print(config['project_name'])
```

### `downloaders/`
See [downloaders/README.md](downloaders/README.md) for detailed documentation.

**Modules**:
- **`sec_downloader.py`**: Downloads 10-K filings from SEC EDGAR
- **`csr_downloader.py`**: Placeholder for future CSR report downloader

### `processors/`
See [processors/README.md](processors/README.md) for detailed documentation.

**Modules**:
- **`parser.py`**: Extracts Items 1, 1A, and 7 from 10-K HTML
- **`text_cleaner.py`**: Cleans and normalizes extracted text

### `utils/`
See [utils/README.md](utils/README.md) for detailed documentation.

**Modules**:
- **`logging_utils.py`**: Centralized logging configuration
- **`validators.py`**: Validation functions for data quality

## Quick Start

### Import and Use Modules

```python
# Import downloaders
from src.downloaders import SECDownloader

# Import processors
from src.processors import TenKParser, TextCleaner

# Import utilities
from src.utils import validate_cik, validate_10k_file

# Import configuration
from src.config import load_config
```

### Example Workflow

```python
from src.config import load_config
from src.downloaders import SECDownloader
from src.processors import TenKParser, TextCleaner

# Load configuration
config = load_config()

# Initialize downloader
downloader = SECDownloader(
    user_agent=config['sec_edgar']['user_agent'],
    output_dir=config['paths']['raw_10k']
)

# Download a 10-K
success, filepath, was_skipped = downloader.download_10k(cik="1750", year=2020)

if success:
    # Parse the filing
    parser = TenKParser()
    sections = parser.parse_file(filepath)

    # Clean extracted text
    cleaner = TextCleaner()
    clean_text = cleaner.clean(sections['item_1a'])

    print(f"Cleaned Risk Factors: {len(clean_text)} characters")
```

## Development Guidelines

### Adding New Modules

1. Create the module file in the appropriate subdirectory
2. Add module imports to the subdirectory's `__init__.py`
3. Write tests in `tests/test_<module>.py`
4. Update this README with module documentation

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for function signatures
- Include docstrings for all public functions/classes
- Add logging for important operations
- Handle errors gracefully with try-except blocks

### Testing

```bash
# Run all tests
pytest tests/

# Run specific module tests
pytest tests/test_downloaders.py -v

# Run with coverage
pytest --cov=src tests/
```

## Module Dependencies

### External Dependencies
- **requests**: HTTP requests for downloading
- **beautifulsoup4**: HTML parsing
- **pandas**: Data manipulation
- **pyyaml**: Configuration loading
- **sec-edgar-downloader**: SEC EDGAR API access

### Internal Dependencies
- **config**: Used by all modules for configuration
- **utils**: Used by all modules for validation and logging
- **processors**: Depends on downloaders for input data

## Configuration

All modules read settings from `config.yaml`:

```yaml
sec_edgar:
  rate_limit: 10
  user_agent: "your@email.com"

paths:
  raw_10k: "data/raw/10k"
  cleaned_text: "data/processed/cleaned"

text_extraction:
  sections:
    - "item_1"
    - "item_1a"
    - "item_7"
```

## Error Handling

All modules implement consistent error handling:

1. **Validation errors**: Raise `ValueError` with descriptive message
2. **I/O errors**: Catch and log with `logging.error()`
3. **Network errors**: Retry with exponential backoff (in downloaders)
4. **Parsing errors**: Log warning and return None/empty result

## Logging

All modules use centralized logging:

```python
import logging
logger = logging.getLogger(__name__)

logger.info("Starting process...")
logger.warning("Missing section: Item 1A")
logger.error("Failed to download", exc_info=True)
```

## Performance Considerations

- **Rate limiting**: SEC downloader enforces 10 requests/second
- **Memory usage**: Process files in batches for large datasets
- **Disk I/O**: Use buffered writes for better performance
- **Parallel processing**: Can run multiple downloaders for different years

## Next Steps

1. **Implement LLM scoring module** (Phase 3)
2. **Add CSR downloader** (Phase 2)
3. **Optimize text processing** for large batches
4. **Add caching** for frequently accessed data

## Support

For questions or issues:
- See module-specific READMEs in subdirectories
- Check `docs/` for detailed guides
- Review test files for usage examples

---

**Last Updated**: 2026-01-21
**Version**: 1.0
