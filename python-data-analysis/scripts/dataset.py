import os
import sys
import pandas as pd  # Import pandas for DataFrame operations


# Add project root to Python module search path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)


from modules.data_loader import load_dataset
from modules.data_queries import (
    filter_participant_demographics,
    generate_classification_results,
    calculate_results_by_participant,
    get_correct_classification_values, 
    prepare_image_accuracy_data,
    calculate_group_accuracy,

)
from modules.data_exports import export_to_csv, export_to_md
from modules.data_visualizations import (
    plot_participant_demographics,
    plot_classification_heatmap,
    plot_results_by_participant,
    plot_image_accuracy_heatmap,
    plot_image_accuracy_barchart,
    plot_correct_classification_values,
    plot_classification_heatmap,
    plot_results_by_participant,
    plot_image_accuracy_heatmap,
    plot_image_accuracy_barchart,
    plot_group_comparison,
)

# Define project paths
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
data_file = os.path.join(project_root, "raw-data", "ai-arts-survey-data.csv")
csv_exports_dir = os.path.join(project_root, "csv-exports")
md_exports_dir = os.path.join(project_root, "md-exports")
visualizations_dir = os.path.join(project_root, "visualizations")

# Ensure the visualizations directory exists
os.makedirs(visualizations_dir, exist_ok=True)


if __name__ == "__main__":
    print("Starting dataset analysis...")

    # Load the dataset
    df = load_dataset(data_file)
 # Query 1: Participant Demographics
    participant_demographics = filter_participant_demographics(df)
    export_to_csv(participant_demographics, csv_exports_dir, "participant_demographics.csv")
    export_to_md(participant_demographics, md_exports_dir, "participant_demographics.md")
    plot_participant_demographics(
        participant_demographics, os.path.join(visualizations_dir, "participant_demographics_bar_chart.png")
    )

    # Query 2: Classification Results Table
    classification_results = generate_classification_results(df)
    export_to_csv(classification_results, csv_exports_dir, "classification_results.csv")
    export_to_md(classification_results, md_exports_dir, "classification_results.md")
    plot_classification_heatmap(
        classification_results, os.path.join(visualizations_dir, "classification_results_heatmap.png")
    )

    # Query 3: Results by Participant
    results_by_participant = calculate_results_by_participant(classification_results)
    export_to_csv(results_by_participant, csv_exports_dir, "classification_results_by_participant.csv")
    export_to_md(results_by_participant, md_exports_dir, "classification_results_by_participant.md")
    plot_results_by_participant(
        results_by_participant, os.path.join(visualizations_dir, "results_by_participant_bar_chart.png")
    )

    # Query 4: Results by Image
    results_by_image = prepare_image_accuracy_data(classification_results, df)
    plot_image_accuracy_heatmap(
        results_by_image, os.path.join(visualizations_dir, "classification_accuracy_heatmap.png")
    )
    plot_image_accuracy_barchart(
        results_by_image, os.path.join(visualizations_dir, "classification_accuracy_barchart.png")
    )

    # Query 5: Correct Classification Values
    correct_classification_values = get_correct_classification_values(df)
    export_to_csv(correct_classification_values, csv_exports_dir, "correct_classification_values.csv")
    export_to_md(correct_classification_values, md_exports_dir, "correct_classification_values.md")
    plot_correct_classification_values(
        correct_classification_values, os.path.join(visualizations_dir, "correct_classification_values_bar_chart.png")
    )


    # Query 6: Group Accuracy
    yes_group_stats, no_group_stats, combined_group_stats = calculate_group_accuracy(classification_results, participant_demographics)
    export_to_csv(pd.DataFrame([yes_group_stats]), csv_exports_dir, "creative_yes_group_accuracy.csv")
    export_to_md(pd.DataFrame([yes_group_stats]), md_exports_dir, "creative_yes_group_accuracy.md")
    export_to_csv(pd.DataFrame([no_group_stats]), csv_exports_dir, "creative_no_group_accuracy.csv")
    export_to_md(pd.DataFrame([no_group_stats]), md_exports_dir, "creative_no_group_accuracy.md")
    export_to_csv(combined_group_stats, csv_exports_dir, "combined_group_accuracy.csv")
    export_to_md(combined_group_stats, md_exports_dir, "combined_group_accuracy.md")


    # Visualize group comparisons
    plot_group_comparison(
        combined_group_stats, 
        os.path.join(visualizations_dir, "total_accuracy_comparison.png"),
        "Total % Correct", "Total % Correct"
    )
    plot_group_comparison(
        combined_group_stats, 
        os.path.join(visualizations_dir, "ai_accuracy_comparison.png"),
        "AI % Correct", "AI % Correct"
    )
    plot_group_comparison(
        combined_group_stats, 
        os.path.join(visualizations_dir, "human_accuracy_comparison.png"),
        "Human % Correct", "Human % Correct"
    )