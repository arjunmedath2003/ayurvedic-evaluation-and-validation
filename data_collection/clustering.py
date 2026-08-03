import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import igraph as ig
import leidenalg
import json

def creategraph(G,proteins,score_data):
   G.add_nodes_from(proteins)
   edges = []
   for row in score_data.itertuples():
      edges.append((row.Protein1,row.Protein2,row.Score))
   G.add_weighted_edges_from(edges)
   
def draw_clusters(G, clusters, title):
    plt.figure(figsize=(6, 5))
    pos = nx.spring_layout(G, seed=42)
    colors = plt.cm.tab10.colors

    for i, cluster in enumerate(clusters):
        nx.draw_networkx_nodes(G, pos,
                               nodelist=cluster,
                               node_color=[colors[i % len(colors)]],
                               label=f"Cluster {i+1}",
                               node_size=20 )
    nx.draw_networkx_edges(G, pos, alpha=0.3)
    plt.title(title)
    plt.legend()
    plt.axis("off")
    plt.show()

def nx_to_igraph(G):
    mapping = {node: idx for idx, node in enumerate(G.nodes())}
    G_ig = ig.Graph()
    G_ig.add_vertices(len(mapping))
    edges = [(mapping[u], mapping[v]) for u, v in G.edges()]
    G_ig.add_edges(edges)

    if nx.get_edge_attributes(G, 'weight'):
        weights = [G[u][v].get('weight', 1.0) for u, v in G.edges()]
        G_ig.es['weight'] = weights

    return G_ig, mapping

def leiden_clustering(G):
    G_ig, mapping = nx_to_igraph(G)
    partition = leidenalg.find_partition(G_ig, leidenalg.ModularityVertexPartition)
    clusters = [list(comm) for comm in partition]
    reverse_mapping = {v: k for k, v in mapping.items()}
    clusters_named = [[reverse_mapping[node] for node in cluster] for cluster in clusters]
    return clusters_named

with open("ayurveda.json","rb") as file:
    ayurveda_data = json.load(file)

def createncluster(ayurveda):
    print("Creating Graph")
    G = nx.Graph()
    plants=ayurveda_data[ayurveda]['ingredients']
    proteins=[]
    for i in plants:
        df = pd.read_csv(f"proteins/{i.lower().replace(' ','_')}.csv")
        proteins+=df['Protein'].tolist()
    df = pd.read_csv(f"protein_links/{ayurveda}.csv")
    creategraph(G,proteins,df)
    print("Graph created")
    clusters_leiden = leiden_clustering(G)
    # draw_clusters(G,clusters_leiden,plant)
    return clusters_leiden

ayurveda = ayurveda_data.keys()
res={}
for i in ayurveda:
    print(f"{i} started ")
    res[i]=[i for i in createncluster(i) if len(i)>1]
    print(f"{i} ended ")
    # break

with open("cluster.json", "w", encoding="utf-8") as file:
    json.dump(res, file,indent=4)
