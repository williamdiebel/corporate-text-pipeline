# Data Directory

Storage for all pipeline data: input firm lists, raw downloads, and processed output.

## Directory Structure

```
data/
├── firm_lists/              # Input firm-year lists
│   ├── target_firm_years.csv     # Main target list (~8,673 firm-years)
│   └── Unique firm-year list.xlsx # Excel version
│
├── raw/                     # Raw downloaded files
│   └── 10k/                # SEC EDGAR 10-K filings
│       ├── {CIK}_{YEAR}_10K.html  # Downloaded HTML files
│       └── download_logs/         # Download tracking logs
│           ├── successful_*.csv   # Successful downloads
│           ├── failed_*.csv       # Failed downloads
│           ├── skipped_*.csv      # Skipped downloads
│           └── summary_*.txt      # Summary statistics
│
├── processed/               # Processed data
│   ├── cleaned/            # Cleaned text sections
│   │   ├── {CIK}_{YEAR}_10K_item_1.txt    # Item 1: Business
│   │   ├── {CIK}_{YEAR}_10K_item_1a.txt   # Item 1A: Risk Factors
│   │   ├── {CIK}_{YEAR}_10K_item_7.txt    # Item 7: MD&A
│   │   └── processing_logs/               # Processing logs
│   │       ├── processing_results_*.csv
│   │       └── processing_summary_*.txt
│   │
│   └── scores/             # LLM-generated scores (Phase 3)
│       └── supply_chain_scores.csv  # Final scored dataset
│
└── archive/                # Archived/backup data
    └── previous_versions/
```

---

## Input Data

### Firm Lists (`firm_lists/`)

**Purpose**: Specify which firm-years to download and process

**Main File**: `target_firm_years.csv`

**Required Columns**:
- `cik` (or `CIK`): Central Index Key (numeric)
- `year` (or `Year`, `fyear`): Fiscal year

**Example Format**:
```csv
cik,year
1750,2020
1750,2021
320193,2020
789019,2021
```

**Statistics**:
- Total firm-years: ~8,673
- Unique firms: ~1,100 US manufacturing firms
- Year range: Typically 2010-2023 (varies by event study design)

**Creating Firm Lists**:

```python
import pandas as pd

# Create firm list
firm_list = pd.DataFrame({
    'cik': ['1750', '320193', '789019'],
    'year': [2020, 2021, 2020]
})

# Save
firm_list.to_csv('data/firm_lists/my_firm_list.csv', index=False)
```

---

## Raw Data (`raw/`)

### 10-K Files (`raw/10k/`)

**Purpose**: Store downloaded 10-K HTML files from SEC EDGAR

**File Naming**: `{CIK}_{YEAR}_10K.html`
- CIK is 10-digit zero-padded (e.g., `0000001750`)
- Year is 4-digit fiscal year (e.g., `2020`)
- Example: `0000001750_2020_10K.html`

**Typical File Sizes**:
- Average: 500KB - 2MB per filing
- Large filings: Up to 20MB
- Total for 8,600 filings: ~4-17GB

**Download Logs** (`raw/10k/download_logs/`):

Files track download history and results:

1. **`successful_{timestamp}.csv`**
   ```csv
   cik,year,filename,file_size,download_time
   0000001750,2020,0000001750_2020_10K.html,1245678,1.23
   ```

2. **`failed_{timestamp}.csv`**
   ```csv
   cik,year,error,attempts
   0000999999,2020,Filing not found,3
   ```

3. **`skipped_{timestamp}.csv`**
   ```csv
   cik,year,reason
   0000001750,2020,File already exists
   ```

4. **`summary_{timestamp}.txt`**
   ```
   10-K Download Summary
   ==================================================
   timestamp: 20260121_143022
   total_attempted: 100
   successful: 95
   failed: 3
   skipped: 2
   success_rate: 96.94%
   ```

---

## Processed Data (`processed/`)

### Cleaned Text (`processed/cleaned/`)

**Purpose**: Store extracted and cleaned text sections from 10-Ks

**File Naming**: `{CIK}_{YEAR}_10K_{SECTION}.txt`
- Sections: `item_1`, `item_1a`, `item_7`
- Example: `0000001750_2020_10K_item_1a.txt`

**File Structure**:
```
processed/cleaned/
├── 0000001750_2020_10K_item_1.txt      # Business description
├── 0000001750_2020_10K_item_1a.txt     # Risk factors
├── 0000001750_2020_10K_item_7.txt      # MD&A
└── ...
```

**Typical Sizes**:
- Item 1: 10-50KB
- Item 1A: 20-100KB (often longest)
- Item 7: 30-150KB
- Total per firm-year: ~60-300KB
- Total for 8,600 firm-years: ~500MB-2.5GB

**Processing Logs** (`processed/cleaned/processing_logs/`):

1. **`processing_results_{timestamp}.csv`**
   ```csv
   filename,success,sections_extracted,sections_cleaned,item_1a_length
   0000001750_2020_10K.html,True,3,3,45678
   ```

2. **`processing_summary_{timestamp}.txt`**
   ```
   10-K Processing Summary
   ==================================================
   Total files: 100
   Successful: 98
   Failed: 2
   Success rate: 98.00%
   Average sections per file: 2.95
   ```

### Scores (`processed/scores/`)

**Purpose**: Store LLM-generated supply chain transparency scores

**Main File**: `supply_chain_scores.csv`

**Planned Schema** (Phase 3):
```csv
cik,year,filename,overall_score,environmental_score,social_score,...
0000001750,2020,0000001750_2020_10K,7.5,8.0,7.0,...
```

**Scoring Dimensions** (0-10 scale):
1. Overall supply chain transparency
2. Environmental supply chain transparency
3. Social supply chain transparency
4. Supply base transparency
5. Digital transformation
6. Supplier audits
7. Supplier code of conduct
8. Supply base reconfiguration
9. Supplier development

---

## Data Management

### Disk Space Requirements

Estimated storage for ~8,600 firm-years:

| Data Type | Size per Firm-Year | Total Size |
|-----------|-------------------|------------|
| Raw 10-Ks | 500KB - 2MB | 4-17 GB |
| Cleaned Sections | 60-300KB | 500MB-2.5GB |
| Scores CSV | ~1KB | ~9MB |
| **Total** | | **5-20 GB** |

Add 20-30% buffer for logs and temporary files.

### Backup Strategy

```bash
# Backup critical data
tar -czf backup_$(date +%Y%m%d).tar.gz data/

# Backup to external storage
rsync -av data/ /external/drive/corporate-text-pipeline/data/

# Backup only processed data (smaller)
tar -czf processed_backup_$(date +%Y%m%d).tar.gz data/processed/
```

### Cleanup

```bash
# Remove old logs (keep last 30 days)
find data/raw/10k/download_logs -name "*.csv" -mtime +30 -delete

# Remove temporary files
find data/ -name "*.tmp" -delete

# Archive old data
mv data/processed/scores/old_scores.csv data/archive/
```

---

## Data Quality

### Validation

Run validation regularly:

```bash
# Validate entire pipeline
python scripts/validate_data.py --report

# Check for missing downloads
python -c "
from src.utils import get_missing_downloads
import pandas as pd

firm_list = pd.read_csv('data/firm_lists/target_firm_years.csv')
missing = get_missing_downloads(firm_list, 'data/raw/10k')
print(f'Missing {len(missing)} downloads')
missing.to_csv('missing_downloads.csv', index=False)
"
```

### Quality Checks

Monitor these metrics:

1. **Download Success Rate**: Should be >95%
2. **Processing Success Rate**: Should be >90%
3. **Section Extraction Rate**: Should be >85% for Item 1A
4. **Average Text Length**: Items should be >1,000 characters
5. **File Corruption**: Zero corrupt files

### Data Integrity

```bash
# Check file integrity
python -c "
from pathlib import Path
from src.utils import validate_10k_file

invalid = []
for file in Path('data/raw/10k').glob('*.html'):
    is_valid, msg = validate_10k_file(file)
    if not is_valid:
        invalid.append((file.name, msg))

if invalid:
    print(f'Found {len(invalid)} invalid files')
    for name, msg in invalid[:10]:
        print(f'  {name}: {msg}')
"
```

---

## Common Operations

### List All Downloaded Firms

```bash
# List all CIK-year combinations
ls data/raw/10k/*.html | sed 's/.*\///' | sed 's/_10K.html//' | sort
```

### Count Files

```bash
# Count raw 10-Ks
ls data/raw/10k/*.html | wc -l

# Count processed sections
ls data/processed/cleaned/*_item_*.txt | wc -l

# Count by section
ls data/processed/cleaned/*_item_1a.txt | wc -l
```

### Find Specific Firms

```bash
# Find all filings for CIK 1750
ls data/raw/10k/0000001750_*.html

# Find all 2020 filings
ls data/raw/10k/*_2020_*.html

# Find Item 1A sections for 2020
ls data/processed/cleaned/*_2020_*_item_1a.txt
```

### Batch Operations

```python
from pathlib import Path
import pandas as pd

# List all processed firm-years
processed_files = list(Path('data/processed/cleaned').glob('*_item_1a.txt'))

# Extract CIK and year from filenames
results = []
for file in processed_files:
    parts = file.stem.split('_')
    cik = parts[0]
    year = parts[1]
    size = file.stat().st_size

    results.append({'cik': cik, 'year': year, 'size': size})

# Save inventory
df = pd.DataFrame(results)
df.to_csv('data_inventory.csv', index=False)
print(f"Processed {len(df)} firm-years")
```

---

## Git Ignore

These directories should be in `.gitignore`:

```gitignore
# Large data files
data/raw/
data/processed/
data/archive/

# Keep structure and samples
!data/README.md
!data/firm_lists/
!data/raw/.gitkeep
!data/processed/.gitkeep
```

Only commit:
- ✅ Firm lists (`data/firm_lists/`)
- ✅ README files
- ✅ Directory structure (via `.gitkeep` files)

Never commit:
- ❌ Raw 10-K files (too large)
- ❌ Processed text (generated)
- ❌ Log files (temporary)

---

## Data Sharing

### Sharing Processed Data

```bash
# Create compressed archive
tar -czf processed_data.tar.gz data/processed/cleaned/

# Split large archive
split -b 1000M processed_data.tar.gz processed_data.tar.gz.part_

# Combine splits
cat processed_data.tar.gz.part_* > processed_data.tar.gz
tar -xzf processed_data.tar.gz
```

### Data Transfer

```bash
# Upload to cloud storage
# AWS S3
aws s3 sync data/processed/cleaned/ s3://bucket-name/cleaned/

# Download from cloud
aws s3 sync s3://bucket-name/cleaned/ data/processed/cleaned/
```

---

## Security

### Sensitive Data

This project processes public SEC filings only - no sensitive data.

However, follow these guidelines:

✅ **Do NOT commit**:
- API keys (use environment variables)
- Credentials (use .env files)
- Personal emails (use config.yaml)

✅ **Do commit**:
- Public firm lists
- Configuration templates
- Documentation

---

## Troubleshooting

### Disk Space Full

```bash
# Check disk usage
df -h
du -sh data/*/

# Clean up logs
find data/ -name "*.log" -delete

# Compress old data
tar -czf archive_old.tar.gz data/raw/10k/old/ && rm -r data/raw/10k/old/
```

### Missing Files

```bash
# Find missing downloads
python scripts/validate_data.py --stage downloads

# Re-download missing
python scripts/download_10k.py --no-skip-existing
```

### Corrupted Files

```bash
# Validate all files
python scripts/validate_data.py --report

# Remove corrupted files
# Review validation report first, then manually delete

# Re-download
python scripts/download_10k.py --no-skip-existing
```

---

**Last Updated**: 2026-01-21
**Version**: 1.0
