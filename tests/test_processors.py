"""
Tests for processor modules (parser and text cleaner).
"""

import pytest
import tempfile
from pathlib import Path

from src.processors import TenKParser, TextCleaner, parse_10k, clean_text


class TestTenKParser:
    """Tests for 10-K parser."""

    def test_initialization(self):
        """Test parser initialization."""
        parser = TenKParser(min_section_length=500)
        assert parser.min_section_length == 500

    def test_extract_metadata(self):
        """Test metadata extraction from filename."""
        from src.processors import extract_metadata_from_filename

        cik, year = extract_metadata_from_filename("0000001750_2020_10K.html")
        assert cik == "0000001750"
        assert year == 2020

        # Invalid filename
        cik, year = extract_metadata_from_filename("invalid.html")
        assert cik is None
        assert year is None


class TestTextCleaner:
    """Tests for text cleaner."""

    def test_initialization(self):
        """Test cleaner initialization."""
        cleaner = TextCleaner(
            remove_tables=True,
            normalize_whitespace=True
        )
        assert cleaner.remove_tables is True
        assert cleaner.normalize_whitespace is True

    def test_remove_html_artifacts(self):
        """Test HTML artifact removal."""
        cleaner = TextCleaner()
        text = "Hello&nbsp;World &amp; More"
        cleaned = cleaner._remove_html_artifacts(text)
        assert "&nbsp;" not in cleaned
        assert "&amp;" not in cleaned

    def test_normalize_whitespace(self):
        """Test whitespace normalization."""
        cleaner = TextCleaner()
        text = "Hello    World\n\n\n\nTest"
        cleaned = cleaner._normalize_whitespace(text)
        assert "    " not in cleaned  # Multiple spaces removed
        lines = cleaned.split('\n')
        empty_count = sum(1 for line in lines if not line.strip())
        assert empty_count <= cleaner.max_consecutive_newlines

    def test_clean_text_convenience_function(self):
        """Test convenience clean_text function."""
        text = "Hello   World&nbsp;Test"
        cleaned = clean_text(text)
        assert len(cleaned) > 0
        assert "Hello" in cleaned


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
