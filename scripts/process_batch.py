#!/usr/bin/env python3
"""
Process Batch Script

Processes downloaded 10-K files: parses sections and cleans text.
This script runs after download_10k.py to extract and clean the relevant sections.

Usage:
    python scripts/process_batch.py [--input-dir data/raw/10k] [--output-dir data/processed/cleaned]

Arguments:
    --input-dir: Directory containing raw 10-K HTML files
    --output-dir: Directory to save processed text
    --batch-size: Number of files to process (default: all)
    --skip-existing: Skip files already processed (default: True)
    --sections: Which sections to extract (default: item_1,item_1a,item_7)

Author: Corporate Text Pipeline Team
Date: 2026-01-21
"""

import sys
import os
import argparse
import logging
from pathlib import Path
from datetime import datetime
from tqdm import tqdm
import pandas as pd

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.config import load_config
from src.processors import TenKParser, TextCleaner
from src.utils.logging_utils import setup_logging


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Process downloaded 10-K files: parse and clean sections",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process all 10-Ks in default directory
  python scripts/process_batch.py

  # Process specific directory
  python scripts/process_batch.py --input-dir data/raw/10k --output-dir data/processed/cleaned

  # Process first 50 files
  python scripts/process_batch.py --batch-size 50

  # Extract only Item 1A (Risk Factors)
  python scripts/process_batch.py --sections item_1a
        """
    )

    parser.add_argument(
        '--input-dir',
        type=str,
        default=None,
        help='Input directory with raw 10-K files (default: from config)'
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        default=None,
        help='Output directory for processed text (default: from config)'
    )

    parser.add_argument(
        '--batch-size',
        type=int,
        default=None,
        help='Number of files to process (default: all)'
    )

    parser.add_argument(
        '--skip-existing',
        action='store_true',
        default=True,
        help='Skip files that have already been processed (default: True)'
    )

    parser.add_argument(
        '--no-skip-existing',
        dest='skip_existing',
        action='store_false',
        help='Re-process files even if they exist'
    )

    parser.add_argument(
        '--sections',
        type=str,
        default='item_1,item_1a,item_7',
        help='Comma-separated list of sections to extract (default: item_1,item_1a,item_7)'
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
        '--min-section-length',
        type=int,
        default=1000,
        help='Minimum section length in characters (default: 1000)'
    )

    parser.add_argument(
        '--clean',
        action='store_true',
        default=True,
        help='Clean extracted text (default: True)'
    )

    parser.add_argument(
        '--no-clean',
        dest='clean',
        action='store_false',
        help='Do not clean extracted text (keep raw)'
    )

    return parser.parse_args()


def get_processed_files(output_dir: Path, sections: list) -> set:
    """
    Get set of files that have already been processed.

    Args:
        output_dir: Output directory
        sections: List of sections being extracted

    Returns:
        Set of base filenames that have all sections
    """
    if not output_dir.exists():
        return set()

    processed = {}

    for txt_file in output_dir.glob('*_item_*.txt'):
        # Extract base name (e.g., 0000001750_2020_10K)
        base_name = '_'.join(txt_file.stem.split('_')[:-2])

        if base_name not in processed:
            processed[base_name] = set()

        # Extract section name
        section = '_'.join(txt_file.stem.split('_')[-2:])
        processed[base_name].add(section)

    # Return only files that have all required sections
    complete = set()
    for base_name, found_sections in processed.items():
        if all(section in found_sections for section in sections):
            complete.add(base_name)

    return complete


def process_file(
    filepath: Path,
    parser: TenKParser,
    cleaner: TextCleaner,
    output_dir: Path,
    sections: list,
    clean_text: bool = True
) -> dict:
    """
    Process a single 10-K file.

    Args:
        filepath: Path to 10-K file
        parser: TenKParser instance
        cleaner: TextCleaner instance
        output_dir: Output directory
        sections: List of sections to extract
        clean_text: Whether to clean extracted text

    Returns:
        Dictionary with processing results
    """
    base_name = filepath.stem
    results = {
        'filename': filepath.name,
        'base_name': base_name,
        'success': False,
        'sections_extracted': 0,
        'sections_cleaned': 0
    }

    try:
        # Parse file
        extracted = parser.parse_file(filepath)

        # Save each section
        for section_name in sections:
            text = extracted.get(section_name)

            if text:
                results['sections_extracted'] += 1

                # Clean text if requested
                if clean_text:
                    text = cleaner.clean(text)
                    results['sections_cleaned'] += 1

                # Save to file
                output_file = output_dir / f"{base_name}_{section_name}.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(text)

                results[f'{section_name}_length'] = len(text)

        results['success'] = results['sections_extracted'] > 0

    except Exception as e:
        logging.error(f"Error processing {filepath.name}: {e}", exc_info=True)
        results['error'] = str(e)

    return results


def save_results(results: list, output_dir: Path, timestamp: str):
    """
    Save processing results to CSV.

    Args:
        results: List of result dictionaries
        output_dir: Output directory
        timestamp: Timestamp string
    """
    results_dir = output_dir / "processing_logs"
    results_dir.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(results)

    # Save full results
    results_file = results_dir / f"processing_results_{timestamp}.csv"
    df.to_csv(results_file, index=False)
    logging.info(f"Saved results to {results_file}")

    # Save summary
    summary_file = results_dir / f"processing_summary_{timestamp}.txt"
    with open(summary_file, 'w') as f:
        f.write("10-K Processing Summary\n")
        f.write("=" * 50 + "\n")
        f.write(f"Total files: {len(df)}\n")
        f.write(f"Successful: {df['success'].sum()}\n")
        f.write(f"Failed: {(~df['success']).sum()}\n")
        f.write(f"Success rate: {df['success'].mean() * 100:.2f}%\n")
        f.write(f"\nAverage sections per file: {df['sections_extracted'].mean():.2f}\n")

    logging.info(f"Saved summary to {summary_file}")


def main():
    """Main execution function."""
    args = parse_arguments()

    # Setup logging
    log_dir = project_root / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"process_batch_{timestamp}.log"

    setup_logging(log_file=str(log_file), level=args.log_level)
    logger = logging.getLogger(__name__)

    logger.info("=" * 70)
    logger.info("Starting 10-K Processing")
    logger.info("=" * 70)
    logger.info(f"Arguments: {vars(args)}")

    try:
        # Load configuration
        config = load_config(args.config)
        logger.info(f"Loaded configuration from {args.config}")

        # Determine directories
        input_dir = Path(args.input_dir) if args.input_dir else Path(config['paths']['raw_10k'])
        output_dir = Path(args.output_dir) if args.output_dir else Path(config['paths']['cleaned_text'])

        # Parse sections
        sections = [s.strip() for s in args.sections.split(',')]

        logger.info(f"Input directory: {input_dir}")
        logger.info(f"Output directory: {output_dir}")
        logger.info(f"Sections to extract: {sections}")

        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)

        # Get list of files to process
        html_files = list(input_dir.glob('*.html'))
        logger.info(f"Found {len(html_files)} HTML files")

        if args.batch_size:
            html_files = html_files[:args.batch_size]
            logger.info(f"Processing first {len(html_files)} files")

        # Skip already processed files
        if args.skip_existing:
            processed = get_processed_files(output_dir, sections)
            html_files = [f for f in html_files if f.stem not in processed]
            logger.info(f"Skipping {len(processed)} already processed files")
            logger.info(f"Remaining to process: {len(html_files)}")

        if not html_files:
            logger.info("No files to process")
            return 0

        # Initialize parser and cleaner
        parser = TenKParser(min_section_length=args.min_section_length)
        cleaner = TextCleaner() if args.clean else None

        logger.info("Starting batch processing...")

        # Process files
        results = []
        for filepath in tqdm(html_files, desc="Processing files"):
            result = process_file(
                filepath=filepath,
                parser=parser,
                cleaner=cleaner,
                output_dir=output_dir,
                sections=sections,
                clean_text=args.clean
            )
            results.append(result)

        # Save results
        save_results(results, output_dir, timestamp)

        # Print summary
        df = pd.DataFrame(results)
        print("\n" + "=" * 70)
        print("Processing Complete!")
        print("=" * 70)
        print(f"Total files: {len(df)}")
        print(f"Successful: {df['success'].sum()}")
        print(f"Failed: {(~df['success']).sum()}")
        print(f"Success rate: {df['success'].mean() * 100:.2f}%")
        print(f"\nLog file: {log_file}")
        print("=" * 70 + "\n")

        return 0 if df['success'].all() else 1

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\nERROR: {e}")
        print(f"See log file: {log_file}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
