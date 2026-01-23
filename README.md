# Corporate Text Pipeline

**Automated pipeline for measuring supply chain transparency from 10-K filings**

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📖 Table of Contents

- [What is This Project?](#what-is-this-project)
- [For Complete Beginners](#for-complete-beginners)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [How to Use the Pipeline](#how-to-use-the-pipeline)
- [For Developers](#for-developers)
- [Troubleshooting](#troubleshooting)
- [Team](#team)

---

## 🎯 What is This Project?

This project helps researchers measure **supply chain transparency** by analyzing corporate 10-K filings (annual reports that public companies must file with the SEC).

### Research Question
Do supply chain executive appointments increase supply chain transparency? What management practices moderate this relationship?

### What We Measure
We analyze ~1,100 US manufacturing firms to score them on 9 dimensions:

**Transparency (Primary Outcomes)**:
1. Overall supply chain transparency
2. Environmental supply chain transparency
3. Social supply chain transparency
4. Supply base transparency

**Management Practices (Moderators)**:
5. Digital transformation
6. Supplier audits
7. Supplier code of conduct
8. Supply base reconfiguration
9. Supplier development

### How It Works
```
10-K Filing → Download → Parse → Clean → LLM Scoring → Analysis
```

---

## 👶 For Complete Beginners

### What is Python?
Python is a programming language. Think of it as a way to give instructions to your computer. This project is written in Python, which means it's a collection of instructions that download and analyze documents automatically.

### What is Git/GitHub?
- **Git**: A system for tracking changes to files (like "Track Changes" in Word, but much more powerful)
- **GitHub**: A website where we store our project so the team can collaborate

### What is a "Repository" (or "Repo")?
A repository is like a project folder that's tracked with Git. This repo contains all our code, data, and documentation.

### What is a "Virtual Environment" (venv)?
Python projects need specific versions of tools (called "packages"). A virtual environment is like a separate workspace where we install exactly what THIS project needs, without interfering with other Python projects on your computer.

Think of it like having a separate toolbox for each project.

### File Organization Analogy
```
corporate-text-pipeline/     ← The project folder
├── src/                     ← The tools/library 
│   ├── downloaders/        ← Tools for downloading
│   ├── processors/         ← Tools for processing text
│   └── utils/              ← Helper tools
├── scripts/                ← Ready-to-use programs (we'll use these -- automatically accesses tools in library)
├── data/                   ← Where we store files
├── docs/                   ← Instruction manuals
└── tests/                  ← Quality checks
```

---

## 🚀 Quick Start

### Prerequisites

1. **Python 3.9 or newer** - [Download here](https://www.python.org/downloads/)
2. **Git** - [Download here](https://git-scm.com/downloads)
3. **A text editor** - VS Code recommended ([Download](https://code.visualstudio.com/))

### Installation (Step-by-Step)

#### Step 1: Get the Code

Open Terminal (Mac) or Command Prompt (Windows) and run:

```bash
# Go to where you want to put the project
cd ~/Documents  # or wherever you want

# Download the project from GitHub
git clone https://github.com/williamdiebel/corporate-text-pipeline.git

# Go into the project folder
cd corporate-text-pipeline
```

#### Step 2: Create a Virtual Environment

```bash
# Create a virtual environment named "venv"
python3 -m venv venv

# Activate it (Mac/Linux):
source venv/bin/activate

# Activate it (Windows):
venv\Scripts\activate

# You should see (venv) at the start of your terminal line
```

#### Step 3: Install the Project

```bash
# Install everything you need (this might take a few minutes)
pip install -e .

# This installs:
# - All the required packages
# - The pipeline tools
# - Command-line shortcuts
```

#### Step 4: Configure Your Email

The SEC requires you to identify yourself when downloading files.

```bash
# Open config.yaml in a text editor
# Find this line:
#   user_agent: "william.diebel@moore.sc.edu"
# Replace with YOUR email:
#   user_agent: "your.email@university.edu"
```

#### Step 5: Test It Works

```bash
# Download 10 test filings
download-10k --batch-size 10

# If successful, you'll see files in data/raw/10k/
ls data/raw/10k/
```

**Congratulations!** 🎉 You've set up the pipeline!

---

## 📁 Project Structure

### Overview

```
corporate-text-pipeline/
│
├── 📚 src/                          # The library (reusable tools)
│   ├── downloaders/                # Download 10-K filings
│   │   ├── sec_downloader.py      # SEC EDGAR downloader
│   │   └── csr_downloader.py      # CSR downloader (future)
│   ├── processors/                 # Parse and clean text
│   │   ├── parser.py              # Extract sections from 10-Ks
│   │   └── text_cleaner.py        # Clean extracted text
│   ├── utils/                      # Helper utilities
│   │   ├── validators.py          # Data validation
│   │   └── logging_utils.py       # Logging setup
│   └── config.py                   # Configuration loader
│
├── 🚀 scripts/                      # Executable programs
│   ├── download_10k.py            # Download 10-K filings
│   ├── process_batch.py           # Parse and clean files
│   └── validate_data.py           # Validate data quality
│
├── 🗄️  data/                        # Data storage
│   ├── firm_lists/                # Input: which firms to analyze
│   ├── raw/10k/                   # Downloaded 10-K files
│   └── processed/cleaned/         # Processed text
│
├── 📖 docs/                         # Documentation
│   ├── SETUP.md                   # Setup instructions
│   ├── USAGE.md                   # How to use the pipeline
│   └── github_guide.md            # Git/GitHub guide
│
├── 🧪 tests/                        # Automated tests
│   ├── test_downloaders.py
│   ├── test_processors.py
│   └── test_utils.py
│
├── 📓 notebooks/                    # Jupyter notebooks for analysis
│
├── ⚙️  config.yaml                   # Project settings
├── 📋 pyproject.toml               # Project metadata & dependencies
└── 📄 README.md                    # This file!
```

### What's What?

#### `src/` - The Library (The Toolbox)

**Think of this as**: A toolbox full of tools you can use

**What it contains**: Python classes and functions that do the actual work
- **Downloaders**: Get files from the internet
- **Processors**: Read and clean text
- **Utils**: Helper functions

**You use it by**: Importing in other code
```python
from src.downloaders import SECDownloader
downloader = SECDownloader(...)
```

**You DON'T**: Run files in src/ directly

#### `scripts/` - Executable Programs (Pre-Built Tools)

**Think of this as**: Pre-assembled tools ready to use

**What it contains**: Programs you can run from the command line

**You use it by**: Running from terminal
```bash
python scripts/download_10k.py --batch-size 100
# OR (after installation):
download-10k --batch-size 100
```

**When to use**: When you want to run standard pipeline tasks

#### `data/` - Data Storage (Filing Cabinet)

**What it contains**:
- **Input**: Lists of firms to analyze
- **Raw**: Downloaded 10-K files
- **Processed**: Cleaned, extracted text
- **Scores**: LLM-generated scores (future)

**Important**: This folder is NOT tracked in Git (files are too large)

#### `docs/` - Documentation (Instruction Manuals)

**What it contains**: Guides and how-tos
- `SETUP.md` - First-time setup
- `USAGE.md` - How to use the pipeline
- `github_guide.md` - Git/GitHub basics

#### `tests/` - Automated Tests (Quality Checks)

**What it contains**: Code that tests if everything works correctly

**You use it by**: Running pytest
```bash
pytest tests/
```

**Why it matters**: Catches bugs before they cause problems

---

## 🔄 How to Use the Pipeline

### The Complete Workflow

#### Stage 1: Download 10-K Filings

```bash
# Download all filings in your firm list
download-10k

# OR download a test batch first
download-10k --batch-size 10

# Where files go: data/raw/10k/
```

**What happens**: Downloads HTML files from SEC EDGAR

**Time**: ~15-30 minutes for ~8,600 filings

#### Stage 2: Process Files (Parse & Clean)

```bash
# Process all downloaded files
process-batch

# OR process just a few for testing
process-batch --batch-size 10

# Where files go: data/processed/cleaned/
```

**What happens**:
1. Extracts Items 1, 1A, and 7 from each 10-K
2. Cleans the text (removes tables, formatting, etc.)
3. Saves as clean text files

**Time**: ~20-40 minutes for ~8,600 filings

#### Stage 3: Validate Data

```bash
# Check everything is working correctly
validate-data

# Generate a detailed report
validate-data --report
```

**What happens**:
- Checks if files downloaded correctly
- Validates text quality
- Reports missing or corrupted files

#### Stage 4: LLM Scoring (Coming Soon)

This will use Claude or GPT to score each firm on the 9 dimensions.

---

## 🛠️ For Developers

### Running from Python Code

You can use the library directly in your own Python scripts:

```python
from src.downloaders import SECDownloader
from src.processors import TenKParser, TextCleaner

# Download a specific filing
downloader = SECDownloader(
    user_agent="your@email.com",
    output_dir="data/raw/10k"
)
success, filepath = downloader.download_10k(cik="1750", year=2020)

# Parse it
if success:
    parser = TenKParser()
    sections = parser.parse_file(filepath)

    # Clean the Risk Factors section
    cleaner = TextCleaner()
    clean_text = cleaner.clean(sections['item_1a'])

    print(f"Risk Factors: {len(clean_text)} characters")
```

### Running in Jupyter Notebooks

```bash
# Install with analysis tools
pip install -e ".[analysis]"

# Start Jupyter
jupyter notebook

# Open notebooks/exploratory_analysis.ipynb
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage report
pytest tests/ --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Installing for Development

```bash
# Install with development tools
pip install -e ".[dev]"

# This gives you:
# - pytest (testing)
# - pytest-cov (coverage)
# - ipython (better Python shell)
```

---

## 🆘 Troubleshooting

### "Command not found" errors

**Problem**: `download-10k: command not found`

**Solution**: Make sure you installed the package:
```bash
pip install -e .
```

### "Permission denied" errors

**Problem**: Can't write to data folder

**Solution**: Check folder permissions:
```bash
chmod -R u+w data/
```

### "Module not found" errors

**Problem**: `ModuleNotFoundError: No module named 'src'`

**Solution**: Install the package in editable mode:
```bash
pip install -e .
```

### Virtual environment not activating

**Mac/Linux**:
```bash
source venv/bin/activate
```

**Windows**:
```bash
venv\Scripts\activate
```

### Downloads failing with 403 error

**Problem**: SEC blocking your requests

**Solution**: Check your email in `config.yaml`:
```yaml
sec_edgar:
  user_agent: "your.email@university.edu"  # Must be a real email!
```

---

## 📚 Additional Resources

### For Beginners

- [Python Basics Tutorial](https://docs.python.org/3/tutorial/)
- [Git and GitHub Basics](https://docs.github.com/en/get-started)
- Our [GitHub Guide](docs/github_guide.md) - team-specific git workflows

### Project Documentation

- [Setup Guide](docs/SETUP.md) - Detailed setup instructions
- [Usage Guide](docs/USAGE.md) - How to use each tool
- [Downloader Guide](docs/DOWNLOADER_USAGE.md) - Download 10-Ks
- [Data Dictionary](docs/DATA_DICTIONARY.md) - What each variable means

### Code Documentation

- [src/](src/) - Library modules (see README in each folder)
- [scripts/](scripts/) - Executable programs (see README)
- [tests/](tests/) - Test suite (see README)
- [data/](data/) - Data organization (see README)

---

## 👥 Team

**Assistant Professor**: Will Diebel (william.diebel@moore.sc.edu)

**PhD Student**: Katelyn Thompson (katelyn.thompson@grad.moore.sc.edu)

**Undergraduate RA**: Lachlan Carroll (ldc2@email.sc.edu)

**Institution**: University of South Carolina - Darla Moore School of Business

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙋 Getting Help

1. **Check the docs** - Look in `docs/` folder
2. **Run validation** - `validate-data` might tell you what's wrong
3. **Check logs** - Look in `logs/` folder for error details
4. **Ask the team** - Use GitHub Issues or email Will

---

## 🎯 Next Steps

**For New Team Members**:
1. ✅ Complete [Quick Start](#quick-start) above
2. ✅ Read [docs/SETUP.md](docs/SETUP.md)
3. ✅ Read [docs/github_guide.md](docs/github_guide.md)
4. ✅ Try downloading 10 test filings
5. ✅ Try processing those test filings
6. ✅ Run validation

**For Development**:
1. ✅ Read [For Developers](#for-developers) section
2. ✅ Explore the code in `src/`
3. ✅ Run tests with `pytest tests/`
4. ✅ Try the examples in Jupyter notebooks

**Questions?** Email Will or create a GitHub Issue!

---

**Last Updated**: January 2026
**Version**: 0.1.0
