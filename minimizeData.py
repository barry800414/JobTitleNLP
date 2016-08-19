#!/usr/bin/env python3 

# minimize data for later usage

import sys, json

def minimize(jobs):
	newJobs = dict()
	for catID, jobDict in jobs.items():
		newJobs[catID] = list()
		for jobID, job in jobDict.items():
			newJobs[catID].append(job['title'])
	return newJobs

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print('Usage:', sys.argv[0], 'inJobJsonFile outJobJsonFile', file=sys.stderr)
		exit(-1)
		
	with open(sys.argv[1], 'r') as f:
		jobs = json.load(f)
	
	newJobs = minimize(jobs)
	
	with open(sys.argv[2], 'w') as f:
		json.dump(newJobs, f, indent=1, ensure_ascii=False)
