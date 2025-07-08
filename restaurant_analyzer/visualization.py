import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import argparse

def create_heatmap_from_csv(file_path, title, output_filename):
    """
    Reads peak times data from a CSV and creates a heatmap.
    """
    print(f"Reading data from {file_path}...")
    peak_times_df = pd.read_csv(file_path, index_col=0)

    print("Creating heatmap...")
    plt.figure(figsize=(20, 10))
    
    sns.heatmap(peak_times_df, cmap="viridis", annot=True, fmt=".2f", linewidths=.5)
    
    plt.title(title, fontsize=20)
    plt.xlabel("Hour of the Day", fontsize=15)
    plt.ylabel("Day of the Week", fontsize=15)
    plt.tight_layout()
    
    plt.savefig(output_filename)
    print(f"Heatmap saved as {output_filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize combined restaurant traffic scores from a CSV file.")
    parser.add_argument("city", type=str, help="The city name used in the CSV file (e.g., 'Philadelphia').")
    args = parser.parse_args()

    city_slug = args.city.lower().replace(" ", "_")
    output_dir = "results_data"

    INPUT_CSV = os.path.join(output_dir, f"{city_slug}_combined_peak_times.csv")
    OUTPUT_PNG = os.path.join(output_dir, f"{city_slug}_combined_heatmap.png")
    CHART_TITLE = f"Combined Restaurant Traffic Score for {args.city}"
    
    create_heatmap_from_csv(INPUT_CSV, CHART_TITLE, OUTPUT_PNG)