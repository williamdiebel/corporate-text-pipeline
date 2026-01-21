"""
Downloaders module for SEC EDGAR and CSR reports.

This module contains classes for downloading corporate filings and reports.
"""

from .sec_downloader import SECDownloader

__all__ = ['SECDownloader']
