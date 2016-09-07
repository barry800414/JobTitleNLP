#!/usr/bin/env python3 

# get job category json from 104 website 

import requests
import json
	
	
# get the third layer job category mapping (category id to name)
def getL3ID(rawCat):
	d = dict()
	for L1 in rawCat['n']:
		for L2 in L1['n']:
			for L3 in L2['n']:
				d[L3['no']] = L3['des']
	return d

def getL3ToL2(rawCat):
	to2 = dict()
	for L1 in rawCat['n']:
		for L2 in L1['n']:
			for L3 in L2['n']:
				to2[L3['des']] = L2['des']
	return to2

def getL2ToL1(rawCat):
	to1 = dict()
	for L1 in rawCat['n']:
		for L2 in L1['n']:
			to1[L2['des']] = L1['des']
	return to1

if __name__ == '__main__':
	r = requests.get('http://www.104.com.tw/104i/js/js.cfm?p=documentation.cfm') 
	print('Status:', r.status_code)

	html = r.text

	# find variable
	v = html.find('jsonJobCatRoot')
	# find left '
	s = html.find("'", v)
	# find right ' 
	e = html.find("'", s + 1)

	body = html[s+1:e]
	cat = json.loads(body)
	with open('104RawCategory.json', 'w') as f:
		json.dump(cat, f, ensure_ascii=False, indent=1, sort_keys=True)
		
	
	



