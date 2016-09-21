
import sys, json, math
from collections import defaultdict

'''
To calculate TF-IDF value for each job-title term (in window-size) in each job category
and to sort the list of term by TF-IDF value

Each job category is viewed as a document in TF-IDF calculation
Each job title is like a sentence in the document
'''

# data: job-category -> list of job-titles
# dim-list: the list of window size 
def calcTFIDF(data, dim_list=[1,2,3,4,5]):
    result = dict()

    # calculate idf first
    print('Calculating idf ...', file=sys.stderr)
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
    print('Calculating tf ...', file=sys.stderr)
    for i, (jobCat, titles) in enumerate(data.items()):
        print('Progress: (%d/%d) %s' % (i, len(data), jobCat), file=sys.stderr)
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

        result[jobCat] = list()
        for key, value in sorted(list(tfidf.items()), key=lambda x:x[1], reverse=True):
            result[jobCat].append([''.join(key), value])

    return result

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage:', sys.argv[0], 'Cat2TitleJsonFile outTFIDFJsonFile', file=sys.stderr)
        exit(-1)

    with open(sys.argv[1], 'r') as f:
        data = json.load(f)

    result = calcTFIDF(data)

    with open(sys.argv[2], 'w') as f:
        json.dump(result, f, indent=1, ensure_ascii=False)

