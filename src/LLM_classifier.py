# Imports from other python scripts
from create_database_and_tables import get_connection
import total_tokens_tracker

# Standard/Built-in python libraries
import json
import os

# Third-party libraries that require pip installation
from dotenv import load_dotenv
from openai import OpenAI



def get_schema(choice:str) -> str :
    """
    Retrieves the schema of SQL database
    :param choice: user's choice of database
    :return: JSON formatted string containing schema information
    """
    # Empty dictionary to store schema
    schema = {}

    # Calling the get_connection function to connect to SQL database of user's choice
    conn = get_connection(choice)
    cursor = conn.cursor()

    # Executing the SQL function, show tables; which will list all the tables in the database
    cursor.execute("show tables;")

    # Using cursor.fetchall() to obtain all rows of the query result
    # cursor.fetchall() will return a list of tuples.
    # Each tuple is a row, or in this case a table. [('weapons',), ('type_of_crime',)]
    # Iterates over each tuple in the list, obtains only the first element of the tuple (table name), appends to a list.
    tables = [table[0] for table in cursor.fetchall()]

    # Iterating though each table in tables
    # For each table, executing the SQL command describe table; which will return one row of information for each column in the table
    # Using cursor.fetchall() to fetch all the rows in the query result
    # Iterating through the list of tuples in cursor.fetchall() to obtain only the column names for each table
    # Inserting the table name as key in schema dictionary, and the list of columns in the table as the value
    for table in tables:
        cursor.execute(f"describe {table};")
        columns = [column[0] for column in cursor.fetchall()]
        schema[table] = columns

    # Converting the schema dictionary into a json formatted string, so that it can be inputted to the llm model
    schema_text = json.dumps(schema, indent=2)
    return schema_text


def classifier(prompt:str, choice:str) -> int:
    """
    Classifier llm model that returns a score that represents the level of relevancy of the user's prompt to the
    database schema
    :param prompt: user's natural language prompt
    :param choice: user's choice of database
    :return: relevancy score as integer
     """
    # Load the environment variables
    load_dotenv()

    # Obtain the api key from the .env file
    api_key = os.getenv("LLM_API_KEY")

    # Creates an OpenAI API client instance
    client = OpenAI(api_key= api_key)

    # Obtains the schema of the database that the user chose
    schema = get_schema(choice)

    # Initiates chat with the llm model
    response = client.chat.completions.create(
        # Defines the system prompt which instructs the model how to behave.
        messages=[
            {"role": "system",
             "content": """"
You are a classifier that determines the level of relevancy of the user's prompt to the SQL database.
To do this, you will internally calculate a relevancy score between 0 and 100 with 100 being the most relevant and 0 being 
the least relevant. Do not generate an sql query. Only estimate this relevancy score. To estimate a relevancy score, 
you have been given the user's prompt and a schema of the SQL database. 
Based on the schema and the user's prompt, you will estimate and return a relevancy score.  
The schema is in the form of a python dictionary. The dictionary contains the keys as the table names of the database,
and the values as the column names of the database. The prompt could mention column names that are short forms of 
column names in the database schema. For example "still birth rate" is an abbreviation for "stillbirth rate - per 
1000 births". The prompt could also contain synonyms such as add, remove, modify for INSERT, DELETE, 
or UPDATE commands. 

Some examples to guide you are the following:

If the user is focusing on the crime database:
Relevant prompts and their scores are:
What is the most common type of weapon in crime incidents? - Score: 95
What are the tables in the la_crime database? - Score: 95
What are the tables in the world_public_health database? - Score: 95
What country has the highest average stunting under 5 percentage? - Score: 95
Insert the following data into the weapons table: {data} - Score: 95
Update the following data in the weapons table: {data} - Score: 95
Delete the following data in the weapons table: {data} - Score: 95
Add the following data into the crime incidents table: {data} - Score: 95
What is the least common type of weapon in crime incidents. - Score: 95
What country has the lowest average percentage of low birthweight babies? - Score: 95
What are the top 5 countries with the highest average undernourishment percentage? - Score: 95
Delete or remove the following data from the victims table: {data to be removed} - Score: 95
Update the following data in the maternal_health table: {data to be updated} - Score: 95
How many crimes involve a knife? - Score: 85
What are the most dangerous things used in attacks? - Score: 60
Tell me what most often happens in dangerous situations? - Score: 45
What are some common items involved in incidents - Score: 50
Tell me a joke - Score: 0

Only return the relevancy score. Do not return anything else. Only return the score; do not provide any formatting 
like Score: 60. Just return the number. 
"""},
            # User message to the model, providing the schema and the user's prompt
            # This is so that the model can respond accordingly
            {"role": "user", "content": f"""Schema:
{schema}

Prompt:
{prompt}
"""}
        ],
        model="gpt-4o-mini")

    # Retrieving the response from the model
    result = response.choices[0].message.content.strip()
    total_tokens_tracker.add_tokens(response.usage.total_tokens)
    return int(result)


def helping_agent(choice:str, exception_message:str) -> str:
    """
    LLM model is acting as helping agent for user if the query execution results in an error/exception
    :param choice: user's choice of database
    :param exception_message: exception message due to query execution
    :return: helpful tips from nlp model
    """
    load_dotenv()
    api_key = os.getenv("LLM_API_KEY")

    client = OpenAI(api_key=api_key)
    schema = get_schema(choice)

    response = client.chat.completions.create(
        messages=[
            {"role": "system",
             "content": """"You are an AI helping agent for the user when executing the SQL query results in an 
             exception/error. You are given the exception message, and based on that you are to provide the user with some helpful tips on what the exception message means, and how the user can change his prompt accordingly.  
"""},
            {"role": "user", "content": f"""Exception Message:
{exception_message}
"""}
        ],
        model="gpt-4o-mini")

    result = response.choices[0].message.content.strip()
    total_tokens_tracker.add_tokens(response.usage.total_tokens)
    return result

