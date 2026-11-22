# Standard/Built-in python libraries
import os

# Imports from other python scripts
from clean_merge_downloaded_data import merge_downloaded_data
from clean_merge_downloaded_data import clean_downloaded_data
from clean_merge_downloaded_data import Immunization_data_clean

# Third-party libraries to be installed with pip
import pandas as pd


processed_final_data = "../processed_final_data/downloaded"
def immunization_final_table() -> pd.DataFrame:
    """
    Creating the final immunization table by concatenating all the cleaned sub-datasets
    :return: immunization table/pandas dataframe
    """
    DPT_12m_23m = Immunization_data_clean("../raw_data/downloaded/Immunization/DPT % of children 12-23 months.xlsx",
                                          "coverage percentage",
                                          "DPT", "12-23 months")
    HepB3_1 = Immunization_data_clean("../raw_data/downloaded/Immunization/HepB3 % of one-year-old children.xlsx", "coverage percentage",
                                      "HepB3", "1 year")
    Hib3_12m_23m = Immunization_data_clean("../raw_data/downloaded/Immunization/Hib3 % of children ages 12-23 months.xlsx",
                                           "coverage percentage", "Hib3", "12-23 months")
    measles_12m_23m = Immunization_data_clean("../raw_data/downloaded/Immunization/measles % of children ages 12-23 months.xlsx",
                                              "coverage percentage", "MCV", "12-23 months")
    measles_2nd_dose = Immunization_data_clean(
        "../raw_data/downloaded/Immunization/measles second dose % of children by the nationally recommended age.xlsx", "coverage percentage",
        "MCV2", "national recommended age")
    Pol3_1 = Immunization_data_clean("../raw_data/downloaded/Immunization/Pol3 % of one-year-old children.xlsx", "coverage percentage", "Pol3",
                                     "1 year")
    BCG_1 = Immunization_data_clean("../raw_data/downloaded/Immunization/BCG % of one-year-old children.xlsx", "coverage percentage", "BCG",
                                    "1 year")

    immunization_table = pd.concat([DPT_12m_23m, HepB3_1, Hib3_12m_23m, measles_12m_23m, measles_2nd_dose, Pol3_1, BCG_1])

    immunization= os.path.join(processed_final_data, "immunization.xlsx")
    immunization_table.to_excel(immunization, index=False)

    return immunization_table

def maternal_health_final_table() -> pd.DataFrame:
    """
    Creating the final maternal health table by concatenating all the cleaned sub-datasets
    :return: maternal health table/pandas dataframe
    """
    maternal_deaths = clean_downloaded_data("../raw_data/downloaded/Maternal Health/Number of maternal deaths.xlsx",
                                            "Number of Maternal Deaths")
    fertility_rate = clean_downloaded_data("../raw_data/downloaded/Maternal Health/Fertility rate total births per woman.xlsx",
                                           "Fertility Rate - births per woman")
    stillbirth_rate = clean_downloaded_data("../raw_data/downloaded/Maternal Health/Stillbirth rate per 1,000 total births.xlsx",
                                            "Stillbirth rate - per 1000 total births")
    prevalence_of_anemia = clean_downloaded_data("../raw_data/downloaded/Maternal Health/Prevalence of anemia among pregnant women %.xlsx",
                                                 "Prevalence of anemia among pregnant woman in %")

    list_of_dataframes = [maternal_deaths, fertility_rate, stillbirth_rate, prevalence_of_anemia]

    maternal_health_table = merge_downloaded_data(list_of_dataframes)

    maternal_health = os.path.join(processed_final_data, "maternal_health.xlsx")
    maternal_health_table.to_excel(maternal_health, index=False)

    return maternal_health_table

def non_communicable_disease_final_table() -> pd.DataFrame:
    """
    Creating the final non-communicable disease table by concatenating all the cleaned sub-datasets
    :return: non-communicable disease table/pandas dataframe
    """
    mortality_rate_cvd_cancer_crd_diabetes = clean_downloaded_data(
        "../raw_data/downloaded/Non Communicable Diseases/Mortality from CVD cancer diabetes or CRD btwn ages 30-70 %.xlsx",
        "mortality_ncd_30_70_total")
    mortality_rate_cvd_cancer_crd_diabetes_female = clean_downloaded_data(
        "../raw_data/downloaded/Non Communicable Diseases/Mortality from CVD, cancer, diabetes or CRD btwn ages 30-70 female %.xlsx",
        "mortality_ncd_30_70_female")
    mortality_rate_cvd_cancer_crd_diabetes_male = clean_downloaded_data(
        "../raw_data/downloaded/Non Communicable Diseases/Mortality from CVD, cancer, diabetes or CRD btwn ages 30-70 male %.xlsx",
        "mortality_ncd_30_70_male")
    prevalence_of_hypertension_adults_ages_30_79 = clean_downloaded_data(
        "../raw_data/downloaded/Non Communicable Diseases/Prevalence of hypertension % of adults ages 30-79.xlsx",
        "hypertension_prevalence_30_79_total")
    percent_of_female_adults_ages_30_to_79_with_hypertension = clean_downloaded_data(
        "../raw_data/downloaded/Non Communicable Diseases/% of female adults  ages 30 to 79 with hypertension.xlsx",
        "hypertension_prevalence_30_79_female")
    percent_of_male_adults_ages_30_to_79_with_hypertension = clean_downloaded_data(
        "../raw_data/downloaded/Non Communicable Diseases/% of  male adults ages 30 to 79 with hypertension.xlsx",
        "hypertension_prevalence_30_79_male")

    list_of_dataframes = [
        mortality_rate_cvd_cancer_crd_diabetes,
        mortality_rate_cvd_cancer_crd_diabetes_male,
        mortality_rate_cvd_cancer_crd_diabetes_female,
        prevalence_of_hypertension_adults_ages_30_79,
        percent_of_female_adults_ages_30_to_79_with_hypertension,
        percent_of_male_adults_ages_30_to_79_with_hypertension
    ]

    non_communicable_disease_final_table = merge_downloaded_data(list_of_dataframes)

    non_communicable_disease = os.path.join(processed_final_data, "non_communicable_disease.xlsx")
    non_communicable_disease_final_table.to_excel(non_communicable_disease, index=False)

    return non_communicable_disease_final_table

def life_expectancy_final_table() -> pd.DataFrame:
    """
    Creating the final life expectancy table by concatenating all the cleaned sub-datasets
    :return: life expectancy table/pandas dataframe
    """
    le_total_at_birth = clean_downloaded_data("../raw_data/downloaded/Life Expectancy/le_total_at_birth.xlsx", "le_total_at_birth")
    infant_deaths = clean_downloaded_data("../raw_data/downloaded/Life Expectancy/number_of_infant_deaths.xlsx", "number_of_infant_deaths")
    neonatal_deaths = clean_downloaded_data("../raw_data/downloaded/Life Expectancy/number_of_neonatal_deaths.xlsx",
                                            "number_of_neonatal_deaths")

    list_of_dataframes = [le_total_at_birth, infant_deaths, neonatal_deaths]

    life_expectancy_final_table = merge_downloaded_data(list_of_dataframes)

    life_expectancy = os.path.join(processed_final_data, "life_expectancy.xlsx")
    life_expectancy_final_table.to_excel(life_expectancy, index=False)

    return life_expectancy_final_table

def nutrition_final_table() -> pd.DataFrame:
    """
    Creating the final nutrition table by concatenating all the cleaned sub-datasets
    :return: nutrition table/pandas dataframe
    """
    low_birth_weight_babies = clean_downloaded_data("../raw_data/downloaded/Nutrition/% of low birth-weight babies.xlsx",
                                              "low_birthweight_babies_pct")
    anemia_prevalence = clean_downloaded_data("../raw_data/downloaded/Nutrition/Prevalence of anemia % of children ages 6-59 months.xlsx",
                                        "anemia_6m_59m_pct")
    stunting_prevalence = clean_downloaded_data(
        "../raw_data/downloaded/Nutrition/Prevalence of stunting, height for age modeled estimate, % of children under 5.xlsx",
        "stunting_under_5_pct")
    undernourishment_prevalence = clean_downloaded_data("../raw_data/downloaded/Nutrition/Prevalence of undernourishment% of population.xlsx",
                                                  "undernourishment_pct")

    list_of_dataframes = [low_birth_weight_babies, anemia_prevalence, stunting_prevalence, undernourishment_prevalence]

    nutrition_final_table = merge_downloaded_data(list_of_dataframes)

    nutrition = os.path.join(processed_final_data, "nutrition.xlsx")
    nutrition_final_table.to_excel(nutrition, index=False)

    return nutrition_final_table

def sanitation_final_table() -> pd.DataFrame:
    """
    Creating the final sanitation table by concatenating all the cleaned sub-datasets
    :return: sanitation table/pandas dataframe
    """
    basic_sanitation_access_pct = clean_downloaded_data(
        "../raw_data/downloaded/Sanitation Services/People using at least basic sanitation services % of population.xlsx",
        "basic_sanitation_access_pct")
    safely_managed_drinking_water_pct = clean_downloaded_data(
        "../raw_data/downloaded/Sanitation Services/People using safely managed drinking water services % of population.xlsx",
        "safely_managed_drinking_water_pct")
    safely_managed_sanitation_pct = clean_downloaded_data(
        "../raw_data/downloaded/Sanitation Services/People using safely managed sanitation services % of population.xlsx",
        "safely_managed_sanitation_pct")


    list_of_dataframes = [basic_sanitation_access_pct, safely_managed_drinking_water_pct,
                          safely_managed_sanitation_pct]

    sanitation_final_table = merge_downloaded_data(list_of_dataframes)

    sanitation = os.path.join(processed_final_data, "sanitation.xlsx")
    sanitation_final_table.to_excel(sanitation, index=False)

    return sanitation_final_table

def education_final_table() -> pd.DataFrame:
    """
    Creating the final education table by concatenating all the cleaned sub-datasets
    :return: education table/pandas dataframe
    """
    literacy_rate_adult_male_pct = clean_downloaded_data(
        "../raw_data/downloaded/Education/Literacy rate, adult male % of males ages 15 and above.xlsx", "literacy_rate_adult_male_pct")
    literacy_rate_adult_total_pct = clean_downloaded_data(
        "../raw_data/downloaded/Education/Literacy rate, adult total % of people ages 15 and above.xlsx", "literacy_rate_adult_total_pct")
    literacy_rate_adult_female_pct = clean_downloaded_data(
        "../raw_data/downloaded/Education/Literacy rate, adult female % of females ages 15 and above.xlsx", "literacy_rate_adult_female_pct")

    primary_completion_rate_female_pct = clean_downloaded_data(
        "../raw_data/downloaded/Education/Primary completion rate, female % of relevant age group.xlsx", "primary_completion_rate_female_pct")
    primary_completion_rate_male_pct = clean_downloaded_data(
        "../raw_data/downloaded/Education/Primary completion rate, male % of relevant age group.xlsx", "primary_completion_rate_male_pct")
    primary_completion_rate_total_pct = clean_downloaded_data(
        "../raw_data/downloaded/Education/Primary completion rate, total % of relevant age group.xlsx", "primary_completion_rate_total_pct")

    secondary_enrollment_net_pct = clean_downloaded_data("../raw_data/downloaded/Education/School enrollment, secondary %net.xlsx",
                                                   "secondary_enrollment_net_pct")
    secondary_enrollment_female_net_pct = clean_downloaded_data("../raw_data/downloaded/Education/School enrollment, secondary, female % net.xlsx",
                                                          "secondary_enrollment_female_net_pct")
    secondary_enrollment_male_net_pct = clean_downloaded_data("../raw_data/downloaded/Education/School enrollment, secondary, male % net.xlsx",
                                                        "secondary_enrollment_male_net_pct")

    education_expenditure_gdp_pct = clean_downloaded_data("../raw_data/downloaded/Education/Public spending on education, total % of GDP.xlsx",
                                                    "education_expenditure_gdp_pct")

    list_of_dataframes = [literacy_rate_adult_male_pct, literacy_rate_adult_female_pct,
                          literacy_rate_adult_total_pct, primary_completion_rate_female_pct,
                          primary_completion_rate_male_pct,
                          primary_completion_rate_total_pct, secondary_enrollment_net_pct,
                          secondary_enrollment_female_net_pct, secondary_enrollment_male_net_pct,
                          education_expenditure_gdp_pct]
    education_final_table = merge_downloaded_data(list_of_dataframes)

    education = os.path.join(processed_final_data, "education.xlsx")
    education_final_table.to_excel(education, index=False)

    return education_final_table

def lifestyle_final_table() -> pd.DataFrame:
    """
    Creating the final lifestyle table by concatenating all the cleaned sub-datasets
    :return: lifestyle table/pandas dataframe
    """
    tobacco_use_prevalence_adults_pct = clean_downloaded_data("../raw_data/downloaded/Lifestyle/Prevalence of current tobacco use % of adults.xlsx",
                                                        "tobacco_use_prevalence_adults_pct")
    overweight_prevalence_adults_pct = clean_downloaded_data("../raw_data/downloaded/Lifestyle/Prevalence of overweight % of adults.xlsx",
                                                       "overweight_prevalence_adults_pct")
    alcohol_consumption_per_capita_liters_15plus = clean_downloaded_data(
        "../raw_data/downloaded/Lifestyle/Total alcohol consumption per capita liters of pure alcohol, projected estimates, 15+ years of age.xlsx",
        "alcohol_consumption_per_capita_liters_15plus")

    list_of_dataframes = [tobacco_use_prevalence_adults_pct, overweight_prevalence_adults_pct, alcohol_consumption_per_capita_liters_15plus]

    lifestyle_final_table = merge_downloaded_data(list_of_dataframes)

    lifestyle = os.path.join(processed_final_data, "lifestyle.xlsx")
    lifestyle_final_table.to_excel(lifestyle, index=False)

    return lifestyle_final_table










