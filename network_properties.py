import csv
import json
import networkx as nx
from networkx.algorithms import community

def degree_distribution(fname):
    f = open(fname)
    reader = csv.reader(f, delimiter=',')
    out_file = open(fname[:-4]+'_degree_distribution'+'.csv', 'w', newline='')
    writer = csv.writer(out_file)
    degree_count = {}
    for entry in reader:
        if entry[0] in degree_count:
            degree_count[entry[0]] += 1
        elif entry[1] in degree_count:
            degree_count[entry[1]] += 1
        else:
            degree_count[entry[0]] = 1
    
    degree = {}
    for key in degree_count:
        val = str(degree_count[key])
        if val in degree:
            degree[val] += 1
        else:
            degree[val] = 1
    
    for key in degree:
        writer.writerow([key,degree[key]])

    out_file.close()
    f.close()

def getStats(fname):
    f = open(fname)
    reader = csv.reader(f, delimiter=',')
    adjacency_list = {}
    for entry in reader:
        if entry[0] in adjacency_list:
            adjacency_list[entry[0]].append(entry[1])
        else:
            adjacency_list[entry[0]] = [entry[1]]

    G = nx.DiGraph(adjacency_list)
    avg_clus = nx.average_clustering(G)
    print(f'Average Clustering Coefficient: {avg_clus}')
    density = nx.density(G)
    print(f'Density of Graph: {density}')
    # avg_path = nx.average_shortest_path_length(G)
    # print(f'Average shortest path: {avg_path}')
    print('WCC', end=": ")
    print(len([len(c) for c in sorted(nx.weakly_connected_components(G), key=len, reverse=True)]))
    print('SCC', end=": ")
    print(len([len(c) for c in sorted(nx.strongly_connected_components(G), key=len, reverse=True)]))
    
    # degree centrality
    with open('./data/degree_centrality.json', 'w') as f:
        node_degrees = nx.degree_centrality(G)
        sorted_keys = sorted(node_degrees, key=node_degrees.get)
        sorted_dict = {}
        for key in sorted_keys:
            sorted_dict[key] = node_degrees[key]
        json.dump(sorted_dict, f)

    # closeness centrality
    with open('./data/closeness_centrality.json', 'w') as f:
        node_close = nx.closeness_centrality(G)
        sorted_keys = sorted(node_close, key=node_close.get)
        sorted_dict = {}
        for key in sorted_keys:
            sorted_dict[key] = node_close[key]
        json.dump(sorted_dict, f)

    # betweenness centrality
    with open('./data/betweenness_centrality.json', 'w') as f:
        node_btw = nx.betweenness_centrality(G)
        sorted_keys = sorted(node_btw, key=node_btw.get)
        sorted_dict = {}
        for key in sorted_keys:
            sorted_dict[key] = node_btw[key]
        json.dump(sorted_dict, f)
    
    # diameter = nx.diameter(G)
    # print(f'Diameter: {diameter}')
    # different community detection algorithms
    print('detecting communities...')
    print('Girvan Newman')
    community_generator = community.girvan_newman(G)
    top_level_communities = next(community_generator)
    print(sorted(map(sorted, top_level_communities)))

    print('Greedy Modularity')
    community_generator = community.greedy_modularity_communities(G)
    top_level_communities = next(community_generator)
    print(sorted(map(sorted, top_level_communities)))

    print('Louvain')
    community_generator = community.louvain_communities(G)
    top_level_communities = next(community_generator)
    print(sorted(map(sorted, top_level_communities)))


if __name__ == "__main__":
    # calculating degree distribution
    degree_distribution('./data/edges_140.csv')

    # get statistics
    getStats('./data/edges_140.csv')