# Setup Guide

**First-time installation for the Corporate Text Pipeline**

---

## Prerequisites

Before starting, you'll need:

- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Git** - [Download](https://git-scm.com/downloads)
- **VS Code** (recommended) - [Download](https://code.visualstudio.com/)
- **Dropbox access** - Request from Will

---

## Step 1: Install Python

**Check if already installed:**
```bash
python3 --version
```

If you see `Python 3.9.x` or higher, skip to Step 2.

**Install Python:**
- **Mac:** `brew install python@3.11` or download from python.org
- **Windows:** Download from python.org (check "Add Python to PATH" during install)
- **Linux:** `sudo apt install python3.11 python3.11-venv`

---

## Step 2: Install Git

**Check if already installed:**
```bash
git --version
```

If you see a version number, skip to Step 3.

**Install Git:**
- **Mac:** `brew install git` or download from git-scm.com
- **Windows:** Download from git-scm.com
- **Linux:** `sudo apt install git`

---

## Step 3: Configure Git Identity

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@university.edu"
```

---

## Step 4: Clone the Repository

```bash
# Navigate to where you want the project
cd ~/Documents

# Clone the repository
git clone https://github.com/williamdiebel/corporate-text-pipeline.git

# Enter the project folder
cd corporate-text-pipeline
```

**Verify:** You should see `src/`, `scripts/`, `docs/`, `config.yaml`, etc.

---

## Step 5: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it (Mac/Linux)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate
```

**Verify:** You should see `(venv)` at the start of your terminal prompt.

---

## Step 6: Install the Pipeline

```bash
# Upgrade pip first
pip install --upgrade pip

# Install the pipeline
pip install -e .
```

**Verify installation:**
```bash
download-10k --help
process-batch --help
```

If these show help text, installation succeeded.

---

## Step 7: Configure Settings

### 7a: Set Your SEC Email

The SEC requires identification. Open `config.yaml` and update:

```yaml
sec_edgar:
  user_agent: "your.name@university.edu"  # Use YOUR email
```

### 7b: Set Dropbox Data Path

Set where data files will be stored:

```yaml
data_root: "/Users/YourName/Dropbox/corporate-text-pipeline-data"  # Mac
# data_root: "C:/Users/YourName/Dropbox/corporate-text-pipeline-data"  # Windows
```

**Important:**
- Use the exact path to your Dropbox folder
- Create the folder if it doesn't exist
- Ask Will for access to the shared Dropbox folder

### 7c: Verify Dropbox Structure

Your Dropbox data folder should have this structure (Will creates this):

```
corporate-text-pipeline-data/
├── raw/
│   └── 10k/
├── processed/
│   ├── cleaned/
│   └── scores/
└── logs/
```

---

## Step 8: Test Everything

```bash
# Test download (small batch)
download-10k --batch-size 3
```

**Expected output:**
```
Downloading 3 10-K filings...
Progress: 3/3 | Success: 3 | Failed: 0 | Skipped: 0
```

**Verify files appeared in Dropbox:**
```bash
ls /path/to/Dropbox/corporate-text-pipeline-data/raw/10k/
```

---

## You're Done!

Setup is complete. Next steps:

1. Read the [Workflow Guide](WORKFLOW_GUIDE.md) for daily operations
2. Review the [Quick Start](QUICK_START.md) for command reference
3. Check [Troubleshooting](TROUBLESHOOTING.md) if you hit issues

---

## Quick Reference: Activating Your Environment

Every time you work on the project:

```bash
cd ~/Documents/corporate-text-pipeline
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows
git pull origin main
```

---

## Team Contacts

- **Will Diebel** (PI): william.diebel@moore.sc.edu
- **Katelyn Thompson** (PhD): katelyn.thompson@grad.moore.sc.edu
- **Lachlan Carroll** (RA): ldc2@email.sc.edu

---

*Last Updated: January 2026*
