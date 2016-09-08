
import sys, json, math
from collections import defaultdict

# calculate logP(w1w2 ..)
def calcLogProb(docs, dim=1, logP=None):
    if logP is None:
        logP = defaultdict(float)
    
    for doc in docs:
        words = doc.split(' ')
        for i, w in enumerate(words):
            if i + dim > len(words):
                break
            if dim == 1:
                logP[words[i]] += 1
            else:
                logP[tuple(words[i:i+dim])] += 1 
            
    total = sum(logP.values())
    for key, value in logP.items():
        logP[key] = math.log(value / total)
    return logP

def calcNGram(logP1, logP2):
    # calculate one-gram and bi-gram
    # logP(w1)
    one_gram = logP1  
    
    # logP(w2|w1) = logP(w1w2) - logP(w1)
    bi_gram = dict()
    for (w1, w2), logp in logP2.items():
        if w1 not in bi_gram:
            bi_gram[w1] = dict()
        if w2 not in bi_gram[w1]:
            bi_gram[w1][w2] = math.exp(logp - logP1[w1])

    return one_gram, bi_gram

def calcLogProbAvg(words, one_gram, bi_gram):
    v = one_gram[words[0]]
    for i in range(1, len(words)):
        v = v + bi_gram[words[i-1]][words[i]]
    return v / len(words)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage:', sys.argv[0], 'inJsonFile', file=sys.stderr)
        exit(-1)

    with open(sys.argv[1], 'r') as f:
        data = json.load(f)

    docs = list()
    for jobCat, titles in data.items():
        docs.extend(titles)

    print('Calculating one-gram and bi-gram ...', file=sys.stderr)
    # calculate log probability
    logP1 = calcLogProb(docs, dim=1)
    logP2 = calcLogProb(docs, dim=2)

    one_gram, bi_gram = calcNGram(logP1, logP2)

    print('Start to calculate average of log probability ...', file=sys.stderr)
    for jobCat, titles in data.items():
        avg = dict()  
        for title in titles:
            words = title.split(' ')
            for dim in range(1, 3):
                for i, w in enumerate(words):
                    if i + dim > len(words):
                        break
                    s = tuple(words[i:i+dim])
                    if s not in avg:
                        avg[s] = calcLogProbAvg(s, one_gram, bi_gram)

        for key, value in sorted(list(avg.items()), key=lambda x:x[1], reverse=True):
            print(key, value)
        break
