"""
10-K Filing Parser

Extracts specific sections (Items 1, 1A, and 7) from 10-K HTML filings.
Uses regex patterns and BeautifulSoup to identify and extract sections.

The parser handles various 10-K formats and HTML structures from different years.
"""

import re
import logging
from pathlib import Path
from typing import Dict, Optional, Tuple
from bs4 import BeautifulSoup
import pandas as pd

logger = logging.getLogger(__name__)


class TenKParser:
    """
    Parser for extracting specific sections from 10-K filings.

    Extracts:
    - Item 1: Business Description
    - Item 1A: Risk Factors
    - Item 7: Management's Discussion and Analysis (MD&A)
    """

    # Section patterns for different 10-K formats
    SECTION_PATTERNS = {
        'item_1': [
            r'(?:item\s*1[\.\:\s]+|item\s*1\s*\-\s*)(?:business|description\s+of\s+business)',
            r'>item\s*1[\.\:\s]',
            r'item\s*1\s*business'
        ],
        'item_1a': [
            r'(?:item\s*1a[\.\:\s]+|item\s*1a\s*\-\s*)(?:risk\s*factors?)',
            r'>item\s*1a[\.\:\s]',
            r'item\s*1a\s*risk'
        ],
        'item_7': [
            r'(?:item\s*7[\.\:\s]+|item\s*7\s*\-\s*)(?:management|md&a|discussion)',
            r'>item\s*7[\.\:\s]',
            r'item\s*7\s*management'
        ]
    }

    # Section end patterns (to know where each section stops)
    SECTION_END_PATTERNS = {
        'item_1': [r'item\s*1a', r'item\s*2'],
        'item_1a': [r'item\s*1b', r'item\s*2'],
        'item_7': [r'item\s*7a', r'item\s*8']
    }

    def __init__(self, min_section_length: int = 1000):
        """
        Initialize parser.

        Args:
            min_section_length: Minimum character length for valid section (default: 1000)
        """
        self.min_section_length = min_section_length

    def parse_file(self, filepath: str) -> Dict[str, Optional[str]]:
        """
        Parse a 10-K HTML file and extract all sections.

        Args:
            filepath: Path to 10-K HTML file

        Returns:
            Dictionary with keys: item_1, item_1a, item_7
            Values are extracted text or None if not found
        """
        filepath = Path(filepath)

        if not filepath.exists():
            logger.error(f"File not found: {filepath}")
            return {'item_1': None, 'item_1a': None, 'item_7': None}

        try:
            # Read and parse HTML
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                html_content = f.read()

            soup = BeautifulSoup(html_content, 'lxml')

            # Get text content
            text = soup.get_text(separator='\n')

            # Extract each section
            results = {}
            for section_name in ['item_1', 'item_1a', 'item_7']:
                results[section_name] = self._extract_section(text, section_name)

                if results[section_name]:
                    logger.info(f"Extracted {section_name}: {len(results[section_name])} characters")
                else:
                    logger.warning(f"Could not extract {section_name} from {filepath.name}")

            return results

        except Exception as e:
            logger.error(f"Error parsing {filepath}: {e}", exc_info=True)
            return {'item_1': None, 'item_1a': None, 'item_7': None}

    def _extract_section(self, text: str, section_name: str) -> Optional[str]:
        """
        Extract a specific section from 10-K text.

        Args:
            text: Full 10-K text
            section_name: Section to extract ('item_1', 'item_1a', 'item_7')

        Returns:
            Extracted section text or None if not found
        """
        text_lower = text.lower()

        # Find section start
        start_pos = None
        for pattern in self.SECTION_PATTERNS[section_name]:
            match = re.search(pattern, text_lower, re.IGNORECASE)
            if match:
                start_pos = match.end()
                break

        if start_pos is None:
            logger.debug(f"Could not find start of {section_name}")
            return None

        # Find section end
        end_pos = len(text)
        for pattern in self.SECTION_END_PATTERNS[section_name]:
            match = re.search(pattern, text_lower[start_pos:], re.IGNORECASE)
            if match:
                end_pos = start_pos + match.start()
                break

        # Extract section text
        section_text = text[start_pos:end_pos]

        # Validate minimum length
        if len(section_text) < self.min_section_length:
            logger.debug(f"{section_name} too short: {len(section_text)} characters")
            return None

        return section_text.strip()

    def parse_batch(self, filepaths: list, output_dir: str = None) -> pd.DataFrame:
        """
        Parse multiple 10-K files in batch.

        Args:
            filepaths: List of file paths to parse
            output_dir: Optional directory to save extracted sections

        Returns:
            DataFrame with columns: filepath, item_1_length, item_1a_length, item_7_length, success
        """
        results = []

        for filepath in filepaths:
            filepath = Path(filepath)
            logger.info(f"Parsing {filepath.name}...")

            sections = self.parse_file(filepath)

            # Save extracted sections if output_dir provided
            if output_dir and any(sections.values()):
                self._save_sections(filepath, sections, output_dir)

            # Record results
            results.append({
                'filepath': str(filepath),
                'filename': filepath.name,
                'item_1_length': len(sections['item_1']) if sections['item_1'] else 0,
                'item_1a_length': len(sections['item_1a']) if sections['item_1a'] else 0,
                'item_7_length': len(sections['item_7']) if sections['item_7'] else 0,
                'item_1_success': sections['item_1'] is not None,
                'item_1a_success': sections['item_1a'] is not None,
                'item_7_success': sections['item_7'] is not None,
                'all_sections_extracted': all(sections.values())
            })

        return pd.DataFrame(results)

    def _save_sections(self, filepath: Path, sections: Dict[str, Optional[str]], output_dir: str):
        """
        Save extracted sections to individual text files.

        Args:
            filepath: Original 10-K filepath
            sections: Dictionary of extracted sections
            output_dir: Directory to save sections
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Create filename base from original (e.g., 0000001750_2020_10K)
        base_name = filepath.stem

        for section_name, text in sections.items():
            if text:
                output_file = output_dir / f"{base_name}_{section_name}.txt"
                try:
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write(text)
                    logger.debug(f"Saved {section_name} to {output_file}")
                except Exception as e:
                    logger.error(f"Error saving {section_name} to {output_file}: {e}")


def extract_metadata_from_filename(filename: str) -> Tuple[Optional[str], Optional[int]]:
    """
    Extract CIK and year from standardized filename.

    Args:
        filename: Filename in format {CIK}_{YEAR}_10K.html

    Returns:
        Tuple of (cik, year) or (None, None) if parsing fails
    """
    pattern = r'(\d{10})_(\d{4})_10K'
    match = re.search(pattern, filename)

    if match:
        cik = match.group(1)
        year = int(match.group(2))
        return cik, year

    return None, None


# Convenience function for single file parsing
def parse_10k(filepath: str, min_section_length: int = 1000) -> Dict[str, Optional[str]]:
    """
    Parse a single 10-K file and extract sections.

    Args:
        filepath: Path to 10-K HTML file
        min_section_length: Minimum section length in characters

    Returns:
        Dictionary with extracted sections
    """
    parser = TenKParser(min_section_length=min_section_length)
    return parser.parse_file(filepath)


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) > 1:
        filepath = sys.argv[1]

        # Setup basic logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        print(f"Parsing {filepath}...")
        sections = parse_10k(filepath)

        print("\nExtraction Results:")
        print("-" * 50)
        for section_name, text in sections.items():
            if text:
                print(f"{section_name}: {len(text):,} characters")
                print(f"Preview: {text[:200]}...")
                print()
            else:
                print(f"{section_name}: NOT FOUND")
                print()
    else:
        print("Usage: python parser.py <path_to_10k_file.html>")
