from html_reader import HTMLReader
import json

layer = input('>')
data_layer = []

html = HTMLReader()
html.read_url('https://www.logishotels.com/fr/')

page = html.render()

code = json.loads(layer)

for c in code:
    data_layer.append(c["event"])

print(data_layer)