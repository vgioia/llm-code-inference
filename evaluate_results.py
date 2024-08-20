import numpy as np
import os

LOGS_PATH = './logs'
SUCCESS_STRING = 'PASSED'


def pass_at_k(n, c, k):
    if n - c < k:
        return 1.0
    return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))

def is_correct(file_path):
    with open(file_path, 'r') as f:    
        for line in f:
            if line.strip() != SUCCESS_STRING:
                return False
        return True

n = 1
c = 0
k = 1
p = np.array([])

for filename in os.listdir(LOGS_PATH):
    file_path = os.path.join(LOGS_PATH, filename)
    c = 0
    if is_correct(file_path):
        c = 1
    p = np.append(p, c)

print(f'pass@{k} of algorithm is {100 * round(np.mean(p), 4)}%')