# Restaurant Traffic Analyzer

## This Python application analyzes data from the Yelp Academic Dataset to calculate a weighted "Traffic Score" for restaurants in a given city, identifying peak dining hours by combining "review" and "check-in" data.

![Sample Heatmap](results_data/philadelphia_combined_heatmap.png)

---

# Project Goal

The goal of this project was to build a tool that could can provide actionable intelligence to independant restauranteurs.
By analyzing publicly available data, the application identifies the busiest hours and days of the week for any city covered in the dataset,
helping a restaurant owner make proactive decisions about staffing levels.

As a former chef, this is an issue that is near and dear to my heart, and represents just one of the many challenges that face independant restaurants.

---

## Key Features

* **Automated Data Sourcing**: Uses the official Kaggle API (`kagglehub`) to download and cache the multi-gigabyte Yelp dataset.
* **Interactive Menu**: A user-friendly command-line interface that prompts the user for a city and state.
* **Combined Traffic Score**: Blends two different data sources—review timestamps and check-in data—to create a more robust and accurate traffic metric.
* **Data Normalization**: Fairly combines the two data sources by first scaling each to a common `0-1` range before applying weights.
* **Dynamic Visualization**: Automatically generates and saves a heatmap visualization of the results for the chosen city.
* **Unit Tested**: Core logic is verified with a `pytest` test suite to ensure reliability and correctness.

---

## Technology Stack

* **Language**: Python
* **Libraries**:
    * `pandas` for data manipulation and analysis.
    * `matplotlib` & `seaborn` for data visualization.
    * `kagglehub` for interacting with the Kaggle API.
    * `pytest` for unit testing.

---

## Usage

Run the application's interactive menu from the project's root directory with the following command:
```bash
python3 main.py
```
The application will then guide you, prompting for a city and state to analyze.


---

## Known Issues

*City data provided by Yelp's Academic Dataset is limited. Many major cities are not included.

*Known Excluded Major Cities*
* Austin, TX
* Boston, MA
* Dallas, TX
* Denver, CO
* Houston, TX
* New York City, NY
* Phoenix, AZ
* San Diego, CA
* San Francisco, CA
* San Jose, CA
* Seattle, WA
* Washington, D.C.

---

## Testing

The project includes a suite of unit tests to verify the core logic. To run the tests, execute the following command from the root directory:
```bash
pytest
```