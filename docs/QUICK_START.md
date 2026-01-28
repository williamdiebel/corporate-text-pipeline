# Quick Start Reference

**One-page reference for daily pipeline operations**

---

## Pre-Flight Checklist

Before running any commands:

- [ ] Terminal open in project directory: `cd ~/path/to/corporate-text-pipeline`
- [ ] Virtual environment activated: `source venv/bin/activate` (see `(venv)` prefix)
- [ ] Latest code pulled: `git pull origin main`
- [ ] Config verified: `data_root` in `config.yaml` points to Dropbox

---

## Pipeline Commands

### Stage 1: Download 10-K Filings

```bash
# Download all filings
download-10k

# Download test batch (recommended first)
download-10k --batch-size 10

# Resume from specific index
download-10k --start-index 500 --batch-size 100
```

**Output location:** `{Dropbox}/raw/10k/*.html`

**Verify:** `ls {Dropbox}/raw/10k/ | wc -l`

---

### Stage 2: Process Files (Parse & Clean)

```bash
# Process all downloaded files
process-batch

# Process test batch
process-batch --batch-size 10
```

**Output location:** `{Dropbox}/processed/cleaned/*.txt`

**Verify:** `ls {Dropbox}/processed/cleaned/ | wc -l`

---

### Stage 3: Validate Data

```bash
# Quick validation
validate-data

# Generate detailed report
validate-data --report
```

---

### Stage 4: Score with LLM (Coming Soon)

```bash
# Score all processed files
score-batch

# Score test batch
score-batch --batch-size 10
```

**Output location:** `{Dropbox}/processed/scores/*.csv`

---

## Quick Validation Commands

```bash
# Count downloaded files
ls {Dropbox}/raw/10k/*.html 2>/dev/null | wc -l

# Count processed files
ls {Dropbox}/processed/cleaned/*.txt 2>/dev/null | wc -l

# Check for failed downloads
cat {Dropbox}/raw/10k/download_logs/failed_*.csv

# Check processing logs
cat {Dropbox}/processed/cleaned/processing_logs/summary_*.txt
```

---

## Common Issues (Quick Fixes)

| Problem | Solution |
|---------|----------|
| `command not found` | Run `pip install -e .` |
| `(venv)` not showing | Run `source venv/bin/activate` |
| 403 errors | Check email in `config.yaml` |
| Files not in Dropbox | Check `data_root` in `config.yaml` |

---

## Need Help?

- **Setup issues:** See [SETUP.md](SETUP.md)
- **Workflow questions:** See [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md)
- **Errors:** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **Contact:** Will Diebel (william.diebel@moore.sc.edu)

---

*Last Updated: January 2026*
