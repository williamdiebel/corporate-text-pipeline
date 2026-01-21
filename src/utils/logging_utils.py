"""
Logging utilities for the corporate text pipeline.

Provides centralized logging configuration with file and console output.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logging(
    log_file: str = None,
    level: str = "INFO",
    format_string: str = None,
    console_output: bool = True
):
    """
    Setup logging configuration for the application.

    Args:
        log_file: Path to log file (optional)
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        format_string: Custom format string (optional)
        console_output: Whether to output to console (default: True)

    Returns:
        logging.Logger: Configured root logger
    """
    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    # Default format string with timestamp, level, module, and message
    if format_string is None:
        format_string = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"

    # Date format
    date_format = "%Y-%m-%d %H:%M:%S"

    # Create formatter
    formatter = logging.Formatter(format_string, datefmt=date_format)

    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()

    # Add console handler if requested
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    # Add file handler if log_file specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

        root_logger.info(f"Logging initialized. Log file: {log_file}")

    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.

    Args:
        name: Name of the logger (typically __name__)

    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name)


class LoggerContext:
    """
    Context manager for temporary logging configuration.

    Usage:
        with LoggerContext(level='DEBUG'):
            # Code that needs debug logging
            pass
    """

    def __init__(self, level: str = None, log_file: str = None):
        """
        Initialize logger context.

        Args:
            level: Temporary logging level
            log_file: Temporary log file
        """
        self.level = level
        self.log_file = log_file
        self.original_level = None
        self.original_handlers = []

    def __enter__(self):
        """Enter context: save current config and apply temporary config."""
        root_logger = logging.getLogger()
        self.original_level = root_logger.level
        self.original_handlers = root_logger.handlers.copy()

        if self.level:
            numeric_level = getattr(logging, self.level.upper(), logging.INFO)
            root_logger.setLevel(numeric_level)

        if self.log_file:
            handler = logging.FileHandler(self.log_file, mode='a')
            handler.setFormatter(logging.Formatter(
                "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
            ))
            root_logger.addHandler(handler)

        return root_logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context: restore original config."""
        root_logger = logging.getLogger()
        root_logger.setLevel(self.original_level)
        root_logger.handlers = self.original_handlers


def log_exception(logger: logging.Logger, exception: Exception, context: str = ""):
    """
    Log an exception with full traceback.

    Args:
        logger: Logger instance
        exception: Exception to log
        context: Additional context string
    """
    if context:
        logger.error(f"{context}: {str(exception)}", exc_info=True)
    else:
        logger.error(f"Exception occurred: {str(exception)}", exc_info=True)


# Example usage
if __name__ == "__main__":
    # Test logging setup
    setup_logging(log_file="test.log", level="DEBUG")

    logger = get_logger(__name__)
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")

    # Test context manager
    with LoggerContext(level="WARNING"):
        logger.debug("This debug won't show")
        logger.warning("This warning will show")

    print("Logging test complete!")
