import json, os

filename = "data.json"

__all__ = ["salva_estado", "carrega_estado"]

def salva_estado(data):
    if type(data) is not list:
        return False
    with open(filename,"w") as f:
        json.dump(data, f, indent=2)

    return True

def carrega_estado():
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
        return data
    else:
        return []
