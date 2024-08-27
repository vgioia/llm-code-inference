import numpy as np
import os

LOGS_PATH = f'./logs'
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

def is_correct(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            status = line.strip()

            if status == FAILURE_STATUS:
                return False

            if status == TIMEOUT_STATUS:
                return False

        return True

n = 5
c = 0
ks = [1, 3, 5]

for run in os.listdir(LOGS_PATH):
    run_path = os.path.join(LOGS_PATH, run)

    for k in ks:
        p = np.array([])

        for task_dir in os.listdir(run_path):
            full_task_dir = os.path.join(run_path, task_dir)
            c = 0

            for task_run in os.listdir(full_task_dir):
                file_path = os.path.join(full_task_dir, task_run)

                if is_correct(file_path):
                    c += 1

            p = np.append(p, pass_at_k(n, c, k))

        print(f'pass@{k} of run {run} is {round(100 * np.mean(p), 2)}%')
