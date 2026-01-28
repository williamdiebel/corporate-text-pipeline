"""
Configuration loader for the corporate text pipeline.

This module loads settings from config.yaml and environment variables,
making them available throughout the project.
"""

import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get project root directory (where config.yaml lives)
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_PATH = PROJECT_ROOT / "config.yaml"


def load_config(config_path=None):
    """
    Load configuration from config.yaml file.

    Args:
        config_path (str, optional): Path to config file. Defaults to config.yaml in project root.

    Returns:
        dict: Configuration dictionary with all settings
    """
    if config_path is None:
        config_path = CONFIG_PATH
    else:
        config_path = Path(config_path)

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Add project root to config for easy path construction
    config['project_root'] = str(PROJECT_ROOT)

    # Resolve data_root - priority: environment variable > config file > default
    data_root = os.getenv('DATA_ROOT') or config.get('data_root')
    if data_root:
        data_root = Path(data_root).expanduser().resolve()
    else:
        data_root = PROJECT_ROOT / 'data'

    config['data_root'] = str(data_root)

    # Get collaborator name for per-person folder structure
    collaborator = config.get('collaborator', '').lower()
    if collaborator:
        config['collaborator'] = collaborator
        # Each collaborator's data goes in their own subfolder
        collaborator_data_root = data_root / collaborator
    else:
        collaborator_data_root = data_root

    config['collaborator_data_root'] = str(collaborator_data_root)

    # Update paths to use collaborator's data root
    if 'paths' in config:
        for key, value in config['paths'].items():
            if value.startswith('data/'):
                # Replace 'data/' prefix with collaborator's data root
                relative_path = value[5:]  # Remove 'data/' prefix
                config['paths'][key] = str(collaborator_data_root / relative_path)

    return config


def get_api_key(provider="claude"):
    """
    Get API key from environment variables.
    
    Args:
        provider (str): API provider - "claude" or "openai"
    
    Returns:
        str: API key or None if not found
    """
    if provider == "claude":
        return os.getenv("ANTHROPIC_API_KEY")
    elif provider == "openai":
        return os.getenv("OPENAI_API_KEY")
    else:
        raise ValueError(f"Unknown provider: {provider}")


def get_sec_user_agent():
    """
    Get SEC EDGAR user agent from environment.
    SEC requires a valid email in the user agent.
    
    Returns:
        str: User agent string
    """
    return os.getenv("SEC_USER_AGENT", "research@university.edu")


def load_firm_list():
    """
    Load the list of target firm-years from CSV.
    
    Returns:
        pandas.DataFrame: DataFrame with columns: CIK, Year
    """
    import pandas as pd
    
    firm_list_path = Path(CONFIG['project_root']) / CONFIG['firm_list_file']
    
    if not firm_list_path.exists():
        raise FileNotFoundError(
            f"Firm list not found at {firm_list_path}. "
            f"Please create target_firm_years.csv with columns: cik, year"
        )
    
    df = pd.read_csv(firm_list_path)
    
    # Standardize column names (in case they're capitalized differently)
    df.columns = df.columns.str.lower()
    
    # Ensure CIK is properly formatted (10 digits with leading zeros)
    df['cik'] = df['cik'].astype(int).astype(str).str.zfill(10)
    df['year'] = df['year'].astype(int)
    
    # Rename to uppercase for consistency
    df = df.rename(columns={'cik': 'CIK', 'year': 'Year'})
    
    print(f"Loaded {len(df)} firm-year observations")
    print(f"  - Unique firms: {df['CIK'].nunique()}")
    print(f"  - Year range: {df['Year'].min()}-{df['Year'].max()}")
    
    return df


# Load config when module is imported
CONFIG = load_config()


# Example usage (for testing):
if __name__ == "__main__":
    print("Configuration loaded successfully!")
    print(f"Project: {CONFIG['project_name']}")
    print(f"Data period: {CONFIG['data_period']}")
    print(f"Project root: {CONFIG['project_root']}")
    
    # Test loading firm list
    print("\nTesting firm list loading:")
    df = load_firm_list()
    print(df.head())