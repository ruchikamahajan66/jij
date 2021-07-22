import json

configJson = {}
with open('config/configuration.json', 'r') as f:
    configJson = json.load(f)
