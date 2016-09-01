
import sys, json
from collections import defaultdict
from getCat import *

with open('jobs.min.json', 'r') as f:
    data = json.load(f)

with open('104RawCategory.json', 'r') as f:
    rawCat = json.load(f)

to2 = getL3ToL2(rawCat)
to1 = getL2ToL1(rawCat)

L3Cnt = dict()
L2Cnt = defaultdict(int)
L1Cnt = defaultdict(int)

for L3 in data.keys():
    L3Cnt[L3] = len(data[L3])
    L2Cnt[to2[L3]] += L3Cnt[L3]
    L1Cnt[to1[to2[L3]]] += L3Cnt[L3]

with open('L1.csv', 'w') as f:
    for name, cnt in sorted(list(L1Cnt.items()), key=lambda x:x[1], reverse=True):
        print(name, cnt, sep=',', file=f)

with open('L2.csv', 'w') as f:
    for name, cnt in sorted(list(L2Cnt.items()), key=lambda x:x[1], reverse=True):
        print(name, cnt, sep=',', file=f)

with open('L3.csv', 'w') as f:
    for name, cnt in sorted(list(L3Cnt.items()), key=lambda x:x[1], reverse=True):
        print(name, cnt, sep=',', file=f)