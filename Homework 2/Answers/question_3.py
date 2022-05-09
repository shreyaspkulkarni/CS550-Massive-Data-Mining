# -*- coding: utf-8 -*-
"""question_3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SKJ5f41jCympiIBz0qiv-KtO6PLC7y6a
"""

#importing libraries
import numpy as np

n = 100
beta = 0.8
iter = 40
filepath = 'graph.txt'

#s = source node; d = destination node
M = np.zeros((n,n))
r = np.zeros((n,1))
one = np.ones((n,1))

with open(filepath) as fp:
   line = fp.readline()
   while line:
       node = line.strip().split()
       s = node[0]   
       d = node[1]
       M[int(d)-1][int(s)-1] += 1
       line = fp.readline()

outdegree = np.sum(M,axis = 0)
for i in range(n):
    M[:,i] = np.true_divide(M[:,i],outdegree[i])

rank = one/n
tp = np.multiply(one,1-beta)/n
for i in range(iter):
    rank =  tp + np.matmul(beta*M, rank)

sc = np.transpose(rank)
id = sc.argsort()
highest_page_rank = np.flip(id[0][-5:]) + 1
lowest_page_rank = id[0][:5] + 1

"""(a) List the top 5 node IDs with the highest PageRank scores."""

print("\n node ID \t Page rank")
for i in highest_page_rank:
    print(i, "\t\t", sc[0][i-1])

"""(b) List the bottom 5 node IDs with the lowest PageRank scores."""

print("\nNode ID \t Page rank")
for i in lowest_page_rank:
    print(i, "\t\t", sc[0][i-1])