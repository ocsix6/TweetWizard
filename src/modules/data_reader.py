import configparser
import csv
import json

def read_config(file):
    # Create configparser object
    config = configparser.ConfigParser()
    # Read the config file
    config.read(file)
    return config

def load_csv(file_path, sep=","):
    with open(file_path, "r") as f:
        reader = csv.DictReader(f, delimiter=sep)
        return list(reader)

def load_json(file):
    # Read the json file
    with open(file) as f:
        data = json.load(f)
    return data

def find_json_entry_by_mail(json, mail):
    # Find the entry by mail
    for i in range(len(json)):
        if json[i]["mail"] == mail:
            return i
    return None