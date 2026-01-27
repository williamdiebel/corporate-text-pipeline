# Notes for Will: The Corporate Text Pipeline Story

*A behind-the-scenes look at building an automated research pipeline*

---

## The Big Picture: What We Built and Why

Imagine you're a librarian tasked with reading 8,600 annual reports, finding specific sections about supply chain practices, and scoring each company on how transparent they are. That's roughly 26,000 sections to read, each averaging 50-100 pages. At 10 minutes per section, that's about 4,300 hours of work—or two years of full-time reading.

This pipeline automates that entire process.

**The workflow is deceptively simple:**
```
Firm List → Download 10-Ks → Extract Sections → Clean Text → Score with AI → Analyze
   (CSV)      (SEC EDGAR)       (Parser)        (Cleaner)     (Claude API)   (Stats)
```

But like an iceberg, 90% of the complexity is hidden below the surface.

---

## The Architecture: A Factory Assembly Line

Think of the pipeline like a factory assembly line. Raw materials (10-K filings) come in one end, and finished products (transparency scores) come out the other. Each station on the line does one specific job.

### The Stations

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CORPORATE TEXT PIPELINE                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐          │
│   │  FIRM    │     │   SEC    │     │  PARSER  │     │ CLEANER  │          │
│   │  LIST    │ ──▶ │ DOWNLOAD │ ──▶ │          │ ──▶ │          │ ──▶ ...  │
│   │  (CSV)   │     │          │     │          │     │          │          │
│   └──────────┘     └──────────┘     └──────────┘     └──────────┘          │
│       │                 │                │                │                  │
│       ▼                 ▼                ▼                ▼                  │
│   firm_lists/      raw/10k/        (in memory)     processed/cleaned/       │
│                    *.html                           *.txt                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Why this design?** Each station is independent. If the parser breaks, you don't lose your downloads. If you need to re-clean files, you don't need to re-download. This is called **separation of concerns**—a fundamental principle of good software design.

### The Code Structure

```
corporate-text-pipeline/
│
├── src/                      # The LIBRARY (tools you can reuse)
│   ├── downloaders/          # Knows how to talk to SEC EDGAR
│   │   └── sec_downloader.py # The workhorse: downloads 10-Ks
│   ├── processors/           # Knows how to read and clean 10-Ks
│   │   ├── parser.py         # Extracts Items 1, 1A, 7 from HTML
│   │   └── text_cleaner.py   # Removes tables, headers, cruft
│   ├── utils/                # Helper functions
│   │   └── validators.py     # Checks data quality
│   └── config.py             # Loads settings from config.yaml
│
├── scripts/                  # EXECUTABLES (what you actually run)
│   ├── download_10k.py       # Command: download-10k
│   ├── process_batch.py      # Command: process-batch
│   └── validate_data.py      # Command: validate-data
│
├── data/                     # WHERE FILES LIVE (now in Dropbox!)
│   ├── firm_lists/           # Input: which firms to analyze
│   ├── raw/10k/              # Downloaded HTML files
│   └── processed/cleaned/    # Extracted text files
│
└── config.yaml               # All settings in one place
```

**The key insight:** `src/` contains *reusable tools*, `scripts/` contains *specific workflows*. This is like the difference between a hammer (tool) and "build a birdhouse" instructions (workflow). The hammer can build lots of things; the instructions are for one specific project.

---

## Technologies: Why We Chose What We Chose

### Python: The Swiss Army Knife

We use Python because:
1. **SEC EDGAR libraries exist** (`sec-edgar-downloader`)
2. **Text processing is easy** (`beautifulsoup4`, `lxml`)
3. **Your team already knows it** (learning curve matters!)
4. **Claude's API has great Python support**

Could we have used R? Yes, but the SEC libraries are weaker, and web scraping is clunkier.

### Key Libraries and Why

| Library | What It Does | Why We Need It |
|---------|--------------|----------------|
| `sec-edgar-downloader` | Downloads from SEC EDGAR | Handles rate limiting, filing discovery |
| `beautifulsoup4` | Parses HTML | 10-Ks are HTML documents |
| `pandas` | Data manipulation | Firm lists, results tracking |
| `pyyaml` | Config files | Human-readable settings |
| `tenacity` | Retry logic | Networks fail; we retry gracefully |
| `tqdm` | Progress bars | Sanity during long downloads |

### The Config System: One Source of Truth

```yaml
# config.yaml - everything in one place
data_root: "/Users/will/Dropbox/corporate-text-pipeline-data"

paths:
  raw_10k: "data/raw/10k"
  cleaned_text: "data/processed/cleaned"
```

**Why this matters:** Without centralized config, you'd have paths hardcoded in 10 different files. Change your Dropbox location? Change it once in config.yaml, not everywhere.

The config system has a clever priority order:
1. Environment variable `DATA_ROOT` (highest priority)
2. `data_root` in config.yaml
3. Default to local `data/` folder

This means you can override settings per-machine without editing shared files.

---

## The Dropbox Integration: Collaborative Data at Scale

### The Problem We Solved

Git is great for code. Git is *terrible* for data.

- 8,600 10-K filings = ~10 GB of HTML
- 26,000 text files = ~2 GB of processed text
- Git would choke. GitHub would reject it. Cloning would take hours.

### The Solution

**Code in Git. Data in Dropbox.**

```
Git Repository (GitHub)           Dropbox Shared Folder
├── src/                          ├── raw/10k/
├── scripts/                      │   └── *.html (10 GB)
├── config.yaml                   ├── processed/cleaned/
├── data/firm_lists/ (small!)     │   └── *.txt (2 GB)
└── README.md                     └── logs/
```

Each collaborator:
1. Clones the git repo (small, fast)
2. Points `data_root` to shared Dropbox folder
3. Runs scripts that read/write to Dropbox
4. Everyone sees the same data automatically

### How It Works Under the Hood

```python
# config.py - the magic happens here
def load_config():
    # Priority: environment > config file > default
    data_root = os.getenv('DATA_ROOT') or config.get('data_root')

    if data_root:
        data_root = Path(data_root).expanduser().resolve()
    else:
        data_root = PROJECT_ROOT / 'data'  # fallback

    # Rewrite all paths to use data_root
    for key, value in config['paths'].items():
        if value.startswith('data/'):
            config['paths'][key] = str(data_root / value[5:])
```

This means `data/raw/10k` becomes `/Users/will/Dropbox/.../raw/10k` automatically.

---

## Lessons Learned: Bugs, Pitfalls, and Wisdom

### Bug #1: The Phantom Downloads

**What happened:** Downloads showed "Successful: 0, Failed: 10" even though files were being downloaded.

**The investigation:**
```
sec-edgar-downloader saves to: sec-edgar-filings/{CIK}/10-K/...
Our code looked in: {data_root}/sec-edgar-filings/...
```

The library was downloading to the *current working directory*, not our specified `data_root`.

**The fix:**
```python
# Check BOTH locations - library behavior varies
possible_roots = [download_root, Path.cwd()]
for root in possible_roots:
    candidate = root / "sec-edgar-filings" / cik / "10-K"
    if candidate.exists():
        sec_edgar_dir = candidate
        break
```

**The lesson:** When using third-party libraries, *verify where they actually write files*. Documentation lies (or is outdated). Print statements don't.

### Bug #2: The Missing Module

**What happened:** `ModuleNotFoundError: No module named 'scripts'`

**The cause:** Python needs `__init__.py` files to recognize directories as packages. The `scripts/` folder was missing one.

**The fix:** Create `scripts/__init__.py` (can be empty!) and add `"scripts"` to the packages list in `pyproject.toml`.

**The lesson:** Python's import system has quirks. When you get `ModuleNotFoundError`, check:
1. Is there an `__init__.py`?
2. Is the package listed in `pyproject.toml`?
3. Did you run `pip install -e .` after changes?

### Bug #3: The Skipped Confusion

**What happened:** After fixing downloads, everything showed as "Skipped: 10" with 0 successful.

**The reality:** This was *correct behavior*. The files already existed (from the previous attempt that found them via the cwd fallback). The script correctly skipped re-downloading.

**The lesson:** "Skipped" isn't failure—it's efficiency. Read your logs carefully before panicking.

### Pitfall: The Section Explosion

**Current state:**
- 8,672 firm-years × 3 sections = **26,016 files**

**The problem:** For LLM scoring, we need all sections together anyway. Why create 26,000 files just to recombine them?

**Better approach (recommended):**
```
One file per firm-year with marked sections:

=== ITEM 1: BUSINESS DESCRIPTION ===
[content]

=== ITEM 1A: RISK FACTORS ===
[content]

=== ITEM 7: MD&A ===
[content]
```

This reduces file count from 26,000 to 8,672 and eliminates a recombination step.

---

## How Good Engineers Think

### Principle 1: Fail Fast, Fail Loud

Bad code:
```python
try:
    download_file()
except:
    pass  # Silently ignore all errors
```

Good code:
```python
try:
    download_file()
except RequestError as e:
    logger.error(f"Download failed for {cik}: {e}")
    results['failed'].append({'cik': cik, 'error': str(e)})
    raise  # Or handle specifically
```

**Why:** Silent failures are *worse* than crashes. A crash tells you something's wrong. Silent failure means you discover problems weeks later when your analysis is garbage.

### Principle 2: Make State Visible

Our scripts print progress:
```
Progress: 7/10 | Success: 6 | Failed: 0 | Skipped: 1
```

And write detailed logs:
```
2026-01-27 11:45:23 | INFO | Successfully downloaded 10-K for CIK 0000027419, year 2017
```

**Why:** Long-running processes need feedback. Without it, you don't know if the script is working, stuck, or crashed.

### Principle 3: Idempotency

**Idempotent** = running something twice gives the same result as running it once.

Our download script is idempotent:
```python
if skip_if_exists and filepath.exists():
    return True, filepath  # Already done, skip
```

**Why:** Networks fail. Laptops die. Scripts get interrupted. If your script isn't idempotent, a crash means starting over. With idempotency, you just re-run and it picks up where it left off.

### Principle 4: Separation of Concerns

Each module does ONE thing:
- `sec_downloader.py`: Downloads files (doesn't parse them)
- `parser.py`: Extracts sections (doesn't clean them)
- `text_cleaner.py`: Cleans text (doesn't know what a 10-K is)

**Why:** When the SEC changes their HTML format (they will), you fix `parser.py`. The downloader and cleaner don't care—they keep working.

### Principle 5: Configuration Over Code

Bad:
```python
output_dir = "/Users/will/Documents/research/data/10k"  # Hardcoded
```

Good:
```yaml
# config.yaml
paths:
  raw_10k: "data/raw/10k"
```

```python
output_dir = config['paths']['raw_10k']  # From config
```

**Why:** Hardcoded paths break when *anyone else* tries to use your code. Config files let each user customize without editing source code.

---

## Best Practices We Followed

### 1. Entry Points via pyproject.toml

Instead of:
```bash
python scripts/download_10k.py --batch-size 10
```

Users run:
```bash
download-10k --batch-size 10
```

This is configured in `pyproject.toml`:
```toml
[project.scripts]
download-10k = "scripts.download_10k:main"
```

**Why:** Cleaner commands, works from any directory, proper Python packaging.

### 2. Logging to Files AND Console

```python
# Logs go to both terminal and file
setup_logging(log_file="logs/download_20260127.log", level="INFO")
```

**Why:** Terminal output is ephemeral—close the window and it's gone. Log files persist for debugging later.

### 3. Progress Tracking with CSV

After each batch:
```
download_logs/
├── successful_20260127_114517.csv
├── failed_20260127_114517.csv
└── summary_20260127_114517.txt
```

**Why:** When something fails at firm #3,847, you need to know which ones succeeded. These CSVs let you resume from failures.

### 4. Type Hints (Where We Have Them)

```python
def download_10k(
    self,
    cik: str,
    year: int,
    skip_if_exists: bool = True
) -> Tuple[bool, Optional[str]]:
```

**Why:** Your IDE can catch errors before you run the code. Future-you (or your RA) can understand what functions expect.

---

## What's Next: The Road Ahead

### Immediate Next Steps

1. **Run `process-batch`** to extract and clean the downloaded 10-Ks
2. **Verify files appear in Dropbox** for all collaborators
3. **Scale to full dataset** (8,672 firm-years)

### The LLM Scoring Module (Stage 4)

This is the crown jewel—using Claude to score transparency. The design:

```python
# Pseudocode for scoring
for firm_year in firm_years:
    # Load all sections for this firm-year
    text = load_aggregated_text(firm_year)

    # Send to Claude with scoring prompt
    response = claude.analyze(
        prompt=TRANSPARENCY_SCORING_PROMPT,
        text=text
    )

    # Parse scores (1-10 for each dimension)
    scores = parse_response(response)

    # Save to database/CSV
    save_scores(firm_year, scores)
```

**Key considerations:**
- **Cost:** Claude API has costs per token. 8,672 firm-years × ~50K tokens each = significant cost
- **Rate limits:** API has request limits; need throttling
- **Reproducibility:** Use `temperature=0` for deterministic results
- **Validation:** Score a subset manually to verify AI accuracy

### Recommended Improvements

1. **Aggregate sections** into single files (reduces complexity)
2. **Add unit tests** (currently none—risky for research code)
3. **Dockerize** (ensures identical environment across machines)
4. **Add data validation** between stages (catch errors early)

---

## Final Thoughts: Why This Matters

Building this pipeline taught us that **software engineering is about managing complexity**. A 10-line script can download one file. But downloading 8,600 files reliably, across multiple machines, with progress tracking, error handling, and collaborative data management—that requires *architecture*.

The techniques here—separation of concerns, configuration management, idempotency, logging—aren't just for "real" software projects. They're essential for *any* research involving code. The alternative is spaghetti scripts that work on one machine, for one researcher, until something changes.

Your future self will thank you for the logs. Your collaborators will thank you for the config files. And your paper reviewers will appreciate the reproducibility.

Now go score some supply chains.

---

*Last updated: January 27, 2026*
*Pipeline version: 0.1.0*
*Written by Claude, edited by Will*
