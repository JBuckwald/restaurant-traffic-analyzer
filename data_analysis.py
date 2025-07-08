import json
import pandas as pd
import time
import os
import kagglehub
import argparse # New import

def download_data_from_kaggle(dataset_id):
    """Downloads data if needed and returns the local cache path."""
    print("Ensuring dataset is available locally via Kaggle Hub...")
    dataset_path = kagglehub.dataset_download(dataset_id)
    print(f"Dataset cached at: {dataset_path}")
    return dataset_path

def load_and_filter_data(business_path, review_path, city, state):
    """
    Loads business and review data, using a city and state provided by the user.
    """
    print(f"Loading business data for {city}, {state}...")
    businesses = pd.read_json(business_path, lines=True)

    print(f"Filtering for {city} restaurants...")
    
    # Use the city and state arguments in the filter
    restaurants = businesses[
        (businesses['city'] == city) &
        (businesses['state'] == state) &
        (businesses['categories'].str.contains('Restaurants', na=False))
    ]
    
    restaurant_ids = restaurants['business_id'].unique()
    del businesses # Free up memory

    print(f"Found {len(restaurant_ids)} restaurants in {city}, {state}.")
    
    if len(restaurant_ids) == 0:
        print("No restaurants found for the specified location. Exiting.")
        return None

    print("Loading and filtering review data in chunks...")
    review_chunks = pd.read_json(review_path, lines=True, chunksize=100000)
    
    filtered_reviews_list = []
    for chunk in review_chunks:
        filtered_chunk = chunk[chunk['business_id'].isin(restaurant_ids)]
        filtered_reviews_list.append(filtered_chunk)
    
    filtered_reviews = pd.concat(filtered_reviews_list, ignore_index=True)
    return filtered_reviews

def analyze_peak_times(df):
    print("\n--- Analyzing Peak Times ---")
    df['day_of_week'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    peak_times = df.groupby(['day_of_week', 'hour']).size()
    peak_times_grid = peak_times.unstack(fill_value=0)
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    peak_times_grid = peak_times_grid.reindex(day_order)
    return peak_times_grid


if __name__ == "__main__":
    # --- Setup to parse command-line arguments ---
    parser = argparse.ArgumentParser(description="Analyze Yelp review data to find peak restaurant hours for a given city.")
    parser.add_argument("city", type=str, help="The city to analyze (e.g., 'Philadelphia').")
    parser.add_argument("state", type=str, help="The two-letter state abbreviation (e.g., 'PA').")
    args = parser.parse_args()
    
    # --- Main script logic ---
    KAGGLE_DATASET_HANDLE = "yelp-dataset/yelp-dataset"
    
    dataset_path = download_data_from_kaggle(KAGGLE_DATASET_HANDLE)

    BUSINESS_FILE_PATH = os.path.join(dataset_path, "yelp_academic_dataset_business.json")
    REVIEW_FILE_PATH = os.path.join(dataset_path, "yelp_academic_dataset_review.json")
    
    start_time = time.time()
    
    # Pass the user's city and state to the function
    reviews_df = load_and_filter_data(BUSINESS_FILE_PATH, REVIEW_FILE_PATH, args.city, args.state)
    
    if reviews_df is not None:
        peak_grid = analyze_peak_times(reviews_df)
        
        output_dir = "results_data"
        os.makedirs(output_dir, exist_ok=True)
        
        # Create a dynamic filename based on the city
        city_slug = args.city.lower().replace(" ", "_")
        output_path = os.path.join(output_dir, f"{city_slug}_peak_times.csv")
        peak_grid.to_csv(output_path)
        print(f"\nAnalysis complete. Results saved to {output_path}")

    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")