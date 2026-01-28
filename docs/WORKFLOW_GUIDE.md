# Workflow Guide

**Complete operational guide for the Corporate Text Pipeline**

---

## Overview

### What This Pipeline Does

This pipeline automates the measurement of supply chain transparency from SEC 10-K filings. It downloads annual reports, extracts relevant sections, cleans the text, and scores companies on transparency dimensions using AI.

### The 5-Stage Pipeline

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  DOWNLOAD   │───▶│   PROCESS   │───▶│    SCORE    │───▶│    MERGE    │───▶│   ANALYZE   │
│   10-Ks     │    │   (Parse)   │    │   (LLM)     │    │   (Panel)   │    │   (Stats)   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
     │                   │                  │                  │                  │
     ▼                   ▼                  ▼                  ▼                  ▼
  raw/10k/         processed/          processed/          final/            analysis/
  *.html           cleaned/*.txt       scores/*.csv        panel.csv         results/
```

### What We Measure

| Construct | Category | Description |
|-----------|----------|-------------|
| Supply Chain Transparency (Aggregate) | Outcome | Overall upstream disclosure |
| Environmental SCT | Outcome | Environmental impacts/risks |
| Social SCT | Outcome | Social impacts/risks |
| Supply Base Transparency | Outcome | Tier-1 supplier disclosures |
| Digital Transformation | Mechanism | Supply chain technology adoption |
| Supplier Audits | Mechanism | Systematic supplier evaluations |
| Supplier Code of Conduct | Mechanism | Formal supplier standards |
| Supply Base Reconfiguration | Mechanism | Supplier restructuring |
| Supplier Development | Mechanism | Supplier capability building |

### Team Roles

| Person | Role | Responsibilities |
|--------|------|------------------|
| **Will** | PI / Developer | Pipeline architecture, troubleshooting, oversight |
| **Katelyn** | PhD Student | Pilot validation, rubric development, full pipeline runs |
| **Lachlan** | RA | Pipeline runs, quality checks, progress monitoring |

---

## Stage 1: Download 10-K Filings

### What This Does

Downloads HTML 10-K filings from SEC EDGAR for each firm-year in your target list.

### Quick Start

```bash
# Test with small batch first
download-10k --batch-size 10

# Download all filings
download-10k
```

### Command Options

| Option | Default | Description |
|--------|---------|-------------|
| `--batch-size N` | All | Number of firm-years to download |
| `--start-index N` | 0 | Starting row in firm list |
| `--skip-existing` | True | Skip files that already exist |
| `--no-skip-existing` | - | Re-download existing files |
| `--config PATH` | config.yaml | Path to config file |
| `--log-level` | INFO | Logging verbosity |

### Output Location

Files save to: `{Dropbox}/raw/10k/{CIK}_{YEAR}_10K.html`

Example: `0000001750_2020_10K.html`

### Quality Control Checklist

After downloading, verify:

- [ ] Download count matches expected firm-years
- [ ] Review `download_logs/failed_*.csv` for errors
- [ ] Spot-check 3 random files (open in browser, verify content)
- [ ] Log any issues in progress tracker spreadsheet

### Common Issues

- **403 Forbidden:** Invalid email in `config.yaml` - use your real email
- **Slow downloads:** Normal - SEC limits to 10 requests/second
- **Missing filings:** Some firm-years don't have 10-Ks filed - check `failed_*.csv`

---

## Stage 2: Process Files (Parse & Clean)

### What This Does

Extracts Items 1, 1A, and 7 from each 10-K and cleans the text (removes tables, HTML artifacts, boilerplate).

### Quick Start

```bash
# Test with small batch first
process-batch --batch-size 10

# Process all downloaded files
process-batch
```

### Command Options

| Option | Default | Description |
|--------|---------|-------------|
| `--batch-size N` | All | Number of files to process |
| `--start-index N` | 0 | Starting index |
| `--input-dir PATH` | From config | Override input directory |
| `--output-dir PATH` | From config | Override output directory |
| `--log-level` | INFO | Logging verbosity |

### Output Location

Files save to: `{Dropbox}/processed/cleaned/{CIK}_{YEAR}_10K.txt`

Each file contains all three sections with clear headers:

```
================================================================================
ITEM 1: BUSINESS DESCRIPTION
================================================================================
[content]

================================================================================
ITEM 1A: RISK FACTORS
================================================================================
[content]

================================================================================
ITEM 7: MANAGEMENT DISCUSSION AND ANALYSIS
================================================================================
[content]
```

### Quality Control Checklist

After processing, verify:

- [ ] Output file count matches input file count (approximately)
- [ ] Section headers (`=== ITEM`) present in output files
- [ ] Check processing logs for success rate (target: >90%)
- [ ] Open 3 random outputs - text readable, no HTML tags, no garbled characters

### Common Issues

- **Empty sections:** Some 10-Ks have non-standard formatting - logged in processing report
- **HTML artifacts:** Parser handles most cases; report persistent issues to Will
- **Missing files:** Processing only runs on existing downloads - check Stage 1 first

---

## Stage 3: Score with LLM

### What This Does

Sends cleaned text to GPT 5.2 API to score each firm-year on all 9 transparency constructs.

### Quick Start

```bash
# Test with small batch first
score-batch --batch-size 10

# Score all processed files
score-batch
```

### Command Options

| Option | Default | Description |
|--------|---------|-------------|
| `--batch-size N` | All | Number of files to score |
| `--start-index N` | 0 | Starting index |
| `--model` | gpt-5.2 | LLM model to use |
| `--temperature` | 0.0 | Randomness (0 = deterministic) |

### Output Location

Scores save to: `{Dropbox}/processed/scores/transparency_scores.csv`

Format:
```csv
cik,year,sct_aggregate,sct_environmental,sct_social,supply_base_transparency,...
0000001750,2020,7.5,6.2,8.1,5.4,...
```

### Quality Control Checklist

After scoring, verify:

- [ ] Score count matches processed file count
- [ ] All scores in expected range (0-10)
- [ ] No missing values in required columns
- [ ] Spot-check 5 scores against manual reading of original text
- [ ] Review distribution - no unusual clustering at 0 or 10

### Common Issues

- **API errors:** Check API key in config; monitor rate limits
- **Slow scoring:** Normal - API calls take time; use batching
- **Inconsistent scores:** Verify temperature=0; check prompt consistency

---

## Stage 4: Merge to Panel Dataset

### What This Does

Combines all scores into a single panel dataset ready for econometric analysis.

### Quick Start

```bash
# Create analysis dataset
create-dataset
```

### Output Location

Final dataset: `{Dropbox}/final/analysis_panel.csv`

### Quality Control Checklist

- [ ] Row count matches expected firm-years
- [ ] All required columns present
- [ ] No duplicate firm-year observations
- [ ] Merge with external data successful (if applicable)

---

## Team Coordination

### Daily Workflow

1. **Start of session:**
   - Pull latest code: `git pull origin main`
   - Check shared progress tracker for assigned work
   - Verify Dropbox sync is current

2. **During work:**
   - Run assigned batches
   - Log progress in shared tracker
   - Note any errors or unusual results

3. **End of session:**
   - Update progress tracker with completion status
   - Push any code changes: `git add . && git commit -m "message" && git push`
   - Note blockers or questions for next sync

### Progress Tracking

Use the shared spreadsheet to track:

| Batch | CIK Range | Assigned To | Download | Process | Score | Notes |
|-------|-----------|-------------|----------|---------|-------|-------|
| 1 | 0-1000 | Katelyn | Done | Done | Pending | |
| 2 | 1001-2000 | Lachlan | In Progress | | | Started 1/25 |

### Communication Protocol

- **Daily updates:** Post in Slack/Teams with brief status
- **Blockers:** Escalate to Will immediately
- **Questions:** Post in shared channel; check before starting new work
- **Errors:** Screenshot + log file + description of what you were doing

### Splitting Work

To avoid duplicate processing:

```bash
# Katelyn: rows 0-4000
download-10k --start-index 0 --batch-size 4000

# Lachlan: rows 4001-8672
download-10k --start-index 4001 --batch-size 4672
```

---

## File Locations Summary

| Stage | Location | File Pattern |
|-------|----------|--------------|
| Input (firm list) | `data/firm_lists/` | `target_firm_years.csv` |
| Downloaded 10-Ks | `{Dropbox}/raw/10k/` | `{CIK}_{YEAR}_10K.html` |
| Processed text | `{Dropbox}/processed/cleaned/` | `{CIK}_{YEAR}_10K.txt` |
| LLM scores | `{Dropbox}/processed/scores/` | `transparency_scores.csv` |
| Final dataset | `{Dropbox}/final/` | `analysis_panel.csv` |
| Logs | `{Dropbox}/logs/` | Various `.log` and `.csv` |

---

## Appendix: Expected Timeline

| Week | Stage | Target |
|------|-------|--------|
| 1-2 | Download + Process | All 8,672 firm-years downloaded and processed |
| 3-4 | Pilot Scoring | 100-firm sample scored and validated |
| 5-6 | Full Scoring | All firm-years scored |
| 7+ | Analysis | Panel merged and analysis begun |

---

*Last Updated: January 2026*
