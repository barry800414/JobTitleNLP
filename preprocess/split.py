import sys, json

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print('Usage:', sys.argv[0], 'inJsonFile outFolder', file=sys.stderr)
		exit(-1)

	inJsonFile = sys.argv[1]
	outFolder = sys.argv[2]

	with open(inJsonFile, 'r') as f:
		data = json.load(f)

	s = inJsonFile.rfind('/') + 1
	e = inJsonFile.find('.json')
	name = inJsonFile[s:e]

	for i, (jobCat, titles) in enumerate(data.items()):
		newData = {jobCat: titles}
		fileName = '%s/%s-part%d.json' % (outFolder, name, i+1)
		print(fileName)
		with open(fileName, 'w') as f:
			json.dump(newData, f, indent=1, ensure_ascii=False)
		