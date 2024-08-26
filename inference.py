import os
import requests
from datetime import datetime
from openai import OpenAI
from groq import Groq

PROMPTS_ROOT_PATH = './prompts'
SYSTEM_PROMPT_FPATH = f'{PROMPTS_ROOT_PATH}/system/system.txt'
USER_PROMPTS_FPATH = f'{PROMPTS_ROOT_PATH}/user'
RUNS_PATH = './runs'
RUNS_PER_PROBLEM = 5
MODEL = 'llama3.1:70b'

oai_client = OpenAI()
groq_client = Groq()


def llama3_70b(sys_prompt, user_prompt):
    completion = groq_client.chat.completions.create(
        messages=[
            {"role": "assistant", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ],
        model="llama-3.1-70b-versatile",
        temperature=1
    )
    return completion.choices

def gpt(sys_prompt, user_prompt):
    completion = oai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_prompt}
        ],
        n=RUNS_PER_PROBLEM
    )
    return completion.choices

def complete_chats(func, sys_prompt, user_prompt):
    msgs = list()
    for choice in func(sys_prompt, user_prompt):
        msgs.append(choice.message.content)

    return msgs
    
def save_runs(dir, runs):
    i = 1
    for run in runs:
        with open(f'{dir}_{i}', 'w') as f:
            f.write(run)
        i += 1



with open(SYSTEM_PROMPT_FPATH, 'r') as f:
    system_prompt = f.read()

run_datetime = datetime.now().strftime('%Y%m%d%H%M') 
model_rname = MODEL.replace('-','_').replace('.', '_').replace(':', '_')
run_name = f'{run_datetime}_{model_rname}'
os.mkdir(f'{RUNS_PATH}/{run_name}')

for filename in os.listdir(USER_PROMPTS_FPATH):

    file_path = os.path.join(USER_PROMPTS_FPATH, filename)
    file_prefix = filename.split('.')[0]
    run_file_dir = f'{RUNS_PATH}/{run_name}/{file_prefix}'
    os.mkdir(run_file_dir)

    responses = list()

    with open(file_path, 'r') as f:
        user_prompt = f.read()

        begin = datetime.now()
        print('started code generation')

    if MODEL == 'gpt-4o':
        model_func = gpt
        responses = complete_chats(model_func, system_prompt, user_prompt)

    if MODEL == 'llama3.1:70b':
        model_func = llama3_70b
        for _ in range(RUNS_PER_PROBLEM):
            responses.append(complete_chats(model_func, system_prompt, user_prompt)[0])

    if responses is None:
        print("responses not generated, exiting the code")
        break

    print(f'obtained {RUNS_PER_PROBLEM} response(s) in {(datetime.now() - begin).total_seconds():.2f} seconds')

    prefix_run_dir = f'{run_file_dir}/{file_prefix}'
    save_runs(prefix_run_dir, responses)