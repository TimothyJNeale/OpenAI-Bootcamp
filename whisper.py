# Use the whisper API
######################################### IMPORTS #############################################
import openai
import logging
import os

from dotenv import load_dotenv

######################################## CONSTANTS ############################################

DATA_DIRECTORY ='data'

########################################### DATA ##############################################

# load environment variables from .env file
load_dotenv()

##################################### HELPER FUCTIONS #########################################

# Standard completion
def get_completion(prompt, model="gpt-3.5-turbo-instruct", temperature=0, max_tokens=300, stop="\"\"\""):
    response = openai.Completion.create(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        stop=stop)

    return response.choices[0].text

######################################## LOGGING ##############################################
logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.DEBUG) # Supress debugging output from modules imported
#logging.disable(logging.CRITICAL) # Uncomment to disable all logging

######################################## CLASSES ##############################################



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

# Read the audio file
audio_file =  open("Warren_Buffett_On_Exposing_Business_Frauds_And_Deception.mp3", "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)
audio_file.close()

write_file = open("transcript.txt", "w")
write_file.write(transcript['text'])
write_file.close()

# get a summary of the transcript
prompt = f'''
Produce a summary of the following: 
Transcript: {transcript['text']}
Summary: '''

summary = get_completion(prompt, max_tokens=500)
summary_file = open("summary.txt", "w")
summary_file.write(summary)
summary_file.close()

######################################### FINISH ##############################################
logging.info('End of program')