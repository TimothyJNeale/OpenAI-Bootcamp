# Search on embedded documants 

######################################### IMPORTS #############################################
import openai
import logging
import os

import pandas as pd
import numpy as np

import ast
import tiktoken

from dotenv import load_dotenv

######################################## CONSTANTS ############################################

DATA_DIRECTORY ='data'
DATA_FILE = 'unicorns.csv'
TRAINING_COST_PER_1KTOKEN = 0.0004

########################################### DATA ##############################################

# load environment variables from .env file
load_dotenv()


##################################### HELPER FUCTIONS #########################################

# Use chat completion
def get_chat_completion(prompt, model="gpt-3.5-turbo", temperature=0):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message["content"]

# Standard completion
def get_completion(prompt, model="gpt-3.5-turbo-instruct", temperature=0, max_tokens=300, stop="\"\"\""):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        stop=stop)

    return response.choices[0].text

# Get the number of tokens in a string
def get_num_tokens_from_string(string, encoding_name="gpt2"):
    tokenizer = tiktoken.get_encoding(encoding_name)
    tokens = tokenizer.encode(string)

    return len(tokens)

def summary(compnay, crunchbase_url, city, country, industry, investor_list):
    investors = "The investors in the compaany are "
    for investor in ast.literal_eval(investor_list):
        investors += investor + ", "
    investors = investors[:-2] + "."
    text = f"{compnay} is a company based in {city}, {country}. It is in the {industry} industry. {investors}"
    return text

def get_embedding(text):
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response['data'][0]['embedding']

def vector_simliarity(v1, v2):
    # logging.info(v1)
    # logging.info(type(v1))
    # logging.info(v2)
    # logging.info(type(v2))

    return np.dot(np.array(v1), np.array(v2))

def prompt_with_context(context):
    prompt = f'''
    Only answer the question below if you are 100% certain of the facts. If you are not certain, please leave the answer blank.
    Context: {context}
    Q: What does the company do and who are the investors and how much seed funding have they provided?
    A: '''
    return prompt

######################################## LOGGING ##############################################

logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.DEBUG) # Supress debugging output from modules imported
#logging.disable(logging.CRITICAL) # Uncomment to disable all logging

######################################### START ###############################################
logging.info('Start of program')

# Get the current DATA directory
home = os.getcwd()
data_dir = os.path.join(home, DATA_DIRECTORY)
logging.info(data_dir)

os.chdir(data_dir)

# Authenticate with OpenAI                             
api_key = os.environ["OPENAI_API_KEY"]
openai.api_key = api_key

########################################## MAIN ###############################################
logging.info('Main section entered')

# Load the data using pandas
df = pd.read_csv(DATA_FILE)
logging.info(df.head())
logging.info(df.shape)
logging.info(df.columns)

# Create a summary column
df['summary'] = df.apply(lambda df: summary(df['Company'], df['Crunchbase Url'], df['City'], df['Country'], df['Industry'], df['Investors']), axis=1)
# logging.info(df.columns)

# Find the number of tokens in first summary
logging.info(df['summary'][0])
logging.info(len(df['summary'][0]))
logging.info(get_num_tokens_from_string(df['summary'][0]))

# Calculate the number of tokens in the summary column
df['token_count'] = df.apply(lambda df: get_num_tokens_from_string(df['summary'],"cl100k_base"), axis=1)
# logging.info(df.columns)

total_tokens = df['token_count'].sum()
logging.info(total_tokens)

embeddings_cost = total_tokens * TRAINING_COST_PER_1KTOKEN / 1000
logging.info(embeddings_cost)

# # Get the embedding for the first summary
# logging.info(df['summary'][0])
# logging.info(get_embedding(df['summary'][0]))

# # Get the embeddings for all summaries
# df['embedding'] = df['summary'].apply(get_embedding)
# logging.info(df.columns)
# df.to_csv('unicorns_with_embeddings.csv', index=False)

# Load the embeddings from the csv
df_embeddings = pd.read_csv('unicorns_with_embeddings.csv')
# logging.info(df_embeddings.columns)

prompt = "What does the company Greater Bay Technology do and who invested in it?"
promp_embedding = get_embedding(prompt)
logging.info(type(promp_embedding))
logging.info(type(df_embeddings['embedding']))

# Calculate the distance between the prompt and the first summary
# logging.info(df_embeddings['embedding'][0]) # This is a string
# logging.info(type(df_embeddings['embedding'][0]))
# logging.info(ast.literal_eval(df_embeddings['embedding'][0])) # This is a list
# logging.info(type(ast.literal_eval(df_embeddings['embedding'][0])))
# logging.info(np.array(ast.literal_eval(df_embeddings['embedding'][0]))) # This is a numpy array
# prompt_simliarity = vector_simliarity(ast.literal_eval(df_embeddings['embedding'][0]), promp_embedding)


df_embeddings['l_embeddings'] = df_embeddings['embedding'].apply(ast.literal_eval)
df_embeddings['prompt_similarity'] = df_embeddings['l_embeddings'].apply(lambda x: vector_simliarity(x, promp_embedding))

company = df_embeddings.nlargest(1, 'prompt_similarity')['summary'].values[0]
logging.info(company)

prompt = prompt_with_context(company)
logging.info(prompt)

response = get_completion(prompt, temperature=0, max_tokens=512)
logging.info(response)

######################################### FINISH ##############################################
logging.info('End of program')