import pandas as pd  # Import pandas for DataFrame operations

def filter_participant_demographics(df):
    """
    Filters participants with non-null, non-zero participantId
    and retrieves demographic columns.
    
    Parameters:
        df (pd.DataFrame): The full dataset.
        
    Returns:
        pd.DataFrame: A filtered DataFrame with participant demographics.
    """
    try:
        # Filter rows where participantId is non-null and greater than zero
        filtered_df = df[df['particpantId'].notnull() & (df['particpantId'] > 0)]
        
        # Select demographic columns (columnIndex 33-36)
        demographic_columns = df.columns[33:37]  # Adjusted to include 33-36
        result_df = filtered_df[['particpantId'] + list(demographic_columns)]
        print(f"Filtered {len(result_df)} participants with demographic data.")
        return result_df
    except KeyError as e:
        print(f"Error accessing columns: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error during filtering: {e}")
        raise

def get_correct_classification_values(df):
    """
    Extracts the correct classification values for each image from the answer key row.
    
    Parameters:
        df (pd.DataFrame): The full dataset.
        
    Returns:
        pd.DataFrame: A DataFrame with the correct classification values for each image.
    """
    try:
        # Get the answer key row (rowIndex == 14)
        answer_key_row = df[df['rowIndex'] == 14].iloc[0]  # Extract the answer key row
        
        # Identify the columns for image classifications (odd column indices: columnIndex 1-23)
        classification_columns = df.columns[1:24:2]  # Odd-indexed columns only
        
        # Create a DataFrame with the correct classifications
        correct_classifications = pd.DataFrame({
            "Image": [f"Image {i}" for i in range(1, len(classification_columns) + 1)],
            "Correct Classification": [answer_key_row[col] for col in classification_columns]
        })
        
        print("Extracted correct classification values.")
        return correct_classifications
    except Exception as e:
        print(f"Error extracting correct classification values: {e}")
        raise


def is_classification_correct(participant_value, answer_key_value):
    """
    Checks if a participant's classification matches the answer key.
    
    Parameters:
        participant_value (str): Classification value from the participant.
        answer_key_value (str): Classification value from the answer key.
        
    Returns:
        bool: True if correct, False otherwise.
    """
    try:
        return participant_value == answer_key_value
    except Exception as e:
        print(f"Error during classification comparison: {e}")
        raise

def generate_classification_results(df):
    """
    Generates a table indicating whether each participant classified each image correctly.
    
    Parameters:
        df (pd.DataFrame): The full dataset.
        
    Returns:
        pd.DataFrame: A DataFrame with participantId and correctness for each image.
    """
    try:
        # Extract participant rows and answer key row
        participant_rows = df[df['particpantId'].notnull() & (df['particpantId'] > 0)]
        answer_key_row = df[df['rowIndex'] == 14].iloc[0]  # Get the last row (answer key)
        
        # Columns for image classifications (odd-indexed columns from columnIndex 1-23)
        classification_columns = df.columns[1:24:2]  # Select odd columns only
        
        # Create result table
        result_table = pd.DataFrame()
        result_table['particpantId'] = participant_rows['particpantId']
        
        for col in classification_columns:
            result_table[col] = participant_rows[col].apply(
                lambda x: "Correct" if is_classification_correct(x, answer_key_row[col]) else "Incorrect"
            )
        
        # Rename columns for clarity
        result_table.columns = ['particpantId'] + [f"Image {i} Result" for i in range(1, 13)]
        
        print(f"Generated classification results for {len(result_table)} participants.")
        return result_table
    except KeyError as e:
        print(f"Error accessing classification columns: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error during result generation: {e}")
        raise

def calculate_results_by_participant(df):
    """
    Calculates classification results for each participant:
    - Total Correct
    - Percent Correct
    - Correct AI Images
    - Correct Human Images
    - AI % Correct
    - Human % Correct
    
    Parameters:
        df (pd.DataFrame): The DataFrame with classification results.
        
    Returns:
        pd.DataFrame: A DataFrame with participantId and calculated results.
    """
    try:
        # Identify columns for image results
        result_columns = [col for col in df.columns if "Image" in col]
        
        # Initialize the result table
        participant_results = pd.DataFrame()
        participant_results['particpantId'] = df['particpantId']
        
        # Calculate metrics
        participant_results['Total Correct'] = df[result_columns].apply(lambda row: row[row == "Correct"].count(), axis=1)
        participant_results['Percent Correct'] = participant_results['Total Correct'] / len(result_columns) * 100
        
        # AI and Human classifications
        ai_image_indices = list(range(1, 13, 2))  # Odd images are AI (Image 1, 3, ...)
        human_image_indices = list(range(2, 13, 2))  # Even images are Human (Image 2, 4, ...)
        
        ai_columns = [f"Image {i} Result" for i in ai_image_indices]
        human_columns = [f"Image {i} Result" for i in human_image_indices]
        
        participant_results['Correct AI Images'] = df[ai_columns].apply(lambda row: row[row == "Correct"].count(), axis=1)
        participant_results['Correct Human Images'] = df[human_columns].apply(lambda row: row[row == "Correct"].count(), axis=1)
        
        # Calculate percentages for AI and Human images
        participant_results['AI % Correct'] = participant_results['Correct AI Images'] / len(ai_columns) * 100
        participant_results['Human % Correct'] = participant_results['Correct Human Images'] / len(human_columns) * 100
        
        print("Calculated results by participant.")
        return participant_results
    except Exception as e:
        print(f"Error calculating results by participant: {e}")
        raise

def calculate_results_by_image(df, original_df):
    """
    Calculates classification results for each image:
    - Total Correct
    - Percent Correct
    - Correct Value
    - Dominant Classification (most provided classification for the image)
    
    Parameters:
        df (pd.DataFrame): The DataFrame with classification results.
        original_df (pd.DataFrame): The original DataFrame with participant classifications.
        
    Returns:
        pd.DataFrame: A DataFrame with image-level calculated results.
    """
    try:
        # Identify columns for image results
        result_columns = [col for col in df.columns if "Image" in col]
        
        # Initialize the result table
        image_results = pd.DataFrame()
        image_results['Image'] = [f"Image {i}" for i in range(1, len(result_columns) + 1)]
        
        # Add the "Correct Value" column from the answer key
        answer_key_row = original_df[original_df['rowIndex'] == 14].iloc[0]  # Get the answer key row
        classification_columns = original_df.columns[1:24:2]  # Odd columns for classification
        
        correct_values = [answer_key_row[col] for col in classification_columns]
        image_results['Correct Value'] = correct_values
        
        # Calculate metrics
        image_results['Total Correct'] = df[result_columns].apply(lambda col: col[col == "Correct"].count(), axis=0).values
        image_results['Percent Correct'] = image_results['Total Correct'] / len(df) * 100
        
        # Calculate dominant classification from the original DataFrame
        dominant_classifications = []
        for col in classification_columns:
            dominant = original_df[col].mode()[0]  # Get the most common classification
            dominant_classifications.append(dominant)
        
        image_results['Dominant Classification'] = dominant_classifications
        
        print("Calculated results by image.")
        return image_results
    except Exception as e:
        print(f"Error calculating results by image: {e}")
        raise

def tabulate_overall_results(df):
    """
    Tabulates overall results across all participants and images:
    - Total Correct
    - Total Incorrect
    - Percentage Correct
    - Total AI Correct
    - % AI Correct
    - Total Human Correct
    - % Human Correct
    
    Parameters:
        df (pd.DataFrame): The DataFrame with classification results.
        
    Returns:
        pd.DataFrame: A single-row DataFrame with the overall tabulated results.
    """
    try:
        # Identify columns for image results
        result_columns = [col for col in df.columns if "Image" in col]
        
        # Flatten all classification results into a single series
        all_results = df[result_columns].values.flatten()
        
        # Calculate total correct and incorrect
        total_correct = (all_results == "Correct").sum()
        total_incorrect = (all_results == "Incorrect").sum()
        total_attempts = total_correct + total_incorrect
        
        # Calculate overall percentage correct
        percentage_correct = (total_correct / total_attempts) * 100 if total_attempts > 0 else 0
        
        # AI and Human classifications
        ai_image_indices = list(range(1, 13, 2))  # Odd images are AI (Image 1, 3, ...)
        human_image_indices = list(range(2, 13, 2))  # Even images are Human (Image 2, 4, ...)
        
        ai_columns = [f"Image {i} Result" for i in ai_image_indices]
        human_columns = [f"Image {i} Result" for i in human_image_indices]
        
        # Calculate AI and Human results
        total_ai_correct = df[ai_columns].apply(lambda row: row[row == "Correct"].count(), axis=1).sum()
        total_human_correct = df[human_columns].apply(lambda row: row[row == "Correct"].count(), axis=1).sum()
        
        # Calculate percentages
        total_ai_attempts = len(ai_columns) * len(df)
        total_human_attempts = len(human_columns) * len(df)
        
        percentage_ai_correct = (total_ai_correct / total_ai_attempts) * 100 if total_ai_attempts > 0 else 0
        percentage_human_correct = (total_human_correct / total_human_attempts) * 100 if total_human_attempts > 0 else 0
        
        # Create result table
        overall_results = pd.DataFrame([{
            "Total Correct": total_correct,
            "Total Incorrect": total_incorrect,
            "Percentage Correct": percentage_correct,
            "Total AI Correct": total_ai_correct,
            "% AI Correct": percentage_ai_correct,
            "Total Human Correct": total_human_correct,
            "% Human Correct": percentage_human_correct
        }])
        
        print("Tabulated overall results.")
        return overall_results
    except Exception as e:
        print(f"Error tabulating overall results: {e}")
        raise

def prepare_image_accuracy_data(classification_results, original_df):
    """
    Prepares data for visualizing classification accuracy per image.
    
    Parameters:
        classification_results (pd.DataFrame): The DataFrame with classification results.
        original_df (pd.DataFrame): The original dataset with participant classifications.
        
    Returns:
        pd.DataFrame: A DataFrame with accuracy data for each image.
    """
    try:
        # Identify image result columns
        result_columns = [col for col in classification_results.columns if "Image" in col]
        image_names = [f"Image {i}" for i in range(1, len(result_columns) + 1)]
        
        # Calculate the number of correct classifications for each image
        total_correct = classification_results[result_columns].apply(lambda col: col[col == "Correct"].count(), axis=0)
        
        # Calculate total participants
        total_participants = len(classification_results)
        
        # Calculate percentage correct
        percent_correct = (total_correct / total_participants) * 100
        
        # Get the correct classification values from the answer key
        answer_key_row = original_df[original_df['rowIndex'] == 14].iloc[0]
        classification_columns = original_df.columns[1:24:2]
        correct_values = [answer_key_row[col] for col in classification_columns]
        
        # Create a DataFrame for accuracy data
        accuracy_data = pd.DataFrame({
            "Image": image_names,
            "Correct Classification": correct_values,
            "Total Correct": total_correct.values,
            "Percent Correct": percent_correct.values
        })
        
        print("Prepared image accuracy data for visualization.")
        return accuracy_data
    except Exception as e:
        print(f"Error preparing image accuracy data: {e}")
        raise
    
def calculate_group_accuracy(classification_results, demographics_data):
    """
    Calculates classification accuracy for two groups based on creative status (Yes/No).
    
    Parameters:
        classification_results (pd.DataFrame): Classification results for all participants.
        demographics_data (pd.DataFrame): Participant demographic data.
        
    Returns:
        (pd.DataFrame, pd.DataFrame, pd.DataFrame): DataFrames for the "Yes" group, "No" group, and combined results.
    """
    try:
        # Merge demographics with classification results to associate "creative status"
        merged_data = pd.merge(
            demographics_data[["particpantId", "Do you consider yourself a creative artist?"]],
            classification_results,
            on="particpantId"
        )
        merged_data.rename(columns={"Do you consider yourself a creative artist?": "Creative Status"}, inplace=True)
        
        # Separate the groups
        yes_group = merged_data[merged_data["Creative Status"] == "Yes"]
        no_group = merged_data[merged_data["Creative Status"] == "No"]
        
        # Helper function to calculate accuracy metrics
        def calculate_accuracy(group, image_columns):
            total_correct = group[image_columns].apply(lambda row: row[row == "Correct"].count(), axis=1).sum()
            total_attempts = len(group) * len(image_columns)
            percent_correct = (total_correct / total_attempts) * 100 if total_attempts > 0 else 0
            return total_correct, percent_correct
        
        # Columns for AI and Human classifications
        ai_image_indices = list(range(1, 13, 2))  # Odd images are AI
        human_image_indices = list(range(2, 13, 2))  # Even images are Human
        
        ai_columns = [f"Image {i} Result" for i in ai_image_indices]
        human_columns = [f"Image {i} Result" for i in human_image_indices]
        all_columns = [col for col in classification_results.columns if "Image" in col]
        
        # Calculate accuracy for each group
        group_stats = {}
        for group_name, group_data in [("Yes", yes_group), ("No", no_group)]:
            group_stats[group_name] = {
                "Total Correct": calculate_accuracy(group_data, all_columns)[0],
                "Total % Correct": calculate_accuracy(group_data, all_columns)[1],
                "AI Correct": calculate_accuracy(group_data, ai_columns)[0],
                "AI % Correct": calculate_accuracy(group_data, ai_columns)[1],
                "Human Correct": calculate_accuracy(group_data, human_columns)[0],
                "Human % Correct": calculate_accuracy(group_data, human_columns)[1],
            }
        
        # Combine group stats into a single DataFrame
        combined_stats = pd.DataFrame(group_stats).T.reset_index()
        combined_stats.rename(columns={"index": "Group"}, inplace=True)
        
        return group_stats["Yes"], group_stats["No"], combined_stats
    except Exception as e:
        print(f"Error calculating group accuracy: {e}")
        raise
