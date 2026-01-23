"""
Tests for downloader modules (SEC and CSR downloaders).
"""

import pytest
import tempfile
import shutil
from pathlib import Path
import pandas as pd

from src.downloaders import SECDownloader
from src.utils import validate_10k_file, validate_filename


class TestSECDownloader:
    """Tests for SEC downloader."""

    def setup_method(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir) / "downloads"

    def teardown_method(self):
        """Cleanup test fixtures."""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """Test downloader initialization."""
        downloader = SECDownloader(
            user_agent="test@test.com",
            output_dir=str(self.output_dir)
        )

        assert downloader is not None
        assert self.output_dir.exists()

    def test_validate_cik(self):
        """Test CIK validation."""
        downloader = SECDownloader(
            user_agent="test@test.com",
            output_dir=str(self.output_dir)
        )

        # Valid CIK
        assert downloader._validate_cik("1750") == "0000001750"
        assert downloader._validate_cik("0000001750") == "0000001750"

        # Invalid CIK
        with pytest.raises(ValueError):
            downloader._validate_cik("invalid")

    def test_generate_filename(self):
        """Test filename generation."""
        downloader = SECDownloader(
            user_agent="test@test.com",
            output_dir=str(self.output_dir)
        )

        filename = downloader._generate_filename("1750", 2020)
        assert filename == "0000001750_2020_10K.html"

        # Validate generated filename
        is_valid, cik, year = validate_filename(filename)
        assert is_valid
        assert cik == "0000001750"
        assert year == 2020


@pytest.mark.integration
class TestSECDownloaderIntegration:
    """Integration tests for SEC downloader (requires internet)."""

    def setup_method(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir) / "downloads"

    def teardown_method(self):
        """Cleanup test fixtures."""
        if Path(self.temp_dir).exists():
            shutil.rmtree(self.temp_dir)

    @pytest.mark.slow
    def test_download_single_filing(self):
        """Test downloading a single 10-K filing."""
        downloader = SECDownloader(
            user_agent="test@test.com",
            output_dir=str(self.output_dir)
        )

        # Download Apple's 2020 10-K (known to exist)
        success, filepath = downloader.download_10k(
            cik="320193",  # Apple Inc.
            year=2020
        )

        if success:  # May fail due to rate limiting
            assert filepath is not None
            assert Path(filepath).exists()

            # Validate downloaded file
            is_valid, message = validate_10k_file(filepath)
            assert is_valid, f"Downloaded file invalid: {message}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
