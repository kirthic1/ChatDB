# Standard libraries/built-in python libraries
from typing import List

# Third-party libraries to be installed with pip
import pandas as pd
import numpy as np


# Prevents pandas from silently downcasting (casting to smaller data type to save memory) without warning
pd.set_option('future.no_silent_downcasting', True)

def clean_downloaded_data(filepath: str, value_column_name: str) -> pd.DataFrame:
    """
    Data cleaning and processing on downloaded data.
    :param filepath: path to the downloaded data
    :param value_column_name: name of the main statistic column
    :return: pd.DataFrame
    """
    df = pd.read_excel(filepath, skipfooter=1)
    # First column represents the countries, but isn't named. Hence, renaming the first column
    df = df.rename(columns = {' ': "Country"})
    # Changing data table format from horizontal to vertical
    df = df.melt(id_vars = "Country", var_name = "Year", value_name = value_column_name)
    # Defining the Year column with integer data type
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
    # Replacing any blank values represented by '..' with np.nan and replacing any ',' in the value with empty string
    df[value_column_name] = df[value_column_name].replace('..', np.nan).astype(str).str.replace(',', '', regex=False)
    # Converts all values in the value column from strings to actual numbers
    df[value_column_name] = pd.to_numeric(df[value_column_name], errors='coerce')
    # Drops the na values
    df.dropna(subset = [value_column_name], inplace=True)
    return df


def Immunization_data_clean(filepath: str, value_column_name: str, vaccine_name: str, age_group: str) -> pd.DataFrame:
    """
    Data cleaning and processing specifically for the immunization downloaded data
    :param filepath: path to the downloaded immunization data
    :param value_column_name: name of the main statistic column
    :param vaccine_name: name of the vaccine data is focused on
    :param age_group: name of the age group data is focused on
    :return: pd.DataFrame
    """
    df = pd.read_excel(filepath, skipfooter=1)
    df = df.rename(columns={' ': "Country"})
    df = df.melt(id_vars="Country", var_name="Year", value_name=value_column_name)
    df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
    df[value_column_name] = df[value_column_name].replace('..', np.nan).astype(str).str.replace(',', '', regex=False)
    df[value_column_name] = pd.to_numeric(df[value_column_name], errors='coerce')
    df.dropna(subset=[value_column_name], inplace=True)
    df["vaccine_name"] = vaccine_name
    df["age_group"] = age_group
    return df

def merge_downloaded_data(list_of_dfs:List[pd.DataFrame]) -> pd.DataFrame:
    """
    Merging all the dataframes that relate to one dataset
    :param list_of_dfs: all dataframes in a list that need to be merged
    :return: pd.DataFrame
    """
    # Setting the base_df
    base_df = list_of_dfs[0]
    # Using for loop, to merge every dataframe together
    for df in list_of_dfs[1:]:
        final_df = base_df.merge(df, on=['Country', 'Year'], how='inner')
        base_df = final_df
    return final_df




