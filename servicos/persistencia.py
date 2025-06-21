
import json, os

__all__ = ["salva_estado", "carrega_estado"]

def salva_estado(data, filename):
    if type(data) is not list:
        return False
    with open(filename,"w") as f:
        json.dump(data, f, indent=2)

    return True

def carrega_estado(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
        return data
    else:
        return []