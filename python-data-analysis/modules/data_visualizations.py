import matplotlib.pyplot as plt
import seaborn as sns

def plot_image_accuracy_heatmap(accuracy_data, output_file):
    """
    Generates a heatmap comparing classification accuracy per image.
    
    Parameters:
        accuracy_data (pd.DataFrame): The accuracy data for images.
        output_file (str): The file path to save the heatmap.
    """
    try:
        plt.figure(figsize=(10, 6))
        
        # Reshape the data for heatmap
        heatmap_data = accuracy_data.pivot(index="Image", columns="Correct Classification", values="Percent Correct")
        
        # Generate the heatmap
        sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlGnBu", cbar_kws={"label": "Percent Correct"})
        plt.title("Classification Accuracy per Image")
        plt.xlabel("Correct Classification")
        plt.ylabel("Image")
        plt.tight_layout()
        
        # Save the heatmap
        plt.savefig(output_file)
        plt.close()
        print(f"Heatmap saved to {output_file}")
    except Exception as e:
        print(f"Error generating heatmap: {e}")
        raise
    
def plot_image_accuracy_barchart(accuracy_data, output_file):
    """
    Generates a bar chart comparing classification accuracy per image.
    
    Parameters:
        accuracy_data (pd.DataFrame): The accuracy data for images.
        output_file (str): The file path to save the bar chart.
    """
    try:
        plt.figure(figsize=(12, 6))
        sns.barplot(x="Image", y="Percent Correct", data=accuracy_data, palette="viridis")
        plt.title("Classification Accuracy per Image")
        plt.xlabel("Image")
        plt.ylabel("Percent Correct")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()
        print(f"Bar chart saved to {output_file}")
    except Exception as e:
        print(f"Error generating bar chart: {e}")
        raise


def plot_participant_demographics(demographics_data, output_file):
    """
    Generates a bar chart showing the number of participants by age range.
    
    Parameters:
        demographics_data (pd.DataFrame): Demographics data for participants.
        output_file (str): File path to save the bar chart.
    """
    try:
        plt.figure(figsize=(10, 6))
        sns.countplot(data=demographics_data, y="What is your age range?", palette="viridis")
        plt.title("Participants by Age Range")
        plt.xlabel("Number of Participants")
        plt.ylabel("Age Range")
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()
        print(f"Demographics bar chart saved to {output_file}")
    except Exception as e:
        print(f"Error generating demographics bar chart: {e}")
        raise

def plot_classification_heatmap(classification_results, output_file):
    """
    Generates a heatmap showing classification results for participants and images.
    
    Parameters:
        classification_results (pd.DataFrame): Classification results.
        output_file (str): File path to save the heatmap.
    """
    try:
        plt.figure(figsize=(12, 8))
        classification_matrix = classification_results.set_index("particpantId").replace(
            {"Correct": 1, "Incorrect": 0}
        )
        sns.heatmap(classification_matrix, cmap="coolwarm", annot=True, cbar_kws={"label": "Classification (1 = Correct, 0 = Incorrect)"})
        plt.title("Classification Results Heatmap")
        plt.xlabel("Images")
        plt.ylabel("Participants")
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()
        print(f"Classification heatmap saved to {output_file}")
    except Exception as e:
        print(f"Error generating classification heatmap: {e}")
        raise

def plot_results_by_participant(participant_results, output_file):
    """
    Generates a grouped bar chart showing classification results by participant.
    
    Parameters:
        participant_results (pd.DataFrame): Results by participant.
        output_file (str): File path to save the bar chart.
    """
    try:
        participant_results_melted = participant_results.melt(
            id_vars="particpantId",
            value_vars=["Total Correct", "Correct AI Images", "Correct Human Images"],
            var_name="Metric",
            value_name="Count"
        )
        plt.figure(figsize=(12, 8))
        sns.barplot(data=participant_results_melted, x="particpantId", y="Count", hue="Metric", palette="viridis")
        plt.title("Results by Participant")
        plt.xlabel("Participant ID")
        plt.ylabel("Count")
        plt.legend(title="Metric")
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()
        print(f"Results by participant bar chart saved to {output_file}")
    except Exception as e:
        print(f"Error generating results by participant bar chart: {e}")
        raise

def plot_correct_classification_values(correct_values, output_file):
    """
    Generates a horizontal bar chart for correct classification values for each image.
    
    Parameters:
        correct_values (pd.DataFrame): Correct classification values.
        output_file (str): File path to save the bar chart.
    """
    try:
        plt.figure(figsize=(10, 6))
        sns.barplot(data=correct_values, y="Image", x="Correct Classification", palette="viridis", orient="h")
        plt.title("Correct Classification Values for Images")
        plt.xlabel("Correct Classification")
        plt.ylabel("Image")
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()
        print(f"Correct classification bar chart saved to {output_file}")
    except Exception as e:
        print(f"Error generating correct classification bar chart: {e}")
        raise

def plot_group_comparison(group_stats, output_file, metric_name, y_label):
    """
    Creates a bar chart comparing the two groups on a specific metric.
    
    Parameters:
        group_stats (pd.DataFrame): DataFrame containing group accuracy stats.
        output_file (str): Path to save the chart.
        metric_name (str): Column name to plot.
        y_label (str): Y-axis label.
    """
    try:
        plt.figure(figsize=(8, 6))
        sns.barplot(data=group_stats, x="Group", y=metric_name, palette="viridis")
        plt.title(f"Comparison of {metric_name} by Group")
        plt.ylabel(y_label)
        plt.xlabel("Group")
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()
        print(f"Comparison chart for {metric_name} saved to {output_file}")
    except Exception as e:
        print(f"Error generating group comparison chart for {metric_name}: {e}")
        raise
