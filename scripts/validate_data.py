#!/usr/bin/env python3
"""
Data Validation Script

Validates downloaded and processed data at each stage of the pipeline.
Checks file integrity, content quality, and completeness.

Usage:
    python scripts/validate_data.py [--stage downloads|processed|all]

Arguments:
    --stage: Which pipeline stage to validate (default: all)
    --firm-list: Path to firm list CSV (default: from config)
    --downloads-dir: Directory with downloaded 10-Ks (default: from config)
    --processed-dir: Directory with processed text (default: from config)
    --report: Generate detailed validation report

Author: Corporate Text Pipeline Team
Date: 2026-01-21
"""

import sys
import os
import argparse
import logging
from pathlib import Path
from datetime import datetime
import pandas as pd

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.config import load_config
from src.utils import (
    validate_firm_list,
    validate_download_directory,
    validate_10k_file,
    validate_filename,
    validate_extracted_text,
    get_missing_downloads,
    validate_pipeline_data
)
from src.utils.logging_utils import setup_logging


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Validate pipeline data at various stages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate everything
  python scripts/validate_data.py

  # Validate only downloads
  python scripts/validate_data.py --stage downloads

  # Generate detailed report
  python scripts/validate_data.py --report

  # Validate specific directories
  python scripts/validate_data.py --downloads-dir data/raw/10k --firm-list data/firm_lists/target_firm_years.csv
        """
    )

    parser.add_argument(
        '--stage',
        type=str,
        default='all',
        choices=['downloads', 'processed', 'all'],
        help='Which stage to validate (default: all)'
    )

    parser.add_argument(
        '--firm-list',
        type=str,
        default=None,
        help='Path to firm list CSV (default: from config)'
    )

    parser.add_argument(
        '--downloads-dir',
        type=str,
        default=None,
        help='Directory with downloaded 10-Ks (default: from config)'
    )

    parser.add_argument(
        '--processed-dir',
        type=str,
        default=None,
        help='Directory with processed text (default: from config)'
    )

    parser.add_argument(
        '--report',
        action='store_true',
        help='Generate detailed validation report'
    )

    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )

    parser.add_argument(
        '--log-level',
        type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Logging level (default: INFO)'
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        default='validation_reports',
        help='Directory to save validation reports (default: validation_reports)'
    )

    return parser.parse_args()


def validate_firm_list_stage(firm_list_path: Path) -> dict:
    """
    Validate the firm list CSV.

    Args:
        firm_list_path: Path to firm list CSV

    Returns:
        Validation results dictionary
    """
    print("\n" + "=" * 70)
    print("VALIDATING FIRM LIST")
    print("=" * 70)

    results = {'stage': 'firm_list', 'valid': False}

    if not firm_list_path.exists():
        print(f"❌ Firm list not found: {firm_list_path}")
        results['errors'] = [f"File not found: {firm_list_path}"]
        return results

    try:
        # Load firm list
        df = pd.read_csv(firm_list_path)
        df.columns = df.columns.str.lower()

        print(f"✓ Loaded {len(df)} firm-year combinations")

        # Validate
        is_valid, errors = validate_firm_list(df)

        if is_valid:
            print("✓ Firm list is valid")
            print(f"  - Unique firms: {df['cik'].nunique()}")
            print(f"  - Year range: {df['year'].min()}-{df['year'].max()}")

            results['valid'] = True
            results['count'] = len(df)
            results['unique_firms'] = df['cik'].nunique()
            results['year_range'] = (int(df['year'].min()), int(df['year'].max()))
        else:
            print("❌ Firm list has validation errors:")
            for error in errors:
                print(f"  - {error}")

            results['valid'] = False
            results['errors'] = errors

    except Exception as e:
        print(f"❌ Error loading firm list: {e}")
        results['errors'] = [str(e)]

    return results


def validate_downloads_stage(downloads_dir: Path, firm_list: pd.DataFrame = None) -> dict:
    """
    Validate downloaded 10-K files.

    Args:
        downloads_dir: Directory with downloads
        firm_list: Optional firm list for completeness check

    Returns:
        Validation results dictionary
    """
    print("\n" + "=" * 70)
    print("VALIDATING DOWNLOADS")
    print("=" * 70)

    results = {'stage': 'downloads', 'valid': False}

    if not downloads_dir.exists():
        print(f"❌ Downloads directory not found: {downloads_dir}")
        results['errors'] = [f"Directory not found: {downloads_dir}"]
        return results

    # Validate directory
    is_valid, stats = validate_download_directory(str(downloads_dir))

    print(f"Files found: {stats['total_files']}")
    print(f"Valid files: {stats['valid_files']}")
    print(f"Invalid files: {stats['invalid_files']}")

    if stats['too_small'] > 0:
        print(f"  - Too small: {stats['too_small']}")
    if stats['unreadable'] > 0:
        print(f"  - Unreadable: {stats['unreadable']}")

    # Check filenames
    print(f"\nFilename validation:")
    print(f"  Valid: {stats['valid_filenames']}")
    print(f"  Invalid: {stats['invalid_filenames']}")

    # Check completeness if firm list provided
    if firm_list is not None:
        missing = get_missing_downloads(firm_list, str(downloads_dir))
        print(f"\nCompleteness:")
        print(f"  Expected: {len(firm_list)}")
        print(f"  Downloaded: {stats['valid_files']}")
        print(f"  Missing: {len(missing)}")

        if len(missing) > 0:
            print(f"\n  First 5 missing:")
            for _, row in missing.head().iterrows():
                print(f"    - CIK: {row['cik']}, Year: {row['year']}")

        results['missing'] = missing
        results['completeness_rate'] = (stats['valid_files'] / len(firm_list) * 100) if len(firm_list) > 0 else 0

    results['valid'] = is_valid
    results['stats'] = stats

    if is_valid:
        print("\n✓ All downloads are valid")
    else:
        print(f"\n❌ {stats['invalid_files']} files have issues")

    return results


def validate_processed_stage(processed_dir: Path, downloads_dir: Path = None) -> dict:
    """
    Validate processed text files.

    Args:
        processed_dir: Directory with processed text
        downloads_dir: Optional downloads directory for comparison

    Returns:
        Validation results dictionary
    """
    print("\n" + "=" * 70)
    print("VALIDATING PROCESSED TEXT")
    print("=" * 70)

    results = {'stage': 'processed', 'valid': True}

    if not processed_dir.exists():
        print(f"❌ Processed directory not found: {processed_dir}")
        results['errors'] = [f"Directory not found: {processed_dir}"]
        results['valid'] = False
        return results

    # Get all text files
    txt_files = list(processed_dir.glob('*_item_*.txt'))
    print(f"Found {len(txt_files)} processed section files")

    # Group by base file
    files_by_base = {}
    for txt_file in txt_files:
        # Extract base name (e.g., 0000001750_2020_10K)
        base_name = '_'.join(txt_file.stem.split('_')[:-2])
        section = '_'.join(txt_file.stem.split('_')[-2:])

        if base_name not in files_by_base:
            files_by_base[base_name] = []
        files_by_base[base_name].append(section)

    print(f"Unique source files: {len(files_by_base)}")

    # Validate each file
    validation_errors = []
    section_stats = {'item_1': 0, 'item_1a': 0, 'item_7': 0}
    total_chars = 0
    total_words = 0

    for txt_file in txt_files:
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                text = f.read()

            # Validate text quality
            is_valid, message = validate_extracted_text(text)

            if not is_valid:
                validation_errors.append(f"{txt_file.name}: {message}")
            else:
                total_chars += len(text)
                total_words += len(text.split())

                # Track section stats
                for section in section_stats.keys():
                    if section in txt_file.name:
                        section_stats[section] += 1

        except Exception as e:
            validation_errors.append(f"{txt_file.name}: Error reading file - {e}")

    # Print statistics
    print(f"\nSection counts:")
    for section, count in section_stats.items():
        print(f"  {section}: {count}")

    if len(txt_files) > 0:
        print(f"\nAverage length:")
        print(f"  Characters: {total_chars / len(txt_files):,.0f}")
        print(f"  Words: {total_words / len(txt_files):,.0f}")

    # Compare with downloads if provided
    if downloads_dir and downloads_dir.exists():
        html_files = len(list(downloads_dir.glob('*.html')))
        coverage = len(files_by_base) / html_files * 100 if html_files > 0 else 0
        print(f"\nProcessing coverage:")
        print(f"  Downloaded: {html_files}")
        print(f"  Processed: {len(files_by_base)}")
        print(f"  Coverage: {coverage:.1f}%")

        results['coverage'] = coverage

    # Report errors
    if validation_errors:
        print(f"\n❌ Found {len(validation_errors)} validation errors:")
        for error in validation_errors[:10]:  # Show first 10
            print(f"  - {error}")
        if len(validation_errors) > 10:
            print(f"  ... and {len(validation_errors) - 10} more")

        results['valid'] = False
        results['errors'] = validation_errors
    else:
        print("\n✓ All processed files are valid")

    results['stats'] = {
        'total_files': len(txt_files),
        'unique_sources': len(files_by_base),
        'section_stats': section_stats,
        'avg_chars': total_chars / len(txt_files) if txt_files else 0,
        'avg_words': total_words / len(txt_files) if txt_files else 0
    }

    return results


def generate_report(validation_results: dict, output_dir: Path):
    """
    Generate detailed validation report.

    Args:
        validation_results: Dictionary with all validation results
        output_dir: Directory to save report
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = output_dir / f"validation_report_{timestamp}.txt"

    with open(report_file, 'w') as f:
        f.write("PIPELINE DATA VALIDATION REPORT\n")
        f.write("=" * 70 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")

        for stage, results in validation_results.items():
            f.write(f"\n{stage.upper()}\n")
            f.write("-" * 70 + "\n")

            if 'valid' in results:
                f.write(f"Status: {'PASS' if results['valid'] else 'FAIL'}\n")

            # Write all result fields
            for key, value in results.items():
                if key not in ['valid', 'stage']:
                    if isinstance(value, pd.DataFrame):
                        f.write(f"\n{key}:\n")
                        f.write(value.to_string(index=False))
                        f.write("\n")
                    elif isinstance(value, dict):
                        f.write(f"\n{key}:\n")
                        for k, v in value.items():
                            f.write(f"  {k}: {v}\n")
                    elif isinstance(value, list):
                        f.write(f"\n{key}: ({len(value)} items)\n")
                        for item in value[:10]:
                            f.write(f"  - {item}\n")
                        if len(value) > 10:
                            f.write(f"  ... and {len(value) - 10} more\n")
                    else:
                        f.write(f"{key}: {value}\n")

            f.write("\n")

    print(f"\n✓ Detailed report saved to: {report_file}")


def main():
    """Main execution function."""
    args = parse_arguments()

    # Setup logging
    log_dir = project_root / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"validate_data_{timestamp}.log"

    setup_logging(log_file=str(log_file), level=args.log_level)
    logger = logging.getLogger(__name__)

    logger.info("=" * 70)
    logger.info("Starting Data Validation")
    logger.info("=" * 70)
    logger.info(f"Arguments: {vars(args)}")

    try:
        # Load configuration
        config = load_config(args.config)

        # Determine paths
        firm_list_path = Path(args.firm_list) if args.firm_list else Path(config['project_root']) / config['firm_list_file']
        downloads_dir = Path(args.downloads_dir) if args.downloads_dir else Path(config['paths']['raw_10k'])
        processed_dir = Path(args.processed_dir) if args.processed_dir else Path(config['paths']['cleaned_text'])

        validation_results = {}

        # Load firm list
        firm_list = None
        firm_list_results = validate_firm_list_stage(firm_list_path)
        validation_results['firm_list'] = firm_list_results

        if firm_list_results['valid']:
            firm_list = pd.read_csv(firm_list_path)
            firm_list.columns = firm_list.columns.str.lower()

        # Validate downloads
        if args.stage in ['downloads', 'all']:
            downloads_results = validate_downloads_stage(downloads_dir, firm_list)
            validation_results['downloads'] = downloads_results

        # Validate processed files
        if args.stage in ['processed', 'all']:
            processed_results = validate_processed_stage(processed_dir, downloads_dir)
            validation_results['processed'] = processed_results

        # Generate report if requested
        if args.report:
            output_dir = Path(args.output_dir)
            generate_report(validation_results, output_dir)

        # Print final summary
        print("\n" + "=" * 70)
        print("VALIDATION SUMMARY")
        print("=" * 70)

        all_valid = all(r.get('valid', False) for r in validation_results.values())

        for stage, results in validation_results.items():
            status = "✓ PASS" if results.get('valid', False) else "❌ FAIL"
            print(f"{stage.ljust(20)}: {status}")

        print("=" * 70)

        if all_valid:
            print("✓ All validation checks passed")
            return 0
        else:
            print("❌ Some validation checks failed")
            return 1

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\nERROR: {e}")
        print(f"See log file: {log_file}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
