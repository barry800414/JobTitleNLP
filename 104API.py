#!/usr/bin/env python3 

# invoke 104 API to get all 104 jobs 

import sys
import requests
import json
from getCat import getL3ID
	
API_URL = "http://www.104.com.tw/i/apis/jobsearch.cfm"
	
def getJobsByCatID(catID, verbose=0):
	jobs = dict()	
	
	payload = {
		"cat": catID,
		"role": 1,
		"fmt": 8,
		"cols": "J"
	}
	try:
		r = requests.get(API_URL, params = payload)
		if verbose >= 1: 
			print(r.url, r.status_code)
		
		p = r.json()
		nPage = int(p['TOTALPAGE'])
		
		for i in range(0, nPage):
			jobs.update(__getJobsByCatID(catID, i+1, verbose))
		
	except Exception as e:
		print(e, file=sys.stderr)
	
	return jobs
		
def __getJobsByCatID(catID, page, verbose=0):
	jobs = dict()
	payload = {
		"cat": catID,
		"role": 1,
		"fmt": 8,
		"cols": "J,JOB,JOBCAT_DESCRIPT",
		"page": page
	}
	try:
		r = requests.get(API_URL, params = payload)
		if verbose >= 2:
			print(r.url, r.status_code)
		
		p = r.json()
		
		for d in p['data']:
			cat = [c for c in d['JOBCAT_DESCRIPT'].split('@') if c != "類目"]
			jobs[d['J']] = { "title": d['JOB'], "cat": cat }
			
	except Exception as e:
		print(e, file=sys.stderr)
		
	return jobs
	

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print('Usage:', sys.argv[0], 'category outJsonFile', file=sys.stderr)
		exit(-1)
		
	with open(sys.argv[1], 'r') as f:
		rawCat = json.load(f)
		cat = getL3ID(rawCat)
	
	# all job category ids 
	allJobs = dict()
	for i, (catID, catName) in enumerate(cat.items()):
		print('(%d/%d) Start crawling Category %s(%s):' % (i+1, len(cat), catName, catID), end='', flush=True)
		jobs = getJobsByCatID(catID)
		print('%d' % len(jobs), flush=True)
		allJobs[catName] = jobs
		
	with open(sys.argv[2], 'w') as f:
		json.dump(allJobs, f, indent=1, ensure_ascii=False)
	

