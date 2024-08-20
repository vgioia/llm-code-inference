import os

RAW_PROMPTS_PATH = './raw_prompts'
USER_PROMPTS_FPATH = './prompts/user'
SKIP_LINES = 2
SHOT_PATTERN_START = 'Exemplo de entrada 1'
HEADER_PREFIX = 'Maratona de Programa¸c˜ao da SBC – ICPC – 2023'
REPLACE_DICT = {
    "´a": "á",
    "`a": "à",
    "˜a": "ã",
    "¸c": "ç",
    "´e": "é",
    "ˆe": "ê",
    "´ı": "í",
    "´o": "ó",
    "˜o": "õ",
    "´u": "ú",
}


def clean_up_string(s, is_shot):
    s = s.strip()
    for k, v in REPLACE_DICT.items():
        s = s.replace(k, v)

    if is_shot:
        return s + r'\n'

    return s + ' '

def clean_file(file_path):
    with open(file_path, 'r') as file:
        for _ in range(SKIP_LINES):
            next(file)

        text = ''
        shots_started = False
        for line in file:
            if line.strip() == HEADER_PREFIX:
                continue

            if line.strip() == SHOT_PATTERN_START:
                shots_started = True
            
            cleaned_str = clean_up_string(line, shots_started)
            text += cleaned_str
    
    write_path = os.path.join(USER_PROMPTS_FPATH, filename)
    with open(write_path, 'w') as file:
        file.write(text)


for filename in os.listdir(RAW_PROMPTS_PATH):
    file_path = os.path.join(RAW_PROMPTS_PATH, filename)
    if os.path.isfile(file_path):
        clean_file(file_path)