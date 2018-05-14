import networkx as nx

print("Reading in network")
G = nx.read_adjlist("output.csv", delimiter=",")
print("Finished reading")

print("Trimming Graph")

nodeset = [k for k in G.nodes]
print("Number nodes before: {}".format(len(nodeset)))

for node in nodeset:
    if G.degree(node) <= 1:
        G.remove_node(node)

print("Finished trimming")
print("Number nodes after: {}".format(len(G.nodes)))
