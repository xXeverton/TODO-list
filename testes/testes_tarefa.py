# testes_tarefa.py

import unittest
from tarefas import *

class TestTarefa(unittest.TestCase):

    def setUp(self):
        limpaTarefas()

    def test_01_consulta_existente(self):
        # Tem que decidir sobre como testar a consulta de tarefas sem de fato pegar o ngc do outro modulo(ou mudar tudo nao sei)
        self.assertTrue(False)  

    def test_02_consulta_inexistente(self):
        codigo, _ = consultaTarefa("Fantasma")
        self.assertEqual(codigo, 1)

    def test_03_criar_ok(self):
        self.assertEqual(criaTarefa("Estudar", "Capítulo 1", 2, "2025/01/01", "2025/01/02"), 0)

    def test_04_criar_titulo_duplicado(self):
        criaTarefa("Estudar", "Capítulo 1", 2, "2025/01/01", "2025/01/02")
        self.assertEqual(criaTarefa("Estudar", "Outro", 1, "2025/01/03", "2025/01/04"), 1)

    def test_05_criar_titulo_vazio(self):
        self.assertEqual(criaTarefa("", "Descrição", 2, "2025/01/01", "2025/01/02"), 2)

    def test_06_criar_prioridade_invalida(self):
        self.assertEqual(criaTarefa("Arrumar cama", "Manhã", 5, "2025/01/01", "2025/01/02"), 3)

    def test_07_criar_data_invalida(self):
        self.assertEqual(criaTarefa("Tarefa X", "Datas erradas", 2, "2025/01/05", "2025/01/01"), 4)

    def test_08_criar_titulo_muito_longo(self):
        titulo = "A" * 51
        self.assertEqual(criaTarefa(titulo, "Descrição", 2, "2025/01/01", "2025/01/02"), 5)

    def test_09_criar_descricao_muito_longa(self):
        descricao = "X" * 251
        self.assertEqual(criaTarefa("Tarefa Longa", descricao, 2, "2025/01/01", "2025/01/02"), 6)

    def test_10_edita_ok(self):
        criaTarefa("Original", "Desc", 2, "2025/01/01", "2025/01/03")
        resultado = editaTarefa("Original", {
            "titulo": "Editada",
            "descricao": "Nova",
            "prioridade": 1,
            "data_inicio": "2025/01/01",
            "data_vencimento": "2025/01/05"
        })
        self.assertEqual(resultado, 0)
        codigo, _ = consultaTarefa("Editada")
        self.assertEqual(codigo, 0)

    def test_11_edita_inexistente(self):
        self.assertEqual(editaTarefa("Inexistente", {"titulo": "Nova"}), 1)

    def test_12_edita_titulo_vazio(self):
        criaTarefa("Estudar", "Desc", 2, "2025/01/01", "2025/01/02")
        self.assertEqual(editaTarefa("Estudar", {"titulo": ""}), 2)

    def test_13_edita_prioridade_invalida(self):
        criaTarefa("Estudar", "Desc", 2, "2025/01/01", "2025/01/02")
        self.assertEqual(editaTarefa("Estudar", {"prioridade": 9}), 3)

    def test_14_edita_data_invalida(self):
        criaTarefa("Estudar", "Desc", 2, "2025/01/01", "2025/01/02")
        self.assertEqual(editaTarefa("Estudar", {"data_inicio": "2025/01/05", "data_vencimento": "2025/01/01"}), 4)

    def test_15_edita_titulo_longo(self):
        criaTarefa("Estudar", "Desc", 2, "2025/01/01", "2025/01/02")
        titulo_longo = "A" * 51
        self.assertEqual(editaTarefa("Estudar", {"titulo": titulo_longo}), 5)

    def test_16_edita_descricao_longa(self):
        criaTarefa("Estudar", "Desc", 2, "2025/01/01", "2025/01/02")
        desc_longa = "X" * 251
        self.assertEqual(editaTarefa("Estudar", {"descricao": desc_longa}), 6)

    def test_17_edita_sem_infos(self):
        criaTarefa("Estudar", "Desc", 2, "2025/01/01", "2025/01/02")
        self.assertEqual(editaTarefa("Estudar", {}), 7)

    def test_18_apaga_ok(self):
        criaTarefa("Estudar", "Desc", 2, "2025/01/01", "2025/01/02")
        self.assertEqual(apagaTarefa("Estudar"), 0)
        codigo, _ = consultaTarefa("Estudar")
        self.assertEqual(codigo, 1)

    def test_19_apaga_inexistente(self):
        self.assertEqual(apagaTarefa("Inexistente"), 1)

    def test_20_apaga_titulo_vazio(self):
        self.assertEqual(apagaTarefa(""), 2)

    def test_21_apaga_titulo_longo(self):
        titulo_longo = "A" * 51
        self.assertEqual(apagaTarefa(titulo_longo), 3)

if __name__ == "__main__":
    unittest.main()
