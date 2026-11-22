# Imports from other python scripts
from create_database_and_tables import *
from tables_from_downloaded_data import *
from tables_from_api_data import *
from LLM_classifier import *
from LLM_query import *
import total_tokens_tracker
from total_tokens_tracker import save_session_token_log

# Third-party libraries that requires pip installation
from sqlalchemy import String, Integer, Float

def reset_database(database: str) -> None:
    """
    Resets by dropping all databases
    :param database:
    :return: None
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"DROP DATABASE IF EXISTS {database};")
    conn.commit()
    cursor.close()
    conn.close()


def main() -> None:
    """
    A main function that orders all the functions in all py files into steps, to create a functional ChatDB
    :return:None
    """
    # Creating a metadata database in mysql if it doesn't already exist
    create_database('metadata')
    print("⚠️ If the metadata database already existed, nothing was overwritten. If it did not exist, the database was created. The metadata database will store information regarding latest database refreshes. User need not worry about this\n")
    conn = get_connection('metadata')
    cursor = conn.cursor()
    # Creating a table called metadata in the metadata database if it doesn't already exist
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS metadata (
                id INT PRIMARY KEY,
                last_refresh TIMESTAMP
            )
        """)
    # Checking if refresh of data is needed, and alerting the user
    refresh = is_refresh_needed()

    if refresh:
        print("\n‼️ It looks like its been quite some time since you last refreshed the databases\n")
        print("🛑 WARNING: If you choose to refresh the database and create all the tables again, this will result in your updates to the data being lost\n")
        user_question = input('👉 Would you like to refresh all the databases and create the tables again? Input y for yes or n for no: ')

        # Refresh the data in mysql if user says yes
        if user_question.lower() == 'y' or user_question.lower() == 'yes':
            print("\n📁 Refreshing the databases and creating the tables again. Please wait for few minutes.")
            reset_database("la_crime")
            reset_database("world_public_health")
            reset_database("world_socioeconomics")

            create_database("la_crime")
            create_database("world_public_health")
            create_database("world_socioeconomics")

            immunization = immunization_final_table()
            maternal_health = maternal_health_final_table()
            non_communicable_disease = non_communicable_disease_final_table()
            life_expectancy = life_expectancy_final_table()
            nutrition = nutrition_final_table()
            sanitation = sanitation_final_table()
            education = education_final_table()
            lifestyle = lifestyle_final_table()


            create_table(immunization, "world_public_health", "immunization", primary_key_cols=["Country", "Year", "vaccine_name"],foreign_key = None, column_types = {"Country": String(100), "Year": Integer(),"vaccine_name": String(100), "coverage percentage":  Float(asdecimal=False)} )


            create_table(maternal_health, "world_public_health", "maternal_health", primary_key_cols=["Country", "Year"],foreign_key = None, column_types = {"Country": String(100), "Year": Integer(), "Number of Maternal Deaths":Integer(), "Fertility Rate - births per woman": Float(asdecimal=False), "Stillbirth rate - per 1000 total births": Float(asdecimal=False), "Prevalence of anemia among pregnant woman in %": Float(asdecimal=False)})


            create_table(non_communicable_disease, "world_public_health", "non_communicable_disease", primary_key_cols=["Country", "Year"], foreign_key = None, column_types = {"Country": String(100), "Year": Integer(), "mortality_ncd_30_70_total": Float(asdecimal=False), "mortality_ncd_30_70_female": Float(asdecimal=False), "mortality_ncd_30_70_male": Float(asdecimal=False), "hypertension_prevalence_30_79_total": Float(asdecimal=False), "hypertension_prevalence_30_79_female": Float(asdecimal=False),"hypertension_prevalence_30_79_male": Float(asdecimal=False)})


            create_table(life_expectancy, "world_public_health", "life_expectancy", primary_key_cols =["Country", "Year"], foreign_key = None, column_types = {"Country": String(100), "Year": Integer(), "le_total_at_birth": Float(asdecimal=False), "number_of_infant_deaths":Integer(), "number_of_neonatal_deaths": Integer()})


            create_table(nutrition, "world_public_health", "nutrition", primary_key_cols =["Country", "Year"], foreign_key = None, column_types = {"Country": String(100), "Year": Integer(), "low_birthweight_babies_pct": Float(asdecimal=False),"anemia_6m_59m_pct": Float(asdecimal=False), "stunting_under_5_pct": Float(asdecimal=False), "undernourishment_pct": Float(asdecimal=False)})


            create_table(sanitation, "world_socioeconomics", "sanitation", primary_key_cols =["Country", "Year"], foreign_key = None, column_types = {"Country": String(100), "Year": Integer(), "basic_sanitation_access_pct": Float(asdecimal=False), "safely_managed_drinking_water_pct": Float(asdecimal=False), "safely_managed_sanitation_pct": Float(asdecimal=False)})


            create_table(education, "world_socioeconomics", "education", primary_key_cols =["Country", "Year"], foreign_key= None, column_types = {"Country": String(100), "Year": Integer(), "literacy_rate_adult_male_pct": Float(asdecimal=False), "literacy_rate_adult_total_pct": Float(asdecimal=False), "literacy_rate_adult_female_pct": Float(asdecimal=False), "primary_completion_rate_female_pct": Float(asdecimal=False), "primary_completion_rate_male_pct": Float(asdecimal=False), "primary_completion_rate_total_pct":Float(asdecimal=False),  "secondary_enrollment_net_pct":Float(asdecimal=False), "secondary_enrollment_female_net_pct":Float(asdecimal=False),  "secondary_enrollment_male_net_pct": Float(asdecimal=False), "education_expenditure_gdp_pct":Float(asdecimal=False)})


            create_table(lifestyle, "world_socioeconomics", "lifestyle", primary_key_cols =["Country", "Year"], foreign_key= None, column_types = {"Country": String(100), "Year": Integer(), "tobacco_use_prevalence_adults_pct": Float(asdecimal=False), "overweight_prevalence_adults_pct": Float(asdecimal=False), "alcohol_consumption_per_capita_liters_15plus":Float(asdecimal=False)})


            cleaned_crime_data = load_clean_crime_data()
            print("Obtained cleaned and processed LA crime data. Will now break the dataset into multiple tables that will be uploaded to mysql")

            type_of_crime_df = type_of_crime(cleaned_crime_data)
            print("Created type of crime table from cleaned LA crime dataset")

            weapons_df = weapons(cleaned_crime_data)
            print("Created weapons table from cleaned LA crime dataset")

            locations_df = locations(cleaned_crime_data)
            print("Created locations table from cleaned LA crime dataset")

            victims_df = victims(cleaned_crime_data)
            print("Created victims table from cleaned LA crime dataset")

            crime_incident_df = crime_incident(cleaned_crime_data, weapons_df, locations_df, type_of_crime_df)
            print("Created crime incident table from cleaned LA crime dataset")

            create_table(type_of_crime_df, "la_crime", "type_of_crime", primary_key_cols = ["type_of_crime_id"], column_types = {"type_of_crime_id": String(10), "crm_cd": String(50), "crm_cd_desc": String(200)})


            create_table(locations_df, "la_crime", "locations", primary_key_cols =["location_id"], column_types = {"location_id": String(10), "area": String(100), "area_name":String(100), "rpt_dist_no":String(50), "premis_cd":String(50), "premis_desc":String(200)})


            create_table(weapons_df, "la_crime", "weapons", primary_key_cols =["weapon_id"], column_types = {"weapon_id":String(10), "weapon_used_cd":String(50), "weapon_desc":String(100)})


            create_table(crime_incident_df, "la_crime", "crime_incidents", primary_key_cols =["dr_no"], foreign_key=[{"column": "weapon_id", "ref_table":"weapons", "ref_column": "weapon_id"}, {"column": "location_id", "ref_table":"locations", "ref_column":"location_id"}, {"column":"type_of_crime_id", "ref_table":"type_of_crime","ref_column":"type_of_crime_id"}], column_types = {"dr_no": String(100), "weapon_id":String(10), "location_id":String(10), "type_of_crime_id":String(10)})


            create_table(victims_df, "la_crime", "victims", primary_key_cols = ["dr_no"], foreign_key=[{"column":"dr_no","ref_table":"crime_incidents", "ref_column": "dr_no"}], column_types = {"dr_no": String(100), "vict_age": Integer(), "vict_sex": String(10), "vict_descent": String(10)})


            # Updating the metadata table with data refresh information with the current timestamp
            update_metadata_timestamp()

    # Calling this function to start the actual ChatDB
    create_execute_sql_query()

    # Saving token usage data to a file by calling this function
    total_tokens_tracker.save_session_token_log()

if __name__ == "__main__":
    main()














