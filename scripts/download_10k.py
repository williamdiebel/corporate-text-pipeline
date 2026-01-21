#!/usr/bin/env python3
"""
10-K Download Script

Main executable script for downloading 10-K filings from SEC EDGAR.
Reads firm-year combinations from CSV and orchestrates the download process.

Usage:
    python scripts/download_10k.py [--batch-size 100] [--start-index 0] [--skip-existing]

Arguments:
    --batch-size: Number of firm-years to process (default: all)
    --start-index: Starting index in the firm list (default: 0)
    --skip-existing: Skip files that already exist (default: True)
    --config: Path to config file (default: config.yaml)

Author: Corporate Text Pipeline Team
Date: 2026-01-21
"""

import sys
import os
import argparse
import logging
import pandas as pd
from pathlib import Path
from datetime import datetime
from tqdm import tqdm

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.config import load_config
from src.downloaders.sec_downloader import SECDownloader
from src.utils.logging_utils import setup_logging


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Download 10-K filings from SEC EDGAR",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download all 10-Ks
  python scripts/download_10k.py

  # Download first 100 10-Ks
  python scripts/download_10k.py --batch-size 100

  # Resume from index 500, download 200 more
  python scripts/download_10k.py --start-index 500 --batch-size 200

  # Re-download everything (overwrite existing)
  python scripts/download_10k.py --no-skip-existing
        """
    )

    parser.add_argument(
        '--batch-size',
        type=int,
        default=None,
        help='Number of firm-years to process (default: all)'
    )

    parser.add_argument(
        '--start-index',
        type=int,
        default=0,
        help='Starting index in the firm list (default: 0)'
    )

    parser.add_argument(
        '--skip-existing',
        action='store_true',
        default=True,
        help='Skip files that already exist (default: True)'
    )

    parser.add_argument(
        '--no-skip-existing',
        dest='skip_existing',
        action='store_false',
        help='Re-download files even if they exist'
    )

    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='Path to configuration file (default: config.yaml)'
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        default=None,
        help='Override output directory from config'
    )

    parser.add_argument(
        '--log-level',
        type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Logging level (default: INFO)'
    )

    return parser.parse_args()


def load_firm_list(config: dict, start_index: int = 0, batch_size: int = None) -> pd.DataFrame:
    """
    Load firm-year list from CSV.

    Args:
        config: Configuration dictionary
        start_index: Starting index for slicing
        batch_size: Number of rows to load

    Returns:
        DataFrame with CIK and year columns
    """
    # Handle both nested and flat config structures
    if 'data' in config and 'firm_list' in config['data']:
        firm_list_path = Path(config['data']['firm_list'])
    elif 'firm_list_file' in config:
        firm_list_path = Path(config['project_root']) / config['firm_list_file']
    else:
        raise ValueError("Config must contain either 'data.firm_list' or 'firm_list_file'")

    if not firm_list_path.exists():
        raise FileNotFoundError(f"Firm list not found: {firm_list_path}")

    # Load CSV
    df = pd.read_csv(firm_list_path)

    # Validate required columns (handle both lowercase and uppercase)
    required_cols = ['cik', 'year']
    df.columns = df.columns.str.lower()  # Normalize to lowercase

    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        # Try alternative column names
        if 'fyear' in df.columns:
            df = df.rename(columns={'fyear': 'year'})

        # Check again
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}. Found: {df.columns.tolist()}")

    # Convert CIK to string and year to int
    df['cik'] = df['cik'].astype(str)
    df['year'] = df['year'].astype(int)

    # Apply slicing
    end_index = start_index + batch_size if batch_size else len(df)
    df_batch = df.iloc[start_index:end_index].copy()

    logging.info(f"Loaded {len(df_batch)} firm-year combinations "
                f"(from index {start_index} to {end_index} of {len(df)} total)")

    return df_batch


def progress_callback(current: int, total: int, results: dict):
    """
    Progress callback for batch download.

    Args:
        current: Current item number
        total: Total items
        results: Results dictionary
    """
    success_count = len(results['successful'])
    failed_count = len(results['failed'])
    skipped_count = len(results['skipped'])

    print(f"\rProgress: {current}/{total} | "
          f"Success: {success_count} | Failed: {failed_count} | Skipped: {skipped_count}",
          end='', flush=True)


def save_results(results: dict, output_dir: Path, timestamp: str):
    """
    Save download results to CSV files.

    Args:
        results: Results dictionary from batch download
        output_dir: Directory to save results
        timestamp: Timestamp string for filename
    """
    results_dir = output_dir / "download_logs"
    results_dir.mkdir(parents=True, exist_ok=True)

    # Save successful downloads
    if results['successful']:
        df_success = pd.DataFrame(results['successful'])
        success_file = results_dir / f"successful_{timestamp}.csv"
        df_success.to_csv(success_file, index=False)
        logging.info(f"Saved successful downloads to {success_file}")

    # Save failed downloads
    if results['failed']:
        df_failed = pd.DataFrame(results['failed'])
        failed_file = results_dir / f"failed_{timestamp}.csv"
        df_failed.to_csv(failed_file, index=False)
        logging.info(f"Saved failed downloads to {failed_file}")

    # Save skipped downloads
    if results['skipped']:
        df_skipped = pd.DataFrame(results['skipped'])
        skipped_file = results_dir / f"skipped_{timestamp}.csv"
        df_skipped.to_csv(skipped_file, index=False)
        logging.info(f"Saved skipped downloads to {skipped_file}")

    # Save summary
    summary = {
        'timestamp': timestamp,
        'total_attempted': len(results['successful']) + len(results['failed']) + len(results['skipped']),
        'successful': len(results['successful']),
        'failed': len(results['failed']),
        'skipped': len(results['skipped']),
        'success_rate': len(results['successful']) / max(1, len(results['successful']) + len(results['failed'])) * 100
    }

    summary_file = results_dir / f"summary_{timestamp}.txt"
    with open(summary_file, 'w') as f:
        f.write("10-K Download Summary\n")
        f.write("=" * 50 + "\n")
        for key, value in summary.items():
            if key == 'success_rate':
                f.write(f"{key}: {value:.2f}%\n")
            else:
                f.write(f"{key}: {value}\n")

    logging.info(f"Saved summary to {summary_file}")


def main():
    """Main execution function."""
    # Parse arguments
    args = parse_arguments()

    # Setup logging
    log_dir = project_root / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"download_10k_{timestamp}.log"

    setup_logging(log_file=str(log_file), level=args.log_level)
    logger = logging.getLogger(__name__)

    logger.info("=" * 70)
    logger.info("Starting 10-K Download Process")
    logger.info("=" * 70)
    logger.info(f"Arguments: {vars(args)}")

    try:
        # Load configuration
        config = load_config(args.config)
        logger.info(f"Loaded configuration from {args.config}")

        # Determine output directory
        output_dir = args.output_dir if args.output_dir else config['paths']['raw_10k']
        output_dir = Path(output_dir)

        # Load firm list
        logger.info("Loading firm-year list...")
        firm_years = load_firm_list(
            config,
            start_index=args.start_index,
            batch_size=args.batch_size
        )

        # Initialize downloader
        # Handle both 'sec' and 'sec_edgar' config keys
        sec_config = config.get('sec_edgar', config.get('sec', {}))
        user_agent = sec_config['user_agent']
        rate_limit = 1.0 / sec_config['rate_limit']  # Convert from req/sec to sec/req

        logger.info("Initializing SEC downloader...")
        downloader = SECDownloader(
            user_agent=user_agent,
            output_dir=str(output_dir),
            rate_limit=rate_limit,
            max_retries=sec_config.get('max_retries', config.get('max_retries', 3))
        )

        # Download files
        logger.info(f"Starting download of {len(firm_years)} 10-K filings...")
        print(f"\nDownloading {len(firm_years)} 10-K filings to {output_dir}")
        print(f"Rate limit: {sec_config['rate_limit']} requests/second")
        print(f"Skip existing: {args.skip_existing}\n")

        results = downloader.download_batch(
            firm_years=firm_years,
            skip_if_exists=args.skip_existing,
            progress_callback=progress_callback
        )

        print("\n")  # New line after progress

        # Close downloader
        downloader.close()

        # Save results
        logger.info("Saving download results...")
        save_results(results, output_dir, timestamp)

        # Print summary
        print("\n" + "=" * 70)
        print("Download Complete!")
        print("=" * 70)
        print(f"Total attempted: {len(firm_years)}")
        print(f"Successful: {len(results['successful'])}")
        print(f"Failed: {len(results['failed'])}")
        print(f"Skipped: {len(results['skipped'])}")

        if results['failed']:
            success_total = len(results['successful']) + len(results['failed'])
            success_rate = len(results['successful']) / max(1, success_total) * 100
            print(f"Success rate: {success_rate:.2f}%")

        print(f"\nLog file: {log_file}")
        print("=" * 70 + "\n")

        # Return exit code
        if results['failed']:
            logger.warning(f"{len(results['failed'])} downloads failed. See logs for details.")
            return 1
        else:
            logger.info("All downloads completed successfully!")
            return 0

    except Exception as e:
        logger.error(f"Fatal error in download process: {e}", exc_info=True)
        print(f"\nERROR: {e}")
        print(f"See log file for details: {log_file}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
