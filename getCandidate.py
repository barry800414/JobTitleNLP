import json

with open('tfidf.json', 'r') as f:
	tfidf = json.load(f)

with open('data.json', 'r') as f:
	data = json.load(f)

titleSet = set([d['job_title'] for d in data])

top = 0.05

newList = dict()
for jobCat, titleList in tfidf.items():
	tmp = list()
	num = round(top*len(titleList))
	for i, (title, value) in enumerate(titleList):
		if title in titleSet:
			tmp.append([title, 1])
		elif i < num:
			tmp.append([title, value])
	tmp.sort(key=lambda x:x[1], reverse=True)
	newList[jobCat] = tmp
	print(jobCat, len(tmp))

with open('test.json', 'w') as f:
	json.dump(newList, f, indent=1, ensure_ascii=False)

for jobCat, titleList in newList.items():
	print('-----------------Category:%s------------------' % (jobCat))
	for key, value in titleList:
		print(key, value)