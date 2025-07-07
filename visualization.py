import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_heatmap_from_csv(file_path, title, output_name):
    print(f"Reading data from {file_path}...")
    peak_times_df = pd.read_csv(file_path, index_col=0)

    print("Creating Heatmap...")
    plt.figure(figsize=(20, 10))
    sns.heatmap(peak_times_df, cmap="viridis", annot=True, fmt="d", linewidths=.5)

    plt.title(title, fontsize=20)
    plt.xlabel("Hour of the Day", fontsize=15)
    plt.ylabel("Day of the Week", fontsize=15)
    plt.tight_layout()

    plt.savefig(output_name)
    print(f"Heatmap saved as {output_name}")

if __name__ == "__main__":
    
    output_dir = "results_data"
    INPUT_CSV = os.path.join(output_dir, "philadelphia_peak_times.csv")
    OUTPUT_PNG = os.path.join(output_dir, "philadelphia_peak_times_heatmap.png")
    CHART_TITLE = "Philadelphia Restaurant Reviews by Day and Hour"
    
    create_heatmap_from_csv(INPUT_CSV, CHART_TITLE, OUTPUT_PNG)