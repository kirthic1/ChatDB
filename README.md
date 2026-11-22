# DSCI 551 Final Project

## Name of the Project
ChatDB – Talking to MySQL Database Management System using Natural Language
## Team Members (Name and Student IDs)
Kirthi Chillakanti 
Student ID: 8900-2352-76
Email: kchillak@usc.edu

## Introduction
This project is a natural language interface to the relational database management system, MySQL. First, this interface 
prompts the user to ask a question, in human/natural language, about the data in the MySQL databases. In the backend, 
the question will be parsed, and a formal SQL query will be created to answer the user's question. The SQL query 
will then be executed, and the results/answer will be returned to the user. The user can query an LA crime database, a 
world public health database, and a world socioeconomics database.

## Instructions to create a conda environment
1. Install Conda 
2. conda create -n name_of_env python=3.12.4 
3. conda activate name_of_env

## Software Installed 
1. MySQL server

## Instructions on how to install the required libraries
1. Ensure steps 1-3 in "Instructions to create a conda environment" are done
2. Change directory (cd in Terminal) to the ChatDB folder
3. pip install -r requirements.txt

## Accessing the Raw Data
The raw datasets required to run ChatDB are available in the GitHub Releases section. 
1. Download raw_data.zip from the latest release.
2. Extract the ZIP file.
3. Place the extracted raw_data folder in the ChatDB directory.

## How the Raw Data Was Collected
The following provides information on how the raw crime dataset (API data) was collected.
The code automatically collects the raw crime data. 
The user just needs to sign up for an App token. 
Crime Data from API
1. Go to https://data.lacity.org/Public-Safety/Crime-Data-from-2020-to-Present/2nrs-mtv8/about_data
2. Click on Export, API Endpoint, API documentation
3. Sign up for App token
4. Use the App token in request to API
5. Use offset and limit parameters to retrieve data in small sets (already implemented in my code)

The following provides information on how the raw Immunization, Education, Lifestyle, Life Expectancy, Maternal Health, Non-Communicable Diseases, Nutrition, and Sanitation Services data was collected.
This is the downloaded data. This has already been provided in the raw_data.zip file under GitHub Releases.
1. Go to https://databank.worldbank.org/source/health-nutrition-and-population-statistics
2. Select the same countries, years, and measures as indicated in the raw data folders
3. Click download as Excel

The code will automatically clean and process all raw data, and upload the processed data tables into the corresponding database in MySQL.

## Instructions regarding creating a .env file 
1. There is a file called .env copy in the src folder. This is a template .env file for users
2. In this template, users must type their own passwords/tokens
3. DB_HOST, DB_PASSWORD, DB_USER is regarding the user's credentials to connect to the user's local MySQL server
4. CRIME_DATA_APP_TOKEN is the App token needed to request the LA crime data from the API
5. LLM_API_KEY is the key required for the LLM model, gpt-4o-mini, in the code, to function. 
6. To obtain the LLM_API_KEY:
        a. Sign up here: https://auth.openai.com/log-in
        b. Click on Libraries under "Get Started"
        c. Click on "create an API key in the dashboard"
        d. Click on "Create new secret key"
7. Ensure to rename the .env copy file to just .env

## Instructions on how to start interface 
1. Ensure steps 1-4 in "Instructions on how to install the required libraries" are done
2. Ensure all steps in "Instructions regarding creating a .env file" are done
3. Inside the ChatDB, move to the src folder
4. Open a new terminal session
5. Make sure to activate the conda environment that was created as part of previous instructions
6. Type the following command as is: python main.py 

## Other Notes
1. The "Victims Table - Victims Descent Code Meaning" file refers to the vict_descent column in the victims table. This 
   table provides the meaning for each vict_descent code in the data
