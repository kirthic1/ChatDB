# Standard/Built-in python libraries
import os

# Third-party libraries to be installed with pip
import requests
from requests.exceptions import RequestException
import pandas as pd
from dotenv import load_dotenv

raw_data_folder = "../raw_data/from_api"
def load_crime_data() -> pd.DataFrame:
    """
    Retrieves Los Angeles CRIME data through API request and writes the data to a JSON file in the data/raw folder.
    This code retrieves the data in sets of 10,000 rows till it reaches end of dataset since the API has querying
    limits.
    :return: pd.DataFrame
    """
    # Loading the environment variables
    load_dotenv()
    # Obtaining the app token for api request to retrieve data
    app_token = os.getenv('CRIME_DATA_APP_TOKEN')
    headers = {"X-App-Token": app_token}
    # Setting limit which determines how many rows of data are retrieved at once in one api request
    params = {"$limit": 5000}
    # API endpoint link
    url = "https://data.lacity.org/resource/2nrs-mtv8.json"
    data = []
    offset = 0
    print("📁 Loading raw LA crime data...")
    while True:
        try:
            params["$offset"] = offset
            # API request
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            print(f"Retrieved 5000 rows. Offset = {offset}")
            results = response.json()
            data.extend(results)
            if len(results) < 5000 or len(results) == 0:
                print("Retrieved all data")
                break
            offset = offset + 5000
        except RequestException:
            raise Exception("Error occurred while fetching data")
        except Exception:
            raise Exception("Error occurred while fetching data")
    # Creating pandas dataframe from data
    results_df = pd.DataFrame(data)
    # Writing data to json file
    raw_crime_data = os.path.join(raw_data_folder, "LA_crime_data.json")
    results_df.to_json(raw_crime_data, orient="records", lines=False)
    return results_df
