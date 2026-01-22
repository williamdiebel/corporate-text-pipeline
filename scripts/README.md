# Scripts Directory

Executable scripts for running the pipeline.

## Available Scripts

### 1. `download_10k.py` - Download 10-K Filings

Downloads 10-K filings from SEC EDGAR.

**Usage**:
```bash
# Download all firm-years from config
python scripts/download_10k.py

# Download first 100
python scripts/download_10k.py --batch-size 100

# Resume from index 500
python scripts/download_10k.py --start-index 500 --batch-size 100

# Override output directory
python scripts/download_10k.py --output-dir custom/directory

# Re-download existing files
python scripts/download_10k.py --no-skip-existing
```

**Options**:
- `--batch-size N`: Number of firm-years to process
- `--start-index N`: Starting index in firm list
- `--skip-existing`: Skip already downloaded files (default)
- `--no-skip-existing`: Re-download existing files
- `--config PATH`: Config file path (default: config.yaml)
- `--output-dir PATH`: Override output directory
- `--log-level LEVEL`: Logging level (DEBUG/INFO/WARNING/ERROR)

**Output**:
- Downloaded files: `data/raw/10k/{CIK}_{YEAR}_10K.html`
- Logs: `data/raw/10k/download_logs/`
- Application logs: `logs/download_10k_*.log`

**Example**:
```bash
# Download first batch of 50 for testing
python scripts/download_10k.py --batch-size 50

# Check results
cat data/raw/10k/download_logs/summary_*.txt
```

---

### 2. `process_batch.py` - Process Downloaded Files

Parses and cleans downloaded 10-K files.

**Usage**:
```bash
# Process all downloaded files
python scripts/process_batch.py

# Process specific directories
python scripts/process_batch.py --input-dir data/raw/10k --output-dir data/processed/cleaned

# Process first 50 files
python scripts/process_batch.py --batch-size 50

# Extract only Item 1A (Risk Factors)
python scripts/process_batch.py --sections item_1a

# Skip cleaning step (keep raw extracted text)
python scripts/process_batch.py --no-clean
```

**Options**:
- `--input-dir PATH`: Input directory with raw 10-K files
- `--output-dir PATH`: Output directory for processed text
- `--batch-size N`: Number of files to process
- `--skip-existing`: Skip already processed files (default)
- `--sections LIST`: Comma-separated sections (item_1,item_1a,item_7)
- `--min-section-length N`: Minimum section length (default: 1000)
- `--clean`: Clean extracted text (default)
- `--no-clean`: Skip text cleaning
- `--log-level LEVEL`: Logging level

**Output**:
- Processed files: `data/processed/cleaned/{CIK}_{YEAR}_10K_{SECTION}.txt`
- Logs: `data/processed/cleaned/processing_logs/`
- Application logs: `logs/process_batch_*.log`

**Example**:
```bash
# Process all downloads
python scripts/process_batch.py

# Check results
head -n 50 data/processed/cleaned/0000001750_2020_10K_item_1a.txt
```

---

### 3. `validate_data.py` - Validate Pipeline Data

Validates data quality at each pipeline stage.

**Usage**:
```bash
# Validate everything
python scripts/validate_data.py

# Validate only downloads
python scripts/validate_data.py --stage downloads

# Validate only processed files
python scripts/validate_data.py --stage processed

# Generate detailed report
python scripts/validate_data.py --report

# Validate specific directories
python scripts/validate_data.py \
  --firm-list data/firm_lists/target_firm_years.csv \
  --downloads-dir data/raw/10k \
  --processed-dir data/processed/cleaned
```

**Options**:
- `--stage STAGE`: Which stage to validate (downloads/processed/all)
- `--firm-list PATH`: Path to firm list CSV
- `--downloads-dir PATH`: Downloads directory
- `--processed-dir PATH`: Processed files directory
- `--report`: Generate detailed validation report
- `--output-dir PATH`: Report output directory
- `--config PATH`: Config file path
- `--log-level LEVEL`: Logging level

**Output**:
- Console summary of validation results
- Optional detailed report: `validation_reports/validation_report_*.txt`
- Application logs: `logs/validate_data_*.log`

**Example**:
```bash
# Validate all data
python scripts/validate_data.py

# Generate detailed report
python scripts/validate_data.py --report

# View report
cat validation_reports/validation_report_*.txt
```

---

## Complete Pipeline Workflow

### Step 1: Download 10-Ks

```bash
# Download all firm-years (or start with a test batch)
python scripts/download_10k.py --batch-size 100

# Check download results
cat data/raw/10k/download_logs/summary_*.txt

# Validate downloads
python scripts/validate_data.py --stage downloads
```

### Step 2: Process Files

```bash
# Parse and clean all downloaded files
python scripts/process_batch.py

# Check processing results
cat data/processed/cleaned/processing_logs/processing_summary_*.txt

# Validate processed files
python scripts/validate_data.py --stage processed
```

### Step 3: Validate Everything

```bash
# Full pipeline validation with report
python scripts/validate_data.py --report

# Review validation report
cat validation_reports/validation_report_*.txt
```

---

## Batch Processing Tips

### Processing Large Datasets

For ~8,600 firm-years, process in manageable batches:

```bash
# Download in batches of 500
for i in $(seq 0 500 8600); do
  echo "Downloading batch starting at index $i"
  python scripts/download_10k.py --start-index $i --batch-size 500
  sleep 10  # Brief pause between batches
done

# Process in batches of 500
python scripts/process_batch.py --batch-size 500
```

### Resume After Interruption

All scripts support resuming:

```bash
# Downloads automatically skip existing files
python scripts/download_10k.py --start-index 2000

# Processing automatically skips existing files
python scripts/process_batch.py --skip-existing
```

### Parallel Processing

For multi-year processing (advanced):

```bash
# Download different years in parallel (separate terminals)
python scripts/download_10k.py --batch-size 1000  # Terminal 1
python scripts/download_10k.py --start-index 1000 --batch-size 1000  # Terminal 2
```

---

## Error Handling

### Download Failures

```bash
# Check failed downloads
cat data/raw/10k/download_logs/failed_*.csv

# Retry failed downloads (they'll be automatically retried)
python scripts/download_10k.py --no-skip-existing
```

### Processing Failures

```bash
# Check processing results
cat data/processed/cleaned/processing_logs/processing_results_*.csv

# Filter for failures
grep "False" data/processed/cleaned/processing_logs/processing_results_*.csv
```

### Validation Issues

```bash
# Generate detailed validation report
python scripts/validate_data.py --report --output-dir validation_reports

# Review issues
cat validation_reports/validation_report_*.txt
```

---

## Logging

All scripts generate detailed logs:

```bash
# View latest download log
tail -f logs/download_10k_*.log

# View latest processing log
tail -f logs/process_batch_*.log

# View latest validation log
tail -f logs/validate_data_*.log

# Search for errors
grep "ERROR" logs/*.log
```

---

## Configuration

Scripts read settings from `config.yaml`:

```yaml
sec_edgar:
  rate_limit: 10  # requests per second
  user_agent: "your@email.com"
  max_retries: 3

paths:
  raw_10k: "data/raw/10k"
  cleaned_text: "data/processed/cleaned"

batch_size: 100  # default batch size

text_extraction:
  sections:
    - "item_1"
    - "item_1a"
    - "item_7"
  min_text_length: 1000
```

Override config settings via command-line arguments.

---

## Common Workflows

### Quick Test (10 files)

```bash
python scripts/download_10k.py --batch-size 10
python scripts/process_batch.py --batch-size 10
python scripts/validate_data.py
```

### Standard Batch (100 files)

```bash
python scripts/download_10k.py --batch-size 100
python scripts/process_batch.py
python scripts/validate_data.py --report
```

### Full Dataset

```bash
# Download all
python scripts/download_10k.py

# Process all
python scripts/process_batch.py

# Validate all
python scripts/validate_data.py --report
```

---

## Script Development

### Adding New Scripts

1. Create script in `scripts/` directory
2. Add shebang: `#!/usr/bin/env python3`
3. Add docstring with usage examples
4. Import from `src/` modules
5. Use `argparse` for CLI arguments
6. Setup logging with `setup_logging()`
7. Make script executable: `chmod +x scripts/your_script.py`

### Template

```python
#!/usr/bin/env python3
"""
Script Description

Usage:
    python scripts/your_script.py [args]
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.config import load_config
from src.utils.logging_utils import setup_logging

def main():
    # Your script logic
    pass

if __name__ == "__main__":
    sys.exit(main())
```

---

## Troubleshooting

See individual script documentation and `docs/TROUBLESHOOTING.md` for detailed troubleshooting guides.

---

**Last Updated**: 2026-01-21
**Version**: 1.0
