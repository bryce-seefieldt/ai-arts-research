import os

def export_to_csv(df, output_dir, filename):
    """
    Exports DataFrame to CSV format.
    
    Parameters:
        df (pd.DataFrame): DataFrame to export.
        output_dir (str): Directory to save the file.
        filename (str): Name of the file.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, filename)
        df.to_csv(output_path, index=False)
        print(f"Data exported to CSV: {output_path}")
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        raise

def export_to_md(df, output_dir, filename):
    """
    Exports DataFrame to Markdown format.
    
    Parameters:
        df (pd.DataFrame): DataFrame to export.
        output_dir (str): Directory to save the file.
        filename (str): Name of the file.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, filename)
        with open(output_path, "w") as f:
            f.write(df.to_markdown(index=False))
        print(f"Data exported to Markdown: {output_path}")
    except Exception as e:
        print(f"Error exporting to Markdown: {e}")
        raise
