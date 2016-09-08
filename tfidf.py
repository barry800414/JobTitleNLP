
import sys, json, math
from collections import defaultdict

def calcTFIDF(data, dim_list=[1,2,3,4,5]):
    result = dict()

    # calculate idf first
    idf = defaultdict(float)
    for jobCat, titles in data.items():
        for dim in dim_list:
            wordSet = set()
            for doc in titles:
                words = doc.split(' ')
                for i, w in enumerate(words):
                    if i + dim > len(words):
                        break
                    s = tuple(words[i:i+dim]) 
                    if s not in wordSet:
                        wordSet.add(s)
                        idf[s] += 1
    for key, value in idf.items():
        idf[key] = math.log(len(data) / value)
    
    # calculate tf
    for jobCat, titles in data.items():
        tf = defaultdict(float)
        for dim in dim_list:
            for doc in titles:
                words = doc.split(' ')
                for i, w in enumerate(words):
                    if i + dim > len(words):
                        break
                    tf[tuple(words[i:i+dim])] += 1
                    
        # calculate tf (probability)
        total = sum(tf.values())
        for key, value in tf.items():
            #tf[key] = math.pow(value / total, 1.0/dim)
            tf[key] = value / total
    
        # finally calculate idf
        tfidf = { k: v*idf[k] for k, v in tf.items() }

        print('==================category : %s===================' % jobCat)
        result[jobCat] = list()
        for key, value in sorted(list(tfidf.items()), key=lambda x:x[1], reverse=True):
            result[jobCat].append([''.join(key), value])

    return result

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage:', sys.argv[0], 'inJsonFile', file=sys.stderr)
        exit(-1)

    with open(sys.argv[1], 'r') as f:
        data = json.load(f)

    result = calcTFIDF(data)

    with open('test.json', 'w') as f:
        json.dump(result, f, indent=1, ensure_ascii=False)

