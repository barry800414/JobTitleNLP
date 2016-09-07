#!/usr/bin/env python3 

import sys, json, re
import jieba

'''
	Preprocess text (word segmentation)
'''

# load dictionary file for traditional Chinese in Jieba
jieba.set_dictionary('dict.txt.big')

# segment Chinese string
def segment(str):
	allWords = list()
	for sent in str.split(' '):
		words = jieba.cut(sent, cut_all=False)
		allWords.extend(words)
	return ' '.join(allWords)

	
if __name__ == '__main__':
	if len(sys.argv) != 3:
		print('Usage:', sys.argv[0], 'inJsonFile outJsonFile', file=sys.stderr)
		exit(-1)
	
	# load jobs 
	with open(sys.argv[1], 'r') as f:
		jobs = json.load(f)
	
	for i, (catID, jobDict) in enumerate(jobs.items()):
		print('(%d/%d) Now preprocess jobs in category: %s' % (i+1, len(jobs), catID))
		for jobID, job in jobDict.items():		
			r = segment(job['title'])
			job['title'] = r

	with open(sys.argv[2], 'w') as f:
		json.dump(jobs, f, indent=1, ensure_ascii=False)
		
