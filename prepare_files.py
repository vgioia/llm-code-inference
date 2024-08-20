import os
import shutil
import zipfile

RAW_DATASET_PATH = './packages'
TESTS_PATH = './tests'
INPUT_FOLDER = 'input'
OUTPUT_FOLDER = 'output'
USER_PROMPTS_FOLDER = 'description'


def unzip_file(zip_file_path, extract_to_dir):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_dir)
        print(f'Unzipped {zip_file_path} to {extract_to_dir}')

def get_fname_prefix(filename):
    return filename.split('.')[0]

def copy_folder_files(source, destination, folder):
    shutil.copytree(f'{source}/{folder}', f'{destination}/{folder}', dirs_exist_ok=True)
    print(f'Copied from {source}/{folder} to {destination}/{folder}')

for filename in os.listdir(RAW_DATASET_PATH):
    if '.zip' not in filename:
        continue

    file_path = os.path.join(RAW_DATASET_PATH, filename)
    prefix_name = get_fname_prefix(filename)
    prefix_path = f'{RAW_DATASET_PATH}/{prefix_name}'

    if os.path.isfile(file_path):
        unzip_file(file_path, prefix_path)

    task_tests_path = f'{TESTS_PATH}/{prefix_name}'

    copy_folder_files(prefix_path, task_tests_path, INPUT_FOLDER)
    copy_folder_files(prefix_path, task_tests_path, OUTPUT_FOLDER)

