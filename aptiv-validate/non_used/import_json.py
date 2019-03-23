import json
from pprint import pprint

with open('/Users/diogovalentepcs/PycharmProjects/aptiv/files/dictTeste.json') as f:
    data = json.load(f)

pprint(data)


