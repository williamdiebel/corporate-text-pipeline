# Source Code (`src/`) Directory

This directory contains the core pipeline modules for downloading, processing, and analyzing 10-K filings.

## Directory Structure

```
src/
├── __init__.py              # Package initialization
├── config.py                # Configuration loader
├── downloaders/             # Download modules
│   ├── sec_downloader.py   # SEC EDGAR 10-K downloader
│   └── csr_downloader.py   # CSR report downloader (Phase 2)
├── processors/              # Text processing modules
│   ├── parser.py           # 10-K section extraction
│   └── text_cleaner.py     # Text cleaning and normalization
└── utils/                   # Utility functions
    ├── logging_utils.py    # Logging setup
    └── validators.py       # Data validation functions
```

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
success, filepath = downloader.download_10k(cik="1750", year=2020)

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
