
import os
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
def generate_directory_structure(start_path, indent_level=0):
    """
    Recursively generates a hierarchical structure of directories and files.
    
    Parameters:
        start_path (str): The path to start parsing.
        indent_level (int): Current indentation level for hierarchy visualization.
    
    Returns:
        str: A string representing the directory structure.
    """
    structure = ""
    items = sorted(os.listdir(start_path))  # Sort to maintain consistent order
    for item in items:
        item_path = os.path.join(start_path, item)
        if os.path.isdir(item_path):
            # Add directory to structure
            structure += "  " * indent_level + f"- **{item}/**\n"
            # Recurse into the directory
            structure += generate_directory_structure(item_path, indent_level + 1)
        else:
            # Add file to structure
            structure += "  " * indent_level + f"- {item}\n"
    return structure

def save_structure_to_md(structure, output_file):
    """
    Saves the directory structure to a .md file.
    
    Parameters:
        structure (str): The directory structure to save.
        output_file (str): The path to the output .md file.
    """
    try:
        with open(output_file, "w") as f:
            f.write("# Project Directory Structure\n\n")
            f.write(structure)
        print(f"Directory structure saved to {output_file}")
    except Exception as e:
        print(f"Error saving directory structure: {e}")

if __name__ == "__main__":
    # Define project root and output file
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    output_file = os.path.join(project_root, "project_structure.md")

    # Generate and save directory structure
    try:
        print(f"Parsing directory structure from: {project_root}")
        directory_structure = generate_directory_structure(project_root)
        save_structure_to_md(directory_structure, output_file)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# print("Current working directory:", os.getcwd())
# # Load the dataset 
# file_path = "raw-data/ai-arts-survey-data.csv" 

# if not os.path.exists(file_path):
#     raise FileNotFoundError(f"The file {file_path} was not found.")

# df = pd.read_csv(file_path) 

# #Preview the data print
# (df.head())

# # participantIds = df[['particpantId']]


# # participantIds.to_csv('csv-exports/participant_Ids.csv', index=False)
# # participantIds.to_markdown('csv-exports/participant_Ids.md')


# df['particpantId'].hist()    
# # Example plotting code
# plt.plot([1, 2, 3], [4, 5, 6])
# plt.title("Sample Plot")
# plt.show()  # Displays the plot if supported; no warning