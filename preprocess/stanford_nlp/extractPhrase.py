import sys, json

class Node:
	def __init__(self, _id, _type, tagWord):
		self.children = None
		self._id = _id
		self._type = _type
		self.tagWord = tagWord

	# assume node id is in ascending order
	def addChild(self, node):
		if self.child is None:
			self.children = list()
		self.child.append(node)


class Tree:
	def __init__(self):
		self.nodes = dict()

	def setRoot(self, root):
		self.root = root

	def addNode(self, node):
		assert node._id not in self.nodes
		self.nodes[node._id] = node
	
	def addEdge(self, parentID, childID):
		assert parentID in self.nodes
		assert childID in self.nodes
		self.nodes[parentID].addChild(self.nodes[childID])

	def getOriginalString(self):
		words = [node.tagWord for node in self.nodes.values() if node._type == 'word']
		return ' '.join(words)

	def traverse(self):
		pass		

	def extractPhrase(self):
		pass


class TreeFactory:
	def build(nodesList, edgesList):
		tree = Tree()
		for node in nodesList:
			s = node.split(' ')
			assert len(s) == 3
			_id, _type, tagWord = int(s[0]), s[1], s[2]
			node = Node(_id, _type, tagWord)
			tree.addNode(node)
			if _id == 0:
				tree.setRoot(node)

		for edge in edgesList:
			s = node.split(' ')
			assert len(s) == 2
			parentID, childID = int(s[0]), int(s[1])
			tree.addEdge(parentID, childID)
		return tree


if __name__ == '__main__':
	if len(sys.argv) < 3:
		print('Usage:', sys.argv[0], 'inJsonFile outJsonFile', file=sys.stderr)
		exit(-1)

	with open(sys.argv[1], 'r') as f:
		data = json.load(f)

	for jobCat, titles in data.items():
		for title in titles:
			tree = TreeFactory.build(title)
			print(tree.getOriginalString())
			break
		break



