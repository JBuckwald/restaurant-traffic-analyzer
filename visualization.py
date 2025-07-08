import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import argparse

def create_heatmap_from_csv(file_path, title, output_filename):
    print(f"Reading data from {file_path}...")
    peak_times_df = pd.read_csv(file_path, index_col=0)

    print("Creating heatmap...")
    plt.figure(figsize=(20, 10))
    
    sns.heatmap(peak_times_df, cmap="viridis", annot=True, fmt="d", linewidths=.5)
    
    plt.title(title, fontsize=20)
    plt.xlabel("Hour of the Day", fontsize=15)
    plt.ylabel("Day of the Week", fontsize=15)
    
    plt.tight_layout()
    
    plt.savefig(output_filename)
    print(f"Heatmap saved as {output_filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize peak restaurant hours from a CSV file.")
    parser.add_argument("city", type=str, help="The city name used in the CSV file (e.g., 'Philadelphia').")
    args = parser.parse_args()

    city_slug = args.city.lower().replace(" ", "_")
    output_dir = "results_data"

    # Create dynamic paths based on the city argument
    INPUT_CSV = os.path.join(output_dir, f"{city_slug}_peak_times.csv")
    OUTPUT_PNG = os.path.join(output_dir, f"{city_slug}_peak_times_heatmap.png")
    CHART_TITLE = f"{args.city} Restaurant Reviews by Day and Hour"
    
    create_heatmap_from_csv(INPUT_CSV, CHART_TITLE, OUTPUT_PNG)