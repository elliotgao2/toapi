from lxml import etree

root = etree.HTML("<a src=1312>1<a>")
print(root.cssselect('a')[0])