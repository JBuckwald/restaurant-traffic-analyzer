import json
import pandas as pd
import time

def load_fliter_merge_data(business_path, review_path):
    """ 
    Loads Yelp Business and Review data, filters for Philadelphia restaurants,
    and returns a DataFrame of their reviews.
    """

    # - - Handle Business Data - - #
    print("Loading business data...")
    businesses = pd.read_json(business_path, lines=True)

    print("Filtering for Philadelphia restaurants...")
    
    restaurants = businesses[
        (businesses['city'] == 'Philadelphia') &
        (businesses['state'] == 'PA') &
        (businesses['categories'].str.contains('Restaurants', na=False))
    ]

    restaurant_ids = restaurants['business_id'].unique()
    del businesses # Free memory

    print(f"Found {len(restaurant_ids)} restaurants in Philadelphia.")

    if len(restaurant_ids) == 0:
        print("No restaurants found in the specified area. Exiting.")
        return None
    

    # - - Handle Review Data - - #
    print("Loading review data.. This could take up to 15 minutes.")
    review_chunks = pd.read_json(review_path, lines=True, chunksize=100000)

    filtered_review_list = []
    for chunk in review_chunks:
        filtered_chunk = chunk[chunk["business_id"].isin(restaurant_ids)]
        filtered_review_list.append(filtered_chunk)

    filtered_reviews = pd.concat(filtered_review_list)

    return filtered_reviews


# - - Main Program - - #

if __name__ == "__main__":
    BUSINESS_FILE_PATH = "yelp_data/yelp_academic_dataset_business.json"
    REVIEW_FILE_PATH = "yelp_data/yelp_academic_dataset_review.json"
    
    start_time = time.time()
    philly_reviews_df = load_fliter_merge_data(BUSINESS_FILE_PATH, REVIEW_FILE_PATH)
    
    if philly_reviews_df is not None:
        print("\n--- Philadelphia Restaurant Review Data ---")
        philly_reviews_df.info()
        
        print("\n--- First 5 Filtered Reviews ---")
        print(philly_reviews_df.head())

    end_time = time.time()
    print(f"\nTotal execution time: {end_time - start_time:.2f} seconds")



    
