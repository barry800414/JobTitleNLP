import sys, json


'''
websiteData: data crawled from our website
apiData: data crawled from 104 API (preprocessed and filtered)
'''

def parseArgument(argv):
	top = float(argv[5]) if len(argv) >=6 else 0.05
	minSize = int(argv[6]) if len(argv) >=7 else None
	maxSize = int(argv[7]) if len(argv) >=8 else None
	return (top, minSize, maxSize)

def getCandidateNum(total, top, minSize, maxSize):
	num = round(top*total)
	if minSize is not None:
		if num < minSize:
			num = minSize
	if maxSize is not None:
		if num > maxSize:
			num = maxSize
	return num

if __name__ == '__main__':
	if len(sys.argv) < 5:
		print('Usage:', sys.argv[0], 'webSiteData apiData outJson outTxt [[[topPercent] min] max]', file=sys.stderr)
		exit(-1)

	with open(sys.argv[1], 'r') as f:
		data = json.load(f)
	titleSet = set([d['job_title'] for d in data])

	with open(sys.argv[2], 'r') as f:
		tfidf = json.load(f)

	top, minSize, maxSize = parseArgument(sys.argv)

	newDict = dict()
	for i, (jobCat, titleList) in enumerate(tfidf.items()):
		newList = list()
		num = getCandidateNum(len(titleList), top, minSize, maxSize)
		print('Progress (%d/%d) %s targetNum: %d' % (i, len(tfidf), jobCat, num), file=sys.stderr)
		for title, value in titleList:
			if title in titleSet:
				newList.append([title, 1])
			else:
				newList.append([title, value])
			if len(newList) >= num:
				break
		newList.sort(key=lambda x:x[1], reverse=True)
		newDict[jobCat] = newList

	with open(sys.argv[3], 'w') as f:
		json.dump(newDict, f, indent=1, ensure_ascii=False)

	with open(sys.argv[4], 'w') as f:
		cnt = 0
		for jobCat, titleList in newDict.items():
			print('----------%s----------' % (jobCat), file=f, end='\r\n')
			for key, value in titleList:
				if value == 1:
					print(key, value, file=f, end='\r\n')
				else:
					print(key, file=f, end='\r\n')
