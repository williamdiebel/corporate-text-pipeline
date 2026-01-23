# Downloaders Module

This module handles downloading corporate filings and reports from various sources.

## Contents

- **`sec_downloader.py`**: SEC EDGAR 10-K downloader (Phase 1)
- **`csr_downloader.py`**: CSR report downloader (Phase 2 - future)

---

## SEC Downloader (`sec_downloader.py`)

Downloads 10-K annual reports from the SEC EDGAR database.

### Features

✅ **SEC EDGAR Integration**: Direct access to SEC EDGAR filing system
✅ **Rate Limiting**: Respects SEC's 10 requests/second requirement
✅ **Automatic Retry**: Exponential backoff for failed downloads
✅ **Batch Processing**: Download multiple filings efficiently
✅ **File Validation**: Checks downloaded file integrity
✅ **Progress Tracking**: Optional callback for batch progress

### Class: `SECDownloader`

#### Initialization

```python
from src.downloaders import SECDownloader

downloader = SECDownloader(
    user_agent="your@email.com",      # Required by SEC
    output_dir="data/raw/10k",        # Where to save files
    rate_limit=0.1,                    # Seconds between requests (0.1 = 10/sec)
    max_retries=3                      # Retry failed downloads
)
```

#### Methods

##### `download_10k(cik, year, skip_if_exists=True)`

Download a single 10-K filing.

**Parameters**:
- `cik` (str): Central Index Key (will be zero-padded to 10 digits)
- `year` (int): Fiscal year of the filing
- `skip_if_exists` (bool): Skip if file already exists

**Returns**:
- `(success: bool, filepath: str | None)`

**Example**:
```python
success, filepath = downloader.download_10k(
    cik="1750",
    year=2020
)

if success:
    print(f"Downloaded to: {filepath}")
else:
    print("Download failed")
```

##### `download_batch(firm_years, skip_if_exists=True, progress_callback=None)`

Download multiple 10-K filings.

**Parameters**:
- `firm_years` (pd.DataFrame): DataFrame with 'cik' and 'year' columns
- `skip_if_exists` (bool): Skip existing files
- `progress_callback` (callable): Optional function called on each file
  - Signature: `callback(current: int, total: int, results: dict)`

**Returns**:
- `dict` with keys:
  - `successful`: List of successful downloads
  - `failed`: List of failed downloads with error messages
  - `skipped`: List of skipped (already existing) files

**Example**:
```python
import pandas as pd

firm_years = pd.DataFrame({
    'cik': ['1750', '320193', '789019'],
    'year': [2020, 2020, 2021]
})

def progress(current, total, results):
    print(f"Progress: {current}/{total}")

results = downloader.download_batch(
    firm_years=firm_years,
    skip_if_exists=True,
    progress_callback=progress
)

print(f"Successful: {len(results['successful'])}")
print(f"Failed: {len(results['failed'])}")
```

##### `validate_downloads(firm_years)`

Validate downloaded files against expected firm-years.

**Parameters**:
- `firm_years` (pd.DataFrame): Expected downloads

**Returns**:
- `pd.DataFrame` with validation results

**Example**:
```python
validation_df = downloader.validate_downloads(firm_years)
print(validation_df[['cik', 'year', 'exists', 'valid', 'file_size']])
```

##### `close()`

Close the downloader session.

```python
downloader.close()
```

### Output Format

Downloaded files are saved as: `{CIK}_{YEAR}_10K.html`

Example:
- CIK 1750, Year 2020 → `0000001750_2020_10K.html`
- CIK 320193, Year 2021 → `0000320193_2021_10K.html`

### Error Handling

The downloader implements robust error handling:

1. **Network Errors**: Automatic retry with exponential backoff (1s, 2s, 4s)
2. **Invalid CIK**: Raises `ValueError` with message
3. **File Not Found**: Returns `(False, None)` with logged warning
4. **Rate Limiting**: Automatic throttling to prevent IP blocking

### Usage Example (Complete Workflow)

```python
from src.downloaders import SECDownloader
from src.config import load_config
import pandas as pd

# Load configuration
config = load_config()

# Initialize downloader
downloader = SECDownloader(
    user_agent=config['sec_edgar']['user_agent'],
    output_dir=config['paths']['raw_10k'],
    rate_limit=0.1,  # 10 requests/second
    max_retries=3
)

# Load firm list
firm_list = pd.read_csv('data/firm_lists/target_firm_years.csv')

# Download all filings
results = downloader.download_batch(
    firm_years=firm_list,
    skip_if_exists=True
)

# Save results
results_df = pd.DataFrame(results['successful'])
results_df.to_csv('download_results.csv', index=False)

# Check for failures
if results['failed']:
    failed_df = pd.DataFrame(results['failed'])
    print(f"Failed downloads: {len(failed_df)}")
    print(failed_df[['cik', 'year', 'error']])

# Clean up
downloader.close()
```

---

## CSR Downloader (`csr_downloader.py`)

**Status**: Placeholder for Phase 2 implementation

This module will download Corporate Social Responsibility (CSR) reports from company websites and sustainability databases.

### Planned Features (Phase 2)

- 🔲 Automated CSR report URL discovery
- 🔲 PDF download and validation
- 🔲 Support for multiple report formats
- 🔲 Integration with GRI database
- 🔲 Multi-year report tracking

### Future Data Sources

1. Company investor relations websites
2. GRI Sustainability Disclosure Database
3. CDP (Carbon Disclosure Project)
4. Company sustainability report archives
5. SEC EDGAR (some companies file CSR as exhibits)

### Example (Future API)

```python
from src.downloaders import CSRDownloader

# Initialize (Phase 2)
csr_downloader = CSRDownloader(
    output_dir="data/raw/csr"
)

# Download CSR report (Phase 2)
success, filepath = csr_downloader.download_report(
    company_name="Apple Inc.",
    year=2020
)
```

---

## Command-Line Usage

The downloaders can be used via command-line scripts:

### Download 10-Ks

```bash
# Download all 10-Ks from firm list
python scripts/download_10k.py

# Download specific batch
python scripts/download_10k.py --batch-size 100 --start-index 0

# Override output directory
python scripts/download_10k.py --output-dir custom/directory
```

See `docs/DOWNLOADER_USAGE.md` for complete CLI documentation.

---

## Testing

```bash
# Run downloader tests
pytest tests/test_downloaders.py -v

# Run integration tests (requires internet)
pytest tests/test_downloaders.py -m integration

# Skip slow tests
pytest tests/test_downloaders.py -m "not slow"
```

---

## SEC EDGAR Requirements

### User Agent

SEC EDGAR requires a valid email in the user agent string:

```python
# ✅ Correct
downloader = SECDownloader(user_agent="researcher@university.edu")

# ❌ Incorrect - may result in IP ban
downloader = SECDownloader(user_agent="MyBot/1.0")
```

### Rate Limits

- **Maximum**: 10 requests per second
- **Recommended**: 8-9 requests per second to be safe
- **Enforcement**: IP-based blocking for violations

### Best Practices

1. Always include a valid email in user agent
2. Respect rate limits (use built-in throttling)
3. Handle failures gracefully (use retry logic)
4. Cache downloaded files (use `skip_if_exists=True`)
5. Log all download attempts for auditing

---

## Troubleshooting

### Issue: 403 Forbidden Error

**Cause**: Invalid or missing user agent

**Solution**:
```python
# Ensure user agent includes valid email
downloader = SECDownloader(user_agent="your.email@domain.com")
```

### Issue: Downloads are slow

**Cause**: Rate limiting

**Solution**: This is expected. With 10 requests/second:
- 100 filings ≈ 10 seconds
- 1,000 filings ≈ 100 seconds (~2 minutes)
- 8,600 filings ≈ 14-20 minutes

### Issue: Connection timeout

**Cause**: Network instability or SEC server issues

**Solution**: The downloader automatically retries. Check logs for details:
```bash
tail -f logs/download_10k_*.log
```

### Issue: File not found for specific CIK/year

**Cause**: Filing doesn't exist or wrong fiscal year

**Solution**:
1. Verify CIK on SEC EDGAR website
2. Check if company filed 10-K for that year
3. Some companies may file 10-K/A (amended) instead

---

## Performance Optimization

### Batch Processing

For large datasets, process in batches:

```python
batch_size = 500
for i in range(0, len(firm_list), batch_size):
    batch = firm_list.iloc[i:i+batch_size]
    results = downloader.download_batch(batch)
    # Save results incrementally
```

### Parallel Downloads (Advanced)

For multi-year downloads of same firms:

```python
from concurrent.futures import ThreadPoolExecutor

def download_year(year):
    downloader = SECDownloader(...)
    firms = firm_list[firm_list['year'] == year]
    return downloader.download_batch(firms)

with ThreadPoolExecutor(max_workers=3) as executor:
    results = executor.map(download_year, [2018, 2019, 2020])
```

**Warning**: Ensure combined rate across all threads doesn't exceed SEC limit!

---

## API Reference

See inline docstrings for complete API documentation:

```python
help(SECDownloader)
help(SECDownloader.download_10k)
help(SECDownloader.download_batch)
```

---

**Last Updated**: 2026-01-21
**Version**: 1.0
