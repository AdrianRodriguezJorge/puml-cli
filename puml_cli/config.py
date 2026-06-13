import os
import json

# Default configuration settings
DEFAULT_CONFIG = {
    "jar_path": "",
    "enable_theme_selection": False,
    "enable_dpi_selection": False,
    "default_dpi": 600,
    "default_theme": None,
    "language": "en"
}

def load_config(config_path="config.json"):
    """
    Load the JSON configuration file and merge it with DEFAULT_CONFIG
    to ensure all default options are present.
    """
    config = DEFAULT_CONFIG.copy()
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                config.update(loaded)
        except Exception:
            pass  # Fall back to default config if reading fails
    return config

def save_config(config, config_path="config.json"):
    """
    Save the given configuration dictionary to config.json.
    """
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception:
        return False
