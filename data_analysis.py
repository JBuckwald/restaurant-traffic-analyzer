import json
import pandas as pd
import time
import os
import kagglehub
import argparse

def download_data_from_kaggle(dataset_id):
    print("Ensuring dataset is available locally via Kaggle Hub...")
    dataset_path = kagglehub.dataset_download(dataset_id)
    print(f"Dataset cached at: {dataset_path}")
    return dataset_path

def load_and_prepare_data(dataset_path, city, state):
    business_path = os.path.join(dataset_path, "yelp_academic_dataset_business.json")
    print(f"Loading business data for {city}, {state}...")
    businesses = pd.read_json(business_path, lines=True)
    
    print(f"Filtering for {city} restaurants...")
    restaurants = businesses[
        (businesses['city'] == city) &
        (businesses['state'] == state) &
        (businesses['categories'].str.contains('Restaurants', na=False))
    ]
    restaurant_ids = restaurants['business_id'].unique()
    del businesses
    print(f"Found {len(restaurant_ids)} restaurants in {city}, {state}.")
    if len(restaurant_ids) == 0:
        return None, None, None

    review_path = os.path.join(dataset_path, "yelp_academic_dataset_review.json")
    print("Loading and filtering review data in chunks...")
    review_chunks = pd.read_json(review_path, lines=True, chunksize=100000)
    filtered_reviews_list = [chunk[chunk['business_id'].isin(restaurant_ids)] for chunk in review_chunks]
    reviews_df = pd.concat(filtered_reviews_list, ignore_index=True)

    checkin_path = os.path.join(dataset_path, "yelp_academic_dataset_checkin.json")
    print("Loading and filtering check-in data...")
    checkins_df = pd.read_json(checkin_path, lines=True)
    checkins_df = checkins_df[checkins_df['business_id'].isin(restaurant_ids)]

    return reviews_df, checkins_df, restaurant_ids

def create_peak_grid_from_reviews(df):
    df['datetime'] = pd.to_datetime(df['date'])
    df['day_of_week'] = df['datetime'].dt.day_name()
    df['hour'] = df['datetime'].dt.hour
    peak_grid = df.groupby(['day_of_week', 'hour']).size().unstack(fill_value=0)
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return peak_grid.reindex(day_order)

def create_peak_grid_from_checkins(df):
    df['date'] = df['date'].str.split(', ')
    df_exploded = df.explode('date')
    return create_peak_grid_from_reviews(df_exploded)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze Yelp data to create a combined restaurant traffic score for a given city.")
    parser.add_argument("city", type=str, help="The city to analyze (e.g., 'Philadelphia').")
    parser.add_argument("state", type=str, help="The two-letter state abbreviation (e.g., 'PA').")
    args = parser.parse_args()

    KAGGLE_DATASET_HANDLE = "yelp-dataset/yelp-dataset"
    dataset_path = download_data_from_kaggle(KAGGLE_DATASET_HANDLE)

    start_time = time.time()
    
    reviews, checkins, ids = load_and_prepare_data(dataset_path, args.city, args.state)
    
    if reviews is not None and checkins is not None:
        review_grid = create_peak_grid_from_reviews(reviews)
        checkin_grid = create_peak_grid_from_checkins(checkins)

        review_norm = (review_grid - review_grid.min().min()) / (review_grid.max().max() - review_grid.min().min())
        checkin_norm = (checkin_grid - checkin_grid.min().min()) / (checkin_grid.max().max() - checkin_grid.min().min())

        review_weight = 0.6
        checkin_weight = 0.4
        combined_grid = (review_weight * review_norm) + (checkin_weight * checkin_norm)

        output_dir = "results_data"
        os.makedirs(output_dir, exist_ok=True)
        city_slug = args.city.lower().replace(" ", "_")
        output_path = os.path.join(output_dir, f"{city_slug}_combined_peak_times.csv")
        combined_grid.to_csv(output_path)
        
        print(f"\nAnalysis complete. Combined results saved to {output_path}")

    end_time = time.time()
    print(f"Total execution time: {end_time - start_time:.2f} seconds")