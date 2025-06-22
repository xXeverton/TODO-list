import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from servicos.persistencia import *
import unittest



if os.path.exists("./data.json"):
    os.remove("./data.json")
tarefa = [{
            "titulo": "Editada",
            "descricao": "Nova",
            "prioridade": 1,
            "data_inicio": "2025/01/01",
            "data_vencimento": "2025/01/05"
}, {
            "titulo": "Editada2",
            "descricao": "Nova",
            "prioridade": 1,
            "data_inicio": "2025/01/01",
            "data_vencimento": "2025/01/05"
        }]
class TestPersist(unittest.TestCase):
    def test_01_carrega_vazio(self):
        self.assertEqual(carrega_estado("data.json"), [])

    def test_02_salva_estado(self):
        self.assertEqual(salva_estado(tarefa,"data.json"), True);
    def test_03_carrega_cheio(self):
        self.assertEqual(carrega_estado("data.json"), tarefa);

unittest.main()
