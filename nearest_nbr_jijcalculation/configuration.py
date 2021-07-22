import json

configJson = {}
with open('configuration.json', 'r') as f:
    configJson = json.load(f)
