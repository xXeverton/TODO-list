# testes_tarefa.py
import unittest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from entidades.tarefas import *
from servicos.persistencia import *

class TestTarefa(unittest.TestCase):

    def setUp(self):
        limpaTarefas()

    # 1) consultaTarefa básico
    def test_01_consulta_existente(self):
        print("\nCaso Teste 01 - Consulta tarefa existente")
        ambienteDeTesteTarefas()
        codigo, tarefa = consultaTarefa("Tarefa Teste 1")
        self.assertEqual(codigo, 0)
        self.assertEqual(tarefa["titulo"], "Tarefa Teste 1")
        self.assertEqual(tarefa["id"], 1)

    def test_02_consulta_inexistente(self):
        print("\nCaso Teste 02 - Consulta tarefa inexistente")
        codigo, _ = consultaTarefa("Fantasma")
        self.assertEqual(codigo, 1)

    # 2) consultaTodasTarefas
    def test_03_consulta_todas_tarefas(self):
        print("\nCaso Teste 03 - Consulta TODAS as tarefas")
        ambienteDeTesteTarefas()                              # 1 tarefa
        criaTarefa("Extra", "d", 0, "2025/01/01", "2025/01/02")  # +1
        lista = consultaTodasTarefas()
        self.assertEqual(len(lista), 2)
        self.assertIsNot(lista, consultaTodasTarefas())         # deve ser cópia

    # 3) consultaId
    def test_04_consulta_codigo_existente(self):
        print("\nCaso Teste 04 - Consulta código existente")
        ambienteDeTesteTarefas()
        codigo, id_tarefa = consultaId("Tarefa Teste 1")
        self.assertEqual(codigo, 0)
        self.assertEqual(id_tarefa, 1)

    def test_05_consulta_codigo_inexistente(self):
        print("\nCaso Teste 05 - Consulta código inexistente")
        ambienteDeTesteTarefas()
        codigo, id_ = consultaId("Fantasma")
        self.assertEqual(codigo, 1)
        self.assertEqual(id_, -1)

    # 4) ambiente e IDs
    def test_06_ambiente_reseta_id(self):
        print("\nCaso Teste 06 - Ambiente reseta ID")
        criaTarefa("A", "d", 0, "2025/01/01", "2025/01/02")
        _, id1 = consultaId("A")
        self.assertEqual(id1, 1)
        limpaTarefas()
        criaTarefa("B", "d", 0, "2025/01/01", "2025/01/02")
        _, id2 = consultaId("B")
        self.assertEqual(id2, 1)

    def test_07_ids_auto_incrementais(self):
        print("\nCaso Teste 07 - IDs auto-incrementais")
        criaTarefa("X1", "d", 0, "2025/01/01", "2025/01/02")
        criaTarefa("X2", "d", 0, "2025/01/01", "2025/01/02")
        _, id1 = consultaId("X1")
        _, id2 = consultaId("X2")
        self.assertEqual(id1 + 1, id2)

    # 5) prioridades
    def test_08_prioridade_limite_inferior(self):
        print("\nCaso Teste 08 - Prioridade 0 aceita")
        self.assertEqual(criaTarefa("P0", "d", 0, "2025/01/01", "2025/01/02"), 0)

    def test_09_prioridade_limite_superior(self):
        print("\nCaso Teste 09 - Prioridade 4 aceita")
        self.assertEqual(criaTarefa("P4", "d", 4, "2025/01/01", "2025/01/02"), 0)

    def test_10_prioridade_abaixo_limite(self):
        print("\nCaso Teste 10 - Prioridade <0 rejeitada")
        self.assertEqual(criaTarefa("P-1", "d", -1, "2025/01/01", "2025/01/02"), 3)

    def test_11_prioridade_acima_limite(self):
        print("\nCaso Teste 11 - Prioridade >4 rejeitada")
        self.assertEqual(criaTarefa("P5", "d", 5, "2025/01/01", "2025/01/02"), 3)

    # 6) datas malformadas
    def test_12_data_invalida_mes(self):
        print("\nCaso Teste 12 - Data mês inexistente")
        self.assertEqual(criaTarefa("D", "d", 1, "2025/13/01", "2025/12/01"), 4)

    def test_13_data_invalida_formato(self):
        print("\nCaso Teste 13 - Data formato errado")
        self.assertEqual(criaTarefa("D2", "d", 1, "2025-01-01", "2025-01-02"), 4)

    # 7) mutabilidade
    def test_14_mutabilidade_consulta(self):
        print("\nCaso Teste 14 - Consulta devolve cópia")
        criaTarefa("Muta", "orig", 1, "2025/01/01", "2025/01/02")
        _, tarefa = consultaTarefa("Muta")
        tarefa["descricao"] = "mutado"
        _, tarefa2 = consultaTarefa("Muta")
        self.assertEqual(tarefa2["descricao"], "orig")

    # 8) edição preserva ID
    def test_15_edicao_preserva_id(self):
        print("\nCaso Teste 15 - Edição preserva ID")
        criaTarefa("Keep", "d", 1, "2025/01/01", "2025/01/02")
        _, old_id = consultaId("Keep")
        editaTarefa("Keep", {"titulo": "Kept"})
        _, new_id = consultaId("Kept")
        self.assertEqual(old_id, new_id)

    # 9) criação — geral
    def test_16_criar_ok(self):
        print("\nCaso Teste 16 - Criar OK")
        self.assertEqual(criaTarefa("Estudar", "Capítulo 1", 2, "2025/01/01", "2025/01/02"), 0)

    def test_17_criar_titulo_duplicado(self):
        print("\nCaso Teste 17 - Título duplicado")
        criaTarefa("Estudar", "Capítulo 1", 2, "2025/01/01", "2025/01/02")
        self.assertEqual(criaTarefa("Estudar", "Outro", 1, "2025/01/03", "2025/01/04"), 1)

    def test_18_criar_titulo_vazio(self):
        print("\nCaso Teste 18 - Título vazio")
        self.assertEqual(criaTarefa("", "Descrição", 2, "2025/01/01", "2025/01/02"), 2)

    # 10) criação — limites
    def test_19_criar_titulo_muito_longo(self):
        print("\nCaso Teste 19 - Título >50")
        titulo = "A" * 51
        self.assertEqual(criaTarefa(titulo, "Descrição", 2, "2025/01/01", "2025/01/02"), 5)

    def test_20_criar_descricao_muito_longa(self):
        print("\nCaso Teste 20 - Descrição >250")
        descricao = "X" * 251
        self.assertEqual(criaTarefa("Longa", descricao, 2, "2025/01/01", "2025/01/02"), 6)

    # 11) edição
    def test_21_editar_ok(self):
        print("\nCaso Teste 21 - Editar OK")
        criaTarefa("Original", "Desc", 2, "2025/01/01", "2025/01/03")
        self.assertEqual(editaTarefa("Original", {"titulo": "Editada"}), 0)
        self.assertEqual(consultaTarefa("Editada")[0], 0)

    def test_22_editar_inexistente(self):
        print("\nCaso Teste 22 - Editar inexistente")
        self.assertEqual(editaTarefa("Inexistente", {"titulo": "Nova"}), 1)

    def test_23_editar_titulo_vazio(self):
        print("\nCaso Teste 23 - Editar título vazio")
        criaTarefa("Estudar", "Desc", 2, "2025/01/01", "2025/01/02")
        self.assertEqual(editaTarefa("Estudar", {"titulo": ""}), 2)

    # 12) exclusão
    def test_24_apagar_ok(self):
        print("\nCaso Teste 24 - Apagar OK")
        criaTarefa("Apagar", "d", 1, "2025/01/01", "2025/01/02")
        self.assertEqual(apagaTarefa("Apagar"), 0)
        self.assertEqual(consultaTarefa("Apagar")[0], 1)

    def test_25_apagar_inexistente(self):
        print("\nCaso Teste 25 - Apagar inexistente")
        self.assertEqual(apagaTarefa("Nada"), 1)

    def test_26_apagar_titulo_vazio(self):
        print("\nCaso Teste 26 - Apagar título vazio")
        self.assertEqual(apagaTarefa(""), 2)

    def test_27_apagar_titulo_muito_longo(self):
        print("\nCaso Teste 27 - Apagar título >50")
        titulo_longo = "A" * 51
        self.assertEqual(apagaTarefa(titulo_longo), 3)
    
    def test_28_carrega_tarefas_ok(self):
        print("\nCaso Teste 28 - Carrega tarefas OK")
        ambienteDeTesteTarefas()
        esperado = consultaTodasTarefas()

        # escreve arquivo
        self.assertTrue(salva_estado(esperado, 'tarefas.json'))

        limpaTarefas()
        self.assertEqual(consultaTodasTarefas(), [])   # garantimos vazio

        # carrega
        self.assertEqual(carregaTarefas(), 0)

        obtido = consultaTodasTarefas()
        self.assertEqual(esperado, obtido)             # conteúdo igual
        self.assertIsNot(esperado, obtido)             # mas novo objeto

        # contador de ids deve avançar
        criaTarefa("T2","",0,"2025/01/02","2025/01/03")
        self.assertGreater(consultaId("T2")[1],
                        max(t["id"] for t in esperado))
        
        limpaTarefas()

    
def test_29_salva_tarefas_ok(self):
    print("\nCaso Teste 29 - Salva tarefas OK")
    # cria ambiente com alguns registros
    ambienteDeTesteTarefas()
    esperado = consultaTodasTarefas()

    # 1. salva usando a função pública
    self.assertEqual(salvaTarefas(), 0)

    # 2. zera memória e garante que está vazia
    limpaTarefas()
    self.assertEqual(consultaTodasTarefas(), [])

    # 3. recarrega do arquivo salvo
    self.assertEqual(carregaTarefas(), 0)

    obtido = consultaTodasTarefas()

    # 4. conteúdo idêntico, porém lista nova
    self.assertEqual(esperado, obtido)
    self.assertIsNot(esperado, obtido)

    limpaTarefas()          # higiene para evitar interferência em outros testes


if __name__ == "__main__":
    unittest.main()
