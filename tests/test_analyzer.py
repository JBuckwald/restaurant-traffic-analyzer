# --- tests/test_analyzer.py ---

import pandas as pd
import pytest

from restaurant_analyzer.data_analysis import create_peak_grid_from_reviews

def test_peak_time_logic_from_reviews():
    """
    Tests the core logic of creating a peak-time grid from review data.
    """
    # 1. Arrange: Create a small, predictable DataFrame
    data = {
        # The 'date' column now needs to match the input for this specific function
        'date': [
            '2024-01-01 10:30:00', # Monday at 10 AM
            '2024-01-01 10:55:00', # Monday at 10 AM
            '2024-01-02 20:15:00'  # Tuesday at 8 PM
        ]
    }
    sample_df = pd.DataFrame(data)

    # 2. Act: Run the correct function we are testing
    result_grid = create_peak_grid_from_reviews(sample_df)
    
    # 3. Assert: The assertions remain the same and are still valid
    assert result_grid.loc['Monday', 10] == 2
    assert result_grid.loc['Tuesday', 20] == 1
    assert result_grid.loc['Monday', 11] == 0
    assert result_grid.sum().sum() == 3