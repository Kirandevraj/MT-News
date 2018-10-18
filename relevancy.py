
import pandas as pd
import re

stopWords = pd.read_csv('stopwords.txt').values

def word_tokenizer(query):
    query = re.sub("[!@#$'?]", ' ', query)
    tokenized_query = []
    tokenized_query = query.split()
    for x in stopWords:
        if x in tokenized_query:
            tokenized_query.remove(x)
    return tokenized_query

def cleanLines(lines):
    lines = re.sub("[!@#$'?]", ' ', lines)
    lines = lines.split('.')
    for i in range(len(lines)):
        lines[i] = lines[i][:].split()
        for x in range(len(lines[i])):
            lines[i][x] = lines[i][x].lower()
    words = []
    for x in lines:
        words += x
    return words

def total_repeatition(query,para):
    para = cleanLines(para)
    appraisal = 0
    score = 0
    for i in query:
        flag = 0
        for j in para:
            if(i == j):
                flag = 1
                score+=1
        if flag == 1:
            appraisal += 1
    if appraisal >= len(query) - 1:
        score += appraisal*5
    return score

