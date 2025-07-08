import os
import time

from restaurant_analyzer.data_analysis import *
from restaurant_analyzer.visualization import create_heatmap_from_csv

def run_pipeline(city, state):
    """
    Executes the full data analysis and visualization pipeline.
    """
    print(f"\n--- Starting analysis for {city}, {state} ---")
    start_time = time.time()

    # --- Part 1: Analysis (from analyzer.py) ---
    KAGGLE_DATASET_HANDLE = "yelp-dataset/yelp-dataset"
    dataset_path = download_data_from_kaggle(KAGGLE_DATASET_HANDLE)
    reviews, checkins, _ = load_and_prepare_data(dataset_path, city, state)
    
    if reviews is None or reviews.empty:
        print(f"\nCould not find sufficient data for {city}, {state}. Please try another location.")
        return None

    review_grid = create_peak_grid_from_reviews(reviews)
    checkin_grid = create_peak_grid_from_checkins(checkins)

    review_norm = (review_grid - review_grid.min().min()) / (review_grid.max().max() - review_grid.min().min())
    checkin_norm = (checkin_grid - checkin_grid.min().min()) / (checkin_grid.max().max() - checkin_grid.min().min())
    
    review_weight = 0.6
    checkin_weight = 0.4
    combined_grid = (review_weight * review_norm) + (checkin_weight * checkin_norm)

    output_dir = "results_data"
    os.makedirs(output_dir, exist_ok=True)
    city_slug = city.lower().replace(" ", "_")
    csv_path = os.path.join(output_dir, f"{city_slug}_combined_peak_times.csv")
    combined_grid.to_csv(csv_path)
    
    # --- Part 2: Visualization (from visualizer.py) ---
    png_path = os.path.join(output_dir, f"{city_slug}_combined_heatmap.png")
    chart_title = f"Combined Restaurant Traffic Score for {city}, {state}"
    create_heatmap_from_csv(csv_path, chart_title, png_path)
    
    end_time = time.time()
    print(f"--- Full pipeline for {city}, {state} executed in {end_time - start_time:.2f} seconds ---")
    
    return png_path

def main_menu():
    """
    Displays the main menu and handles the user interaction loop.
    """
    print("\n")
    print("="*60)
    print(" Welcome to the Restaurant Traffic Analyzer ".center(60, "="))
    print("="*60)
    print("This tool analyzes Yelp check-in and review data to create a heatmap of peak")
    print("dining hours for any city in the Yelp Academic Dataset.")
    print("-" * 60)

    while True:
        city_input = input("Please enter the city to analyze (e.g., Philadelphia): ")
        state_input = input("Please enter the two-letter state abbreviation (e.g., PA): ")

        if not city_input or not state_input:
            print("City and state cannot be empty. Please try again.")
            continue

        city = city_input.strip().title()
        state = state_input.strip().upper()

        output_file_path = run_pipeline(city, state)

        if output_file_path:
            print("\nSuccess! Your heatmap has been generated.")
            print(f"You can find it here: {output_file_path}")
        
        print("-" * 60)
        another = input("Would you like to run another analysis? (y/n): ").lower()
        if another != 'y':
            print("Thank you for using the analyzer. Goodbye!")
            break
        print("-" * 60)


if __name__ == "__main__":
    main_menu()