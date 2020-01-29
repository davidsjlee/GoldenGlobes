import json

# helper function to load json files for golden globes
def load_json(path, year):
    with open(path + 'gg' + year + '.json') as f:
        data = json.load(f)
    return data
