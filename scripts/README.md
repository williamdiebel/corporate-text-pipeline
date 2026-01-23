# scripts/ - Ready-to-Use Programs

**The scripts you'll actually run to download and process 10-K filings**

---

## 🎯 For Students & Research Assistants

**This is where you'll spend most of your time!** These are the programs you run to do your work.

---

## 📚 What's in This Folder?

```
scripts/
├── download_10k.py      # Download 10-K filings from SEC
├── process_batch.py     # Parse and clean downloaded files
└── validate_data.py     # Check data quality
```

---

## 🚀 The Three Scripts You'll Use

### 1. Download 10-Ks (`download_10k.py`)

**What it does**: Downloads 10-K filings from the SEC website

**When to use it**: When you need to download new filings

**Basic command**:
```bash
# Download first 10 files (for testing)
download-10k --batch-size 10

# Download first 100 files
download-10k --batch-size 100

# Download all files from the firm list
download-10k
```

**What you'll see**:
```
Downloading 10 10-K filings...
Progress: 10/10 | Success: 10 | Failed: 0
Download Complete!
```

**Where files go**: `data/raw/10k/`

---

### 2. Process Files (`process_batch.py`)

**What it does**: Extracts and cleans text from downloaded 10-Ks

**When to use it**: After downloading, to get clean text sections

**Basic command**:
```bash
# Process all downloaded files
process-batch

# Process first 10 files (for testing)
process-batch --batch-size 10
```

**What you'll see**:
```
Processing 10 files...
Progress: 10/10 | Success: 10 | Failed: 0
Processing Complete!
```

**Where files go**: `data/processed/cleaned/`

---

### 3. Validate Data (`validate_data.py`)

**What it does**: Checks that everything downloaded and processed correctly

**When to use it**: To verify data quality and find problems

**Basic command**:
```bash
# Validate everything
validate-data

# Generate detailed report
validate-data --report
```

**What you'll see**:
```
Validation Summary:
✓ Firm list: Valid (8,673 firm-years)
✓ Downloads: 8,500/8,673 (98.0%)
✓ Processed: 8,400/8,500 (98.8%)
```

---

## 📋 Common Workflow

**Step 1: Download** (Takes 10-30 minutes for full dataset)
```bash
download-10k --batch-size 100
```

**Step 2: Process** (Takes 5-10 minutes)
```bash
process-batch
```

**Step 3: Validate** (Takes 1-2 minutes)
```bash
validate-data --report
```

**Step 4: Check Results**
```bash
# Look at downloaded files
ls data/raw/10k/

# Look at processed files
ls data/processed/cleaned/

# Read the validation report
cat validation_reports/validation_report_*.txt
```

---

## 💡 Tips for Students

### Starting Your Work Session

```bash
# 1. Navigate to project
cd ~/Documents/corporate-text-pipeline

# 2. Activate virtual environment
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# 3. Run your commands
download-10k --batch-size 50
```

### Testing Before Full Run

**Always test with a small batch first!**

```bash
# Download just 10 files
download-10k --batch-size 10

# Process just those 10 files
process-batch --batch-size 10

# Validate
validate-data
```

If the test works, then run the full batch.

### If Something Fails

1. **Check the logs**:
   ```bash
   ls logs/
   tail -n 50 logs/download_10k_*.log
   ```

2. **Run validation**:
   ```bash
   validate-data --report
   ```

3. **Ask Will for help** with the error message from the logs

---

## 🔍 Understanding Output

### Downloads Create These Files

```
data/raw/10k/
├── 0000001750_2020_10K.html        # Raw 10-K filing
├── 0000001750_2021_10K.html
└── download_logs/
    ├── successful_*.csv            # List of successful downloads
    ├── failed_*.csv                # List of failed downloads
    └── summary_*.txt               # Summary statistics
```

### Processing Creates These Files

```
data/processed/cleaned/
├── 0000001750_2020_10K_item_1.txt     # Business section
├── 0000001750_2020_10K_item_1a.txt    # Risk Factors section
├── 0000001750_2020_10K_item_7.txt     # MD&A section
└── processing_logs/
    ├── processing_results_*.csv       # Processing results
    └── processing_summary_*.txt       # Summary statistics
```

---

## 📖 Advanced Options (Optional)

### Download Script Options

```bash
# Resume from a specific position
download-10k --start-index 500 --batch-size 100

# Re-download existing files
download-10k --no-skip-existing

# Use different output directory
download-10k --output-dir custom/directory
```

### Process Script Options

```bash
# Extract only Risk Factors (Item 1A)
process-batch --sections item_1a

# Skip the cleaning step
process-batch --no-clean

# Process specific input directory
process-batch --input-dir data/raw/10k --output-dir data/processed/cleaned
```

### Validate Script Options

```bash
# Validate only downloads
validate-data --stage downloads

# Validate only processed files
validate-data --stage processed
```

---

## 🆘 Troubleshooting

### "Command not found"

**Problem**: `download-10k: command not found`

**Solution**: Make sure your virtual environment is activated
```bash
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### "403 Forbidden" error

**Problem**: SEC is blocking downloads

**Solution**: Check that your email is in `config.yaml`
```bash
# Open config.yaml and verify this line:
user_agent: "your.actual.email@university.edu"
```

### Downloads are slow

**This is normal!** The SEC limits downloads to 10 per second.
- 100 filings ≈ 10-15 seconds
- 1,000 filings ≈ 2-3 minutes
- 8,600 filings ≈ 15-30 minutes

---

## 🔍 Main Documentation

For complete details, see:

- **[Main README](../README.md)** - Project overview
- **[Setup Guide](../docs/SETUP.md)** - Installation instructions
- **[Usage Guide](../docs/USAGE.md)** - Detailed usage examples

---

**Last Updated**: January 2026
**Version**: 1.0
