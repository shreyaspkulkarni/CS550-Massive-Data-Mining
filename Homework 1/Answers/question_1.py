# -*- coding: utf-8 -*-
"""question_1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lVV5kIpaxCkAcRK6xzIyRw6wYClMmavb
"""

!pip install pyspark

#importing libraries
from pyspark import SparkContext, SparkConf

conf = SparkConf()
sc = SparkContext(conf=conf)

data = sc.textFile('soc-LiveJournal1Adj.txt')

def process_line(line):
    user, friends = line.split('\t')
    if friends != '':
        list_of_friends = friends.split(',')
    else:
        list_of_friends = []
    return (user, list_of_friends)
def process_pairs(line):
    user = line[0]
    list_of_friends = line[1]
    friend_pairs = []
    for friend in list_of_friends:
        pair = (user, friend)
        if user > friend:
            pair = (friend, user)
        friend_pairs.append((pair, 0))
    for i in range(len(list_of_friends)-1):
        for j in range(i+1, len(list_of_friends)):
            pair = (list_of_friends[i], list_of_friends[j])
            if list_of_friends[i] > list_of_friends[j]:
                pair = (list_of_friends[j], list_of_friends[i])
            friend_pairs.append((pair, 1))
    return friend_pairs

map1 = data.map(lambda line: process_line(line))
pairs = map1.flatMap(lambda line: process_pairs(line))
mutual = pairs.groupByKey().filter(lambda pair: 0 not in pair[1]).flatMapValues(lambda x: x)
reduce1 = mutual.reduceByKey(lambda x, y: x+y)
recommendations = reduce1.flatMap(lambda pair: [(pair[0][0], (pair[0][1], pair[1])), (pair[0][1], (pair[0][0], pair[1]))]).groupByKey().mapValues(list) 
final = recommendations.map(lambda user: (user[0], sorted(user[1], key = lambda x: (-x[1], int(x[0])))))

result = final.collect()

users = ['924', '8941', '8942', '9019', '9020', '9021', '9022', '9990', '9992', '9993']
for user in users:
    for line in result:
        id, output = line
        if id == user:
            PeopleYouMightKnow = []
            for i in output:
                PeopleYouMightKnow.append(i[0])
            print(user, PeopleYouMightKnow)