import numpy as np
import os

RUN_NAME="202408252332_gpt_4o"
LOGS_PATH = f'./logs/{RUN_NAME}'
TIMEOUT_STATUS = 'TIMEOUT'
FAILURE_STATUS = 'FAILED'

def pass_at_k(n, c, k):
    """
    :param n: total number of samples
    :param c: number of correct samples
    :param k: k in pass@k
    """
    if n - c < k:
        return 1.0
    return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))

def is_correct(file_path, timeout_is_failure):
    with open(file_path, 'r') as f:
        for line in f:
            status = line.strip()

            if status == FAILURE_STATUS:
                return False

            if timeout_is_failure and status == TIMEOUT_STATUS:
                return False

        return True

n = 5
c = 0
k = 1
p = np.array([])

for task_dir in os.listdir(LOGS_PATH):
    full_task_dir = os.path.join(LOGS_PATH, task_dir)
    c = 0

    for task_run in os.listdir(full_task_dir):
        file_path = os.path.join(full_task_dir, task_run)

        if is_correct(file_path, timeout_is_failure=True):
            c += 1
    print(f'{task_dir}: correct codes {c}')
    p = np.append(p, pass_at_k(n, c, k))

print(p)
print(f'pass@{k} of run {RUN_NAME} is {100 * round(np.mean(p), 4)}%')