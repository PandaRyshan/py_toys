# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import os
import openai
import json
import ipdb


env_backup = os.environ.copy()

with open('./conf/openai_api_key.txt', 'r') as f:
    os.environ['OPENAI_API_KEY'] = f.read().strip()

openai.api_key = os.environ.get('OPENAI_API_KEY')

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the \
            World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}
    ]
)

# {"role": "assistant", "content": "The World Series was played at Dodger"}
answer = response['choices'][0]['message']

print(answer)
