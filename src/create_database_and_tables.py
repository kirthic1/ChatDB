# Standard/built-in python libraries
import os
from datetime import datetime, timedelta
# For type hints
from typing import Optional, List, Dict

# Third-party libraries to be installed with pip
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import pymysql
from dotenv import load_dotenv
# For type hints
from mysql.connector.connection import MySQLConnection
from sqlalchemy.engine import Engine
from sqlalchemy.types import TypeEngine



def get_connection(db:Optional[str] = None) -> MySQLConnection:
    """
    Connecting to the mysql server or a specific database in the mysql server using the mysql.connector method
    :param db: name of database to connect to
    :return: MySQLConnection
    """
    # Load all environment variables to connect to mysql
    load_dotenv()
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST', "localhost")
    # If db is None, then just connect to the mysql server
    if db is None:
        return mysql.connector.connect(user=user, password=password, host=host)
    # If specific db name is inputted, connect to that specific database
    else:
        return mysql.connector.connect(user=user, password=password, host=host, database=db)


def create_database(name: str) -> str:
    """
    Creating a database in mysql using mysql.connector method
    :param name: name of database
    :return: a string informing the user that database created successfully
    """
    conn = get_connection()
    cursor = conn.cursor()
    # Only create the database if it doesn't already exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {name};")
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ {name} database created successfully")

def get_sqlalchemy_engine(db: str) -> Engine:
    """
    Creating sqlalchemy engine for mysql in order to create tables in mysql
    :param db: name of database to connect to
    :return: sql alchemy engine
    """
    load_dotenv()
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST", "localhost")
    # Using sqlalchemy to create an engine object that will talk to MySQL database.
    # sqlalchemy will translate the python command into a SQL command
    # This engine uses pymysql as the driver or "messenger" to connect to the database and send SQL commands
    return create_engine(f"mysql+pymysql://{user}:{password}@{host}/{db}")

def create_table(df: pd.DataFrame, database: str, table: str, primary_key_cols: Optional[List[str]] = None, foreign_key: Optional[List[Dict[str,str]]] = None, column_types: Optional[Dict[str, TypeEngine]] = None) -> None:
    """
    Creating tables in mysql using sqlalchemy.
    :param df: dataframe to upload as table in mysql
    :param database: name of database to connect to
    :param table: name of table to create
    :param primary_key_cols: list of columns to declare as primary keys in mysql
    :param foreign_key: list of dictionaries to declare the foreign keys and their references
    :param column_types: dictionary of column types to declare when creating table in mysql
    :return: None
    """
    # Creating table in mysql use sqlalchemy
    try:
        engine = get_sqlalchemy_engine(database)
    except Exception:
        print("❗️Something went wrong - I couldn't connect to the sql database. Lets make sure it is created.")
        create_database(database)
        engine = get_sqlalchemy_engine(database)

    try:
        # Dropping any rows where there are null values in the primary_key_cols to be extra cautious
        df.dropna(subset=primary_key_cols, inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.to_sql(table, con=engine, if_exists='replace', index=False, dtype=column_types)
        print(f"✅ Successfully wrote `{table}` to database.")
    except Exception as e:
        print(f"❌ Failed to upload `{table}`: {e}")
        return

    # Connecting to database using mysql.connector in order to add primary keys and foreign keys
    conn = get_connection(database)
    cursor = conn.cursor()

    # Defining the primary keys
    if primary_key_cols:
        pk_clause = ", ".join(primary_key_cols)
        try:
            cursor.execute(f"ALTER TABLE {table} ADD PRIMARY KEY ({pk_clause});")
            print(f"✅ Primary key added to `{table}` on column: {pk_clause}")
        except Exception as e:
            print(f"❌ Failed to add primary key to `{table}`: {e}")


    # Defining the foreign keys
    if foreign_key:
        for fk in foreign_key:
            fk_column = fk["column"]
            ref_table = fk["ref_table"]
            ref_column = fk["ref_column"]
            constraint_name = f"fk_{table}_{fk_column}"
            cursor.execute(f"""ALTER TABLE {table} ADD CONSTRAINT {constraint_name} FOREIGN KEY ({fk_column}) REFERENCES {ref_table}({ref_column});""")

    # Committing the changes so that the changes to the database (primary keys and foreign keys) is saved
    conn.commit()
    cursor.close()
    conn.close()

def update_metadata_timestamp() -> None:
    """
    Updating the metadata table in the metadata database with the timestamp of the last data refresh
    :return: None
    """
    # Using mysql.connector to connect to metadata database, and insert values into metadata table
    conn = get_connection('metadata')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO metadata (id, last_refresh)
        VALUES (1, NOW())
        ON DUPLICATE KEY UPDATE last_refresh = NOW()
    """)
    conn.commit()
    conn.close()

def is_refresh_needed() -> bool:
    """
    Calculating the number of days it has been since the last data refresh
    If number of days since last data refresh is greater than 3, returning boolean value True, else return boolean value False
    :return: None
    """
    conn = get_connection('metadata')
    cursor = conn.cursor()
    cursor.execute("SELECT last_refresh FROM metadata WHERE id = 1")
    # fetchone() obtains only the next single row as a tuple
    result = cursor.fetchone()
    conn.close()

    if not result or result[0] is None:
        return True  # No refresh has happened yet

    last_refresh = result[0]
    now = datetime.now()
    time_since_refresh = now - last_refresh

    print(f"🕒 Last database refresh was {time_since_refresh.days} days ago.")

    threshold_days = 3
    return time_since_refresh > timedelta(days=threshold_days)










