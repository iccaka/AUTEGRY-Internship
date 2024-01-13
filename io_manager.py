import json
import pandas as pd


def read_json(input_file):
    with open(input_file) as source_file:
        data = json.load(source_file)

    return data


def read_csv(input_file):
    return pd.read_csv(input_file)


def write_json(output_file, data):
    with open(output_file, 'w') as out_file:
        json.dump(data, out_file)

