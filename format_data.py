import json
import pandas as pd

from os import listdir
from os.path import isfile, join

FOLLOWING_DIR = './data/following/'

def get_following_df(accounts_df):
    all_files = [f for f in listdir(FOLLOWING_DIR) if isfile(join(FOLLOWING_DIR, f))]
    edge_df = pd.DataFrame({},columns=['source', 'target', 'source_un', 'target_un'])
    nodes_df = pd.DataFrame({},columns=['id', 'name', 'username'])
    for f in all_files:
        source_id = f[2:-5]
        # adding the current node into the nodes list
        adfa= accounts_df.loc[accounts_df['id'] == source_id]
        if nodes_df.loc[nodes_df['id'] == source_id]:
            source_un = nodes_df.loc[nodes_df['id'] == source_id]
        else:
            nodes_df.loc[0] = accounts_df.loc[accounts_df['id'] == source_id]
        
        # loading all the accounts they are following
        with open(join(FOLLOWING_DIR, f), encoding='utf-8') as f_obj:
            data = json.load(f_obj)['data']
        # adding all the accounts they are following into the node and edge list
        for acc in data:
            del acc['created_at']
            if acc['id'] not in accounts_df['id'].values:
                nodes_df.loc[0] = pd.DataFrame.from_dict(acc, columns=['id', 'name', 'username'])
            edge_df.loc[0] = pd.DataFrame([
                                            source_id,
                                            acc['id'],

                                            ], 
                                            columns=['source', 'target', 'source_un', 'target_un'])

def get_accounts_df():
    with open('./data/SMTOWNGLOBAL_followers_og.json', encoding='utf-8') as f_obj:
        data = json.load(f_obj)['data']
    df = pd.DataFrame.from_dict(data)

    return df

if __name__ == "__main__":
    accounts_df = get_accounts_df()
    get_following_df(accounts_df)
        