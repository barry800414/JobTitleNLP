
with open('p.txt') as f:
	for line in f:
		print('"%s": "%s"' % (line[0], hex(ord(line[0]))))