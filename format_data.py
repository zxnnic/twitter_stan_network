import json
from ntpath import join
import pandas as pd

from os import listdir
from os.path import isfile, join

FOLLOWING_DIR = './data/following/'

def get_following_df(accounts_df):
    all_files = [f for f in listdir(FOLLOWING_DIR) if isfile(join(FOLLOWING_DIR, f))]
    following_df = pd.DataFrame({},columns=['source', 'target', 'source_un', 'target_un'])
    for f in all_files:
        source_id = f[2:-5]
        with open(f, encoding='utf-8') as f_obj:
            data = json.load(f_obj)['data']


def get_accounts_df():
    with open('./data/SMTOWNGLOBAL_followers_og.json', encoding='utf-8') as f_obj:
        data = json.load(f_obj)['data']
    df = pd.DataFrame.from_dict(data)

    return df

if __name__ == "__main__":
    accounts_df = get_accounts_df()
    get_following_df(accounts_df)
        