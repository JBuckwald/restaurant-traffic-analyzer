import json
import pandas as pd
import time
import os
import kagglehub

def load_and_filter_data(business_path, review_path):
    """
    Loads business and review data, using chunking for the large review file
    for memory efficiency and speed.
    """
    print("Loading business data from local cache...")
    businesses = pd.read_json(business_path, lines=True)

    print("Filtering for Philadelphia restaurants...")
    restaurants = businesses[
        (businesses['city'] == 'Philadelphia') &
        (businesses['state'] == 'PA') &
        (businesses['categories'].str.contains('Restaurants', na=False))
    ]
    restaurant_ids = restaurants['business_id'].unique()
    del businesses

    print(f"Found {len(restaurant_ids)} restaurants in Philadelphia.")
    if len(restaurant_ids) == 0:
        print("No restaurants found. Exiting.")
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
    """
    Analyzes review dates & times to determine peak restaurant traffic.
    """
    print("\n--- Analyzing Peak Times ---")
    df['day_of_week'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    peak_times = df.groupby(['day_of_week', 'hour']).size()
    peak_times_grid = peak_times.unstack(fill_value=0)
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    peak_times_grid = peak_times_grid.reindex(day_order)
    return peak_times_grid


if __name__ == "__main__":
    KAGGLE_DATASET_HANDLE = "yelp-dataset/yelp-dataset"
    
    print("Ensuring dataset is available locally via Kaggle Hub...")
    dataset_path = kagglehub.dataset_download(KAGGLE_DATASET_HANDLE)
    print(f"Dataset cached at: {dataset_path}")

    BUSINESS_FILE_PATH = os.path.join(dataset_path, "yelp_academic_dataset_business.json")
    REVIEW_FILE_PATH = os.path.join(dataset_path, "yelp_academic_dataset_review.json")
    
    start_time = time.time()
    
    philly_reviews_df = load_and_filter_data(BUSINESS_FILE_PATH, REVIEW_FILE_PATH)
    
    if philly_reviews_df is not None:
        peak_grid = analyze_peak_times(philly_reviews_df)
        
        output_dir = "results_data"
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, "philadelphia_peak_times.csv")
        peak_grid.to_csv(output_path)
        print(f"\nAnalysis complete. Results saved to {output_path}")

    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")