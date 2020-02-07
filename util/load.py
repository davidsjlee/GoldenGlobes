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

#helper function to read various files
def read_data_from_file(path, year, type):
    if type == 'raw':
        filename = path + 'gg' + str(year) + '.json'
    elif type == 'clean':
        filename = path + 'clean'+ str(year) + '.json'
    elif type == 'people':
        filename = path + 'people'+ str(year) + '.json'
    elif type == 'movie':
        filename = path + 'movie'+ str(year) + '.json'
    data = []
    with open(filename, 'r') as f:
        data = json.load(f)
    return data
