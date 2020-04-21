import sys

sys.path.append('..')
from data import load_data

PATH = '..\\..\\data\\model\\'

def save_token_counts(data_prefix):
    tokens = load_data(PATH + 'train_{}_unique_tokens.data'.format(data_prefix))
    with open(PATH + 'train_{}_unique_tokens.txt'.format(data_prefix), 'w') as f:
        for k, v in tokens.items():
            f.write('{}; {}\n'.format(k, v))

save_token_counts('conjecture')
save_token_counts('premise')
