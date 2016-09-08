import sys, json
import networkx as nx


def getOriginalString(tree):
	words = [node[1]['tagWord'] for node in tree.nodes(data=True) if node[1]['_type'] == 'word']
	return ' '.join(words)

def getPhrases(tree, tagSet=set(['NP'])):
	calcLayer(tree)
	candidate = [n[0] for n in tree.nodes(data=True) if (n[1]['tagWord'] in tagSet and n[1]['_type'] == 'phrase')]
	phrases = list()
	for nodeID in candidate:
		if tree.node[nodeID]['layer'] == 2:
			phrases.append(getString(tree, nodeID))
	return phrases

def getString(tree, nodeID):
	return __traverse(tree, nodeID, '')

def __traverse(tree, nodeID, string):
	if tree.out_degree(nodeID) == 0:
		if tree.node[nodeID]['_type'] == 'word':
			string = string + tree.node[nodeID]['tagWord']
		return string
	else:
		for nextID in sorted(tree.neighbors(nodeID)):
			string = __traverse(tree, nextID, string)
		return string

def calcLayer(tree):
	_calcLayer(tree, 0)

def _calcLayer(tree, nodeID):
	if tree.out_degree(nodeID) == 0:
		tree.node[nodeID]['layer'] = 0
		return 0
	else:
		layer = -1
		for nextID in tree.neighbors(nodeID):
			r = _calcLayer(tree, nextID) + 1
			if r > layer:
				layer = r
		tree.node[nodeID]['layer'] = layer
		return layer

class TreeFactory:
	def build(nodesList, edgesList):
		tree = nx.DiGraph()
		for nStr in nodesList:
			s = nStr.split(' ')
			assert len(s) == 3
			_id, _type, tagWord = int(s[0]), s[1], s[2]
			tree.add_node(_id, _type=_type, tagWord=tagWord)

		for edge in edgesList:
			s = edge.split(' ')
			assert len(s) == 2
			parentID, childID = int(s[0]), int(s[1])
			tree.add_edge(parentID, childID)

		return tree


if __name__ == '__main__':
	if len(sys.argv) < 3:
		print('Usage:', sys.argv[0], 'inJsonFile outJsonFile', file=sys.stderr)
		exit(-1)

	with open(sys.argv[1], 'r') as f:
		data = json.load(f)

	newData = dict()
	for jobCat, titles in data.items():
		newData[jobCat] = list()
		for title in titles:
			r = dict()
			tree = TreeFactory.build(title[0], title[1])
			r['original'] = getOriginalString(tree)
			r['phrases'] = getPhrases(tree)
			newData[jobCat].append(r)
		break

	with open(sys.argv[2], 'w') as f:
		json.dump(newData, f, indent=1, ensure_ascii=False)



