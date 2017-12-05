from toapi.storage import Store

store = Store()

url = "https://www.google.com..."
html = "<p> Hello, World!</p>"
store.save(url, html)
print(store.get(url))
