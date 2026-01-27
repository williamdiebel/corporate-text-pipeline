"""
SEC EDGAR 10-K Downloader

This module handles downloading 10-K filings from the SEC EDGAR database.
It respects SEC rate limits, handles retries, and saves raw HTML files.

Key Features:
- Rate limiting (10 requests/second per SEC guidelines)
- Retry logic with exponential backoff
- CIK validation and zero-padding
- Progress tracking and logging
- Graceful error handling

Author: Corporate Text Pipeline Team
Date: 2026-01-21
"""

import os
import time
import logging
import requests
import pandas as pd
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from datetime import datetime
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)


class SECDownloader:
    """
    Downloads 10-K filings from SEC EDGAR database.

    Attributes:
        user_agent (str): User agent string with email (required by SEC)
        rate_limit (float): Seconds between requests (default: 0.1 for 10 req/sec)
        max_retries (int): Maximum number of retry attempts
        output_dir (Path): Directory to save downloaded files
        session (requests.Session): Persistent HTTP session
    """

    # SEC EDGAR API endpoints
    EDGAR_SEARCH_API = "https://www.sec.gov/cgi-bin/browse-edgar"
    EDGAR_ARCHIVES = "https://www.sec.gov/Archives/edgar/data"

    def __init__(
        self,
        user_agent: str,
        output_dir: str = "data/raw/10k",
        rate_limit: float = 0.1,
        max_retries: int = 3
    ):
        """
        Initialize SEC downloader.

        Args:
            user_agent: User agent string with email (e.g., "Name email@domain.com")
            output_dir: Directory to save downloaded 10-K files
            rate_limit: Minimum seconds between requests (default 0.1 = 10 req/sec)
            max_retries: Maximum retry attempts for failed downloads
        """
        self.user_agent = user_agent
        self.rate_limit = rate_limit
        self.max_retries = max_retries
        self.output_dir = Path(output_dir)

        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize session with headers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': self.user_agent,
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'www.sec.gov'
        })

        # Track last request time for rate limiting
        self._last_request_time = 0

        logger.info(f"SECDownloader initialized with output directory: {self.output_dir}")

    def _enforce_rate_limit(self):
        """Enforce rate limit between requests."""
        elapsed = time.time() - self._last_request_time
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self._last_request_time = time.time()

    @staticmethod
    def _format_cik(cik: str) -> str:
        """
        Format CIK with zero-padding to 10 digits.

        Args:
            cik: Central Index Key (can be string or int)

        Returns:
            Zero-padded 10-digit CIK string
        """
        return str(cik).zfill(10)

    def _get_filing_url(self, cik: str, accession_number: str) -> str:
        """
        Construct URL for downloading 10-K filing.

        Args:
            cik: Central Index Key
            accession_number: SEC accession number (e.g., "0000950170-20-000082")

        Returns:
            Full URL to the filing document
        """
        # Remove dashes from accession number for URL path
        accession_clean = accession_number.replace("-", "")

        # Construct URL: https://www.sec.gov/Archives/edgar/data/{CIK}/{ACCESSION}/{ACCESSION}.txt
        url = f"{self.EDGAR_ARCHIVES}/{cik}/{accession_clean}/{accession_number}.txt"
        return url

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((requests.RequestException, requests.Timeout))
    )
    def _search_filing(self, cik: str, year: int, form_type: str = "10-K") -> Optional[Dict]:
        """
        Search for a specific 10-K filing by CIK and year.

        Args:
            cik: Central Index Key
            year: Fiscal year of the filing
            form_type: Type of form to search (default: "10-K")

        Returns:
            Dictionary with filing metadata (accession_number, filing_date, document_url)
            or None if not found
        """
        self._enforce_rate_limit()

        cik_formatted = self._format_cik(cik)

        # SEC EDGAR search parameters
        params = {
            'action': 'getcompany',
            'CIK': cik_formatted,
            'type': form_type,
            'dateb': f"{year}1231",  # Search up to Dec 31 of target year
            'owner': 'exclude',
            'count': 100,  # Get up to 100 results
            'output': 'atom'  # XML format for easier parsing
        }

        try:
            response = self.session.get(self.EDGAR_SEARCH_API, params=params, timeout=30)
            response.raise_for_status()

            # Parse the XML response to find matching filing
            # For simplicity, we'll use a different approach: JSON API
            # Let's use the newer JSON API instead

        except requests.RequestException as e:
            logger.error(f"Error searching for CIK {cik} year {year}: {e}")
            raise

        # Alternative: Use the company facts API or submissions API
        # For now, return None and we'll use the sec-edgar-downloader library approach
        return None

    def download_10k(
        self,
        cik: str,
        year: int,
        skip_if_exists: bool = True
    ) -> Tuple[bool, Optional[str]]:
        """
        Download a single 10-K filing.

        Args:
            cik: Central Index Key
            year: Fiscal year of the filing
            skip_if_exists: Skip download if file already exists

        Returns:
            Tuple of (success: bool, file_path: Optional[str])
        """
        cik_formatted = self._format_cik(cik)

        # Define output filename
        filename = f"{cik_formatted}_{year}_10K.html"
        filepath = self.output_dir / filename

        # Check if file already exists
        if skip_if_exists and filepath.exists():
            logger.info(f"File already exists, skipping: {filename}")
            return True, str(filepath)

        try:
            # Use sec-edgar-downloader library for robust downloading
            from sec_edgar_downloader import Downloader
            import shutil
            import glob

            # Initialize downloader - saves to sec-edgar-filings/ in specified root
            # Use the data root (parent of raw/) as the download root
            download_root = self.output_dir.parent.parent
            dl = Downloader(download_root, self.user_agent.split()[-1])

            # Download the 10-K filing
            self._enforce_rate_limit()

            num_downloaded = dl.get("10-K", cik_formatted, after=f"{year}-01-01", before=f"{year}-12-31")

            if num_downloaded > 0:
                # Find the downloaded file in sec-edgar-filings structure
                # Structure: sec-edgar-filings/{CIK}/10-K/{accession}/full-submission.txt
                # Check both download_root and current working directory (library behavior varies)
                possible_roots = [download_root, Path.cwd()]
                sec_edgar_dir = None

                for root in possible_roots:
                    candidate = root / "sec-edgar-filings" / cik_formatted / "10-K"
                    if candidate.exists():
                        sec_edgar_dir = candidate
                        break

                if sec_edgar_dir and sec_edgar_dir.exists():
                    # Find the most recent filing for the target year
                    downloaded_file = None
                    for accession_dir in sorted(sec_edgar_dir.iterdir(), reverse=True):
                        if accession_dir.is_dir():
                            # Extract year from accession number (format: 0000850209-17-000025)
                            accession_name = accession_dir.name
                            parts = accession_name.split('-')
                            if len(parts) >= 2:
                                year_short = parts[1]
                                # Handle both 2-digit (17) and 4-digit years
                                if len(year_short) == 2:
                                    accession_year = int("20" + year_short) if int(year_short) < 50 else int("19" + year_short)
                                else:
                                    accession_year = int(year_short)

                                if accession_year == year:
                                    submission_file = accession_dir / "full-submission.txt"
                                    if submission_file.exists():
                                        downloaded_file = submission_file
                                        break

                    if downloaded_file:
                        # Copy to our standardized location
                        shutil.copy2(downloaded_file, filepath)
                        logger.info(f"Successfully downloaded and moved 10-K for CIK {cik_formatted}, year {year}")
                        return True, str(filepath)
                    else:
                        logger.warning(f"Downloaded but could not find matching file for year {year}")
                        return False, None
                else:
                    # Log where we looked for debugging
                    searched_paths = [str(root / "sec-edgar-filings" / cik_formatted / "10-K") for root in possible_roots]
                    logger.warning(f"sec-edgar-filings directory not found for CIK {cik_formatted}. Searched: {searched_paths}")
                    return False, None
            else:
                logger.warning(f"No 10-K found for CIK {cik_formatted}, year {year}")
                return False, None

        except Exception as e:
            logger.error(f"Error downloading 10-K for CIK {cik}, year {year}: {e}")
            return False, None

    def download_batch(
        self,
        firm_years: pd.DataFrame,
        skip_if_exists: bool = True,
        progress_callback: Optional[callable] = None
    ) -> Dict[str, List]:
        """
        Download a batch of 10-K filings.

        Args:
            firm_years: DataFrame with 'cik' and 'year' columns
            skip_if_exists: Skip files that already exist
            progress_callback: Optional callback function for progress updates

        Returns:
            Dictionary with 'successful', 'failed', and 'skipped' lists
        """
        results = {
            'successful': [],
            'failed': [],
            'skipped': []
        }

        total = len(firm_years)
        logger.info(f"Starting batch download of {total} firm-year combinations")

        for idx, row in firm_years.iterrows():
            cik = row['cik']
            year = row['year']

            try:
                success, filepath = self.download_10k(cik, year, skip_if_exists)

                if success:
                    if filepath and skip_if_exists and Path(filepath).exists():
                        results['skipped'].append({'cik': cik, 'year': year, 'path': filepath})
                    else:
                        results['successful'].append({'cik': cik, 'year': year, 'path': filepath})
                else:
                    results['failed'].append({'cik': cik, 'year': year, 'error': 'Not found'})

                # Call progress callback if provided
                if progress_callback:
                    progress_callback(idx + 1, total, results)

            except Exception as e:
                logger.error(f"Unexpected error processing CIK {cik}, year {year}: {e}")
                results['failed'].append({'cik': cik, 'year': year, 'error': str(e)})

        logger.info(f"Batch download complete. Successful: {len(results['successful'])}, "
                   f"Failed: {len(results['failed'])}, Skipped: {len(results['skipped'])}")

        return results

    def validate_downloads(self, firm_years: pd.DataFrame) -> pd.DataFrame:
        """
        Validate that all expected files exist and are non-empty.

        Args:
            firm_years: DataFrame with 'cik' and 'year' columns

        Returns:
            DataFrame with validation results
        """
        validation_results = []

        for idx, row in firm_years.iterrows():
            cik = self._format_cik(row['cik'])
            year = row['year']

            filename = f"{cik}_{year}_10K.html"
            filepath = self.output_dir / filename

            result = {
                'cik': cik,
                'year': year,
                'filename': filename,
                'exists': filepath.exists(),
                'file_size': filepath.stat().st_size if filepath.exists() else 0,
                'is_valid': False
            }

            # File is valid if it exists and is larger than 1KB
            if result['exists'] and result['file_size'] > 1024:
                result['is_valid'] = True

            validation_results.append(result)

        df_results = pd.DataFrame(validation_results)

        # Log validation summary
        total = len(df_results)
        valid = df_results['is_valid'].sum()
        missing = (~df_results['exists']).sum()

        logger.info(f"Validation complete: {valid}/{total} valid files, {missing} missing")

        return df_results

    def close(self):
        """Close the session."""
        self.session.close()
        logger.info("SECDownloader session closed")
