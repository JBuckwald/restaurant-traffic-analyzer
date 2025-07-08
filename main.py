import argparse
import os
import time

from restaurant_analyzer.data_analysis import *
from restaurant_analyzer.visualization import create_heatmap_from_csv

def run_pipeline(city, state):
    """
    Executes the full data analysis and visualization pipeline.
    """
    print(f"--- Starting analysis for {city}, {state} ---")
    start_time = time.time()

    # --- Part 1: Analysis ---
    
    # 1. Download data
    KAGGLE_DATASET_HANDLE = "yelp-dataset/yelp-dataset"
    dataset_path = download_data_from_kaggle(KAGGLE_DATASET_HANDLE)

    # 2. Load and filter data
    reviews, checkins, _ = load_and_prepare_data(dataset_path, city, state)
    
    if reviews is None:
        print(f"Could not find sufficient data for {city}, {state}. Exiting.")
        return

    # 3. Analyze peak times
    review_grid = create_peak_grid_from_reviews(reviews)
    checkin_grid = create_peak_grid_from_checkins(checkins)

    # 4. Normalize and create combined score
    review_norm = (review_grid - review_grid.min().min()) / (review_grid.max().max() - review_grid.min().min())
    checkin_norm = (checkin_grid - checkin_grid.min().min()) / (checkin_grid.max().max() - checkin_grid.min().min())
    
    review_weight = 0.6
    checkin_weight = 0.4
    combined_grid = (review_weight * review_norm) + (checkin_weight * checkin_norm)

    # 5. Save intermediate CSV result
    output_dir = "results_data"
    os.makedirs(output_dir, exist_ok=True)
    city_slug = city.lower().replace(" ", "_")
    csv_path = os.path.join(output_dir, f"{city_slug}_combined_peak_times.csv")
    combined_grid.to_csv(csv_path)
    print(f"\nAnalysis data saved to {csv_path}")


    # --- Part 2: Visualization ---
    
    png_path = os.path.join(output_dir, f"{city_slug}_combined_heatmap.png")
    chart_title = f"Combined Restaurant Traffic Score for {city}, {state}"
    create_heatmap_from_csv(csv_path, chart_title, png_path)
    
    end_time = time.time()
    print(f"\n--- Full pipeline for {city}, {state} executed in {end_time - start_time:.2f} seconds ---")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the full Yelp restaurant traffic analysis pipeline for a given city.")
    parser.add_argument("city", type=str, help="The city to analyze (e.g., 'Philadelphia').")
    parser.add_argument("state", type=str, help="The two-letter state abbreviation (e.g., 'PA').")
    args = parser.parse_args()

    run_pipeline(args.city, args.state)