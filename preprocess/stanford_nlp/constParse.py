
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

	for jobCat, titles in data.items():
		for i in range(len(titles)):
			r = client.sendConstParseRequest(titles[i], seg=segmented)
			print(r)
			if r is None:
				print("Error: %s wasn't parsed successfully", file=sys.stderr)
			else:
				titles[i] = r

	with open(sys.argv[2], 'w') as f:
		json.dump(data, f, indent=1, ensure_ascii=False)

