import sys, json, re

rmRegexWords = [
	"臺北", "台北", "新北", "桃園", "臺中", "台中", "臺南", "台南", "高雄", "基隆", 
	"新竹", "嘉義", "苗栗", "彰化", "南投", "雲林", "嘉義", "屏東", "宜蘭", "花蓮",
	"臺東", "澎湖", "金門", "連江", "日本", "越南", "泰國", "中國", "大陸", 
	"北部", "北區", "南部", "南區", "東部", "東區", "西部", "西區", "全區", "中部", 
	"中區", ""
	"[0-9]", 
	"年薪", "月薪", "時薪", "底薪", "急徵", "兼職", "正職", "無經驗", "優渥", "薪資", 
	"分紅", "津貼", "熱忱", "興趣", "不限", "週休", "周休", "月休", "倒扣", "不須",
	"不需", "條件", "面議", "高薪", "履歷", "快投", "轉正", "可在家", "獎金", "搶手",
	"做滿", "我們", "任選", "免費", "地點", "知名", "幫你", "男女", "無須", "月領",
	"月入", "不用", 
	"周一", "周二", "周三", "周四", "周五", "周六", "周日", "每周", "配合", "加班",
	"週一", "週二", "週三", "週四", "週五", "週六", "週日", "每週", "二日",
	"大哥大", "台灣之星", "遠傳", "SOGO", "新光三越", "旺旺", "中時", "爭鮮"
	
]

rmStr = '|'.join(rmRegexWords)
rmRegex = re.compile(rmStr)
minLength = 1

if __name__ == '__main__':
	tfidf = json.load(sys.stdin)

	newDict = dict()
	for i, (jobCat, titleList) in enumerate(tfidf.items()):
		print('Progress (%d/%d) %s' % (i, len(tfidf), jobCat), file=sys.stderr)
		newList = list()
		for title, value in titleList:
			if len(title) > minLength and rmRegex.search(title) is None:
				newList.append([title, value])
		
		newDict[jobCat] = newList

	json.dump(newDict, sys.stdout, indent=1, ensure_ascii=False)
