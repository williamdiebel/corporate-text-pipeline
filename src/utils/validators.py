"""
Data Validators

Validation functions for 10-K downloads, parsing, and data quality checks.
"""

import re
import logging
from pathlib import Path
from typing import Tuple, Optional, List, Dict
import pandas as pd

logger = logging.getLogger(__name__)


def validate_cik(cik: str) -> Tuple[bool, Optional[str]]:
    """
    Validate and format CIK (Central Index Key).

    Args:
        cik: CIK string to validate

    Returns:
        Tuple of (is_valid, formatted_cik)
        formatted_cik is 10-digit zero-padded string or None if invalid
    """
    if not cik:
        return False, None

    # Remove any whitespace
    cik = str(cik).strip()

    # Check if it's a valid number
    if not cik.isdigit():
        return False, None

    # CIK should be at most 10 digits
    if len(cik) > 10:
        return False, None

    # Zero-pad to 10 digits
    formatted_cik = cik.zfill(10)

    return True, formatted_cik


def validate_year(year: int, min_year: int = 1994, max_year: int = None) -> bool:
    """
    Validate fiscal year.

    Args:
        year: Year to validate
        min_year: Minimum valid year (SEC EDGAR starts 1994)
        max_year: Maximum valid year (defaults to current year + 1)

    Returns:
        True if valid, False otherwise
    """
    if max_year is None:
        from datetime import datetime
        max_year = datetime.now().year + 1

    try:
        year = int(year)
        return min_year <= year <= max_year
    except (ValueError, TypeError):
        return False


def validate_10k_file(filepath: str, min_size: int = 1000) -> Tuple[bool, str]:
    """
    Validate a downloaded 10-K file.

    Args:
        filepath: Path to 10-K file
        min_size: Minimum file size in bytes

    Returns:
        Tuple of (is_valid, message)
    """
    filepath = Path(filepath)

    # Check file exists
    if not filepath.exists():
        return False, "File does not exist"

    # Check file size
    file_size = filepath.stat().st_size
    if file_size < min_size:
        return False, f"File too small: {file_size} bytes (minimum: {min_size})"

    # Check file extension
    if filepath.suffix.lower() not in ['.html', '.htm', '.txt']:
        return False, f"Invalid file extension: {filepath.suffix}"

    # Check file is readable
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(1000)  # Read first 1000 chars

        # Check for common 10-K indicators
        content_lower = content.lower()
        has_10k_indicator = any(keyword in content_lower for keyword in [
            '10-k', 'form 10-k', 'annual report', 'securities and exchange commission'
        ])

        if not has_10k_indicator:
            return False, "File does not appear to be a 10-K filing"

    except Exception as e:
        return False, f"Error reading file: {e}"

    return True, "Valid"


def validate_filename(filename: str) -> Tuple[bool, Optional[str], Optional[int]]:
    """
    Validate 10-K filename format.

    Expected format: {CIK}_{YEAR}_10K.html

    Args:
        filename: Filename to validate

    Returns:
        Tuple of (is_valid, cik, year)
    """
    pattern = r'^(\d{10})_(\d{4})_10K\.(html?|txt)$'
    match = re.match(pattern, filename, re.IGNORECASE)

    if not match:
        return False, None, None

    cik = match.group(1)
    year = int(match.group(2))

    # Validate CIK and year
    cik_valid, formatted_cik = validate_cik(cik)
    year_valid = validate_year(year)

    if not (cik_valid and year_valid):
        return False, None, None

    return True, formatted_cik, year


def validate_extracted_text(text: str, min_length: int = 1000, min_words: int = 100) -> Tuple[bool, str]:
    """
    Validate extracted text quality.

    Args:
        text: Extracted text to validate
        min_length: Minimum character length
        min_words: Minimum word count

    Returns:
        Tuple of (is_valid, message)
    """
    if not text:
        return False, "Text is empty"

    # Check minimum length
    if len(text) < min_length:
        return False, f"Text too short: {len(text)} characters (minimum: {min_length})"

    # Check minimum word count
    word_count = len(text.split())
    if word_count < min_words:
        return False, f"Too few words: {word_count} (minimum: {min_words})"

    # Check for excessive non-alphabetic characters (indicates bad extraction)
    alpha_chars = sum(c.isalpha() for c in text)
    alpha_ratio = alpha_chars / len(text)

    if alpha_ratio < 0.5:
        return False, f"Too many non-alphabetic characters: {alpha_ratio:.1%}"

    return True, "Valid"


def validate_firm_list(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Validate firm-year list DataFrame.

    Args:
        df: DataFrame to validate

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    # Check required columns
    required_columns = ['cik', 'year']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        errors.append(f"Missing required columns: {missing_columns}")
        return False, errors

    # Check for empty DataFrame
    if len(df) == 0:
        errors.append("DataFrame is empty")
        return False, errors

    # Validate CIKs
    invalid_ciks = []
    for idx, cik in enumerate(df['cik']):
        is_valid, _ = validate_cik(str(cik))
        if not is_valid:
            invalid_ciks.append(f"Row {idx}: {cik}")

    if invalid_ciks:
        errors.append(f"Invalid CIKs found: {invalid_ciks[:5]}")  # Show first 5

    # Validate years
    invalid_years = []
    for idx, year in enumerate(df['year']):
        if not validate_year(year):
            invalid_years.append(f"Row {idx}: {year}")

    if invalid_years:
        errors.append(f"Invalid years found: {invalid_years[:5]}")  # Show first 5

    # Check for duplicates
    duplicates = df[df.duplicated(subset=['cik', 'year'], keep=False)]
    if len(duplicates) > 0:
        errors.append(f"Found {len(duplicates)} duplicate CIK-year combinations")

    if errors:
        return False, errors

    return True, []


def validate_download_directory(directory: str) -> Tuple[bool, Dict[str, int]]:
    """
    Validate a directory of downloaded 10-K files.

    Args:
        directory: Directory path to validate

    Returns:
        Tuple of (all_valid, statistics_dict)
    """
    directory = Path(directory)

    if not directory.exists():
        return False, {'error': 'Directory does not exist'}

    stats = {
        'total_files': 0,
        'valid_files': 0,
        'invalid_files': 0,
        'valid_filenames': 0,
        'invalid_filenames': 0,
        'too_small': 0,
        'unreadable': 0
    }

    # Get all HTML/TXT files
    files = list(directory.glob('*.html')) + list(directory.glob('*.htm')) + list(directory.glob('*.txt'))
    stats['total_files'] = len(files)

    for filepath in files:
        # Validate filename
        filename_valid, _, _ = validate_filename(filepath.name)
        if filename_valid:
            stats['valid_filenames'] += 1
        else:
            stats['invalid_filenames'] += 1

        # Validate file content
        file_valid, message = validate_10k_file(filepath)
        if file_valid:
            stats['valid_files'] += 1
        else:
            stats['invalid_files'] += 1

            # Categorize error
            if 'too small' in message.lower():
                stats['too_small'] += 1
            elif 'error reading' in message.lower():
                stats['unreadable'] += 1

    all_valid = stats['invalid_files'] == 0 and stats['invalid_filenames'] == 0

    return all_valid, stats


def validate_batch_results(results_df: pd.DataFrame, expected_count: int = None) -> Tuple[bool, Dict]:
    """
    Validate batch processing results.

    Args:
        results_df: DataFrame with batch results
        expected_count: Expected number of results (optional)

    Returns:
        Tuple of (is_valid, summary_dict)
    """
    summary = {
        'total_processed': len(results_df),
        'successful': 0,
        'failed': 0,
        'success_rate': 0.0
    }

    if 'success' in results_df.columns:
        summary['successful'] = results_df['success'].sum()
        summary['failed'] = len(results_df) - summary['successful']
        summary['success_rate'] = (summary['successful'] / len(results_df) * 100) if len(results_df) > 0 else 0

    # Check if count matches expected
    if expected_count is not None:
        summary['count_match'] = len(results_df) == expected_count
        is_valid = summary['count_match'] and summary['success_rate'] > 0
    else:
        is_valid = summary['success_rate'] > 0

    return is_valid, summary


def get_missing_downloads(firm_years: pd.DataFrame, download_dir: str) -> pd.DataFrame:
    """
    Find firm-years that haven't been downloaded.

    Args:
        firm_years: DataFrame with 'cik' and 'year' columns
        download_dir: Directory containing downloads

    Returns:
        DataFrame with missing firm-years
    """
    download_dir = Path(download_dir)

    # Get list of downloaded files
    downloaded = set()
    for filepath in download_dir.glob('*.html'):
        is_valid, cik, year = validate_filename(filepath.name)
        if is_valid:
            downloaded.add((cik, year))

    # Find missing
    missing = []
    for _, row in firm_years.iterrows():
        cik_valid, formatted_cik = validate_cik(str(row['cik']))
        if cik_valid:
            key = (formatted_cik, int(row['year']))
            if key not in downloaded:
                missing.append({'cik': formatted_cik, 'year': int(row['year'])})

    return pd.DataFrame(missing)


# Convenience function for common validation workflow
def validate_pipeline_data(
    firm_list_path: str,
    download_dir: str,
    parsed_dir: str = None
) -> Dict[str, any]:
    """
    Validate entire pipeline data.

    Args:
        firm_list_path: Path to firm list CSV
        download_dir: Directory with downloaded 10-Ks
        parsed_dir: Directory with parsed sections (optional)

    Returns:
        Dictionary with validation results
    """
    results = {}

    # Validate firm list
    try:
        firm_list = pd.read_csv(firm_list_path)
        firm_list.columns = firm_list.columns.str.lower()

        is_valid, errors = validate_firm_list(firm_list)
        results['firm_list'] = {
            'valid': is_valid,
            'errors': errors,
            'count': len(firm_list)
        }
    except Exception as e:
        results['firm_list'] = {
            'valid': False,
            'errors': [f"Error loading firm list: {e}"],
            'count': 0
        }

    # Validate downloads
    is_valid, stats = validate_download_directory(download_dir)
    results['downloads'] = {
        'valid': is_valid,
        'stats': stats
    }

    # Find missing downloads
    if results['firm_list']['valid']:
        missing = get_missing_downloads(firm_list, download_dir)
        results['missing_downloads'] = {
            'count': len(missing),
            'missing': missing
        }

    # Validate parsed files (if directory provided)
    if parsed_dir:
        is_valid, stats = validate_download_directory(parsed_dir)
        results['parsed'] = {
            'valid': is_valid,
            'stats': stats
        }

    return results


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) > 1:
        test_path = sys.argv[1]

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

        print(f"Validating: {test_path}")
        print("-" * 50)

        # Check if it's a file or directory
        path = Path(test_path)

        if path.is_file():
            # Validate single file
            is_valid, message = validate_10k_file(test_path)
            print(f"File validation: {'PASS' if is_valid else 'FAIL'}")
            print(f"Message: {message}")

        elif path.is_dir():
            # Validate directory
            is_valid, stats = validate_download_directory(test_path)
            print(f"Directory validation: {'PASS' if is_valid else 'FAIL'}")
            print("\nStatistics:")
            for key, value in stats.items():
                print(f"  {key}: {value}")

        else:
            print("Path does not exist")

    else:
        print("Usage: python validators.py <file_or_directory>")
