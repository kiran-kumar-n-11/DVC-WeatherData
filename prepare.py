import pandas as pd
import numpy as np
import os

def get_filepaths(root_location,year):

    csv_file_paths = []

    directory = f"{root_location}/Data/{year}/"

    for file in os.listdir(directory):
        # Check if the file is a CSV file
        if file.endswith('.csv'):
            # Construct the full path to the CSV file
            file_path = os.path.join(directory, file)
            # Append the file path to the list
            csv_file_paths.append(file_path)
    
    return csv_file_paths

def prepare(file_paths):
    pass
