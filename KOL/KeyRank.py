import pandas as pd
import numpy as np

def KeyRank(M, alpha, beta, root):
    """
    Personal Rank in matrix formation
    :param M: transfer probability matrix
    :param index2node: index2node dictionary
    :param node2index: node2index dictionary
    :return:type of list of tuple, ex.
    [(node1, prob1),(node2, prob2),...]
    """
    result = []
    n = len(M)
    v = np.zeros(n)
    k = np.zeros(n)
    #print(v)
    v[node2index[root]] = 1
    #print(v)
    i = 1
    #while np.sum(abs(v - (alpha*np.matmul(M,v) + (1-alpha)*v))) > 0.0001:
    while(True):
        v = alpha * np.matmul(M, v) + (1-alpha)*v
        #print(v)
        for j in range(n):
            k = (v**beta) * ((indegree[index2node[j]])**(1-beta))
        #print(k)
        #break 
        i += 1
        if i > 30:
            break
        #print(v)
    #print(v)
    for ind, prob in enumerate(k):
        result.append((index2node[ind], prob))
    result = sorted(result, key=lambda x:x[1], reverse=True)[:num_candidates]
    return result

def Generate_Transfer_Matrix(G):
    """generate transfer matrix given graph"""
    index2node = dict()
    node2index = dict()
    indegree = dict((node2, 0) for node2 in G)
    for index,node in enumerate(G.keys()):
        node2index[node] = index
        index2node[index] = node
    # num of nodes
    n = len(node2index)
    # generate Transfer probability matrix M, shape of (n,n)
    M = np.zeros([n,n])
    for node1 in G.keys():
        for node2 in G[node1]:
            indegree[node2] += 1
            # FIXME: some nodes not in the Graphs.keys, may incur some errors
            try:
                M[node2index[node2],node2index[node1]] = 1/len(G[node1])
            except:
                continue
    return M, node2index, index2node, indegree

if __name__ == '__main__':
    alpha = 0.85
    beta = 0.5
    root = 'A'
    num_iter = 100
    num_candidates = 10
    G = {'A' : {'a' : 1, 'c' : 1},
         'B' : {'a' : 1, 'b' : 1, 'c':1, 'd':1},
         'C' : {'c' : 1, 'd' : 1},
         'a' : {'A' : 1, 'B' : 1},
         'b' : {'B' : 1},
         'c' : {'A' : 1, 'B' : 1, 'C':1},
         'd' : {'B' : 1, 'C' : 1}}
    M, node2index, index2node, indegree = Generate_Transfer_Matrix(G)
    #print(indegree)
    # print transfer matrix
    print(pd.DataFrame(M, index=G.keys(), columns=G.keys()))
    result = KeyRank(M, alpha, beta, root)
    # print results
    print(result)
