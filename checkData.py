#!/usr/bin/env python3 

# check data consistency for the data from 104 API

import sys, json

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print('Usage:', sys.argv[0], 'JobJsonFile JobCategory', file=sys.stderr)
		exit(-1)
		
	# load jobs 
	with open(sys.argv[1], 'r') as f:
		jobs = json.load(f)
	
	titleCnt = 0
	catCnt = 0 
	uniqueJobs = dict()
	for cat, jobDict in jobs.items():
		for jobID, job in jobDict.items():
			if jobID not in uniqueJobs:
				uniqueJobs[jobID] = job 
			else:
				job1 = uniqueJobs[jobID]
				job2 = job
				
				# check title
				if job1['title'] != job2['title']:
					print(jobID)
					print(job1['title'])
					print(job2['title'])
					titleCnt += 1
				
				c1 = set(job1['cat'])
				c2 = set(job2['cat'])
				if len(c1 & c2) != len(c1 | c2):
					print(jobID)
					print(job1['cat'])
					print(job2['cat'])
					catCnt += 1
		
	print('#title inconsistent:', titleCnt)
	print('#category inconsistent:', catCnt)
	
	# load 104 job category
	with open(sys.argv[2], 'r') as f:
		cat = json.load(f)
		
