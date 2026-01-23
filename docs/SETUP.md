# Setup Guide - Corporate Text Pipeline

**Complete setup instructions for team members**

This guide will walk you through setting up the pipeline on your computer, from installing Python to running your first download.

---

## 📋 Table of Contents

1. [Before You Start](#before-you-start)
2. [Step 1: Install Prerequisites](#step-1-install-prerequisites)
3. [Step 2: Get the Code](#step-2-get-the-code)
4. [Step 3: Set Up Python Environment](#step-3-set-up-python-environment)
5. [Step 4: Install the Pipeline](#step-4-install-the-pipeline)
6. [Step 5: Configure Your Settings](#step-5-configure-your-settings)
7. [Step 6: Test Everything Works](#step-6-test-everything-works)
8. [Troubleshooting](#troubleshooting)
9. [Daily Workflow](#daily-workflow)

---

## 🎯 Before You Start

### What You'll Need

- **Computer**: Mac, Windows, or Linux
- **Internet connection**: For downloading Python and filings
- **Text editor**: We recommend [VS Code](https://code.visualstudio.com/) (free)
- **30 minutes**: For first-time setup

### What This Guide Does

By the end, you'll have:
- ✅ Python installed
- ✅ The pipeline code on your computer
- ✅ All required packages installed
- ✅ Ability to download 10-K filings
- ✅ Ability to process and validate data

---

## 📥 Step 1: Install Prerequisites

### 1.1 Install Python

**Check if you have Python:**

```bash
python3 --version
```

If you see `Python 3.9.x` or higher, you're good! Skip to [1.2](#12-install-git).

**If not, install Python:**

- **Mac**: Download from [python.org](https://www.python.org/downloads/) or use Homebrew:
  ```bash
  brew install python@3.11
  ```

- **Windows**: Download from [python.org](https://www.python.org/downloads/)
  - ⚠️ **Important**: Check "Add Python to PATH" during installation

- **Linux**:
  ```bash
  sudo apt update
  sudo apt install python3.11 python3.11-venv
  ```

**Verify installation:**
```bash
python3 --version
# Should show: Python 3.9.x or higher
```

### 1.2 Install Git

**Check if you have Git:**

```bash
git --version
```

If you see `git version 2.x.x`, you're good! Skip to [Step 2](#step-2-get-the-code).

**If not, install Git:**

- **Mac**:
  ```bash
  brew install git
  # OR download from: https://git-scm.com/download/mac
  ```

- **Windows**: Download from [git-scm.com](https://git-scm.com/download/win)

- **Linux**:
  ```bash
  sudo apt install git
  ```

**Verify installation:**
```bash
git --version
```

### 1.3 Install a Text Editor (Optional but Recommended)

Download [VS Code](https://code.visualstudio.com/) - it's free and makes editing files much easier.

---

## 📂 Step 2: Get the Code

### 2.1 Choose a Location

Decide where you want to put the project. Good choices:
- `~/Documents/research/`
- `~/projects/`
- `~/Desktop/` (if you like seeing it)

### 2.2 Open Terminal

- **Mac**: Press `Cmd+Space`, type "Terminal", press Enter
- **Windows**: Press `Win+R`, type "cmd", press Enter
- **Linux**: Press `Ctrl+Alt+T`

### 2.3 Navigate to Your Chosen Location

```bash
# Example: Documents folder
cd ~/Documents

# Or create a new research folder
mkdir -p ~/Documents/research
cd ~/Documents/research
```

### 2.4 Clone the Repository

```bash
git clone https://github.com/williamdiebel/corporate-text-pipeline.git
```

**What this does**: Downloads all the project files to your computer

### 2.5 Enter the Project Folder

```bash
cd corporate-text-pipeline
```

**Verify you're in the right place:**
```bash
ls
# You should see: src/, scripts/, data/, docs/, config.yaml, etc.
```

---

## 🐍 Step 3: Set Up Python Environment

### 3.1 What is a Virtual Environment?

Think of it as a separate workspace for this project. It keeps this project's tools separate from other Python projects.

**Analogy**: It's like having a separate toolbox for woodworking vs. plumbing - you don't mix them up!

### 3.2 Create the Virtual Environment

```bash
python3 -m venv venv
```

**What this does**: Creates a folder called `venv` with a fresh Python setup

**This takes about 1 minute** ⏱️

### 3.3 Activate the Virtual Environment

**Mac/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

**How to know it worked:**
You should see `(venv)` at the start of your terminal line:
```
(venv) your-computer:corporate-text-pipeline username$
```

### 3.4 Upgrade pip (Python's package installer)

```bash
pip install --upgrade pip
```

---

## 📦 Step 4: Install the Pipeline

### 4.1 Install Everything

```bash
pip install -e .
```

**What this does:**
- Installs all required packages (requests, pandas, beautifulsoup4, etc.)
- Makes the pipeline tools available as commands
- Sets up the project so you can run scripts

**This takes 3-5 minutes** ⏱️

You'll see a lot of text scrolling by - that's normal!

### 4.2 Verify Installation

```bash
# Check that commands are available
download-10k --help
process-batch --help
validate-data --help
```

If these show help text, you're all set! ✅

---

## ⚙️ Step 5: Configure Your Settings

### 5.1 Open the Configuration File

The SEC requires you to identify yourself when downloading files (it's their policy, not ours!).

**Open `config.yaml` in your text editor:**

- **VS Code**: `code config.yaml`
- **Other editor**: Just open the file in any text editor

### 5.2 Add Your Email

Find this line (around line 13):

```yaml
sec_edgar:
  rate_limit: 10
  user_agent: "william.diebel@moore.sc.edu"  # ← CHANGE THIS
```

**Replace with YOUR email:**

```yaml
sec_edgar:
  rate_limit: 10
  user_agent: "your.name@university.edu"  # ← Your actual email
```

### 5.3 Save the File

Press `Cmd+S` (Mac) or `Ctrl+S` (Windows)

**Why this matters**: The SEC blocks requests without a valid email. Using a real email ensures downloads work.

---

## ✅ Step 6: Test Everything Works

### 6.1 Test Download (Small Batch)

Let's download 5 test filings to make sure everything works:

```bash
download-10k --batch-size 5
```

**What you should see:**
```
Downloading 5 10-K filings to data/raw/10k
Rate limit: 10 requests/second
Skip existing: True

Progress: 5/5 | Success: 5 | Failed: 0 | Skipped: 0

======================================================================
Download Complete!
======================================================================
Total attempted: 5
Successful: 5
Failed: 0
Skipped: 0
```

**If it works**: Congratulations! 🎉 Setup is complete!

**If it fails**: See [Troubleshooting](#troubleshooting) below

### 6.2 Check Downloaded Files

```bash
ls data/raw/10k/
```

You should see files like:
```
0000001750_2020_10K.html
0000001750_2021_10K.html
...
```

### 6.3 Test Processing

```bash
process-batch --batch-size 5
```

This extracts and cleans text from the downloaded files.

### 6.4 Test Validation

```bash
validate-data
```

This checks that everything downloaded and processed correctly.

---

## 🆘 Troubleshooting

### Problem: "python3: command not found"

**Solution**: Python isn't installed or not in your PATH
```bash
# Try just 'python' instead
python --version

# If that doesn't work, reinstall Python
# Mac: brew install python@3.11
# Windows: Download from python.org
```

### Problem: "pip: command not found"

**Solution**:
```bash
# Try with python3 -m
python3 -m pip install -e .
```

### Problem: "(venv) doesn't appear"

**Solution**: Virtual environment didn't activate

**Mac/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### Problem: "download-10k: command not found"

**Solutions to try:**

1. **Make sure venv is activated** (should see `(venv)`)
2. **Reinstall:**
   ```bash
   pip install -e .
   ```
3. **Use the full path:**
   ```bash
   python scripts/download_10k.py --batch-size 5
   ```

### Problem: "403 Forbidden" error when downloading

**Cause**: Invalid or missing email in config.yaml

**Solution**:
1. Open `config.yaml`
2. Change `user_agent` to YOUR real email
3. Save file
4. Try again

### Problem: "ModuleNotFoundError: No module named 'src'"

**Solution**: Install the package
```bash
pip install -e .
```

### Problem: Downloads are slow

**This is normal!** The SEC limits us to 10 requests per second.

- 100 filings ≈ 10-15 seconds
- 1,000 filings ≈ 2-3 minutes
- 8,600 filings ≈ 15-30 minutes

---

## 🔄 Daily Workflow

Once setup is complete, here's what you'll do each time you work on the project:

### Starting Your Work Session

```bash
# 1. Navigate to project
cd ~/Documents/research/corporate-text-pipeline

# 2. Activate virtual environment
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# 3. Pull latest changes (if working with team)
git pull origin main

# 4. Start working!
download-10k --batch-size 100
```

### Ending Your Work Session

```bash
# 1. Deactivate virtual environment
deactivate

# 2. Close terminal (optional)
```

**That's it!** Simple workflow for daily use.

---

## 🎓 Next Steps

Now that setup is complete:

1. ✅ Read the main [README.md](../README.md) for project overview
2. ✅ Read [docs/USAGE.md](USAGE.md) for how to use each tool
3. ✅ Read [docs/github_guide.md](github_guide.md) for Git/GitHub workflows
4. ✅ Try downloading a larger batch: `download-10k --batch-size 50`

---

## 📚 Additional Resources

### For Complete Beginners

- [What is a terminal/command line?](https://www.youtube.com/watch?v=5XgBd6rjuDQ)
- [Python basics](https://docs.python.org/3/tutorial/)
- [Git basics](https://www.youtube.com/watch?v=8JJ101D3knE)

### Project Documentation

- [Main README](../README.md) - Project overview
- [Usage Guide](USAGE.md) - How to use tools
- [GitHub Guide](github_guide.md) - Team Git workflow
- [Downloader Guide](DOWNLOADER_USAGE.md) - Download details

### Getting Help

1. **Check the docs** - Most answers are in the guides above
2. **Check logs** - Look in `logs/` folder for error details
3. **Ask the team** - Email Will or create a GitHub Issue

---

## ✨ You're All Set!

Setup is complete! You can now:

✅ Download 10-K filings
✅ Process and clean text
✅ Validate data quality
✅ Work with the team via Git/GitHub

**Welcome to the team!** 🎉

---

**Last Updated**: January 2026
**Version**: 1.0
