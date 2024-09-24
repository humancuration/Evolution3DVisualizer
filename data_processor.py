# data_processor.py

import pandas as pd
from util_math import calculate_genetic_distance

def process_data(raw_data):
    """
    Processes raw genetic and taxonomic data.

    Parameters:
        raw_data (list of dict): Raw data entries.

    Returns:
        dict: Processed data with computed genetic distances.
    """
    # Convert raw data to DataFrame for easier manipulation
    df = pd.DataFrame(raw_data)
    
    # Example: Calculate genetic distance matrix
    # Assuming raw_data has 'species' and 'genetic_marker' columns
    species = df['species'].unique()
    distance_matrix = {}
    
    for sp1 in species:
        distance_matrix[sp1] = {}
        markers1 = df[df['species'] == sp1]['genetic_marker'].tolist()
        for sp2 in species:
            markers2 = df[df['species'] == sp2]['genetic_marker'].tolist()
            distance = calculate_genetic_distance(markers1, markers2)
            distance_matrix[sp1][sp2] = distance
    
    processed_data = {
        'species': species,
        'distance_matrix': distance_matrix,
        'raw_dataframe': df
    }
    
    return processed_data
