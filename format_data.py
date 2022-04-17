import json
import csv
import pandas as pd

from os import listdir
from os.path import isfile, join

FOLLOWING_DIR = './data/following/'

def get_following_df(accounts_df):
    all_files = [f for f in listdir(FOLLOWING_DIR) if isfile(join(FOLLOWING_DIR, f))]
    edge_df = pd.DataFrame({},columns=['source', 'target'])
    nodes_df = pd.DataFrame({},columns=['id', 'name', 'username'])
    for f in all_files:
        # sanity check
        source_id = f[2:-5]
        print('Looking at:', source_id)
        # adding the current node into the nodes list
        source_un = accounts_df.loc[accounts_df['id'] == source_id, 'username'].iloc[0]
        source_name = accounts_df.loc[accounts_df['id'] == source_id, 'name'].iloc[0]
        if nodes_df.loc[nodes_df['id'] == source_id].empty:
            df = pd.DataFrame.from_dict({'id': [source_id], 'name': [source_name], 'username': [source_un]})
            nodes_df = pd.concat([nodes_df, df])
        
        # loading all the accounts they are following
        with open(join(FOLLOWING_DIR, f), encoding='utf-8') as f_obj:
            data = json.load(f_obj)['data']
        # adding all the accounts they are following into the node and edge list
        for acc in data:
            if acc['id'] not in accounts_df['id'].values:
                df = pd.DataFrame({'id': [acc['id']], 'name': [acc['name']], 'username': [acc['username']]})
                nodes_df = pd.concat([nodes_df, df])
            df = pd.DataFrame({
                            'source':[source_id], 
                            'target':[acc['id']]
                            })
            edge_df = pd.concat([edge_df, df])
    
    # get rid of any repeated entries
    nodes_df.drop_duplicates(subset='id', keep=False, inplace=True)

    return nodes_df, edge_df

def get_accounts_df():
    with open('./data/SMTOWNGLOBAL_followers_og.json', encoding='utf-8') as f_obj:
        data = json.load(f_obj)['data']
    df = pd.DataFrame.from_dict(data)

    return df

def output_files(nodes_df, edges_df):
    nodes_df.to_csv('./data/nodes.csv')
    edges_df.to_csv('./data/edges.csv')

def filter_out():
    with open('./data/removed_ids.json', encoding='utf-8') as f_obj:
        remove_ids = json.load(f_obj)['removed_ids']
    
    nodes = pd.read_csv('./data/nodes.csv', encoding='utf-8')
    edges = pd.read_csv('./data/edges.csv', encoding='utf-8')
    # filter out nodes
    print('\nremoving entries')
    for id in remove_ids:
        print(id)
        nodes.drop(nodes.index[nodes['id'] == id], inplace=True)
        edges.drop(edges.index[edges['source'] == id], inplace=True)
        edges.drop(edges.index[edges['target'] == id], inplace=True)

    return nodes, edges

if __name__ == "__main__":
    accounts_df = get_accounts_df()
    nodes, edges = get_following_df(accounts_df)
    output_files(nodes, edges)
    nodes, edges = filter_out()
    output_files(nodes, edges)