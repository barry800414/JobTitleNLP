
import sys, json
from stanford_nlp_client import Client

'''
Input: minimized json file (preprocessed text) 
'''

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print('Usage:', sys.argv[0], 'inJsonFile outJsonFile [segmented]', file=sys.stderr)
		exit(-1)

	segmented = False
	if len(sys.argv) == 4:
		if(sys.argv[3]) == 'segmented':
			segmented = True

	with open(sys.argv[1], 'r') as f:
		data = json.load(f)

	client = Client("http://140.112.31.187", 8011)

	for i, (jobCat, titles) in enumerate(data.items()):
		print('(%d/%d) Now preprocess jobs in category: %s' % (i+1, len(data), jobCat))
		for j in range(len(titles)):
			if j % 100 == 0:
				print('Progress: (%d/%d) job titles' % (j, len(titles)))
			r = client.sendConstParseRequest(titles[j], seg=segmented)
			if r is None:
				print("Error: %s wasn't parsed successfully", file=sys.stderr)
			else:
				titles[j] = r

	with open(sys.argv[2], 'w') as f:
		json.dump(data, f, indent=1, ensure_ascii=False)

