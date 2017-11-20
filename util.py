import matplotlib.pyplot as plt
import csv
import math
import matplotlib.pyplot as plt
import networkx as nx

def get_subway_graph(csv_dir, Klass):
    G = Klass()
    # "line","name","colour","stripe"
    lines = {}
    with open(csv_dir+'/lines.csv', 'r') as csvfile:
        creader = csv.reader(csvfile)
        next(creader, None)
        for row in creader:
            lines[int(row[0])] = {"name": row[1], "color": row[2], "stripe": row[3], "line":int(row[0])}

    with open(csv_dir+'/connections.csv', 'r') as csvfile:
        creader = csv.reader(csvfile)
        next(creader, None)

        for row in creader:
            G.add_edge(int(row[0]), int(row[1]), attr_dict=lines[int(row[2])])

    with open(csv_dir+'/stations.csv', 'r') as csvfile:
        creader = csv.reader(csvfile)
        next(creader, None)
        for row in creader:
            G.node[int(row[0])] = {"latitude": float(row[1]), 
                                   "longitude": float(row[2]),
                                   "name": row[3],
                                   "display_name": row[4],
                                   "zone": float(row[5]),
                                   "total_lines": int(row[6]),
                                   "rail": row[7]
                                  }

    for node1, node2 in G.edges():
        norm = math.sqrt(
                (G.node[node1]['longitude'] - G.node[node2]['longitude'])**2 +
                (G.node[node1]['latitude'] - G.node[node2]['latitude'])**2
        )
        G.edge[node1][node2].update({'distance': norm})
        
    return G, lines

def draw_subway_graph(G, lines, figsize=(10,6), show_labels=False):
    plt.figure(figsize=figsize)
    plt.axis('off')
    
    G = graph2nx(G)
    pos = {x: (G.node[x]['longitude'], G.node[x]['latitude']) for x in G.node.keys()}
    nx.draw_networkx_nodes(G, 
                           pos, 
                           node_size=1,
                          )
    if show_labels:
        nx.draw_networkx_labels(G,pos,
                                {x: G.node[x]['name'] for x in G.nodes()},font_size=4)

    for line in lines.keys():
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=[x for x in G.edges() if G.edge[x[0]][x[1]]['line'] == line],
            edge_color="#"+lines[line]['color'],
        )

    plt.show()


def graph2nx(gr):
    G = nx.Graph()
    for node1 in gr.edge.keys():
        for node2, value in gr.edge[node1].items():
            G.add_edge(node1, node2, **value)

    for node, value in gr.node.items():
        G.add_node(node, **value)
       
    return G
  
