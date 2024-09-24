# mod_data_loader.py

import csv
import json

def load_data(file_path):
    """
    Loads data from a CSV or JSON file.

    Parameters:
        file_path (str): Path to the data file.

    Returns:
        list of dict: List containing data entries.
    """
    data = []
    try:
        if file_path.endswith('.csv'):
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    data.append(row)
        elif file_path.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as jsonfile:
                data = json.load(jsonfile)
        else:
            raise ValueError("Unsupported file format. Use CSV or JSON.")
    except Exception as e:
        print(f"Error loading data: {e}")
    return data
