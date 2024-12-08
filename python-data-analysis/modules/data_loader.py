import os
import pandas as pd

def load_dataset(file_path):
    """Load dataset with robust error handling."""
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        df = pd.read_csv(file_path)
        print(f"Dataset loaded successfully: {file_path}")
        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        raise
