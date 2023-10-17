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

''' A function that takes a pandas data frame and returns a string decsribing the dataframe
ready to be passed to a GPT-3 engine'''
def create_table_definition(df):
    prompt = """### sqlite SQL table, with its properties:
    #
    # Sales ({})
    #
    """.format(', '.join(str(col) for col in df.columns))

    return prompt

def prompt_input():
    nlp_text = input("Enter your natural language query: ")
    return nlp_text

def combine_prompt(df, nlp_text):
    definition = create_table_definition(df)
    query_init_string = f"### A query to answer: {nlp_text}\nSELECT"
    return definition + query_init_string

# Use pandas to read the csv file
df = pd.read_csv('data/sales_data_sample.csv')

# Create a connection to a database in the memory
temp_db = create_engine('sqlite:///:memory:', echo=False)

# Create a table from the pandas dataframe
data = df.to_sql(name='Sales', con=temp_db)

nlp_text = prompt_input()
print(nlp_text)
print(create_table_definition(df))

prompt = combine_prompt(df, nlp_text)
print(prompt)

# Create a connection to the database
# with temp_db.connect() as conn:
#     # Execute a SQL query
#     result = conn.execute(text("SELECT * FROM Sales LIMIT 5"))
#     # Print the result
#     for row in result:
#         print(row)



