import os
import pandas as pd

def compile_csv_to_excel(input_folder, output_file):
    """
    Compiles all .csv files in a folder into a single .xlsx workbook.
    Each .csv file becomes a separate tab in the workbook.

    Args:
    - input_folder (str): Path to the folder containing the .csv files.
    - output_file (str): Path to the output .xlsx file.
    """
    # Check if the input folder exists
    if not os.path.exists(input_folder):
        raise FileNotFoundError(f"The folder '{input_folder}' does not exist.")
    
    # Create a Pandas Excel writer using openpyxl
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Loop through all files in the input folder
        for filename in os.listdir(input_folder):
            # Process only .csv files
            if filename.endswith('.csv'):
                file_path = os.path.join(input_folder, filename)
                
                # Read the CSV file into a DataFrame
                try:
                    df = pd.read_csv(file_path)
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
                    continue
                
                # Remove the file extension for the sheet name
                sheet_name = os.path.splitext(filename)[0][:31]  # Excel sheet names are limited to 31 chars
                
                # Write the DataFrame to a new sheet in the workbook
                df.to_excel(writer, index=False, sheet_name=sheet_name)
                print(f"Added '{filename}' as sheet '{sheet_name}'")
    
    print(f"All .csv files have been compiled into '{output_file}'")

# Example usage
input_folder = "../csv"  # Replace with your folder path
output_file = "../workbooks/survey_analysis.xlsx"  # Replace with desired output file name
compile_csv_to_excel(input_folder, output_file)