# util_math.py

def calculate_genetic_distance(markers1, markers2):
    """
    Calculates the average genetic distance between two species based on genetic markers.

    Parameters:
        markers1 (list of str): Genetic markers for species 1.
        markers2 (list of str): Genetic markers for species 2.

    Returns:
        float: Average genetic distance.
    """
    if not markers1 or not markers2:
        return float('inf')  # Handle cases with missing data
    
    distances = []
    for m1 in markers1:
        for m2 in markers2:
            distance = hamming_distance(m1, m2)
            if distance != -1:
                distances.append(distance)
    
    average_distance = sum(distances) / len(distances) if distances else float('inf')
    return average_distance

def hamming_distance(s1, s2):
    """
    Calculates the Hamming distance between two strings.

    Parameters:
        s1 (str): First string.
        s2 (str): Second string.

    Returns:
        int: Hamming distance or -1 if strings are of unequal length.
    """
    if len(s1) != len(s2):
        return -1  # Undefined for unequal lengths
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))
