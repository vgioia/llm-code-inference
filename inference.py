import os
import requests
from datetime import datetime
from openai import OpenAI

URL = 'http://localhost:11434/api/chat'
PROMPTS_ROOT_PATH = './prompts'
SYSTEM_PROMPT_FPATH = f'{PROMPTS_ROOT_PATH}/system/system.txt'
USER_PROMPTS_FPATH = f'{PROMPTS_ROOT_PATH}/user'
RUNS_PATH = './runs'
RUNS_PER_PROBLEM = 5

client = OpenAI()

def gpt(n, sys_prompt, user_prompt):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ],
        n=n
    )
    return completion.choices

def llama3(sys_prompt, user_prompt):
    data = {
        "model": "llama3.1",
        "messages": [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "options": {
            "temperature": 1
        },
        "stream": False
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(URL, headers=headers, json=data)
    
    return(response.json()['message']['content'])

def generate_gpt_codes(n, sys_prompt, user_prompt):
    begin = datetime.now()
    print('Started code generation')

    msgs = list()
    for choice in gpt(n, sys_prompt, user_prompt):
        msgs.append(choice.message.content)
    
    print(f'Obtained {n} response(s) in {(datetime.now() - begin).total_seconds():.2f} seconds')

    return msgs

def generate_llama_codes(n, sys_prompt, user_prompt):
    msgs = list()
    for _ in range(n):
        begin = datetime.now()
        print('Started code generation')

        msgs.append(llama3(sys_prompt, user_prompt))

        print(f'Obtained 1 response in {(datetime.now() - begin).total_seconds():.2f} seconds')

    return msgs
    
def save_runs(dir, runs):
    i = 1
    for run in runs:
        with open(f'{dir}_{i}', 'w') as f:
            f.write(run)
        i += 1


model='gpt-4o'

with open(SYSTEM_PROMPT_FPATH, 'r') as f:
    system_prompt = f.read()

run_datetime = datetime.now().strftime('%Y%m%d%H%M') 
model_rname = model.replace('-','_').replace('.', '_')

run_name = f'{run_datetime}_{model_rname}'
os.mkdir(f'{RUNS_PATH}/{run_name}')

responses = None

for filename in os.listdir(USER_PROMPTS_FPATH):

    file_path = os.path.join(USER_PROMPTS_FPATH, filename)
    file_prefix = filename.split('.')[0]
    run_file_dir = f'{RUNS_PATH}/{run_name}/{file_prefix}'
    os.mkdir(run_file_dir)

    with open(file_path, 'r') as f:
        user_prompt = f.read()

    if model == 'gpt-4o':
        responses = generate_gpt_codes(RUNS_PER_PROBLEM, system_prompt, user_prompt)

    if model == 'llama3.1':
        responses = generate_llama_codes(RUNS_PER_PROBLEM, system_prompt, user_prompt)

    if responses is None:
        print("Exiting the code")
        break

    prefix_run_dir = f'{run_file_dir}/{file_prefix}'
    save_runs(prefix_run_dir, responses)