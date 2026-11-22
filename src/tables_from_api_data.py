# Standard/built-in python libraries
import os

# Imports from other python scripts
from get_crime_data import load_crime_data
from clean_api_data import crime_data_clean

# Third-party libraries to be installed with pip
import pandas as pd

processed_final_data = "../processed_final_data/from_api"

def load_clean_crime_data() -> pd.DataFrame:
    """
    Cleans the crime dataset
    :return: cleaned crime dataset as pandas dataframe
    """
    crime_data = load_crime_data()
    cleaned_crime_data = crime_data_clean(crime_data)
    return cleaned_crime_data

def type_of_crime(cleaned_crime_data: pd.DataFrame) -> pd.DataFrame:
    """
    Creating the type_of_crime table from the cleaned crime dataset
    :param cleaned_crime_data: the cleaned crime dataframe
    :return: type_of_crime table/dataframe
    """
    # Selecting the unique crime codes and their description from the cleaned crime dataset
    type_of_crime_df = cleaned_crime_data[["crm_cd", "crm_cd_desc"]].copy()
    type_of_crime_df = type_of_crime_df.drop_duplicates().reset_index(drop=True)
    # Creating unique id for each unique type of crime
    type_of_crime_df["type_of_crime_id"] = (type_of_crime_df.index + 1).astype(str)

    # Declaring the type of 'crm_cd' as str
    type_of_crime_df["crm_cd"] = type_of_crime_df["crm_cd"].astype(str)

    # Writing data to an Excel file
    type_of_crime_data = os.path.join(processed_final_data, "type_of_crime.xlsx")
    type_of_crime_df.to_excel(type_of_crime_data, index=False)
    return type_of_crime_df

def weapons(cleaned_crime_data: pd.DataFrame) -> pd.DataFrame:
    """
    Creating the weapons table from the cleaned crime dataset
    :param cleaned_crime_data: the cleaned crime dataframe
    :return: weapons table/dataframe
    """
    # Selecting the unique weapon codes and their description from the cleaned crime dataset
    weapons_df = cleaned_crime_data[["weapon_used_cd", "weapon_desc"]].copy()
    weapons_df = weapons_df.drop_duplicates().reset_index(drop=True)
    # Creating unique id for each unqiue weapon
    weapons_df["weapon_id"] = (weapons_df.index + 1).astype(str)

    # Declaring the type of 'weapon_used_cd' as str
    weapons_df["weapon_used_cd"] = weapons_df["weapon_used_cd"].astype(str)

    # Writing data to an Excel file
    weapons_data = os.path.join(processed_final_data, "weapons.xlsx")
    weapons_df.to_excel(weapons_data, index=False)
    return weapons_df

def locations(cleaned_crime_data: pd.DataFrame) -> pd.DataFrame:
    """
    Creating the locations table from the cleaned crime dataset
    :param cleaned_crime_data: the cleaned crime dataframe
    :return: locations table/dataframe
    """
    # Selecting the unique locations from the cleaned crime dataset
    locations_df = cleaned_crime_data[["area", "area_name", "rpt_dist_no", "premis_cd", "premis_desc"]].copy()
    locations_df = locations_df.drop_duplicates().reset_index(drop=True)
    # Creating unique id for each unique location
    locations_df["location_id"] = (locations_df.index + 1).astype(str)

    # Declaring the type of area, rpt_dist_no, and premis_cd as str
    locations_df["area"] = locations_df["area"].astype(str)
    locations_df["rpt_dist_no"] = locations_df["rpt_dist_no"].astype(str)
    locations_df["premis_cd"] = locations_df["premis_cd"].astype(str)

    # Writing data to an Excel file
    locations_data = os.path.join(processed_final_data, "locations.xlsx")
    locations_df.to_excel(locations_data, index=False)
    return locations_df

def victims(cleaned_crime_data: pd.DataFrame) -> pd.DataFrame:
    """
    Creating the victims table from the cleaned crime dataset
    :param cleaned_crime_data: the cleaned crime dataframe
    :return: victims table/dataframe
    """
    # Selecting all crime incidents and their associated victim information
    victims_df = cleaned_crime_data[["dr_no", "vict_age", "vict_sex", "vict_descent"]].copy()
    victims_df["dr_no"] = victims_df["dr_no"].astype(str)
    victims_data = os.path.join(processed_final_data, "victims.xlsx")
    victims_df.to_excel(victims_data, index=False)
    return victims_df


def crime_incident(cleaned_crime_data: pd.DataFrame, weapons_df: pd.DataFrame, locations_df: pd.DataFrame, type_of_crime_df: pd.DataFrame) -> pd.DataFrame:
    """
    Creating the crime incident table from the cleaned crime dataset
    :param cleaned_crime_data: the cleaned crime dataframe
    :param weapons_df: the weapons dataframe
    :param locations_df: the locations dataframe
    :param type_of_crime_df: the type_of_crime dataframe
    :return: crime incident table/dataframe
    """
    crime_incident_df = cleaned_crime_data.copy()
    # Merging the cleaned crime data with the weapons df in order to associate the unique weapon ids with crime incidents that are represented by a unique number under the column name, dr_no
    crime_incident_df = crime_incident_df.merge(weapons_df, on=["weapon_used_cd", "weapon_desc"], how="left")
    # Merging again with the locations df in order to associate the unique location ids with the crime incidents
    crime_incident_df = crime_incident_df.merge(locations_df,
                                                on=["area", "area_name", "rpt_dist_no", "premis_cd", "premis_desc"],
                                                how="left")
    # Merging again with the type_of_crime df in order to associate the unique type of crime ids with crime incidents
    crime_incident_df = crime_incident_df.merge(type_of_crime_df, on=["crm_cd", "crm_cd_desc"], how="left")
    # Filtering the columns to only include dr_no, weapon id, location id, and type of crime id columns in the crime incident dataframe
    crime_incident_df = crime_incident_df[["dr_no", "weapon_id", "location_id", "type_of_crime_id"]].drop_duplicates()

    # Declaring the id columns as type string
    crime_incident_df["weapon_id"] = crime_incident_df["weapon_id"].astype(str)
    crime_incident_df["location_id"] = crime_incident_df["location_id"].astype(str)
    crime_incident_df["type_of_crime_id"] = crime_incident_df["type_of_crime_id"].astype(str)
    crime_incident_df["dr_no"] = crime_incident_df["dr_no"].astype(str)

    # Writing the result dataset to an Excel file
    crime_incident_data = os.path.join(processed_final_data, "crime_incident.xlsx")
    crime_incident_df.to_excel(crime_incident_data, index=False)
    return crime_incident_df

