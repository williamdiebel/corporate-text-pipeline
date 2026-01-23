# GitHub Guide for Corporate Text Pipeline Project

**Author**: Will Diebel  
**Project**: Supply Chain Constructs Measurement Pipeline  
**Pipeline Development Team**: Will Diebel; Katelyn Thompson; Lachlan Carroll  
**Status**: In Development  
**Last Updated**: January 21, 2026  

---

This doc aims to provide a general overview of our proposed measurement approach and associated data collection / cleaning / analysis pipeline. As the pipeline is still in development and we are waiting on approval for API access to ChatGPT (OpenAI) and / or Claude (Anthropic), this is all subject to modification, though the general structure should be flexible enough to accommodate any such changes. In any case, please get oriented with the overarching aims / tasks of the project as detailed below as it will help us with the preliminary work that we can complete while waiting for API approval.

## Table of Contents
1. [Project Overview and Research Pipeline](#project-overview)
2. [What is GitHub and Why We're Using It](#what-is-github)
3. [Getting Started: One-Time Setup](#getting-started)
4. [Daily Workflow: How to Work with the Repository](#daily-workflow)
5. [Common Tasks and Commands](#common-tasks)
6. [Best Practices and Tips](#best-practices)
7. [Troubleshooting Common Issues](#troubleshooting)

### Research Objective

**Research Question**: Do supply chain executive appointments increase supply chain transparency? What management practices moderate this relationship?

To answer our research question, we are aiming to develop **multiple text-derived measures (below)** for 1,100 US manufacturing firms over multiple years (2006 to 2022). Since not all firms exist in all years, we have estimated that we'll need to collect information to develop measures for 8,673 unique firm-year combinations:

**Primary outcome measures (Transparency constructs)**:
- Supply Chain Transparency (aggregate)
- Environmental Supply Chain Transparency
- Social Supply Chain Transparency  
- Supply Base Transparency

**Mechanistic variable measures (Management practices)**:
- Digital Transformation
- Supplier Audits
- Supplier Code of Conduct
- Supply Base Reconfiguration
- Supplier Development

### Our Measurement Approach

**Note**: This pipeline is currently in development. The approach described below represents our planned methodology.

We extract measures from **10-K filings** (annual reports filed with the SEC):
- Publicly available and standardized format
- Contains Items 1, 1A, and 7 with supply chain information
- Consistent disclosure requirements across firms

**CSR/Sustainability reports** may be added as a future extension if time and resources permit.

**Key innovation**: We use Large Language Models (LLMs) to systematically score constructs across thousands of documents - a task previously requiring months of manual coding.

---

### The Complete Pipeline: From Raw Documents to Research Dataset

Our pipeline consists of 5 major stages:

```
Raw Documents → Text Extraction → Text Cleaning → LLM Scoring → Analysis Dataset
```

The following elaborates on each stage:

---

#### **Stage 1: Document Collection**
**What**: Download 10-K filings from SEC EDGAR (and CSR reports from company websites - TBD)  
**Input**: List of firm-year observations (CIK-Year combinations)  
**Output**: Raw HTML/PDF files organized by firm and year  
**Your roles**: Run scripts, monitor download progress, flag errors, verify completeness

**Key files**:
- `scripts/download_10k.py` - Downloads 10-Ks from SEC EDGAR
- `scripts/download_csr.py` - Downloads CSR reports (Phase 2)
- `data/firm_lists/target_firm_years.csv` - Your input list

**Technical details**:
- SEC EDGAR API has rate limits (10 requests/second)
- Each 10-K is ~50-100 pages of HTML
- Process runs in batches of 100 firms
- Takes an estimated ~2-3 hours for 1,000 firm-years

---

#### **Stage 2: Text Extraction**
**What**: Extract relevant text from HTML/PDF files  
**Input**: Raw 10-K HTML files  
**Output**: Plain text files containing key sections  
**Your roles**: Run scripts and complete manual quality checks on output to ensure text extraction didn't fail

**Key sections extracted**:
- **Item 1** (Business Description): Supply chain structure
- **Item 1A** (Risk Factors): Supply chain risks and dependencies
- **Item 7** (MD&A): Management discussion of supply chain initiatives

**Why only these sections?**  
- These contain 95%+ of supply chain disclosures
- Reduces text volume for LLM processing (saves cost/time)
- Based on validated approach from literature (e.g., Astvansh & Simpson, 2025; Maibaum et al., 2024)

**Key files**:
- `src/processors/text_cleaner.py` - Extracts text from HTML
- `src/processors/parser.py` - Identifies and extracts specific sections

---

#### **Stage 3: Text Cleaning**
**What**: Remove boilerplate, tables, and irrelevant content  
**Input**: Raw extracted text  
**Output**: Clean text focused on supply chain content  
**Your roles**: Run scripts and review samples to ensure quality

**What gets removed**:
- Financial tables and numeric data
- Legal disclaimers and safe harbor statements
- Headers/footers repeated on each page
- Exhibit lists and appendices
- HTML artifacts and formatting codes

**What gets kept**:
- All narrative text about supply chain
- Qualitative descriptions of practices
- Risk disclosures
- Sustainability initiatives

**Key files**:
- `src/processors/text_cleaner.py` - Cleaning functions
- `data/processed/cleaned/` - Output directory

---

#### **Stage 4: LLM Scoring**
**What**: Use AI (ChatGPT/Claude) to score supply chain constructs  
**Input**: Clean text for each firm-year  
**Output**: Numeric scores (0-100) across 9 constructs  
**Your role**: Validate through manual pilot study (completed in parallel, as led by Katelyn)

**The 9 measured constructs**:

*Transparency Constructs (Primary Outcomes):*
1. **Supply Chain Transparency (Aggregate)**: Overall upstream disclosure
2. **Environmental SCT**: Environmental impacts/risks in supply chain
3. **Social SCT**: Social impacts/risks in supply chain
4. **Supply Base Transparency**: Disclosures pertaining to tier-1 suppliers

*Mechanism Constructs (Moderators/Mediators):*
5. **Digital Transformation**: Adoption of supply chain technologies
6. **Supplier Audits**: Systematic supplier evaluations
7. **Supplier Code of Conduct**: Formal supplier standards
8. **Supply Base Reconfiguration**: Supplier termination/restructuring
9. **Supplier Development**: Efforts to improve supplier capabilities

**How it works**:
1. Feed firm's cleaned 10-K text to LLM (e.g., OpenAI API)
2. LLM reads text and applies scoring rubrics for all 9 constructs
3. LLM returns structured scores + brief justifications
4. Repeat for all 8,673 firm-years

**Key files**:
- `src/scorers/llm_scorer.py` - Main scoring logic
- `src/scorers/prompts.py` - Scoring instructions for each construct
- `src/scorers/rubrics.py` - Detailed rubrics (developed in pilot study)
- `config.yaml` - LLM settings (model, temperature, etc.)

**Why LLMs?**
- **Consistency**: Same rubrics applied to every firm for every construct
- **Scalability**: Can score 1,000 firms × 9 constructs in hours vs. months manually
- **Replicability**: Anyone with the code can reproduce our scores
- **Multidimensionality**: Captures nuanced differences across constructs

---

#### **Stage 5: Data Assembly**
**What**: Combine scores into analysis dataset  
**Input**: Individual firm-year scores  
**Output**: Panel dataset (CSV) for econometric analysis  
**Your role**: Basic descriptive statistics and data validation

**Output format** (one row per firm-year):
```
CIK, Year, 
SCT_Aggregate, SCT_Environmental, SCT_Social, SupplyBase_Transparency,
Digital_Transformation, Supplier_Audits, Supplier_CodeOfConduct, 
SupplyBase_Reconfiguration, Supplier_Development,
Has10K, TextLength, ...
```

**This dataset gets merged with our other data** (treatment/control status, appointment/event IDs, financial variables, etc.) for the stacked DiD analysis(Wang et al., 2024) examining how supply chain executive appointments affect transparency, and what mechanisms moderate this relationship.

**Key files**:
- `scripts/create_analysis_dataset.py` - Assembles final data
- `data/processed/scores/transparency_scores.csv` - Final output

---

### Your Roles in the Pipeline (to be further clarified as we progress)

**Katelyn**:
- **Lead** pilot validation study
- **Develop** detailed scoring rubrics for all constructs
- **Run** full pipeline on server/local machine in coordination with Lachlan (divide and conquer)
- **Troubleshoot** technical issues
- **Validate** output quality at each stage
- **Document** any deviations or decisions

**Lachlan**:
- **Participate** in pilot validation (manual scoring)
- **Run** full pipeline on server/local machine in coordination with Katelyn
- **Monitor** batch downloads (track progress, flag errors)
- **Quality check** random samples at each stage
- **Report** completion status to team

**Will**:
- **Develop** pipeline architecture and pilot scripts
- **Supervise and Troubleshoot** pipeline implementation
- **Review** validation results
- **Approve** methodology decisions
- **Oversee** overall progress

---

### Timeline Overview

This is ambitious but I think we can do it...

**Week 1-2**: Pilot validation study (manual scoring of sample); pilot and run 10-k downloads
**Week 3-4**: Pilot and run text extraction and cleaning scripts
**Week 5-6**: Pilot and run LLM scoring  
**Week 7-8+**: Merge and analyze dataset

---

### Key Advantages of This Approach

✅ **Reproducible**: All code in GitHub, anyone can re-run  
✅ **Scalable**: Same pipeline works for 100 or 10,000 firms  
✅ **Transparent**: Every step documented and version-controlled  
✅ **Validated**: Human pilot study confirms LLM scores are reliable  
✅ **Flexible**: Can add new dimensions or change scoring rubric easily  
✅ **Cost-effective**: $1,500 for full sample vs. $50,000+ for manual coding  

---

### Repository Structure (What You'll See)

```
corporate-text-pipeline/
├── data/
│   ├── firm_lists/          # Input: which firms to process
│   ├── raw/10k/             # Downloaded 10-K files
│   ├── processed/cleaned/   # Extracted & cleaned text
│   └── processed/scores/    # Final construct scores
│
├── src/                     # Core pipeline code
│   ├── downloaders/         # SEC EDGAR download scripts
│   ├── processors/          # Text extraction & cleaning
│   ├── scorers/             # LLM scoring logic
│   └── utils/               # Helper functions
│
├── scripts/                 # Executable scripts you'll run
│   ├── download_10k.py
│   ├── process_batch.py
│   └── score_constructs.py
│
├── docs/                    # Documentation (guides like this)
├── tests/                   # Unit tests for code
├── logs/                    # Execution logs
└── config.yaml              # Project settings
```

**Pro tip**: Each folder has a README explaining its contents.

---

### Questions to Orient Yourself

If you're unsure before diving into work on any given day, check in with the team. We should communicate regularly enough to remain aligned on the following:

1. **Knowing what stage are we at with respect to overarching plan** 
2. **Understand the specific tasks each other are focusing on in a given week**
3. **Knowing what files to use, how to document progress, and being aware of when to pull/push work from/to GitHub** 

---

**Next**: Let's get you set up with GitHub so you can access all this code (still in development)...

---

## What is GitHub and Why We're Using It {#what-is-github}

### What is GitHub?
GitHub is a platform for storing and managing code collaboratively. Think of it as "Google Docs for code" - it allows multiple people to work on the same project without overwriting each other's work.

### Key Concepts

**Repository (Repo)**: The project folder containing all our code and files. Our repo is called `corporate-text-pipeline`. Once you've created a GitHub account, please share your username/email with me so I can add you as a repo collaborator.

**Commit**: A saved snapshot of your changes with a descriptive message. Like saving a version of a document with notes about what changed.

**Push**: Uploading your commits from your computer to GitHub so others can see them.

**Pull**: Downloading the latest changes from GitHub to your computer to get updates others have made.

**Branch**: A separate version of the code where you can work without affecting the main version. We'll primarily work on the `main` branch.

### Why We're Using GitHub for This Project

1. **Collaboration**: The three of us can work on different parts simultaneously
2. **Version Control**: We can track every change, see who made it, and why
3. **Backup**: All our work is safely stored in the cloud
4. **Reproducibility**: Other researchers can see exactly how we built our pipeline
5. **Recovery**: If something breaks, we can easily revert to a previous working version

---

## Getting Started: One-Time Setup {#getting-started}

### Step 1: Install Required Software

**Git** (version control software):
- **Mac**: Open Terminal and run: `git --version` (Mac will prompt to install if needed)
- **Windows**: Download from [git-scm.com](https://git-scm.com/download/win)

**VS Code** (recommended code editor):
- Download from [code.visualstudio.com](https://code.visualstudio.com/)
- Install the Python extension (search "Python" in Extensions panel)

**Python 3.9+**:
- **Mac**: Already installed, or download from [python.org](https://www.python.org/downloads/)
- **Windows**: Download from [python.org](https://www.python.org/downloads/)

### Step 2: Configure Git with Your Identity

Open Terminal (Mac) or Git Bash (Windows) and run:

```bash
git config --global user.name "Your Name"
git config --global user.email "youremail@email.sc.edu"
```

This identifies you in all future commits.

### Step 3: Get Access to the Repository

As mentioned above, once you're setup I can add you as a collaborator to the repo.

### Step 4: Clone the Repository to Your Computer

**Option A: Using Terminal/Command Line**
```bash
# Navigate to where you want the project folder
cd ~/Documents  # or wherever you keep projects

# Clone the repository
git clone https://github.com/USERNAME/corporate-text-pipeline.git

# Navigate into the project
cd corporate-text-pipeline
```

**Option B: Using VS Code**
1. Open VS Code
2. Open the command pallette: press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows)
3. Type "Git: Clone" and select it
4. Paste the repository URL
5. Choose where to save it
6. Click "Open" when prompted

### Step 5: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

You're now ready to work!

---

## Daily Workflow: How to Work with the Repository {#daily-workflow}

### Every Time You Start Working

**Step 1: Open the project in VS Code**

**Step 2: Activate your virtual environment**
```bash
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows
```

You should see `(venv)` at the start of your terminal prompt.

**Step 3: Pull the latest changes**
```bash
git pull origin main
```

This downloads any changes others have made to main since you last worked.

### While You're Working

**Check what files you've changed:**
```bash
git status
```

Shows files in red (changed but not staged) or green (staged and ready to commit).

### When You're Done for the Day (or Finished a Task)

**Step 1: Stage your changes**
```bash
# Stage all changes
git add .

# OR stage specific files
git add path/to/file.py
```

**Step 2: Commit with a descriptive message**
```bash
git commit -m "Brief description of what you did"
```

**Good commit messages:**
- ✅ "Added 10-K downloader for SEC EDGAR API"
- ✅ "Fixed CIK formatting bug in firm list loader"
- ✅ "Completed manual scoring for pilot firms 1-25"

**Bad commit messages:**
- ❌ "updates"
- ❌ "fixed stuff"
- ❌ "asdfasdf"

**Step 3: Push to GitHub**
```bash
git push origin main
```
Step 2 and 3 can also be completed using the UI in VS Code (see the source control tab on left side column menu) .

**Step 4: Verify on GitHub**
Go to the repository URL in your browser and confirm your changes appear.

---

## Common Tasks and Commands {#common-tasks}

### Viewing Your Changes

**See what you've changed:**
```bash
git diff
```

**See commit history:**
```bash
git log --oneline
```

### Working with Files

**Add a new file to tracking:**
```bash
git add new_file.py
```

**Remove a file:**
```bash
git rm old_file.py
git commit -m "Removed obsolete file"
```

**Rename a file:**
```bash
git mv old_name.py new_name.py
git commit -m "Renamed file for clarity"
```

### Undoing Changes

**Discard changes to a file (before committing):**
```bash
git checkout -- filename.py
```

**Undo the last commit (but keep changes):**
```bash
git reset --soft HEAD~1
```

**Revert to a previous version:**
```bash
git log --oneline  # Find the commit hash
git checkout <commit-hash> filename.py
```

---

## Best Practices and Tips {#best-practices}

### Communication

✅ **DO:**
- Communicate with the team about what you're working on
- Write clear, descriptive commit messages
- Commit frequently (every time you complete a logical chunk of work)
- Pull before you start working each day

❌ **DON'T:**
- Work for days without committing/pushing
- Edit the same file simultaneously as someone else (coordinate first)
- Commit broken/untested code to main branch
- Push files with sensitive information (API keys, passwords)

### File Management

**Files to NEVER commit:**
- API keys or passwords
- Large data files (>100MB)
- Your virtual environment folder (`venv/`)
- System files (`.DS_Store` on Mac, `Thumbs.db` on Windows)

These should already be in `.gitignore`, but double-check.

**Files you SHOULD commit (this will mostly be me, your job will largely be to run the scripts):**
- All Python scripts (`.py` files)
- Configuration files (`config.yaml`, `requirements.txt`)
- Documentation (`.md` files, this guide)
- Small example data files (<1MB)

### Workflow Tips

**Before starting a new task:**
```bash
git pull origin main
```

**Before ending your work session:**
```bash
git add .
git commit -m "Descriptive message"
git push origin main
```
You can also complete the above using the UI in VS Code.

**If you're unsure about changes:**
```bash
git status  # See what's changed
git diff    # See exact changes
```

---

## Troubleshooting Common Issues {#troubleshooting}

### Issue: "fatal: not a git repository"

**Solution:** You're not in the project directory.
```bash
cd path/to/corporate-text-pipeline
```

### Issue: "Your branch is behind 'origin/main'"

**Solution:** Others have made changes. Pull them:
```bash
git pull origin main
```

### Issue: "Merge conflict"

This happens when you and someone else changed the same lines in a file.

**Solution:**
1. Open the conflicting file in VS Code
2. Look for sections marked with `<<<<<<<`, `=======`, `>>>>>>>`
3. Manually edit to keep the correct version
4. Remove the conflict markers
5. Save, then:
```bash
git add conflicted_file.py
git commit -m "Resolved merge conflict"
git push origin main
```

### Issue: "Permission denied (publickey)"

**Solution:** You need to set up SSH keys or use HTTPS. Ask PI for help setting up access.

### Issue: "Changes not appearing on GitHub"

**Checklist:**
1. Did you `git add` the files?
2. Did you `git commit`?
3. Did you `git push`?
4. Check `git status` - is your branch ahead of origin?

### Issue: Accidentally committed something you shouldn't have

**Solution (if not yet pushed):**
```bash
git reset --soft HEAD~1  # Undo last commit, keep changes
# Remove the file you shouldn't commit
git add .
git commit -m "Corrected commit"
```

**Solution (if already pushed):**
Contact PI immediately. Depending on what was exposed (e.g., API keys), we may need to rotate credentials.

---

## Getting Help

### Resources
- **Git Cheat Sheet**: [education.github.com/git-cheat-sheet-education.pdf](https://education.github.com/git-cheat-sheet-education.pdf)
- **Git Documentation**: [git-scm.com/doc](https://git-scm.com/doc)
- **GitHub Guides**: [guides.github.com](https://guides.github.com/)

### For This Project
- **Questions about Git**: Ask PhD student or PI
- **Questions about the code**: Check inline comments or ask in team meeting
- **Found a bug**: Document it, commit what you have, and notify the team

---

## Summary: Essential Commands

```bash
# Daily workflow
git pull origin main           # Start of day: get latest changes
git status                     # Check what you've changed
git add .                      # Stage all changes
git commit -m "Description"    # Save changes with message
git push origin main           # Upload changes to GitHub

# Helpful commands
git log --oneline             # View history
git diff                      # See what changed
git checkout -- file.py       # Discard changes to a file
```

---

## Quick Start Checklist for New Team Members

- [ ] Install Git, VS Code, Python
- [ ] Configure Git with your name and email
- [ ] Get repository access from me
- [ ] Clone the repository
- [ ] Set up virtual environment
- [ ] Install dependencies (`pip install -r requirements.txt`)
- [ ] Test: run `python src/config.py` successfully
- [ ] Read this guide completely
- [ ] Ask questions before starting work!

---

**If you have questions about any of this, don't hesitate to ask.**
