''' Application to create exam questions from a text file'''

import openai
from dotenv import load_dotenv
import os

# load environment variables from .env file
load_dotenv()

# get api key from environment variable
openai.api_key = os.environ["OPENAI_API_KEY"]

# Create the test prompt
def create_test_prompt2(topic, num_questions, num_possible_answers):
    prompt = f"Topic: {topic}\n\n"
    for i in range(num_questions):
        prompt += f"Question {i+1}: "
        prompt += "__________\n\n"
        for j in range(num_possible_answers):
            prompt += f"- Option {j+1}\n"
        prompt += "\n"
    return prompt

# prompt = create_test_prompt2("Python", 5, 4)
# print(prompt)

# Create the test prompt for input to a LLM
def create_test_prompt(topic, num_questions, num_possible_answers):
    prompt = f"""Create a multiple choice quiz on the topic of {topic} consisting of {num_questions} questions.
                 Each question should have {num_possible_answers} as options.
                 Also include the correct answer for each question usinf the starting string 'Correct Answer: '"""
    return prompt

prompt = create_test_prompt("Scitish History", 4, 4)
print(prompt)

response = openai.Completion.create(engine="text-davinci-003",
                                    prompt=prompt,
                                    max_tokens=256,
                                    temperature=0.0)
print(response['choices'][0]['text'])