import json, re

rmRegexWords = [
	"臺北", "台北", "新北", "桃園", "臺中", "台中", "臺南", "台南", "高雄", "基隆", 
	"新竹", "嘉義", "苗栗", "彰化", "南投", "雲林", "嘉義", "屏東", "宜蘭", "花蓮",
	"臺東", "澎湖", "金門", "連江", "[0-9]", "年薪", "月薪", "時薪", "底薪", "急徵", 
	"兼職", "正職", "無經驗", 
]

rmRegex = [re.compile(t) for t in rmRegexWords]

with open('tfidf.json', 'r') as f:
	tfidf = json.load(f)


newDict = dict()
for jobCat, titleList in tfidf.items():
	newList = list()
	for title, value in titleList:
		toRemove = False
		for r in rmRegex:
			if r.search(title) is not None:
				toRemove = True
				break
		if not toRemove: 
			newList.append([title, value])
	newDict[jobCat] = newList

with open('test.json', 'w') as f:
	json.dump(newDict, f, indent=1, ensure_ascii=False)