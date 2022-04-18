import json
import csv
import pandas as pd
import random

from os import listdir
from os.path import isfile, join

FOLLOWING_DIR = './data/following/'
BANDS = ['873092428755894272', '391115625', '4811011050', '887973863824306176', '965487301722701826', '1277453652924366848', '873115441303924736']

def get_following_df(accounts_df):
    all_files = [f for f in listdir(FOLLOWING_DIR) if isfile(join(FOLLOWING_DIR, f))]
    edge_df = pd.DataFrame({},columns=['source', 'target'])
    nodes_df = pd.DataFrame({},columns=['id', 'name', 'username'])
    all_files = all_files[:200]
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
    nodes_df.drop_duplicates(subset='id', inplace=True)

    return nodes_df, edge_df

def get_accounts_df():
    with open('./data/SMTOWNGLOBAL_followers_og.json', encoding='utf-8') as f_obj:
        data = json.load(f_obj)['data']
    df = pd.DataFrame.from_dict(data)

    return df

def output_files(nodes_df, edges_df):
    nodes_df.to_csv('./data/nodes_200.csv', index=False)
    edges_df.to_csv('./data/edges_200.csv', index=False)

def filter_out():
    with open('./data/removed_ids.json', encoding='utf-8') as f_obj:
        remove_ids = json.load(f_obj)['removed_ids']
    
    nodes = pd.read_csv('./data/nodes_200.csv', encoding='utf-8')
    edges = pd.read_csv('./data/edges_200.csv', encoding='utf-8')
    # filter out nodes
    print('\nremoving entries')
    for id in remove_ids:
        print(id)
        nodes.drop(nodes.index[nodes['id'] == id], inplace=True)
        edges.drop(edges.index[edges['source'] == id], inplace=True)
        edges.drop(edges.index[edges['target'] == id], inplace=True)

    # filter based on what is in the nodes
    node_list = nodes['id'].tolist()
    target_list = edges['target'].tolist()
    source_list = edges['source'].tolist()
    for id in target_list:
        if id not in node_list:
            edges.drop(edges.index[edges['target'] == id], inplace=True)
            edges.drop(edges.index[edges['source'] == id], inplace=True)
    
    for id in source_list:
        if id not in node_list:
            edges.drop(edges.index[edges['target'] == id], inplace=True)
            edges.drop(edges.index[edges['source'] == id], inplace=True)

    return nodes, edges

def create_subset(nodes, edges, size):
    source_list = edges['source'].tolist()
    random.shuffle(source_list)
    source_list = source_list[:size]
    node_list = nodes['id'].tolist()
    print('removing all unnecessary sources')
    for id in node_list:
        if id not in source_list:
            edges.drop(edges.index[edges['source'] == id], inplace=True)
            nodes.drop(nodes.index[nodes['id'] == id], inplace=True)
    
    return nodes, edges

def format_d3_json():
    nodes_df = pd.read_csv('./data/nodes_200.csv', encoding='utf-8')
    edges_df = pd.read_csv('./data/edges_200.csv', encoding='utf-8')

    nodes = []
    edges = []
    for idx in range(nodes_df.shape[0]):
        acc = nodes_df.iloc[idx]
        nodes.append({
            "id": int(acc.id),
            "name": acc.username
        })
    for idx in range(edges_df.shape[0]):
        row = edges_df.iloc[idx]
        edges.append({
            "source": int(row.source),
            "target":int(row.target)
        })

    f = open('./data/network_data_200.json', 'w')
    json.dump({"nodes":nodes,"links":edges}, f, sort_keys=True)


if __name__ == "__main__":
    accounts_df = get_accounts_df()
    nodes, edges = get_following_df(accounts_df)
    output_files(nodes, edges)
    nodes, edges = filter_out()
    output_files(nodes, edges)
    # n_df, e_df = create_subset(nodes, edges, 200)
    # n_df.to_csv('./data/nodes_200.csv', index=False)
    # e_df.to_csv('./data/edges_200.csv', index=False)

    # n_df, e_df = create_subset(nodes, edges, 1000)
    # n_df.to_csv('./data/nodes_1000.csv', index=False)
    # e_df.to_csv('./data/edges_1000.csv', index=False)
    format_d3_json()
