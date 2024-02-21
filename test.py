import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_edge('A', 'B') 
G.add_edge('A', 'C')
G.add_edge('B', 'D')
G.add_edge('C', 'E') 
G.add_edge('D', 'H')
G.add_edge('E', 'F')  
G.add_edge('F', 'G')
G.add_edge('D', 'H')

pos = nx.spring_layout(G)

# DFS
print("DFS:")
visited = set() 
visited.add('A')
nx.draw(G, pos, with_labels=True)
plt.savefig("dfs1.png") 

def dfs(node):
    print(node)
    visited.add(node)
    G.nodes[node]['color'] = 'red'
    plt.clf()
    nx.draw(G, pos, with_labels=True, node_color=[G.nodes[i]['color'] for i in G])
    plt.savefig(f"dfs{len(visited)}.png")
    
    for n in G[node]:
        if n not in visited:
            dfs(n)
            
dfs('A')

# BFS
print("\nBFS:")
visited = set()
queue = ['A'] 

visited.add('A')
nx.draw(G, pos, with_labels=True)
plt.savefig("bfs1.png")

while queue:
    node = queue.pop(0)
    print(node)
    visited.add(node)
    G.nodes[node]['color'] = 'red'
    plt.clf()
    nx.draw(G, pos, with_labels=True, node_color=[G.nodes[i]['color'] for i in G])
    plt.savefig(f"bfs{len(visited)}.png")
    for n in G[node]:
        if n not in visited:
            queue.append(n)