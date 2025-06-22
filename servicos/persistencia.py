
import json, os

__all__ = ["salva_estado", "carrega_estado"]

def salva_estado(data, filename):
    path = "data/"+filename
    if type(data) is not list:
        return False
    with open(path,"w") as f:
        json.dump(data, f, indent=2)

    return True

def carrega_estado(filename):
    path = "data/"+filename
    if os.path.exists(path):
        with open(path, "r") as f:
            data = json.load(f)
        return data
    else:
        return []