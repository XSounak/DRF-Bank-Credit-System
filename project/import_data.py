import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# PostgreSQL connection settings
db_settings = {
    "dbname": "db",
    "user": "debasis",
    "password": "password",
    "host": "localhost",
    "port": "5432",
}

# Excel file paths
customer_data_path = "/home/intern/project/customer_data.xlsx"
loan_data_path = "/home/intern/project/loan_data.xlsx"

# Read Excel sheets into Pandas DataFrames
customer_df = pd.read_excel(customer_data_path)
loan_df = pd.read_excel(loan_data_path)

# Establish a connection to PostgreSQL
connection = psycopg2.connect(**db_settings)
cursor = connection.cursor()

# Create SQLAlchemy engine for efficient data transfer
engine = create_engine(f"postgresql://{db_settings['user']}:{db_settings['password']}@{db_settings['host']}:{db_settings['port']}/{db_settings['dbname']}")

# Ingest Customer Data into PostgreSQL
customer_df.to_sql('Customer', engine, if_exists='replace', index=False)

# Ingest Loan Data into PostgreSQL
loan_df.to_sql('Loan', engine, if_exists='replace', index=False)

# Commit changes and close the connection
connection.commit()
connection.close()
