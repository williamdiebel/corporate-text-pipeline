# data/ - Data Configuration

**This directory contains only configuration files. Actual data lives in Dropbox.**

---

## What's Here

```
data/
├── firm_lists/                 # Git-tracked input files
│   └── target_firm_years.csv   # List of firm-years to process
└── README.md                   # This file
```

---

## Where Data Files Live

All downloaded and processed files are stored in a **shared Dropbox folder**, not in this directory. This keeps the git repository lightweight.

### Dropbox Structure

```
Dropbox/corporate-text-pipeline-data/
├── raw/
│   └── 10k/                    # Downloaded 10-K HTML files
│       └── download_logs/      # Download status logs
├── processed/
│   ├── cleaned/                # Extracted/cleaned text files
│   └── scores/                 # LLM scoring output
└── logs/                       # Processing logs
```

### Configuration

Set your Dropbox path in `config.yaml`:

```yaml
data_root: "/Users/YourName/Dropbox/corporate-text-pipeline-data"
```

See [docs/SETUP.md](../docs/SETUP.md) for full configuration instructions.

---

## firm_lists/

This directory contains input CSV files specifying which firm-years to process.

**Main file:** `target_firm_years.csv`

**Format:**
```csv
cik,year
1750,2020
1750,2021
320193,2020
```

**Statistics:**
- ~8,673 firm-year observations
- ~1,100 unique US manufacturing firms
- Years: 2006-2022

---

## What NOT to Put Here

Do not add to this directory:
- Downloaded 10-K files (go to Dropbox)
- Processed text files (go to Dropbox)
- Score outputs (go to Dropbox)
- Large files of any kind

These are gitignored and should be in the shared Dropbox folder.

---

*Last Updated: January 2026*
