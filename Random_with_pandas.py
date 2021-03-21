inf = 99999999
i = 0
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import time
import random

start_time = time.time()

#defining start and end
start = "A"
stop = "Z"

#importing graph data from excel file
df = pd.read_excel(r'C:\Users\user\OneDrive - Landstede Groep\school\PWS\graph_data(big).xlsx')
#df = pd.read_excel(r'C:\Users\Robin\OneDrive - Landstedegroep\school\PWS\graph_data.xlsx')

#converting excel data to nested dictionary
graph = df.set_index('Node2').groupby('Node1').apply(
    lambda x: x.weight.to_dict()
).to_dict()



#setting weight of nodes to inf and making parent of node an empty dictionary
weights = {}
parent = {}
for node in graph:
    weights[node] = inf
    parent[node] = {}

#setting weight of starting node to 0
weights[start] = 0

node = start
#parent_dict() = graph[parent]
    
def random_child_from_node(node):
        random_child = random.choice(list(graph[node].items()))
        child = ''.join(random_child[:1])
        return child
        

if __name__ == "__main__": 
    while i <= 500:
        while node != stop:
            weight = weights[node]
            child = random_child_from_node(node)
            child_weight = graph[node]
            parent[child] = node
            if weights[child] > weight + child_weight[child]:
                weights[child] = weight + child_weight[child]
            node = child
            i = i + 1
        node = start
    
    
    
S = nx.Graph()                                            #make an empty graph
child = stop                                              #
while child != start:                                     #iterate from endpoint to starting point through parents list
    S.add_edge(parent[child], child, weight = 1)          #make an edge from the child and the parent
    #print(child)
    #print(parent[child])
    child = parent[child]                                 #current parent is now child
    #print(S.edges)
            
    
        

#print(f"Costs:  {weights}")
print(f"the cost to go from {start} to {stop} is {weights[stop]}")  #printing the cost to go from a to b


G = nx.Graph()                                                      #make a new empty graph

for k,v in graph.items():                                           #make the edges an attribute of the graph
    for l, w in v.items():
        G.add_edge(k,l, weight=w)
        
same = []                                                           #empty list to add same edges to from S and G

for u,v,d in S.edges(data=True):                                    #check if there are same edges in S and G
    for a,b,c in G.edges(data=True):
        if u == a and v == b or u == b and v ==a:
            d['weight'] = c['weight']                              #make weight of edge from S same as edge from G
            same.append([a,b])
        
G.remove_edges_from(same)                                          #remove all the edges from G that are the same
        

   
shortest = [(u, v, d) for (u, v, d) in S.edges(data=True)]        #make an edgelist from edges in S
normal = [(u, v, d) for (u, v, d) in G.edges(data=True)]          #make an edgelist from edges in G

pos = nx.spring_layout(G)  # positions for all nodes              #make position of each node random

 #nodes
node_colors = []                                                 #make an empty list to store color of nodes
for node in G.nodes:                                              #if node is start node, make it green, if it is end node make it red, else blue
    if node == start:
        node_colors.append("green")
    elif node == stop:
        node_colors.append("red")
    else:
        node_colors.append("blue")


nx.draw_networkx_nodes(G, pos, node_color = node_colors, node_size=200)           #draw the nodes


# edges
nx.draw_networkx_edges(G, pos, edgelist=shortest, width=3, edge_color= 'red')     #draw the edges from the shortest route in color red
#edgelist=elarge

nx.draw_networkx_edges(G, pos, edgelist=normal, width=3)                          #draw every other edge
 

# labels
nx.draw_networkx_labels(G, pos, font_size=10, font_family="arial")                #show labels in the nodes, so that node name is visible

labels = nx.get_edge_attributes(G,'weight')                                       #show edge weight
labels2 = nx.get_edge_attributes(S,'weight')
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
nx.draw_networkx_edge_labels(S,pos,edge_labels=labels2)



plt.axis("off")                                                                   
plt.show()   

print(time.time()- start_time)         


