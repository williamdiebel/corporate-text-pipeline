"""
Text Cleaner for 10-K Filings

Cleans and normalizes extracted text from 10-K sections.
Removes boilerplate, excessive whitespace, and formatting artifacts.
"""

import re
import logging
from typing import Optional, Dict
from pathlib import Path
import pandas as pd

logger = logging.getLogger(__name__)


class TextCleaner:
    """
    Clean and normalize text extracted from 10-K filings.

    Handles:
    - Whitespace normalization
    - Table of contents removal
    - Page headers/footers removal
    - HTML artifacts
    - Special characters
    - Excessive newlines
    """

    # Common boilerplate patterns to remove
    BOILERPLATE_PATTERNS = [
        r'table\s+of\s+contents',
        r'page\s+\d+\s+of\s+\d+',
        r'\d+\s*\n\s*table\s+of\s+contents',
        r'(?:exhibit|schedule)\s+index',
    ]

    # HTML artifacts
    HTML_PATTERNS = [
        r'&nbsp;?',
        r'&[a-z]+;',
        r'<[^>]+>',
    ]

    def __init__(
        self,
        remove_tables: bool = True,
        remove_headers: bool = True,
        normalize_whitespace: bool = True,
        min_word_length: int = 2,
        max_consecutive_newlines: int = 2
    ):
        """
        Initialize text cleaner.

        Args:
            remove_tables: Remove table-like structures
            remove_headers: Remove page headers/footers
            normalize_whitespace: Normalize whitespace and newlines
            min_word_length: Minimum word length to keep (filters noise)
            max_consecutive_newlines: Maximum consecutive newlines to keep
        """
        self.remove_tables = remove_tables
        self.remove_headers = remove_headers
        self.normalize_whitespace = normalize_whitespace
        self.min_word_length = min_word_length
        self.max_consecutive_newlines = max_consecutive_newlines

    def clean(self, text: str) -> str:
        """
        Clean text with all enabled cleaning steps.

        Args:
            text: Raw text to clean

        Returns:
            Cleaned text
        """
        if not text:
            return ""

        # Step 1: Remove HTML artifacts
        text = self._remove_html_artifacts(text)

        # Step 2: Remove boilerplate
        text = self._remove_boilerplate(text)

        # Step 3: Remove tables (if enabled)
        if self.remove_tables:
            text = self._remove_tables(text)

        # Step 4: Remove headers/footers (if enabled)
        if self.remove_headers:
            text = self._remove_headers_footers(text)

        # Step 5: Normalize whitespace (if enabled)
        if self.normalize_whitespace:
            text = self._normalize_whitespace(text)

        # Step 6: Remove very short "words" (likely artifacts)
        text = self._filter_short_words(text)

        # Step 7: Final cleanup
        text = text.strip()

        return text

    def _remove_html_artifacts(self, text: str) -> str:
        """Remove HTML tags and entities."""
        for pattern in self.HTML_PATTERNS:
            text = re.sub(pattern, ' ', text, flags=re.IGNORECASE)
        return text

    def _remove_boilerplate(self, text: str) -> str:
        """Remove common boilerplate text."""
        for pattern in self.BOILERPLATE_PATTERNS:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        return text

    def _remove_tables(self, text: str) -> str:
        """
        Remove table-like structures.

        Tables often contain financial data that's not relevant for
        narrative analysis of supply chain practices.
        """
        # Remove lines with excessive spacing (common in tables)
        lines = text.split('\n')
        cleaned_lines = []

        for line in lines:
            # Skip lines with lots of numbers and dots/spaces (table indicators)
            if re.search(r'(\d+\s+){3,}', line):
                continue
            if re.search(r'(\.{3,}|\s{3,})', line) and re.search(r'\d', line):
                continue
            # Skip lines with mostly punctuation
            if len(re.findall(r'[^\w\s]', line)) > len(line) * 0.4:
                continue

            cleaned_lines.append(line)

        return '\n'.join(cleaned_lines)

    def _remove_headers_footers(self, text: str) -> str:
        """
        Remove page headers and footers.

        Common patterns:
        - Page numbers
        - Company name repetition
        - Form 10-K headers
        """
        # Remove page numbers
        text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)

        # Remove "Form 10-K" repetitions
        text = re.sub(r'form\s+10-k', '', text, flags=re.IGNORECASE)

        # Remove lines that are just dates
        text = re.sub(r'^\s*(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},?\s+\d{4}\s*$',
                     '', text, flags=re.MULTILINE | re.IGNORECASE)

        return text

    def _normalize_whitespace(self, text: str) -> str:
        """
        Normalize whitespace and newlines.

        - Replace multiple spaces with single space
        - Replace excessive newlines
        - Remove leading/trailing whitespace on lines
        """
        # Replace tabs with spaces
        text = text.replace('\t', ' ')

        # Replace multiple spaces with single space
        text = re.sub(r' {2,}', ' ', text)

        # Remove leading/trailing whitespace on each line
        lines = [line.strip() for line in text.split('\n')]

        # Remove empty lines and limit consecutive newlines
        cleaned_lines = []
        consecutive_empty = 0

        for line in lines:
            if line:
                cleaned_lines.append(line)
                consecutive_empty = 0
            else:
                consecutive_empty += 1
                if consecutive_empty <= self.max_consecutive_newlines:
                    cleaned_lines.append(line)

        return '\n'.join(cleaned_lines)

    def _filter_short_words(self, text: str) -> str:
        """
        Remove very short words that are likely artifacts.

        Preserves short words that are common in English (a, I, is, to, etc.)
        """
        # Common short words to preserve
        preserve = {'a', 'i', 'is', 'it', 'to', 'or', 'of', 'in', 'at', 'by', 'on', 'if', 'no', 'we', 'us'}

        words = text.split()
        filtered_words = []

        for word in words:
            # Keep if longer than min_word_length or in preserve set
            if len(word) >= self.min_word_length or word.lower() in preserve:
                filtered_words.append(word)

        return ' '.join(filtered_words)

    def clean_file(self, input_path: str, output_path: str = None) -> str:
        """
        Clean a text file.

        Args:
            input_path: Path to input text file
            output_path: Path to save cleaned text (optional)

        Returns:
            Cleaned text
        """
        input_path = Path(input_path)

        try:
            with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()

            cleaned = self.clean(text)

            if output_path:
                output_path = Path(output_path)
                output_path.parent.mkdir(parents=True, exist_ok=True)

                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned)

                logger.info(f"Cleaned text saved to {output_path}")

            return cleaned

        except Exception as e:
            logger.error(f"Error cleaning file {input_path}: {e}")
            return ""

    def clean_batch(self, input_files: list, output_dir: str = None) -> pd.DataFrame:
        """
        Clean multiple text files in batch.

        Args:
            input_files: List of input file paths
            output_dir: Directory to save cleaned files (optional)

        Returns:
            DataFrame with cleaning statistics
        """
        results = []

        for input_file in input_files:
            input_path = Path(input_file)
            logger.info(f"Cleaning {input_path.name}...")

            # Determine output path
            if output_dir:
                output_path = Path(output_dir) / input_path.name
            else:
                output_path = None

            # Clean file
            try:
                with open(input_path, 'r', encoding='utf-8', errors='ignore') as f:
                    original_text = f.read()

                cleaned_text = self.clean(original_text)

                # Save if output_dir provided
                if output_path:
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(cleaned_text)

                # Calculate statistics
                results.append({
                    'filename': input_path.name,
                    'original_length': len(original_text),
                    'cleaned_length': len(cleaned_text),
                    'reduction_pct': (1 - len(cleaned_text) / len(original_text)) * 100 if original_text else 0,
                    'original_words': len(original_text.split()),
                    'cleaned_words': len(cleaned_text.split()),
                    'success': True
                })

            except Exception as e:
                logger.error(f"Error cleaning {input_path}: {e}")
                results.append({
                    'filename': input_path.name,
                    'original_length': 0,
                    'cleaned_length': 0,
                    'reduction_pct': 0,
                    'original_words': 0,
                    'cleaned_words': 0,
                    'success': False
                })

        return pd.DataFrame(results)


def clean_text(text: str, aggressive: bool = False) -> str:
    """
    Convenience function to clean text with default settings.

    Args:
        text: Text to clean
        aggressive: If True, use more aggressive cleaning

    Returns:
        Cleaned text
    """
    if aggressive:
        cleaner = TextCleaner(
            remove_tables=True,
            remove_headers=True,
            normalize_whitespace=True,
            min_word_length=3,
            max_consecutive_newlines=1
        )
    else:
        cleaner = TextCleaner()

    return cleaner.clean(text)


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        print(f"Cleaning {input_file}...")

        cleaner = TextCleaner()
        cleaned = cleaner.clean_file(input_file, output_file)

        print(f"\nCleaning Results:")
        print(f"Output length: {len(cleaned):,} characters")
        print(f"Word count: {len(cleaned.split()):,} words")

        if output_file:
            print(f"Saved to: {output_file}")
        else:
            print("\nCleaned text preview:")
            print("-" * 50)
            print(cleaned[:500])
    else:
        print("Usage: python text_cleaner.py <input_file> [output_file]")
