__author__ = 'akashmalla'

import sys
import collections

#graph is a dictionary of people and their friends, key is a person, say 'Alice',
# and value is people that Alice knows (her friends)
graph = {}
input=[]
print("\nInput Provided:")
for line in sys.stdin:
    print(line.rstrip())
    #Read each line of input data and remove whitespaces and exit program if user input provided is wrong values.
    #Also, skip any lines starting with '#'
    if not line.startswith('#'):
        cleanedline = line.strip()
        if cleanedline:
            x = cleanedline.split(',')
            #Check if user provided string or not and if each line has only 2 strings seperated by comma, if not, exit program
            #if x[0].strip().isalpha() and x[1].strip().isalpha() and len(x)==2:
            if x[0].strip() and x[1].strip() and len(x)==2:
                name1 = str(x[0].strip())
                name2 = str(x[1].strip())
                input.append(name1+" "+name2)
                gvalues=list(graph.values())
                gkeys=list(graph.keys())
                #For example, input data says: Alice, Bruce
                #If Alice is not in graph, add Alice and set Bruce as friend. If Bruce is in graph, then add Alice as Bruce's friend.
                if name1 not in graph:
                    graph[name1]=set([name2])
                    if name2 in graph.keys():
                        gvalues[gkeys.index(name2)].add(name1)
                else:
                    #If Alice is in graph, get Alice's index and add Bruce as a friend
                    #and if Bruce is also in graph, add Alice as Bruce's friend
                    gvalues[gkeys.index(name1)].add(name2)
                    if name2 in graph.keys():
                        gvalues[gkeys.index(name2)].add(name1)
                #If Bruce is not in graph, add Bruce and Alice as Bruce's friend
                #If Alice in graph then add Bruce as a friend
                if name2 not in graph:
                    graph[name2]=set([name1])
                    if name1 in graph.keys():
                        gvalues=list(graph.values())
                        gkeys=list(graph.keys())
                        gvalues[gkeys.index(name1)].add(name2)
            else:
                sys.exit('Wrong input given to program.')
print("\nGraph:")
print(graph)

#This function returns all friends of a person as a list
def get_children(c):
    for n in graph.keys():
        if n == c:
            return list(graph[n])

def multiParent(root,child,node,visited,allSiblings):
    if child not in [n for n in graph[root]] and child != root and [node,child] not in [v for v in visited]:
        for p in set([v[1] for v in visited if v[1] != 'none']):
            allSiblings.append([v[0] for v in visited if v[1]==p])
            #print(allSiblings)
            if [child,node] not in allSiblings and [node,child] not in allSiblings:
                #print(child,node)
                if [child,node] not in visited:
                    visited.append([child,node])

def iterative_bfs(graph, start):
    q=[start]
    visited,path=[],[]
    level=[]
    allSiblings=[]
    visited.append([start,'none'])
    while q:
        v=q.pop(0)
        if not v in path:
            path=path+[v]
            q=q+list(graph[v])
            for c in graph[v]:
                if [v,c] not in visited:
                    visited.append([c,v])

    weightedNode={}
    multiparentnodes = [[item,count] for item, count in collections.Counter([v[0] for v in visited]).items() if count > 1]
    print(multiparentnodes)

    for v in reversed(visited):
        if not multiparentnodes:
            weightedNode[v[0]+" "+v[1]]=1.0
        else:
            for m in multiparentnodes:
                if v[0] not in m[0]:
                    weightedNode[v[0]+" "+v[1]]=1.0
                else:
                    #Here we set the weight of an edge of a node from BFS tree that has multiple parents to 1 over number of parents
                    weightedNode[v[0]+" "+v[1]]=1.0/m[1]

    #For all distinct parents in tree
    seen = set()
    seen_add = seen.add
    distinctParents=[v[1] for v in reversed(visited) if not (v[1] in seen or seen_add(v[1]))]
    temp={}
    c=0
    for p in distinctParents:
        temp[p]=0
        for v in reversed(visited):
            if v[1]==p and p != 'none':
                temp[p]+=weightedNode[v[0]+" "+p]
            if v[0]==p:
                weightedNode[v[0]+" "+v[1]]+=temp[p]
            if p =='none':
                weightedNode.pop(v[0]+" "+p, None)

    print(visited)
    return weightedNode

def bfs(root):
    queue = [root]
    visited=[]
    visited.append([root,'none'])
    allSiblings=[]
    while queue:
        node = queue.pop(0)
        for child in get_children(node):
            if child not in [v[0] for v in visited]:
                queue.append(child)
                visited.append([child,node])
            else:
                multiParent(root,child,node,visited,allSiblings)

    for s in allSiblings:
        for v in visited:
            if set(s) == set(v) and len(s)==len(v):
                print("found: ",s,v)
                visited.remove(v)
            else:
                if set(v).issubset(s) and len(s)>len(v):
                    print("found: ",s,v)
                    visited.remove(v)


    weightedNode={}
    multiparentnodes = [[item,count] for item, count in collections.Counter([v[0] for v in visited]).items() if count > 1]
    print(multiparentnodes)

    for v in reversed(visited):
        if not multiparentnodes:
            weightedNode[v[0]+" "+v[1]]=1.0
        else:
            for m in multiparentnodes:
                if v[0] not in m[0]:
                    weightedNode[v[0]+" "+v[1]]=1.0
                else:
                    #Here we set the weight of an edge of a node from BFS tree that has multiple parents to 1 over number of parents
                    weightedNode[v[0]+" "+v[1]]=1.0/m[1]

    #For all distinct parents in tree
    seen = set()
    seen_add = seen.add
    distinctParents=[v[1] for v in reversed(visited) if not (v[1] in seen or seen_add(v[1]))]
    temp={}
    c=0
    for p in distinctParents:
        temp[p]=0
        for v in reversed(visited):
            if v[1]==p and p != 'none':
                temp[p]+=weightedNode[v[0]+" "+p]
            if v[0]==p:
                weightedNode[v[0]+" "+v[1]]+=temp[p]
            if p =='none':
                weightedNode.pop(v[0]+" "+p, None)

    print(visited)
    return weightedNode

#print(bfs("Ellen"))
#print(iterative_bfs("node_1"))
#Below will compute the tree and node weights for all nodes as root
allWeighedNodes=[]
for p in graph.keys():
    allWeighedNodes.append(iterative_bfs(graph,p))
#print(allWeighedNodes)

#Compute sum of all edge weights, I am not dividing each edge calculation by 2
#because I was adding for example Cindy to Alice seperately than Alice to Cindy
#So, I have an if condition where key in input which will only pick cindy to alice
sumWeighedNodes = {}
for dict in allWeighedNodes:
    for key, value in dict.items():
        if key in input:
            sumWeighedNodes.setdefault(key, 0)
            sumWeighedNodes[key] += value
#print(sumWeighedNodes)
print("\nEdge weight computation in descending order:")
for w in sorted(sumWeighedNodes, key=sumWeighedNodes.get, reverse=True):
    print(w,"-->",sumWeighedNodes[w])

result=[]
def removeEdge(n1,n2):
    for r in result:
        if n1 in r and n2 in r:
            result.remove(r)
    cluster=[]
    tempCluster=[]
    for n in graph[n1]:
        if n!=n2:
            cluster.append(n)
    cluster.append(n1)
    tempCluster.append(cluster)
    if n2 in graph[n1]:
        graph[n1].remove(n2)
    cluster=[]
    for n in graph[n2]:
        if n!=n1:
            cluster.append(n)
    cluster.append(n2)
    tempCluster.append(cluster)
    if n1 in graph[n2]:
        graph[n2].remove(n1)
    if set(tempCluster[0]).intersection(tempCluster[1]):
        result.append(list(set(tempCluster[0]+tempCluster[1])))
    else:
        for cluster in tempCluster:
            result.append(cluster)
    return result

print("\nCluster Results:")

print("Cluster 1 :",[n for n in graph.keys()])
count=2
for w in sorted(sumWeighedNodes, key=sumWeighedNodes.get, reverse=True):
    if count==len(result) or result==[]:
        print("Cluster",count,":",removeEdge(w.split()[0],w.split()[1]))
        count+=1
    else:
        removeEdge(w.split()[0],w.split()[1])
