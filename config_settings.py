# config_settings.py

import json

def load_settings():
    """
    Loads configuration settings from a JSON file.

    Returns:
        dict: Configuration settings.
    """
    default_settings = {
        "data_file": "data_sample_dataset.csv",
        "visualization_params": {
            "background_color": "#FFFFFF",
            "node_color": "#FF5733",
            "edge_color": "#C70039",
            "node_size": 10,
            "edge_width": 1
        }
    }
    
    try:
        with open('config_settings.json', 'r', encoding='utf-8') as f:
            settings = json.load(f)
    except FileNotFoundError:
        settings = default_settings
        save_settings(settings)
    except json.JSONDecodeError:
        settings = default_settings
        save_settings(settings)
    
    return settings

def save_settings(settings):
    """
    Saves configuration settings to a JSON file.

    Parameters:
        settings (dict): Configuration settings.
    """
    with open('config_settings.json', 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=4)
