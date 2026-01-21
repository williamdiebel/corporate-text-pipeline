# 10-K Downloader Usage Guide

This guide explains how to use the 10-K downloader scripts to download SEC EDGAR filings for your research project.

## Overview

The 10-K downloader consists of two main components:

1. **`src/downloaders/sec_downloader.py`** - Core downloader class with SEC EDGAR integration
2. **`scripts/download_10k.py`** - Executable script for batch downloading

## Quick Start

### 1. Prerequisites

Make sure you have installed all dependencies:

```bash
pip install -r requirements.txt
```

### 2. Verify Configuration

Check your `config.yaml` file has the correct settings:

```yaml
sec_edgar:
  rate_limit: 10  # requests per second
  user_agent: "your.email@university.edu"  # REQUIRED by SEC
  filing_types:
    - "10-K"

paths:
  raw_10k: "data/raw/10k"

firm_list_file: "data/firm_lists/target_firm_years.csv"
```

**Important**: The SEC requires a valid email in the user agent. Update the `user_agent` field with your actual email.

### 3. Prepare Firm List

Your firm list CSV should have at minimum these columns:
- `cik` - Central Index Key (numeric or string)
- `year` - Fiscal year of the filing

Example `data/firm_lists/target_firm_years.csv`:
```csv
cik,year
1750,2020
1750,2021
320193,2020
789019,2021
```

The downloader will automatically:
- Convert CIKs to 10-digit zero-padded format
- Handle various column name formats (cik/CIK, year/Year/fyear)

### 4. Run the Downloader

#### Download all filings:
```bash
python scripts/download_10k.py
```

#### Download first 100 filings (recommended for testing):
```bash
python scripts/download_10k.py --batch-size 100
```

#### Resume from a specific index:
```bash
python scripts/download_10k.py --start-index 500 --batch-size 100
```

#### Re-download everything (overwrite existing files):
```bash
python scripts/download_10k.py --no-skip-existing
```

## Command Line Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--batch-size` | int | None (all) | Number of firm-years to process |
| `--start-index` | int | 0 | Starting index in firm list |
| `--skip-existing` | flag | True | Skip files that already exist |
| `--no-skip-existing` | flag | - | Re-download existing files |
| `--config` | str | config.yaml | Path to config file |
| `--output-dir` | str | from config | Override output directory |
| `--log-level` | str | INFO | Logging level (DEBUG/INFO/WARNING/ERROR) |

## Output Structure

### Downloaded Files

Files are saved as: `{CIK}_{YEAR}_10K.html`

Example:
```
data/raw/10k/
├── 0000001750_2020_10K.html
├── 0000001750_2021_10K.html
└── 0000320193_2020_10K.html
```

### Download Logs

The script creates detailed logs:

```
data/raw/10k/download_logs/
├── successful_20260121_143022.csv  # Successfully downloaded files
├── failed_20260121_143022.csv      # Failed downloads with error messages
├── skipped_20260121_143022.csv     # Skipped (already existed)
└── summary_20260121_143022.txt     # Summary statistics
```

### Application Logs

Full execution logs are saved to:
```
logs/download_10k_20260121_143022.log
```

## Features

### Rate Limiting
- Automatically respects SEC's 10 requests/second limit
- Configurable via `config.yaml`
- Prevents IP blocking

### Retry Logic
- Automatic retry with exponential backoff
- Configurable max retries (default: 3)
- Handles network errors gracefully

### Progress Tracking
- Real-time progress display
- Shows successful/failed/skipped counts
- Saves detailed logs for auditing

### Validation
- CIK format validation and zero-padding
- File existence checking
- Minimum file size validation

## Example Workflow

### Step 1: Test with Small Batch
```bash
# Download first 10 filings to test
python scripts/download_10k.py --batch-size 10
```

### Step 2: Check Results
```bash
# View download summary
cat data/raw/10k/download_logs/summary_*.txt

# Check for failures
cat data/raw/10k/download_logs/failed_*.csv
```

### Step 3: Download Full Dataset in Batches
```bash
# Process in batches of 100
for i in {0..8600..100}; do
    echo "Downloading batch starting at index $i"
    python scripts/download_10k.py --start-index $i --batch-size 100
    sleep 10  # Brief pause between batches
done
```

## Using the Downloader in Python Code

You can also use the downloader directly in your Python scripts:

```python
from src.config import load_config
from src.downloaders import SECDownloader
import pandas as pd

# Load configuration
config = load_config()

# Initialize downloader
downloader = SECDownloader(
    user_agent=config['sec_edgar']['user_agent'],
    output_dir=config['paths']['raw_10k'],
    rate_limit=0.1,  # 10 req/sec
    max_retries=3
)

# Download a single filing
success, filepath = downloader.download_10k(
    cik="1750",
    year=2020,
    skip_if_exists=True
)

if success:
    print(f"Downloaded to: {filepath}")
else:
    print("Download failed")

# Download a batch
firm_years = pd.DataFrame({
    'cik': ['1750', '320193', '789019'],
    'year': [2020, 2020, 2021]
})

results = downloader.download_batch(firm_years)

print(f"Successful: {len(results['successful'])}")
print(f"Failed: {len(results['failed'])}")
print(f"Skipped: {len(results['skipped'])}")

# Clean up
downloader.close()
```

## Troubleshooting

### Issue: "No module named 'sec_edgar_downloader'"
**Solution**: Install dependencies
```bash
pip install sec-edgar-downloader
```

### Issue: "403 Forbidden" from SEC
**Solution**: Check your user agent contains a valid email
```yaml
sec_edgar:
  user_agent: "your.email@domain.com"  # Must be a real email
```

### Issue: "Firm list not found"
**Solution**: Verify the file path in config.yaml matches your actual file location
```bash
ls -la data/firm_lists/target_firm_years.csv
```

### Issue: Download speed is slow
**Solution**: The SEC rate limit is 10 requests/second. For ~8,600 filings, expect:
- Time required: ~860 seconds (~14 minutes) minimum
- Actual time: 20-30 minutes with retries and processing

### Issue: Some downloads failed
**Solution**:
1. Check the `failed_*.csv` log for error messages
2. Common causes:
   - Filing doesn't exist for that CIK/year
   - CIK is invalid
   - Network timeout (will auto-retry)
3. Re-run for failed items:
   ```python
   # Load failed list and retry
   failed = pd.read_csv('data/raw/10k/download_logs/failed_20260121.csv')
   downloader.download_batch(failed[['cik', 'year']])
   ```

## Best Practices

1. **Start Small**: Test with `--batch-size 10` before downloading thousands of filings

2. **Monitor Progress**: Check logs regularly during large downloads

3. **Handle Failures**: Review failed downloads and determine if they need manual inspection

4. **Use Skip Existing**: Always use `--skip-existing` (default) to avoid re-downloading

5. **Batch Processing**: For very large datasets (8,000+ filings), process in batches of 100-500

6. **Network Stability**: Run on a stable network connection for large downloads

7. **Disk Space**: Check available disk space (10-K filings average 500KB-2MB each)
   - 8,600 filings ≈ 4-17 GB

## Next Steps

After downloading 10-K filings:

1. **Validate Downloads**: Run validation script
   ```bash
   python scripts/validate_data.py
   ```

2. **Extract Text**: Process files to extract relevant sections (Items 1, 1A, 7)
   ```bash
   python scripts/process_batch.py
   ```

3. **Manual Review**: Review a sample of filings to verify quality

## API Documentation

### SECDownloader Class

#### `__init__(user_agent, output_dir, rate_limit, max_retries)`
Initialize the downloader.

**Parameters:**
- `user_agent` (str): Email address required by SEC
- `output_dir` (str): Directory to save files
- `rate_limit` (float): Seconds between requests (default: 0.1)
- `max_retries` (int): Max retry attempts (default: 3)

#### `download_10k(cik, year, skip_if_exists)`
Download a single 10-K filing.

**Parameters:**
- `cik` (str): Central Index Key
- `year` (int): Fiscal year
- `skip_if_exists` (bool): Skip if file exists

**Returns:**
- `(success: bool, filepath: Optional[str])`

#### `download_batch(firm_years, skip_if_exists, progress_callback)`
Download multiple filings.

**Parameters:**
- `firm_years` (pd.DataFrame): DataFrame with 'cik' and 'year' columns
- `skip_if_exists` (bool): Skip existing files
- `progress_callback` (callable): Optional progress callback function

**Returns:**
- `dict`: Results with 'successful', 'failed', and 'skipped' lists

#### `validate_downloads(firm_years)`
Validate downloaded files.

**Parameters:**
- `firm_years` (pd.DataFrame): DataFrame with expected filings

**Returns:**
- `pd.DataFrame`: Validation results

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review application logs in `logs/`
3. Contact the project lead: william.diebel@moore.sc.edu

---

**Last Updated**: 2026-01-21
**Version**: 1.0
