# Processors Module

This module handles parsing and cleaning of 10-K filing text.

## Contents

- **`parser.py`**: Extracts specific sections from 10-K HTML files
- **`text_cleaner.py`**: Cleans and normalizes extracted text

---

## Parser (`parser.py`)

Extracts Items 1, 1A, and 7 from 10-K HTML filings using pattern matching and BeautifulSoup.

### Features

✅ **Section Extraction**: Extracts Items 1, 1A, and 7
✅ **Multiple Formats**: Handles various 10-K HTML structures
✅ **Batch Processing**: Process multiple files efficiently
✅ **Validation**: Ensures minimum section length
✅ **Metadata Extraction**: Parses CIK and year from filenames

### Extracted Sections

| Section | Name | Purpose |
|---------|------|---------|
| Item 1 | Business Description | General company and business overview |
| Item 1A | Risk Factors | Key risks (rich in supply chain disclosures) |
| Item 7 | MD&A | Management Discussion & Analysis |

These sections are targeted because supply chain disclosures are typically concentrated in Risk Factors (Item 1A) and MD&A (Item 7).

### Class: `TenKParser`

#### Initialization

```python
from src.processors import TenKParser

parser = TenKParser(
    min_section_length=1000  # Minimum characters for valid section
)
```

#### Methods

##### `parse_file(filepath)`

Parse a single 10-K file and extract all sections.

**Parameters**:
- `filepath` (str): Path to 10-K HTML file

**Returns**:
- `dict` with keys: `item_1`, `item_1a`, `item_7`
- Values are extracted text or `None` if not found

**Example**:
```python
sections = parser.parse_file('data/raw/10k/0000001750_2020_10K.html')

if sections['item_1a']:
    print(f"Risk Factors: {len(sections['item_1a'])} characters")
    print(sections['item_1a'][:500])  # Preview first 500 chars
else:
    print("Item 1A not found")
```

##### `parse_batch(filepaths, output_dir=None)`

Parse multiple 10-K files.

**Parameters**:
- `filepaths` (list): List of file paths
- `output_dir` (str, optional): Directory to save extracted sections

**Returns**:
- `pd.DataFrame` with parsing results and statistics

**Example**:
```python
from pathlib import Path

# Get all 10-K files
files = list(Path('data/raw/10k').glob('*.html'))

# Parse all files and save sections
results = parser.parse_batch(
    filepaths=files,
    output_dir='data/processed/extracted'
)

print(results[['filename', 'item_1a_length', 'all_sections_extracted']])

# Summary statistics
print(f"Success rate: {results['all_sections_extracted'].mean():.1%}")
print(f"Average Item 1A length: {results['item_1a_length'].mean():,.0f} chars")
```

### Helper Functions

##### `extract_metadata_from_filename(filename)`

Extract CIK and year from standardized filename.

**Parameters**:
- `filename` (str): Filename like `0000001750_2020_10K.html`

**Returns**:
- `(cik: str, year: int)` or `(None, None)` if parsing fails

**Example**:
```python
from src.processors import extract_metadata_from_filename

cik, year = extract_metadata_from_filename('0000320193_2021_10K.html')
print(f"CIK: {cik}, Year: {year}")
# Output: CIK: 0000320193, Year: 2021
```

##### `parse_10k(filepath, min_section_length=1000)`

Convenience function to parse a single file.

**Example**:
```python
from src.processors import parse_10k

sections = parse_10k('data/raw/10k/0000001750_2020_10K.html')
```

### Output Format

When using `parse_batch()` with `output_dir`, files are saved as:

```
{output_dir}/
├── 0000001750_2020_10K_item_1.txt
├── 0000001750_2020_10K_item_1a.txt
├── 0000001750_2020_10K_item_7.txt
└── ...
```

### Pattern Matching

The parser uses multiple regex patterns to identify section boundaries:

**Item 1 Patterns**:
- `item\s*1[\.\:\s]+business`
- `item\s*1\s*\-\s*business`
- `>item\s*1[\.\:\s]`

**Item 1A Patterns**:
- `item\s*1a[\.\:\s]+risk\s*factors`
- `>item\s*1a[\.\:\s]`

**Item 7 Patterns**:
- `item\s*7[\.\:\s]+management`
- `item\s*7.*md&a`

### Error Handling

- **File not found**: Returns dict with all values `None`
- **Parse error**: Logs error and returns `None` for affected sections
- **Section too short**: Returns `None` if below `min_section_length`

---

## Text Cleaner (`text_cleaner.py`)

Cleans and normalizes extracted text, removing boilerplate and formatting artifacts.

### Features

✅ **HTML Artifact Removal**: Removes HTML tags and entities
✅ **Boilerplate Removal**: Removes table of contents, headers, footers
✅ **Whitespace Normalization**: Standardizes spacing and line breaks
✅ **Table Removal**: Removes table-like structures (financial data)
✅ **Configurable**: Adjustable cleaning aggressiveness

### Class: `TextCleaner`

#### Initialization

```python
from src.processors import TextCleaner

cleaner = TextCleaner(
    remove_tables=True,              # Remove table structures
    remove_headers=True,             # Remove page headers/footers
    normalize_whitespace=True,       # Normalize spacing
    min_word_length=2,               # Minimum word length
    max_consecutive_newlines=2       # Max empty lines
)
```

#### Methods

##### `clean(text)`

Clean text with all enabled cleaning steps.

**Parameters**:
- `text` (str): Raw text to clean

**Returns**:
- `str`: Cleaned text

**Example**:
```python
raw_text = """
  Item 1A.&nbsp;&nbsp;Risk Factors



  Our business involves&nbsp;significant risks...
  Table of Contents
  Page 15 of 200
"""

clean_text = cleaner.clean(raw_text)
print(clean_text)
# Output: "Item 1A. Risk Factors\n\nOur business involves significant risks..."
```

##### `clean_file(input_path, output_path=None)`

Clean a text file.

**Parameters**:
- `input_path` (str): Path to input file
- `output_path` (str, optional): Path to save cleaned text

**Returns**:
- `str`: Cleaned text

**Example**:
```python
cleaned = cleaner.clean_file(
    input_path='data/processed/extracted/0000001750_2020_10K_item_1a.txt',
    output_path='data/processed/cleaned/0000001750_2020_10K_item_1a.txt'
)
```

##### `clean_batch(input_files, output_dir=None)`

Clean multiple files.

**Parameters**:
- `input_files` (list): List of input file paths
- `output_dir` (str, optional): Directory to save cleaned files

**Returns**:
- `pd.DataFrame` with cleaning statistics

**Example**:
```python
from pathlib import Path

# Get all extracted sections
files = list(Path('data/processed/extracted').glob('*_item_*.txt'))

# Clean all files
results = cleaner.clean_batch(
    input_files=files,
    output_dir='data/processed/cleaned'
)

print(results[['filename', 'original_length', 'cleaned_length', 'reduction_pct']])
print(f"Average reduction: {results['reduction_pct'].mean():.1f}%")
```

### Cleaning Steps

The cleaner applies these steps in order:

1. **HTML Artifacts**: Remove `&nbsp;`, `&amp;`, HTML tags
2. **Boilerplate**: Remove "Table of Contents", page numbers
3. **Tables**: Remove table-like structures (optional)
4. **Headers/Footers**: Remove page headers and footers (optional)
5. **Whitespace**: Normalize spaces and newlines (optional)
6. **Short Words**: Filter very short words (likely artifacts)

### Helper Function

##### `clean_text(text, aggressive=False)`

Convenience function for quick cleaning.

**Parameters**:
- `text` (str): Text to clean
- `aggressive` (bool): Use more aggressive cleaning

**Example**:
```python
from src.processors import clean_text

# Standard cleaning
cleaned = clean_text(raw_text)

# Aggressive cleaning (removes more)
cleaned = clean_text(raw_text, aggressive=True)
```

---

## Complete Workflow Example

```python
from src.processors import TenKParser, TextCleaner
from pathlib import Path

# Initialize
parser = TenKParser(min_section_length=1000)
cleaner = TextCleaner()

# Get all downloaded 10-Ks
raw_files = list(Path('data/raw/10k').glob('*.html'))

print(f"Processing {len(raw_files)} files...")

# Step 1: Parse all files
parsed_results = parser.parse_batch(
    filepaths=raw_files,
    output_dir='data/processed/extracted'
)

print(f"Extracted sections from {len(parsed_results)} files")
print(f"Success rate: {parsed_results['all_sections_extracted'].mean():.1%}")

# Step 2: Clean all extracted sections
extracted_files = list(Path('data/processed/extracted').glob('*_item_*.txt'))

cleaned_results = cleaner.clean_batch(
    input_files=extracted_files,
    output_dir='data/processed/cleaned'
)

print(f"Cleaned {len(cleaned_results)} section files")
print(f"Average text reduction: {cleaned_results['reduction_pct'].mean():.1f}%")

# Step 3: Verify cleaned files
from src.utils import validate_extracted_text

validation_errors = []
for file in Path('data/processed/cleaned').glob('*.txt'):
    with open(file, 'r') as f:
        text = f.read()

    is_valid, message = validate_extracted_text(text)
    if not is_valid:
        validation_errors.append(f"{file.name}: {message}")

if validation_errors:
    print(f"\n⚠ {len(validation_errors)} files have validation issues")
else:
    print("\n✓ All cleaned files passed validation")
```

---

## Command-Line Usage

Process files via the command-line script:

```bash
# Parse and clean all files
python scripts/process_batch.py

# Process specific directory
python scripts/process_batch.py --input-dir data/raw/10k --output-dir data/processed/cleaned

# Extract only Item 1A
python scripts/process_batch.py --sections item_1a

# Skip cleaning step
python scripts/process_batch.py --no-clean
```

---

## Testing

```bash
# Run processor tests
pytest tests/test_processors.py -v

# Test specific functionality
pytest tests/test_processors.py::TestTenKParser::test_extract_metadata -v
```

---

## Troubleshooting

### Issue: Section not extracted

**Possible causes**:
1. Section doesn't exist in the filing
2. Non-standard section formatting
3. Section too short (below `min_section_length`)

**Solutions**:
- Check the raw HTML file manually
- Try lowering `min_section_length`
- Review parser logs for warnings

### Issue: Cleaned text is empty

**Cause**: Overly aggressive cleaning removed all content

**Solution**:
```python
# Use less aggressive settings
cleaner = TextCleaner(
    remove_tables=False,  # Keep tables
    min_word_length=1     # Keep single-char words
)
```

### Issue: Inconsistent extraction across years

**Cause**: SEC changed 10-K format over time

**Solution**: The parser handles multiple formats. If issues persist:
1. Review extraction patterns in `parser.py`
2. Add new patterns for specific formats
3. Report issue with example CIK/year

---

## Performance

### Parsing Speed

- **Average**: ~1-2 seconds per file
- **Batch of 100 files**: ~2-3 minutes
- **Batch of 1,000 files**: ~20-30 minutes

### Cleaning Speed

- **Average**: ~0.1 seconds per section
- **Batch of 1,000 sections**: ~2 minutes

### Optimization Tips

1. **Process in batches**: Use `parse_batch()` and `clean_batch()`
2. **Skip existing**: Check if files exist before reprocessing
3. **Parallel processing**: Process different years in parallel
4. **Reduce logging**: Set log level to WARNING for faster processing

---

## API Reference

Full API documentation:

```python
help(TenKParser)
help(TextCleaner)
```

---

**Last Updated**: 2026-01-21
**Version**: 1.0
