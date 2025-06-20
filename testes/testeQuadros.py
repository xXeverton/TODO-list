import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from entidades.quadros import *
from entidades.tarefas import *

class testeQuadros(unittest.TestCase):

    def test_01_ConsultaQuadroOk(self):
        ambienteDeTesteQuadro()
        print(f"\nCaso Teste 01 - Consulta Quadro\t")

        quadroTeste1 = {'titulo': 'Quadro Teste 1',
                'descricao': 'Descricao 1',
                'colunas': [0, 1, 2]}

        ret = consultaQuadro(quadroTeste1['titulo'])
        self.assertEqual(ret, (0, quadroTeste1))

        apagaTodosOsQuadros()

    def test_02_ConsultaQuadroInexistente(self):
        
        apagaTodosOsQuadros()

        ret = consultaQuadro("Quadro Nao Existente")
        self.assertEqual(ret, (1, None))

        apagaTodosOsQuadros()

        return

    def test_03_CriaQuadroOk(self):
        
        apagaTodosOsQuadros()

        print(f"\nCaso Teste 02 - Cria Quadros\t")

        ret = consultaQuadro('Quadro Teste')
        self.assertEqual(ret, (1, None))
        ret = criaQuadro('Quadro Teste')
        self.assertEqual(ret, 0)
        ret = consultaQuadro('Quadro Teste')
        self.assertEqual(ret, (0, {'titulo': 'Quadro Teste',
                                   'descricao': '',
                                   'colunas': []}))
        
        apagaTodosOsQuadros()

        return
    
    def test_04_CriaQuadroRepetido(self):

        apagaTodosOsQuadros()

        ret = criaQuadro('Quadro Teste')
        self.assertEqual(ret, 0)
        ret = consultaQuadro('Quadro Teste')   
        self.assertEqual(ret, (0, {'titulo': 'Quadro Teste',
                                        'descricao': '',
                                        'colunas': []}))
        ret = criaQuadro('Quadro Teste')
        self.assertEqual(ret, 1)

        apagaTodosOsQuadros()

        return
    
    def test_05_CriaQuadroVazio(self):

        apagaTodosOsQuadros()

        ret = criaQuadro('')
        self.assertEqual(ret, 2)

        apagaTodosOsQuadros()

        return
    
    def test_06_ApagaQuadroOk(self):
        
        ambienteDeTesteQuadro()

        print(f"\nCaso Teste 03 - Apaga Quadro\t")

        quadroTeste1 = {'titulo': 'Quadro Teste 1',
                'descricao': 'Descricao 1',
                'colunas': [0, 1, 2]}
        
        ret = consultaQuadro(quadroTeste1['titulo'])
        self.assertEqual(ret, (0, quadroTeste1))
        ret = apagaQuadro(quadroTeste1['titulo'])
        self.assertEqual(ret, 0)
        ret = consultaQuadro(quadroTeste1['titulo'])
        self.assertEqual(ret, (1, None))

        apagaTodosOsQuadros()

        return
    
    def test_07_ApagaQuadroInexistente(self):
        
        apagaTodosOsQuadros()

        ret = consultaQuadro('Quadro Teste')
        self.assertEqual(ret, (1, None))
        ret = apagaQuadro('Quadro Teste')
        self.assertEqual(ret, 1)

        apagaTodosOsQuadros()

        return
    
    def test_08_ConsultaColunaOk(self):
        
        print(f"\nCaso Teste 04 - Consulta Coluna\t")

        ambienteDeTesteQuadro()

        quadroTeste1 = {'titulo': 'Quadro Teste 1',
                        'descricao': 'Descricao 1',
                        'colunas': [0, 1, 2]}
        ret = consultaColuna(quadroTeste1['titulo'], 'ColunaTeste1.1')
        self.assertEqual(ret, (0, {'titulo': 'ColunaTeste1.1',
                                   'tarefas': [1, 2, 3]}))
        ret = apagaQuadro('Quadro Teste')

        apagaTodosOsQuadros()

        return
    
    def test_09_ConsultaColunaQuadroInexistente(self):

        apagaTodosOsQuadros()

        ret = consultaQuadro('Quadro Teste')
        self.assertEqual(ret, (1, None))
        ret = consultaColuna('Quadro Teste', 'To Do')
        self.assertEqual(ret, (1, None))
        ret = apagaQuadro('Quadro Teste')

        apagaTodosOsQuadros()

        return

    def test_10_ConsultaColunaInexistente(self):

        apagaTodosOsQuadros()

        ret = criaQuadro('Quadro Teste')
        self.assertEqual(ret, 0)
        ret = consultaColuna('Quadro Teste', 'To Do')
        self.assertEqual(ret, (2, None))

        apagaTodosOsQuadros()

        return

    def test_11_CriaColunaOk(self):
        
        print(f"\nCaso Teste 05 - Cria Coluna\t")

        apagaTodosOsQuadros()

        ret = criaQuadro('Quadro Teste')
        self.assertEqual(ret, 0)
        ret = criaColuna('Quadro Teste', 'Coluna Teste')
        self.assertEqual(ret, 0)
        ret = consultaColuna('Quadro Teste', 'Coluna Teste')
        self.assertEqual(ret, (0, {'titulo': 'Coluna Teste',
                                   'tarefas': []}))

        apagaTodosOsQuadros()

        return
    
    def test_12_CriaColunaQuadroInexistente(self):

        apagaTodosOsQuadros()

        ret = consultaQuadro('Quadro Teste')
        self.assertEqual(ret, (1, None))
        ret = criaColuna('Quadro Teste', 'To Do')
        self.assertEqual(ret, 1)

        apagaTodosOsQuadros()

        return
    
    def test_13_CriaColunaVazia(self):

        apagaTodosOsQuadros()

        ret = criaQuadro('Quadro Teste')
        self.assertEqual(ret, 0)
        ret = criaColuna('Quadro Teste', '')
        self.assertEqual(ret, 2)

        apagaTodosOsQuadros()

        return
    
    def test_14_CriaColunaRepetida(self):

        apagaTodosOsQuadros()

        ret = criaQuadro('Quadro Teste')
        self.assertEqual(ret, 0)
        ret = criaColuna('Quadro Teste', 'To Do')
        self.assertEqual(ret, 0)
        ret = consultaQuadro('Quadro Teste')
        self.assertEqual(ret, (0, {'titulo': 'Quadro Teste',
                                   'descricao': '',
                                   'colunas': ret[1]['colunas']}))
        ret = criaColuna('Quadro Teste', 'To Do')
        self.assertEqual(ret, 3)

        apagaTodosOsQuadros()

        return

    def test_15_RemoveColunaOk(self):
        
        print(f"\nCaso Teste 05 - Remove Coluna\t")

        apagaTodosOsQuadros()

        ret = criaQuadro('Quadro Teste')
        self.assertEqual(ret, 0)
        ret = criaColuna('Quadro Teste', 'To Do')
        self.assertEqual(ret, 0)
        ret = consultaColuna('Quadro Teste', 'To Do')
        self.assertEqual(ret, (0, {'titulo': 'To Do',
                                            'tarefas': []}))
        ret = apagaColuna('Quadro Teste', 'To Do')
        self.assertEqual(ret, 0)
        ret = consultaQuadro('Quadro Teste')
        self.assertEqual(ret, (0, {'titulo': 'Quadro Teste',
                                        'descricao': '',
                                        'colunas': []}))

        apagaTodosOsQuadros()

        return
    
    def test_16_RemoveColunaQuadroInexistente(self):

        apagaTodosOsQuadros()

        ret = consultaQuadro('Quadro Teste')
        self.assertEqual(ret, (1, None))
        ret = apagaColuna('Quadro Teste', 'To Do')
        self.assertEqual(ret, 1)

        apagaTodosOsQuadros()

        return
    
    def test_17_RemoveColunaInexistente(self):

        apagaTodosOsQuadros()

        ret = criaQuadro('Quadro Teste')
        self.assertEqual(ret, 0)
        ret = apagaColuna('Quadro Teste', 'To Do')
        self.assertEqual(ret, 2)

        apagaTodosOsQuadros()

        return
    
    def test_18_EditaColunaOk(self):

        apagaTodosOsQuadros()

        print(f"\nCaso Teste 07 - Edita Coluna\t")

        ret = criaQuadro('Quadro Teste')
        self.assertEqual(ret, 0)
        ret = criaColuna('Quadro Teste', 'To Do')
        self.assertEqual(ret, 0)
        ret = editaColuna('Quadro Teste', 'To Do', 'To Do Novo')
        self.assertEqual(ret, 0)
        ret = consultaColuna('Quadro Teste', 'To Do')
        self.assertEqual(ret, (2, None))
        ret = consultaColuna('Quadro Teste', 'To Do Novo')
        self.assertEqual(ret, (0, {'titulo': 'To Do Novo',
                                        'tarefas': []}))

        apagaTodosOsQuadros()

        return
    
    def test_19_EditaColunaQuadroInexistente(self):

        apagaTodosOsQuadros()

        ret = consultaQuadro('Quadro Teste')
        self.assertEqual(ret, (1, None))
        ret = editaColuna('Quadro Teste', 'To Do', 'To Do Novo')
        self.assertEqual(ret, 1)

        apagaTodosOsQuadros()

        return
    
    def test_20_EditaColunaAntigaInexistente(self):

        apagaTodosOsQuadros()

        ret = criaQuadro('Quadro Teste')
        self.assertEqual(ret, 0)
        ret = consultaColuna('Quadro Teste', 'To Do')
        self.assertEqual(ret, (2, None))
        ret = editaColuna('Quadro Teste', 'To Do', 'To Do Novo')
        self.assertEqual(ret, 2)
        ret = apagaQuadro('Quadro Teste')

        apagaTodosOsQuadros()

        return
    
    def test_21_EditaColunaNovaVazia(self):

        apagaTodosOsQuadros()

        ret = criaQuadro('Quadro Teste')
        self.assertEqual(ret, 0)
        ret = criaColuna('Quadro Teste', 'To Do')
        self.assertEqual(ret, 0)
        ret = editaColuna('Quadro Teste', 'To Do', '')
        self.assertEqual(ret, 3)

        apagaTodosOsQuadros()

        return
    
    def test_22_EditaColunaNovaRepetida(self):

        apagaTodosOsQuadros()

        ret = criaQuadro('Quadro Teste')
        self.assertEqual(ret, 0)
        ret = criaColuna('Quadro Teste', 'To Do')
        self.assertEqual(ret, 0)
        ret = criaColuna('Quadro Teste', 'To Do Novo')
        self.assertEqual(ret, 0)
        ret = editaColuna('Quadro Teste', 'To Do', 'To Do Novo')
        self.assertEqual(ret, 4)

        apagaTodosOsQuadros()

        return
    
    def test_23_ConsultaTodosQuadrosOk(self):

        apagaTodosOsQuadros()

        print(f"\nCaso Teste 08 - Consulta Todos os Quadros\t")

        ret = criaQuadro('Quadro Teste')
        self.assertEqual(ret, 0)
        ret = criaQuadro('Quadro Teste2')
        self.assertEqual(ret, 0)
        ret = consultaTodosQuadros()
        self.assertEqual(ret, [{'titulo': 'Quadro Teste',
                                    'descricao': '',
                                    'colunas': []},
                                    {'titulo': 'Quadro Teste2',
                                    'descricao': '',
                                    'colunas': []}])

        apagaTodosOsQuadros()

        return
    
    def test_24_AdicionaTarefaAQuadroOk(self):

        apagaTodosOsQuadros()

        print(f"\nCaso Teste 09 - Adiciona Tarefa Ao Quadro\t")

        ret = criaQuadro('Quadro Teste')
        self.assertEqual(ret, 0)
        ret = criaColuna('Quadro Teste', 'Coluna Teste')
        self.assertEqual(ret, 0)
        ret = criaTarefa('Tarefa Teste', '', 0, '2005/09/10', '2005/09/10')
        self.assertEqual(ret, 0)
        ret = adicionaTarefaAoQuadro('Quadro Teste', 'Coluna Teste', 'Tarefa Teste')
        self.assertEqual(ret, 0)
        ret = consultaColuna('Quadro Teste', 'Coluna Teste')
        self.assertEqual(ret, (0, {'titulo': 'Coluna Teste',
                                        'tarefas': [{"titulo": 'Tarefa Teste',
                                                    "descricao": '',
                                                    "prioridade": 0,
                                                    "data_inicio": '2005/09/10',
                                                    "data_vencimento": '2005/09/10'}]}))
        ret = apagaTarefa('Tarefa Teste')

        apagaTodosOsQuadros()

        return
    
    def test_25_AdicionaTarefaAQuadroInexistente(self):

        apagaTodosOsQuadros()

        ret = consultaQuadro('Quadro Teste')
        self.assertEqual(ret, (1, None))
        ret = criaColuna('Quadro Teste', 'Coluna Teste')
        self.assertEqual(ret, 1)
        ret = criaTarefa('Tarefa Teste', '', 0, '2005/09/10', '2005/09/10')
        self.assertEqual(ret, 0)
        ret = adicionaTarefaAoQuadro('Quadro Teste', 'Coluna Teste', 'Tarefa Teste')
        self.assertEqual(ret, 1)
        ret = apagaTarefa('Tarefa Teste')

        apagaTodosOsQuadros()

        return
    
    def test_26_AdicionaTarefaAQuadroColunaInexistente(self):

        apagaTodosOsQuadros()

        ret = criaQuadro('Quadro Teste')
        self.assertEqual(ret, 0)
        ret = criaTarefa('Tarefa Teste', '', 0, '2005/09/10', '2005/09/10')
        self.assertEqual(ret, 0)
        ret = adicionaTarefaAoQuadro('Quadro Teste', 'Coluna Teste', 'Tarefa Teste')
        self.assertEqual(ret, 2)
        ret = apagaTarefa('Tarefa Teste')

        apagaTodosOsQuadros()

        return
    
    def test_27_AdicionaTarefaAQuadroTarefaInexistente(self):

        apagaTodosOsQuadros()

        ret = criaQuadro('Quadro Teste')
        self.assertEqual(ret, 0)
        ret = criaColuna('Quadro Teste', 'Coluna Teste')
        self.assertEqual(ret, 0)
        ret = adicionaTarefaAoQuadro('Quadro Teste', 'Coluna Teste', 'Tarefa Teste')
        self.assertEqual(ret, 3)

        apagaTodosOsQuadros()

        return
    
    def test_28_RemoveTarefaDoQuadroOk(self):

        apagaTodosOsQuadros()

        print(f"\nCaso Teste 10 - Remove Tarefa do Quadro\t")

        ret = criaQuadro('Quadro Teste')
        self.assertEqual(ret, 0)
        ret = criaColuna('Quadro Teste', 'Coluna Teste')
        self.assertEqual(ret, 0)
        ret = criaTarefa('Tarefa Teste', '', 0, '2005/09/10', '2005/09/10')
        self.assertEqual(ret, 0)
        ret = adicionaTarefaAoQuadro('Quadro Teste', 'Coluna Teste', 'Tarefa Teste')
        self.assertEqual(ret, 0)
        ret = consultaColuna('Quadro Teste', 'Coluna Teste')
        self.assertEqual(ret, (0, {'titulo': 'Coluna Teste',
                                'tarefas': [{"titulo": 'Tarefa Teste',
                                            "descricao": '',
                                            "prioridade": 0,
                                            "data_inicio": '2005/09/10',
                                            "data_vencimento": '2005/09/10'}]}))
        ret = removeTarefaDoQuadro('Quadro Teste', 'Coluna Teste', 'Tarefa Teste')
        self.assertEqual(ret, 0)
        ret = consultaColuna('Quadro Teste', 'Coluna Teste')
        self.assertEqual(ret, (0, {'titulo': 'Coluna Teste',
                                        'tarefas': []}))
        ret = apagaTarefa('Tarefa Teste')

        apagaTodosOsQuadros()

        return 
    
    def test_29_RemoveTarefaDoQuadroInexistente(self):

        apagaTodosOsQuadros()

        ret = consultaQuadro('Quadro Teste')
        self.assertEqual(ret, (1, None))
        ret = criaColuna('Quadro Teste', 'Coluna Teste')
        self.assertEqual(ret, 1)
        ret = criaTarefa('Tarefa Teste', '', 0, '2005/09/10', '2005/09/10')
        self.assertEqual(ret, 0)
        ret = adicionaTarefaAoQuadro('Quadro Teste', 'Coluna Teste', 'Tarefa Teste')
        self.assertEqual(ret, 1)
        ret = removeTarefaDoQuadro('Quadro Teste', 'Coluna Teste', 'Tarefa Teste')
        self.assertEqual(ret, 1)
        ret = apagaTarefa('Tarefa Teste')

        apagaTodosOsQuadros()

        return 
    
    def test_30_RemoveTarefaDoQuadroColunaInexistente(self):

        apagaTodosOsQuadros()

        ret = criaQuadro('Quadro Teste')
        self.assertEqual(ret, 0)
        ret = criaTarefa('Tarefa Teste', '', 0, '2005/09/10', '2005/09/10')
        self.assertEqual(ret, 0)
        ret = adicionaTarefaAoQuadro('Quadro Teste', 'Coluna Teste', 'Tarefa Teste')
        self.assertEqual(ret, 2)
        ret = removeTarefaDoQuadro('Quadro Teste', 'Coluna Teste', 'Tarefa Teste')
        self.assertEqual(ret, 2)
        ret = apagaTarefa('Tarefa Teste')

        apagaTodosOsQuadros()

        return 
    
    def test_31_RemoveTarefaDoQuadroTarefaInexistente(self):

        apagaTodosOsQuadros()

        ret = criaQuadro('Quadro Teste')
        self.assertEqual(ret, 0)
        ret = criaColuna('Quadro Teste', 'Coluna Teste')
        self.assertEqual(ret, 0)
        ret = adicionaTarefaAoQuadro('Quadro Teste', 'Coluna Teste', 'Tarefa Teste')
        self.assertEqual(ret, 3)
        ret = removeTarefaDoQuadro('Quadro Teste', 'Coluna Teste', 'Tarefa Teste')
        self.assertEqual(ret, 3)

        apagaTodosOsQuadros()

        return 
    
    def test_32_MoverTarefaEntreColunasOk(self):

        apagaTodosOsQuadros()

        print(f"\nCaso Teste 10 - Mover Tarefa Entre Colunas\t")

        ret = criaQuadro('Quadro Teste')
        self.assertEqual(ret, 0)
        ret = criaColuna('Quadro Teste', 'Backlog')
        self.assertEqual(ret, 0)
        ret = criaColuna('Quadro Teste', 'Complete')
        self.assertEqual(ret, 0)
        ret = criaTarefa('Tarefa Teste', '', 0, '2005/09/10', '2005/09/10')
        self.assertEqual(ret, 0)
        ret = adicionaTarefaAoQuadro('Quadro Teste', 'Backlog', 'Tarefa Teste')
        self.assertEqual(ret, 0)
        ret = consultaColuna('Quadro Teste', 'Backlog')
        self.assertEqual(ret, (0, {'titulo': 'Backlog',
                                'tarefas': [{"titulo": 'Tarefa Teste',
                                            "descricao": '',
                                            "prioridade": 0,
                                            "data_inicio": '2005/09/10',
                                            "data_vencimento": '2005/09/10'}]}))
        ret = consultaColuna('Quadro Teste', 'Complete')
        self.assertEqual(ret, (0, {'titulo': 'Complete',
                                'tarefas': []}))
        ret = moverTarefaEntreColunas('Quadro Teste', 'Backlog', 'Complete', 'Tarefa Teste')
        self.assertEqual(ret, 0)
        ret = consultaColuna('Quadro Teste', 'Backlog')
        self.assertEqual(ret, (0, {'titulo': 'Backlog',
                                'tarefas': []}))
        ret = consultaColuna('Quadro Teste', 'Complete')
        self.assertEqual(ret, (0, {'titulo': 'Complete',
                                        'tarefas': [{"titulo": 'Tarefa Teste',
                                                    "descricao": '',
                                                    "prioridade": 0,
                                                    "data_inicio": '2005/09/10',
                                                    "data_vencimento": '2005/09/10'}]}))
        ret = apagaTarefa('Tarefa Teste')

        apagaTodosOsQuadros()

        return 
    
    def test_33_MoverTarefaEntreColunasQuadroInexistente(self):

        apagaTodosOsQuadros()

        ret = consultaQuadro('Quadro Teste')
        self.assertEqual(ret, (1, None))
        ret = criaColuna('Quadro Teste', 'Backlog')
        self.assertEqual(ret, 1)
        ret = criaColuna('Quadro Teste', 'Complete')
        self.assertEqual(ret, 1)
        ret = criaTarefa('Tarefa Teste', '', 0, '2005/09/10', '2005/09/10')
        self.assertEqual(ret, 0)
        ret = adicionaTarefaAoQuadro('Quadro Teste', 'Backlog', 'Tarefa Teste')
        self.assertEqual(ret, 1)
        ret = moverTarefaEntreColunas('Quadro Teste', 'Backlog', 'Complete', 'Tarefa Teste')
        self.assertEqual(ret, 1)
        ret = apagaTarefa('Tarefa Teste')

        apagaTodosOsQuadros()

        return 
    
    def test_34_MoverTarefaEntreColunasOrigemInexistente(self):

        apagaTodosOsQuadros()

        ret = criaQuadro('Quadro Teste')
        self.assertEqual(ret, 0)
        ret = criaColuna('Quadro Teste', 'Complete')
        self.assertEqual(ret, 0)
        ret = criaTarefa('Tarefa Teste', '', 0, '2005/09/10', '2005/09/10')
        self.assertEqual(ret, 0)
        ret = adicionaTarefaAoQuadro('Quadro Teste', 'Backlog', 'Tarefa Teste')
        self.assertEqual(ret, 2)
        ret = moverTarefaEntreColunas('Quadro Teste', 'Backlog', 'Complete', 'Tarefa Teste')
        self.assertEqual(ret, 2)
        ret = apagaTarefa('Tarefa Teste')

        apagaTodosOsQuadros()

        return

    def test_35_MoverTarefaEntreColunasDestinoInexistente(self):

        apagaTodosOsQuadros()

        ret = criaQuadro('Quadro Teste')
        self.assertEqual(ret, 0)
        ret = criaColuna('Quadro Teste', 'Backlog')
        self.assertEqual(ret, 0)
        ret = criaTarefa('Tarefa Teste', '', 0, '2005/09/10', '2005/09/10')
        self.assertEqual(ret, 0)
        ret = adicionaTarefaAoQuadro('Quadro Teste', 'Backlog', 'Tarefa Teste')
        self.assertEqual(ret, 0)
        ret = moverTarefaEntreColunas('Quadro Teste', 'Backlog', 'Complete', 'Tarefa Teste')
        self.assertEqual(ret, 3)
        ret = apagaTarefa('Tarefa Teste')

        apagaTodosOsQuadros()

        return  
    
    def test_36_MoverTarefaEntreColunasTarefaInexistente(self):

        apagaTodosOsQuadros()

        ret = criaQuadro('Quadro Teste')
        self.assertEqual(ret, 0)
        ret = criaColuna('Quadro Teste', 'Backlog')
        self.assertEqual(ret, 0)
        ret = criaColuna('Quadro Teste', 'Complete')
        self.assertEqual(ret, 0)
        ret = adicionaTarefaAoQuadro('Quadro Teste', 'Backlog', 'Tarefa Teste')
        self.assertEqual(ret, 3)
        ret = moverTarefaEntreColunas('Quadro Teste', 'Backlog', 'Complete', 'Tarefa Teste')
        self.assertEqual(ret, 4)

        apagaTodosOsQuadros()

        return  

unittest.main()