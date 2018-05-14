import copy
import networkx as nx
import matplotlib.pyplot as plt

def int_to_An(i):
    n = str(i)
    if len(n) < 6:
        n = '0'*(6-len(n)) + n #leading zeros
    An = 'A' + n
    return An

def count(iterable, n):
    return sum([d == n for d in iterable])

G = nx.read_adjlist('output.csv', delimiter=',')
print('Loaded')

degree = nx.degree_centrality(G)
high_d = max(degree.keys(), key=lambda x: degree[x])
print('Most degree-central node: %s with degreeness %f (degree=%d)'
      % (high_d, degree[high_d], G.degree(high_d)))

sorted_degrees = sorted(list(degree.keys()), key=lambda x: degree[x], reverse=True)
high_degrees = sorted_degrees[:100]
print(sorted_degrees[:10])

closeness = {}
for i in high_degrees:
    closeness[i] = nx.closeness_centrality(G, u=i)
high_c = max(closeness.keys(), key=lambda x: closeness[x])
print('Most close-central node: %s with closeness %f'
      % (high_c, closeness[high_c]))

sorted_closeness = sorted(list(closeness.keys()), key=lambda x: closeness[x], reverse=True)
print(sorted_closeness[:10])

betweenness = nx.betweenness_centrality(G, k=100)
high_b = max(betweenness.keys(), key=lambda x: betweenness[x])
print('Most between-central node: %s with betweenness %f'
      % (high_b, betweenness[high_b]))

sorted_betweenness = sorted(list(betweenness.keys()), key=lambda x: betweenness[x], reverse=True)
print(sorted_betweenness[:10])
