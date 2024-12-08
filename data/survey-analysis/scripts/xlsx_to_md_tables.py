import pandas as pd

def excel_to_markdown(excel_file, output_md_file):
    """
    Converts all sheets of an Excel file into a single Markdown document.

    Args:
    - excel_file (str): Path to the input Excel file.
    - output_md_file (str): Path to the output Markdown file.
    """
    # Read the Excel file
    try:
        excel_data = pd.ExcelFile(excel_file)
    except Exception as e:
        raise ValueError(f"Error reading Excel file: {e}")

    with open(output_md_file, 'w') as md_file:
        for sheet_name in excel_data.sheet_names:
            # Load the sheet into a DataFrame
            df = excel_data.parse(sheet_name)
            
            # Write sheet name as a header
            md_file.write(f"# {sheet_name}\n\n")
            
            # Convert DataFrame to Markdown and write to the file
            markdown_table = df.to_markdown(index=False, tablefmt="pipe")
            md_file.write(markdown_table)
            md_file.write("\n\n")  # Add spacing between tables
            
    print(f"All sheets have been converted to Markdown and saved to '{output_md_file}'")

# Example usage
excel_file = "../workbooks/4_Correlations.xlsx"  # Replace with your Excel file path
output_md_file = "../tables/4_Correlations.md"  # Replace with your desired output Markdown file name
excel_to_markdown(excel_file, output_md_file)
