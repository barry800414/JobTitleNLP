import sys,json
sys.path.insert(0, './104API')
from getCat import *


with open('data.json', 'r') as f:
	data = json.load(f)

# to match original 
with open('104API/104RawCategory.json', 'r') as f:
	d = json.load(f)
	cat = getL3ID(d)

catSet = set(cat.values())
leftData = list()
cnt = 0
for d in data:
	if d['job_title'] in catSet:
		cnt += 1
	else:
		leftData.append(d)

print(cnt, len(data))

# to match leftData from 104API
with open('test.json', 'r') as f:
	newCat = json.load(f)

title2Cat = dict()
for jobCat, titles in newCat.items():
	for title, value in titles:
		if title not in title2Cat:
			title2Cat[title] = set()
		title2Cat[title].add(jobCat)

titleSet = set(title2Cat.keys())

cnt = 0
matched = set()
for d in leftData:
	if d['job_title'] in titleSet:
		cnt += 1
		matched.add(d['job_title'])

print(cnt, len(leftData))
for t in matched:
	print(t, title2Cat[t])
