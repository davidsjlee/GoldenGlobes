import json

# helper function to load json files for golden globes
def load_json(path, year):
    with open(path + 'gg' + year + '.json') as f:
        data = json.load(f)
    return data

# helper function to dump to json files for golden globes
def dump_json(path, year, to_dump):
    with open(path + 'gg' + year + '.json', 'w') as f:
        json.dump(to_dump, f, indent=4)
    return
