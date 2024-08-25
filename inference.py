import os
import requests
from datetime import datetime

URL = 'http://localhost:11434/api/chat'

PROMPTS_ROOT_PATH = './prompts'
SYSTEM_PROMPT_FPATH = f'{PROMPTS_ROOT_PATH}/system/system.txt'
USER_PROMPTS_FPATH = f'{PROMPTS_ROOT_PATH}/user'
RUNS_PATH = './runs'
RUNS_PER_PROBLEM = 2

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

with open(SYSTEM_PROMPT_FPATH, 'r') as f:
    system_prompt = f.read()

run_datetime = datetime.now().strftime('%Y%m%d%H%M') 
run_name = f'{run_datetime}_llama3_8b'
os.mkdir(f'{RUNS_PATH}/{run_name}')

for filename in os.listdir(USER_PROMPTS_FPATH):

    file_path = os.path.join(USER_PROMPTS_FPATH, filename)

    with open(file_path, 'r') as f:
        user_prompt = f.read()

        file_prefix = filename.split('.')[0]
        run_file_dir = f'{RUNS_PATH}/{run_name}/{file_prefix}'
        os.mkdir(run_file_dir)
        
        for i in range(RUNS_PER_PROBLEM):
            begin = datetime.now()
            print('Started code generation')

            response = llama3(system_prompt, user_prompt)

            with open(f'{run_file_dir}/{file_prefix}_{i+1}', 'w') as f:
                f.write(response)

            print(f'Executed in {(datetime.now() - begin).total_seconds():.2f} seconds')