"""
Tests for utility modules (validators and logging).
"""

import pytest
import pandas as pd
import tempfile
from pathlib import Path

from src.utils import (
    validate_cik,
    validate_year,
    validate_filename,
    validate_firm_list,
    validate_extracted_text
)


class TestValidators:
    """Tests for validation functions."""

    def test_validate_cik(self):
        """Test CIK validation."""
        # Valid CIKs
        is_valid, formatted = validate_cik("1750")
        assert is_valid
        assert formatted == "0000001750"

        is_valid, formatted = validate_cik("0000320193")
        assert is_valid
        assert formatted == "0000320193"

        # Invalid CIKs
        is_valid, formatted = validate_cik("invalid")
        assert not is_valid
        assert formatted is None

        is_valid, formatted = validate_cik("12345678901")  # Too long
        assert not is_valid

    def test_validate_year(self):
        """Test year validation."""
        assert validate_year(2020) is True
        assert validate_year(1994) is True  # SEC EDGAR start year
        assert validate_year(1990) is False  # Before SEC EDGAR
        assert validate_year(2050) is False  # Too far in future
        assert validate_year("invalid") is False

    def test_validate_filename(self):
        """Test filename validation."""
        # Valid filename
        is_valid, cik, year = validate_filename("0000001750_2020_10K.html")
        assert is_valid
        assert cik == "0000001750"
        assert year == 2020

        # Invalid filename
        is_valid, cik, year = validate_filename("invalid.html")
        assert not is_valid
        assert cik is None
        assert year is None

    def test_validate_firm_list(self):
        """Test firm list validation."""
        # Valid firm list
        df = pd.DataFrame({
            'cik': ['1750', '320193'],
            'year': [2020, 2021]
        })

        is_valid, errors = validate_firm_list(df)
        assert is_valid
        assert len(errors) == 0

        # Invalid firm list (missing column)
        df_invalid = pd.DataFrame({
            'cik': ['1750'],
            'wrong_column': [2020]
        })

        is_valid, errors = validate_firm_list(df_invalid)
        assert not is_valid
        assert len(errors) > 0

    def test_validate_extracted_text(self):
        """Test extracted text validation."""
        # Valid text
        text = "This is a valid text " * 100  # Make it long enough
        is_valid, message = validate_extracted_text(text)
        assert is_valid

        # Too short
        is_valid, message = validate_extracted_text("short")
        assert not is_valid
        assert "too short" in message.lower()

        # Empty
        is_valid, message = validate_extracted_text("")
        assert not is_valid


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
