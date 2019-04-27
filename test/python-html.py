#!/usr/bin/python3

from yattag import *
doc, tag, text = Doc().tagtext()
filename="index.html"
fp=open(filename,'w')

if not fp:
	print("Can not open ", filename, " for writing.")
	exit(1)

mylist = []
mylist.append('Everybody')
mylist.append('likes')
mylist.append('pandas.')
mystring = ' '.join(mylist)

print(mylist)

doc.asis('<!DOCTYPE html>')
with tag('html'):
    with tag('body'):
        text('Hello world!')


print(indent(doc.getvalue()))
fp.write(indent(doc.getvalue()))
fp.write('\n')
fp.close()

