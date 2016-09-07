import requests
import json
import sys


class Client():
	def __init__(self, api_url_prefix="http://localhost", port=8011):
		self.api_url = '%s:%d' % (api_url_prefix, port)
		print(self.api_url)
	
	# segment zht string to zht string, whitespace will be the separator
	def sendSegmentRequest(self, sentence):
		api_url = '%s/segmenter' % (self.api_url)
		payload = {
			's': sentence        
		}
		r = requests.get(api_url, params = payload)
		if r.status_code == 200:
			return r.text
		else:
			return None

	# typedDependency format:  reln gov_index gov_word gov_tag dep_index dep_word dep_tag
	def sendDepParseRequest(self, sentence, seg=False, draw=False, fileFolder=None, 
			fileName=None, returnTokenizedSent=False):
		api_url = '%s/pcfg_dep' % (self.api_url)
		
		if seg == False:
			payload = { 's': sentence }
		else:
			payload = { 'seg_s': sentence }

		if draw == True and fileFolder != None and fileName != None:
			payload['f_folder'] = fileFolder
			payload['f_name'] = fileName
			payload['draw'] = True
			
		r = requests.get(api_url, params = payload)
		if r.status_code == 200:
			lines = r.text.strip().split('\n')
			if not seg:
				tokenizedSent = lines[0]
				typedDependencies = lines[1:]
			else:
				typedDependencies = lines

			if returnTokenizedSent and not seg:
				return (tokenizedSent, typedDependencies)
			else:
				return typedDependencies
		else:
			return None

	#constituent parsing by stanford pcfg parser
	def sendConstParseRequest(self, sentence, seg=False, returnTokenizedSent=False):
		api_url = '%s/pcfg' % (self.api_url)
		
		if seg == False:
			payload = { 's': sentence }
		else:
			payload = { 'seg_s': sentence }
			
		r = requests.get(api_url, params = payload)
		if r.status_code == 200:
			lines = r.text.strip().split('\n')
			if not seg: 
				tokenizedSent = lines[0]
				(nodeLines, edgeLines) = lines2Const(lines[1:])
			else:
				(nodeLines, edgeLines) = lines2Const(lines[1:])

			if returnTokenizedSent and not seg:
				return (tokenizedSent, nodeLines, edgeLines)
			else:
				return (nodeLines, edgeLines)
		else:
			return None

	def sendParseRequest(self, sentence, seg=False, draw=False, fileFolder=None, 
			fileName=None, returnTokenizedSent=False):
		api_url = '%s/pcfg_all' % (self.api_url)
		
		if seg == False:
			payload = { 's': sentence }
		else:
			payload = { 'seg_s': sentence }

		if draw and fileFolder != None and fileName != None:
			payload['f_folder'] = fileFolder
			payload['f_name'] = fileName
			payload['draw'] = True
			
		r = requests.get(api_url, params = payload)
		if r.status_code == 200:
			lines = r.text.strip().split('\n')
			entry = lines[0].split(' ')
			constNum = int(entry[0])
			depNum = int(entry[1])
			#print('constNum:', constNum, 'depNum:', depNum)
			if not seg:
				assert len(lines) == constNum + depNum + 2
				tokenizedSent = lines[1]
				(nodeLines, edgeLines) = lines2Const(lines[2:2+constNum])
				typedDependencies = lines[2+constNum:2+constNum+depNum]
			else:
				assert len(lines) == constNum + depNum + 1
				(nodeLines, edgeLines) = lines2Const(lines[1:1+constNum])
				typedDependencies = lines[1+constNum:1+constNum+depNum]
					
			if returnTokenizedSent and not seg:
				return (tokenizedSent, (nodeLines, edgeLines), typedDependencies)
			else:
				return ((nodeLines, edgeLines), typedDependencies)
		else:
			return None


	def sendTagRequest(self, sentence, seg=False):
		api_url = '%s/pos' % (self.api_url)
		if seg == False:
			payload = { 's': sentence }
		else:
			payload = { 'seg_s': sentence }

		r = requests.get(api_url, params = payload)
		if r.status_code == 200:
			return r.text
		else:
			return None

		
def lines2Const(lines):
    entry = lines[0].strip().split(' ')
    nodesNum = int(entry[0])
    edgesNum = int(entry[1])
    assert (nodesNum + edgesNum + 1) == len(lines)
    nodeLines = lines[1:1+nodesNum]
    edgeLines = lines[1+nodesNum:]
    return (nodeLines, edgeLines)

	
client = Client("http://140.112.31.187", 8011)

# segmentation example
print(client.sendSegmentRequest("我是一名軟體工程師"))

# POS tagging example
print(client.sendTagRequest("我是一名軟體工程師"))

# constituent parsing example
print(client.sendConstParseRequest("我是一名軟體工程師"))

# dependency parsing example
print(client.sendParseRequest("我是一名軟體工程師"))
