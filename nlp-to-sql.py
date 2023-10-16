''' Application to convert natural language to SQL query'''

import openai
from dotenv import load_dotenv
import os

import pandas as pd

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text

# load environment variables from .env file
load_dotenv()

# get api key from environment variable
openai.api_key = os.environ["OPENAI_API_KEY"]

# Use pandas to read the csv file
df = pd.read_csv('data/sales_data_sample.csv')

# Create a connection to a database in the memory
temp_db = create_engine('sqlite:///:memory:', echo=False)

# Create a table from the pandas dataframe
data = df.to_sql(name='Sales', con=temp_db)
print(data)

# Create a connection to the database
with temp_db.connect() as conn:
    # Execute a SQL query
    result = conn.execute(text("SELECT * FROM Sales LIMIT 5"))
    # Print the result
    for row in result:
        print(row)