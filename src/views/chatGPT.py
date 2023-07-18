# Note: you need to be using OpenAI Python v0.27.0 for the code below to work
import os
import openai
import json


openai.api_key = os.environ.get('OPENAI_API_KEY')

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are my English learning assistant, \
            talking with me and correcting my mistakes."},
        {"role": "user", "content": "Hello, how are you?"},
    ]
)

# {"role": "assistant", "content": "The World Series was played at Dodger"}
answer = response['choices'][0]['message']

print(answer)
