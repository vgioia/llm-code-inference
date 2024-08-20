import os
import requests
from datetime import datetime

URL = 'http://localhost:11434/api/chat'

PROMPTS_ROOT_PATH = './prompts'
SYSTEM_PROMPT_FPATH = f'{PROMPTS_ROOT_PATH}/system/system.txt'
USER_PROMPTS_FPATH = f'{PROMPTS_ROOT_PATH}/user'
RUNS_PATH = './runs'


def llama3(sys_prompt, user_prompt):
    data = {
        "model": "llama3",
        "messages": [
            {
              "role": "system",
              "content": sys_prompt
            },
            {
              "role": "user",
              "content": user_prompt
            }
        ],
        "stream": False
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(URL, headers=headers, json=data)
    
    return(response.json()['message']['content'])

def clean_up_res(res):
    return res.replace('```', '')

with open(SYSTEM_PROMPT_FPATH, 'r') as f:
    system_prompt = f.read()


for filename in os.listdir(USER_PROMPTS_FPATH):

    file_path = os.path.join(USER_PROMPTS_FPATH, filename)

    print(filename)
    if filename != 'A':
        continue

    with open(file_path, 'r') as f:
        user_prompt = f.read()

        begin = datetime.now()
        print('Started code generation')

        response = llama3(system_prompt, user_prompt)

        file_prefix = filename.split('.')[0]

        with open(f'{RUNS_PATH}/{file_prefix}', 'w') as f:
            f.write(response)

        print(f'Executed in {(datetime.now() - begin).total_seconds():.2f} seconds')