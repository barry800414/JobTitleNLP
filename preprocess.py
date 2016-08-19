#!/usr/bin/env python3 

import sys, json, re
import jieba

'''
	Preprocess text (including removing punctuation and 
	word segmentation)
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

# replace all special characters to whitespace, and
# normalize consecutive whitespaces to one white space
def normalize(str, reObj):
	newStr = reObj.sub(' ', str)
	
	r = re.compile('( )+')
	newStr = r.sub(' ', newStr)
	
	return newStr.strip()
	
def genRegexStr(punc):
	str = ''
	pList = [re.escape(p) for p in punc.keys()]
	str = '(' + '|'.join(pList) + ')'
	return str
	
if __name__ == '__main__':
	if len(sys.argv) != 4:
		print('Usage:', sys.argv[0], 'inJsonFile PunctuationFile outJsonFile', file=sys.stderr)
		exit(-1)
	

	# load punctuation file 
	with open(sys.argv[2], 'r') as f:
		punc = json.load(f)
	# prepare regex for removing punctuation
	regexStr = genRegexStr(punc)
	reObj = re.compile(regexStr)
	
	# load jobs 
	with open(sys.argv[1], 'r') as f:
		jobs = json.load(f)
	
	for i, (catID, jobDict) in enumerate(jobs.items()):
		print('(%d/%d) Now preprocess jobs in category: %s' % (i+1, len(jobs), catID))
		for jobID, job in jobDict.items():		
			r = normalize(job['title'], reObj)
			r = segment(r)
			job['title'] = r

	with open(sys.argv[3], 'w') as f:
		json.dump(jobs, f, indent=1, ensure_ascii=False)
		
	''' test 
	newStr = normalize("【中壢廠】MIS工程師-1", reObj)
	print(newStr)
	print(segment(newStr))
	'''
