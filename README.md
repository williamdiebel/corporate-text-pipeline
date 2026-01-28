# Corporate Text Pipeline

**Automated pipeline for measuring supply chain transparency from 10-K filings**

---

## What This Project Does

This pipeline automates the measurement of supply chain transparency by analyzing corporate 10-K filings (annual reports filed with the SEC). It downloads filings for ~1,100 US manufacturing firms across multiple years, extracts relevant sections, and uses AI to score each firm on transparency dimensions.

**Research Question:** Do supply chain executive appointments increase supply chain transparency? What management practices moderate this relationship?

The pipeline replaces months of manual coding with automated processing, enabling systematic analysis of thousands of documents while maintaining consistency and reproducibility.

---

## What We Measure

| Construct | Category | Description |
|-----------|----------|-------------|
| Supply Chain Transparency (Aggregate) | Outcome | Overall upstream disclosure |
| Environmental SCT | Outcome | Environmental impacts/risks in supply chain |
| Social SCT | Outcome | Social impacts/risks in supply chain |
| Supply Base Transparency | Outcome | Disclosures about tier-1 suppliers |
| Digital Transformation | Mechanism | Supply chain technology adoption |
| Supplier Audits | Mechanism | Systematic supplier evaluations |
| Supplier Code of Conduct | Mechanism | Formal supplier standards |
| Supply Base Reconfiguration | Mechanism | Supplier restructuring activities |
| Supplier Development | Mechanism | Supplier capability building efforts |

---

## Quick Links

| I want to... | Go to... |
|--------------|----------|
| Set up the pipeline for the first time | [docs/SETUP.md](docs/SETUP.md) |
| Run a command right now | [docs/QUICK_START.md](docs/QUICK_START.md) |
| Understand the full workflow | [docs/WORKFLOW_GUIDE.md](docs/WORKFLOW_GUIDE.md) |
| Fix an error | [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) |
| Understand the architecture | [NotesForWill.md](NotesForWill.md) |

---

## Project Structure

```
corporate-text-pipeline/
├── src/                    # Core library code
│   ├── downloaders/        # SEC EDGAR download tools
│   ├── processors/         # Text extraction & cleaning
│   └── utils/              # Helper functions
│
├── scripts/                # Executable pipeline scripts
│   ├── download_10k.py     # → download-10k command
│   └── process_batch.py    # → process-batch command
│
├── data/                   # Configuration files (data in Dropbox)
│   └── firm_lists/         # Target firm-year lists
│
├── docs/                   # Documentation
│   ├── SETUP.md            # First-time installation
│   ├── QUICK_START.md      # Command quick reference
│   ├── WORKFLOW_GUIDE.md   # Full operational guide
│   └── TROUBLESHOOTING.md  # Error solutions
│
├── config.yaml             # Pipeline settings
└── NotesForWill.md         # Architecture documentation
```

**Note:** Data files (10-Ks, processed text, scores) are stored in a shared Dropbox folder, not in git. See [SETUP.md](docs/SETUP.md) for configuration.

---

## The Pipeline

```
Download → Process → Score → Merge → Analyze
   │          │        │        │        │
   ▼          ▼        ▼        ▼        ▼
 HTML      Clean     LLM      Panel   Results
 files     text     scores    data
```

1. **Download:** Fetch 10-K filings from SEC EDGAR
2. **Process:** Extract Items 1, 1A, 7 and clean text
3. **Score:** Use GPT to score transparency constructs
4. **Merge:** Combine into panel dataset
5. **Analyze:** Statistical analysis

---

## Getting Started

**New to the project?**

1. Follow [docs/SETUP.md](docs/SETUP.md) for installation
2. Read [docs/WORKFLOW_GUIDE.md](docs/WORKFLOW_GUIDE.md) for operations
3. Use [docs/QUICK_START.md](docs/QUICK_START.md) as daily reference

**Quick test after setup:**
```bash
source venv/bin/activate
download-10k --batch-size 3
```

---

## Team

| Role | Name | Email |
|------|------|-------|
| PI | Will Diebel | william.diebel@moore.sc.edu |
| PhD Student | Katelyn Thompson | katelyn.thompson@grad.moore.sc.edu |
| Research Assistant | Lachlan Carroll | ldc2@email.sc.edu |

**Institution:** University of South Carolina - Darla Moore School of Business

---

## License

MIT License - See LICENSE file for details.

---

*Last Updated: January 2026 | Version: 0.2.0*
