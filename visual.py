import networkx as nx
import matplotlib.pyplot as plt

G = nx.read_adjlist('output.csv', delimiter=',')
f = open('cliques.txt', 'r')
s = f.readline()
exec('cliques = ' + s)
f.close()
print('Loaded')

connects = {}
for a in range(len(cliques)-1):
    if len(cliques[a]) < 10:
        break
    for b in range(a+1, len(cliques)):
        if len(cliques[b]) < 10:
            break
        n = 0
        s2 = set(cliques[b])
        for node in cliques[a]:
            neighbors = set(G.neighbors(node))
            n += len(neighbors.intersection(s2))
        connects[(a,b)] = n / (len(cliques[a])*len(cliques[b]))

#priority = sorted(list(connects.keys()), key=lambda x: connects[x], reverse=True)

posG = nx.Graph()
for x in connects.keys():
    posG.add_edge(x[0], x[1], weight=connects[x])
pos = nx.spring_layout(posG)
nx.draw_networkx_nodes(posG, pos, node_size=5)
nx.draw_networkx_edges(posG, pos, edgelist=list(connects.keys()), \
                       width=[10*x for x in connects.values()])
plt.show()
