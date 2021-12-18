import json

def get():
    with open('flask_app/config/mongodb.json', 'r') as f:
        return json.loads(f.read())