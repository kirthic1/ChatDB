# Third-party libraries to be installed with pip
import pandas as pd
import os

processed_data_folder = "../processed_final_data/from_api"

def crime_data_clean(results_df) -> pd.DataFrame:
    """
    Data cleaning and processing on CRIME DATA.
    Removes duplicate rows, processes missing values, adds separate columns for year, month, hour, time groups,
    and writes the newly processed/cleaned Los Angeles CRIME data to a JSON file in the data/processed folder.
    :param results_df: the crime dataframe
    :return: pd.DataFrame
    """
    # Processing the day/time columns.
    results_df["date_occ"] = pd.to_datetime(results_df["date_occ"])
    # dt is a pandas accessor that enables extraction of time components from a datetime column
    results_df["year"] = results_df["date_occ"].dt.year
    results_df["month"] = results_df["date_occ"].dt.month
    results_df["time_occ"] = pd.to_datetime(results_df["time_occ"], format="%H%M")
    results_df["hour"] = results_df["time_occ"].dt.hour

    # Replacing NA values for mocodes with Unknown.
    # Mocodes define codes for different types of criminal/suspect behaviors
    results_df["mocodes"] = results_df["mocodes"].fillna("Unknown")

    # Replacing NA values for weapon_desc and weapon_used_cd with UNKNOWN WEAPON/OTHER WEAPON,
    # Now, all unknown type of weapon values are consolidated into one cateogry as UNKNOWN WEAPON/OTHER WEAPON
    results_df["weapon_desc"] = results_df["weapon_desc"].fillna("UNKNOWN WEAPON/OTHER WEAPON")
    results_df["weapon_used_cd"] = results_df["weapon_used_cd"].fillna("UNKNOWN WEAPON/OTHER WEAPON")

    # Replacing all NA values and unknown values for victim_descent with X.
    results_df["vict_descent"] = results_df["vict_descent"].fillna("X")
    results_df["vict_descent"] = results_df["vict_descent"].replace("-", "X")

    # If victim age less than zero or greater than 100, replacing the value with zero. Zero represents unknown age.
    results_df["vict_age"] = pd.to_numeric(results_df["vict_age"], errors="coerce")
    results_df["vict_age"] = results_df["vict_age"].fillna(0)
    results_df["vict_age"] = results_df["vict_age"].apply(lambda x: 0 if x < 0 else x)
    results_df["vict_age"] = results_df["vict_age"].apply(lambda x: 0 if x > 100 else x)

    # Replacing all unknown values of victim_sex with X.
    # Assuming "H" means unknown, so replacing "H" with X.
    results_df["vict_sex"] = results_df["vict_sex"].fillna("X")
    results_df["vict_sex"] = results_df["vict_sex"].replace("-", "X")
    results_df["vict_sex"] = results_df["vict_sex"].replace("H", "X")

    # Replacing all NA values of premis_desc and premis_cd with Unknown.
    results_df["premis_desc"] = results_df["premis_desc"].fillna("Unknown")
    results_df["premis_cd"] = results_df["premis_cd"].fillna("Unknown")

    # Replacing all NA values of area and area_name with Unknown.
    results_df["area"] = results_df["area"].fillna("Unknown")
    results_df["area_name"] = results_df["area_name"].fillna("Unknown")

    # Replacing all NA values of rpt_dist_no with Unknown.
    results_df["rpt_dist_no"] = results_df["rpt_dist_no"].fillna("Unknown")

    # Replacing all NA values of crm_cd and crm_cd_desc with Unknown.
    results_df["crm_cd"] = results_df["crm_cd"].fillna("Unknown")
    results_df["crm_cd_desc"] = results_df["crm_cd_desc"].fillna("Unknown")

    # Dropping any duplicate rows.
    results_df.drop_duplicates(keep="first", inplace=True)

    # Writing JSON data to file in data/processed folder.
    results_df = results_df.reset_index(drop=True)
    # Converting the datetime columns to str so that it is saved in json file cleanly
    results_df["date_occ"] = results_df["date_occ"].astype(str)
    results_df["time_occ"] = results_df["time_occ"].astype(str)
    processed_crime_data = os.path.join(processed_data_folder, "LA_crime_data_processed.json")
    results_df.to_json(processed_crime_data, orient="records", lines=False)

    return results_df