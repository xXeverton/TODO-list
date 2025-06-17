import unittest
import quadros as quadros
from tarefas import *

nTeste = 0
idAssertiva = 0

def testaQuadros():

    testaConsultaQuadro()
    testaCriaQuadros()
    testaApagaQuadro()
    testaCriaColuna()
    testaRemoveColuna()
    testaConsultaColuna()
    testaEditaColuna()
    testaConsultaTodosQuadros()
    testaAdicionarTarefaAoQuadro()
    testaRemoveTarefaDoQuadro()
    testaMoverTarefaEntreColunas()

    return

def mensagemInicialTeste(nomeTeste):
    global nTeste, idAssertiva
    nTeste += 1
    idAssertiva = 0
    print(f"Caso Teste {nTeste} - {nomeTeste}")
    return

def mensagemResultadoTeste(ret, retornoEsperado):
    if ret == retornoEsperado:
        print("Sucesso")
    else:
        print("Falha")
    print()

def checaAssertiva(ret, retornoEsperado):
    global nTeste, idAssertiva
    idAssertiva += 1
    if ret != retornoEsperado:
        print(f'Falha na assertiva {idAssertiva} do teste {nTeste}')

def testaConsultaQuadro():
    
    quadros.listaQuadros = []

    mensagemInicialTeste('Consulta Quadro nao existente')
    ret = quadros.consultaQuadro("Quadro Nao Existente")
    mensagemResultadoTeste(ret, (1, None))

    tarefaTeste = {'titulo': 'Tarefa Teste',
            'descricao': 'Descricao Teste',
            'prioridade': 0,
            'dtInicio': '05/06/2025',
            'dtVenc': '05/06/2025'}
    colunaTeste = {'titulo': 'ColunaTeste',
            'tarefas': [tarefaTeste]}
    quadroTeste = {'titulo': 'Teste',
            'descricao': 'Quadro Teste',
            'colunas': [colunaTeste]}

    quadros.listaQuadros = [quadroTeste]
    mensagemInicialTeste('Consulta Quadro Ok')
    ret = quadros.consultaQuadro(quadroTeste['titulo'])
    mensagemResultadoTeste(ret, (0, quadroTeste))

    quadros.listaQuadros = []

    return

def testaCriaQuadros():

    quadros.listaQuadros = []
    
    mensagemInicialTeste('Cria Quadro Ok')
    ret = quadros.consultaQuadro('Quadro Teste')
    checaAssertiva(ret, (1, None))
    ret = quadros.criaQuadro('Quadro Teste')
    checaAssertiva(ret, 0)
    ret = quadros.consultaQuadro('Quadro Teste')
    mensagemResultadoTeste(ret, (0, {'titulo': 'Quadro Teste',
                                     'descricao': '',
                                     'colunas': []}))
    
    mensagemInicialTeste('Cria Quadro Repetido')
    ret = quadros.consultaQuadro('Quadro Teste')   
    checaAssertiva(ret, (0, {'titulo': 'Quadro Teste',
                                     'descricao': '',
                                     'colunas': []}))
    ret = quadros.criaQuadro('Quadro Teste')
    mensagemResultadoTeste(ret, 1)

    mensagemInicialTeste('Cria Quadro Vazio')
    ret = quadros.criaQuadro('')
    mensagemResultadoTeste(ret, 2)

    quadros.listaQuadros = []

    return

def testaApagaQuadro():

    quadros.listaQuadros = []
    
    mensagemInicialTeste('Apaga Quadro Ok')
    ret = quadros.criaQuadro('Quadro Teste')
    checaAssertiva(ret, 0)
    ret = quadros.consultaQuadro('Quadro Teste')
    checaAssertiva(ret, (0, {'titulo': 'Quadro Teste',
                                     'descricao': '',
                                     'colunas': []}))
    ret = quadros.apagaQuadro('Quadro Teste')
    checaAssertiva(ret, 0)
    ret = quadros.consultaQuadro('Quadro Teste')
    mensagemResultadoTeste(ret, (1, None))

    mensagemInicialTeste('Apaga Quadro Inexistente')
    ret = quadros.consultaQuadro('Quadro Teste')
    checaAssertiva(ret, (1, None))
    ret = quadros.apagaQuadro('Quadro Teste')
    mensagemResultadoTeste(ret, 1)

    quadros.listaQuadros = []

    return

def testaCriaColuna():

    quadros.listaQuadros = []
    
    mensagemInicialTeste('Cria Coluna Ok')
    ret = quadros.criaQuadro('Quadro Teste')
    checaAssertiva(ret, 0)
    ret = quadros.criaColuna('Quadro Teste', 'To Do')
    checaAssertiva(ret, 0)
    ret = quadros.consultaQuadro('Quadro Teste')
    mensagemResultadoTeste(ret, (0, {'titulo': 'Quadro Teste',
                                    'descricao': '',
                                    'colunas': [{'titulo': 'To Do',
                                                 'tarefas': []}]}))
    quadros.apagaQuadro('Quadro Teste')
    
    mensagemInicialTeste('Cria Coluna Quadro Nao Encontrado')
    ret = quadros.consultaQuadro('Quadro Teste')
    checaAssertiva(ret, (1, None))
    ret = quadros.criaColuna('Quadro Teste', 'To Do')
    mensagemResultadoTeste(ret, 1)

    mensagemInicialTeste('Cria Coluna Vazia')
    ret = quadros.criaQuadro('Quadro Teste')
    checaAssertiva(ret, 0)
    ret = quadros.criaColuna('Quadro Teste', '')
    mensagemResultadoTeste(ret, 2)

    mensagemInicialTeste('Cria Coluna Repetida')
    ret = quadros.criaColuna('Quadro Teste', 'To Do')
    checaAssertiva(ret, 0)
    ret = quadros.consultaQuadro('Quadro Teste')
    checaAssertiva(ret, (0, {'titulo': 'Quadro Teste',
                             'descricao': '',
                             'colunas': [{'titulo': 'To Do',
                                          'tarefas': []}]}))
    ret = quadros.criaColuna('Quadro Teste', 'To Do')
    mensagemResultadoTeste(ret, 3)

    quadros.listaQuadros = []

    return

def testaRemoveColuna():

    quadros.listaQuadros = []
    
    mensagemInicialTeste('Remove Coluna Ok')
    ret = quadros.criaQuadro('Quadro Teste')
    checaAssertiva(ret, 0)
    ret = quadros.criaColuna('Quadro Teste', 'To Do')
    checaAssertiva(ret, 0)
    ret = quadros.consultaQuadro('Quadro Teste')
    checaAssertiva(ret, (0, {'titulo': 'Quadro Teste',
                             'descricao': '',
                             'colunas': [{'titulo': 'To Do',
                                          'tarefas': []}]}))
    ret = quadros.apagaColuna('Quadro Teste', 'To Do')
    checaAssertiva(ret, 0)
    ret = quadros.consultaQuadro('Quadro Teste')
    mensagemResultadoTeste(ret, (0, {'titulo': 'Quadro Teste',
                                     'descricao': '',
                                     'colunas': []}))
    ret = quadros.apagaQuadro('Quadro Teste')

    mensagemInicialTeste('Remove Coluna Quadro Nao Encontrado')
    ret = quadros.consultaQuadro('Quadro Teste')
    checaAssertiva(ret, (1, None))
    ret = quadros.apagaColuna('Quadro Teste', 'To Do')
    mensagemResultadoTeste(ret, 1)
    ret = quadros.apagaQuadro('Quadro Teste')

    mensagemInicialTeste('Remove Coluna Nao Encontrado')
    ret = quadros.criaQuadro('Quadro Teste')
    checaAssertiva(ret, 0)
    ret = quadros.apagaColuna('Quadro Teste', 'To Do')
    mensagemResultadoTeste(ret, 2)

    quadros.listaQuadros = []

    return

def testaConsultaColuna():

    quadros.listaQuadros = []
    
    mensagemInicialTeste('Consulta Coluna Ok')
    ret = quadros.criaQuadro('Quadro Teste')
    checaAssertiva(ret, 0)
    ret = quadros.criaColuna('Quadro Teste', 'To Do')
    checaAssertiva(ret, 0)
    ret = quadros.consultaColuna('Quadro Teste', 'To Do')
    mensagemResultadoTeste(ret, (0, {'titulo': 'To Do',
                                     'tarefas': []}))
    ret = quadros.apagaQuadro('Quadro Teste')

    mensagemInicialTeste('Consulta Coluna Quadro Nao Encontrado')
    ret = quadros.consultaQuadro('Quadro Teste')
    checaAssertiva(ret, (1, None))
    ret = quadros.consultaColuna('Quadro Teste', 'To Do')
    mensagemResultadoTeste(ret, (1, None))
    ret = quadros.apagaQuadro('Quadro Teste')

    mensagemInicialTeste('Consulta Coluna Coluna Nao Encontrado')
    ret = quadros.criaQuadro('Quadro Teste')
    checaAssertiva(ret, 0)
    ret = quadros.consultaColuna('Quadro Teste', 'To Do')
    mensagemResultadoTeste(ret, (2, None))

    quadros.listaQuadros = []

    return

def testaEditaColuna():

    quadros.listaQuadros = []
    
    mensagemInicialTeste('Edita Coluna Ok')
    ret = quadros.criaQuadro('Quadro Teste')
    checaAssertiva(ret, 0)
    ret = quadros.criaColuna('Quadro Teste', 'To Do')
    checaAssertiva(ret, 0)
    ret = quadros.editaColuna('Quadro Teste', 'To Do', 'To Do Novo')
    checaAssertiva(ret, 0)
    ret = quadros.consultaColuna('Quadro Teste', 'To Do')
    checaAssertiva(ret, (2, None))
    ret = quadros.consultaColuna('Quadro Teste', 'To Do Novo')
    mensagemResultadoTeste(ret, (0, {'titulo': 'To Do Novo',
                                     'tarefas': []}))
    ret = quadros.apagaQuadro('Quadro Teste')

    mensagemInicialTeste('Edita Coluna Quadro Nao Encontrado')
    ret = quadros.consultaQuadro('Quadro Teste')
    checaAssertiva(ret, (1, None))
    ret = quadros.editaColuna('Quadro Teste', 'To Do', 'To Do Novo')
    mensagemResultadoTeste(ret, 1)

    mensagemInicialTeste('Edita Coluna Coluna Antiga Nao Encontrado')
    ret = quadros.criaQuadro('Quadro Teste')
    checaAssertiva(ret, 0)
    ret = quadros.consultaColuna('Quadro Teste', 'To Do')
    checaAssertiva(ret, (2, None))
    ret = quadros.editaColuna('Quadro Teste', 'To Do', 'To Do Novo')
    mensagemResultadoTeste(ret, 2)
    ret = quadros.apagaQuadro('Quadro Teste')

    mensagemInicialTeste('Edita Coluna Vazia')
    ret = quadros.criaQuadro('Quadro Teste')
    checaAssertiva(ret, 0)
    ret = quadros.criaColuna('Quadro Teste', 'To Do')
    checaAssertiva(ret, 0)
    ret = quadros.editaColuna('Quadro Teste', 'To Do', '')
    mensagemResultadoTeste(ret, 3)
    ret = quadros.apagaQuadro('Quadro Teste')

    mensagemInicialTeste('Edita Coluna Coluna Nova Ja Existe')
    ret = quadros.criaQuadro('Quadro Teste')
    checaAssertiva(ret, 0)
    ret = quadros.criaColuna('Quadro Teste', 'To Do')
    checaAssertiva(ret, 0)
    ret = quadros.criaColuna('Quadro Teste', 'To Do Novo')
    checaAssertiva(ret, 0)
    ret = quadros.editaColuna('Quadro Teste', 'To Do', 'To Do Novo')
    mensagemResultadoTeste(ret, 4)
    ret = quadros.apagaQuadro('Quadro Teste')

    quadros.listaQuadros = []

    return

def testaConsultaTodosQuadros():

    quadros.listaQuadros = []
    
    mensagemInicialTeste('Consulta Todos os Quadros Ok')
    ret = quadros.criaQuadro('Quadro Teste')
    checaAssertiva(ret, 0)
    ret = quadros.criaQuadro('Quadro Teste2')
    checaAssertiva(ret, 0)
    ret = quadros.consultaTodosQuadros()
    mensagemResultadoTeste(ret, [{'titulo': 'Quadro Teste',
                                  'descricao': '',
                                  'colunas': []},
                                 {'titulo': 'Quadro Teste2',
                                  'descricao': '',
                                  'colunas': []}])
    ret = quadros.apagaQuadro('Quadro Teste')
    ret = quadros.apagaQuadro('Quadro Teste2')

    quadros.listaQuadros = []

    return

def testaAdicionarTarefaAoQuadro():

    quadros.listaQuadros = []
    
    mensagemInicialTeste('Adiciona Tarefa a Quadro Ok')
    ret = quadros.criaQuadro('Quadro Teste')
    checaAssertiva(ret, 0)
    ret = quadros.criaColuna('Quadro Teste', 'Coluna Teste')
    checaAssertiva(ret, 0)
    ret = criaTarefa('Tarefa Teste', '', 0, '2005/09/10', '2005/09/10')
    checaAssertiva(ret, 0)
    ret = quadros.adicionaTarefaAoQuadro('Quadro Teste', 'Coluna Teste', 'Tarefa Teste')
    checaAssertiva(ret, 0)
    ret = quadros.consultaColuna('Quadro Teste', 'Coluna Teste')
    mensagemResultadoTeste(ret, (0, {'titulo': 'Coluna Teste',
                                     'tarefas': [{"titulo": 'Tarefa Teste',
                                                  "descricao": '',
                                                  "prioridade": 0,
                                                  "data_inicio": '2005/09/10',
                                                  "data_vencimento": '2005/09/10'}]}))
    ret = quadros.apagaQuadro('Quadro Teste')
    ret = apagaTarefa('Tarefa Teste')

    mensagemInicialTeste('Adiciona Tarefa a Quadro Nao Existente')
    ret = quadros.consultaQuadro('Quadro Teste')
    checaAssertiva(ret, (1, None))
    ret = quadros.criaColuna('Quadro Teste', 'Coluna Teste')
    checaAssertiva(ret, 1)
    ret = criaTarefa('Tarefa Teste', '', 0, '2005/09/10', '2005/09/10')
    checaAssertiva(ret, 0)
    ret = quadros.adicionaTarefaAoQuadro('Quadro Teste', 'Coluna Teste', 'Tarefa Teste')
    mensagemResultadoTeste(ret, 1)
    ret = quadros.apagaQuadro('Quadro Teste')
    ret = apagaTarefa('Tarefa Teste')

    mensagemInicialTeste('Adiciona Tarefa a Quadro com Coluna Nao Existente')
    ret = quadros.criaQuadro('Quadro Teste')
    checaAssertiva(ret, 0)
    ret = criaTarefa('Tarefa Teste', '', 0, '2005/09/10', '2005/09/10')
    checaAssertiva(ret, 0)
    ret = quadros.adicionaTarefaAoQuadro('Quadro Teste', 'Coluna Teste', 'Tarefa Teste')
    mensagemResultadoTeste(ret, 2)
    ret = quadros.apagaQuadro('Quadro Teste')
    ret = apagaTarefa('Tarefa Teste')

    mensagemInicialTeste('Adiciona Tarefa a Quadro com Tarefa Nao Existente')
    ret = quadros.criaQuadro('Quadro Teste')
    checaAssertiva(ret, 0)
    ret = quadros.criaColuna('Quadro Teste', 'Coluna Teste')
    checaAssertiva(ret, 0)
    ret = quadros.adicionaTarefaAoQuadro('Quadro Teste', 'Coluna Teste', 'Tarefa Teste')
    mensagemResultadoTeste(ret, 3)
    ret = quadros.apagaQuadro('Quadro Teste')

    quadros.listaQuadros = []

    return

def testaRemoveTarefaDoQuadro():

    quadros.listaQuadros = []
    
    mensagemInicialTeste('Remove Tarefa do Quadro Ok')
    ret = quadros.criaQuadro('Quadro Teste')
    checaAssertiva(ret, 0)
    ret = quadros.criaColuna('Quadro Teste', 'Coluna Teste')
    checaAssertiva(ret, 0)
    ret = criaTarefa('Tarefa Teste', '', 0, '2005/09/10', '2005/09/10')
    checaAssertiva(ret, 0)
    ret = quadros.adicionaTarefaAoQuadro('Quadro Teste', 'Coluna Teste', 'Tarefa Teste')
    checaAssertiva(ret, 0)
    ret = quadros.consultaColuna('Quadro Teste', 'Coluna Teste')
    checaAssertiva(ret, (0, {'titulo': 'Coluna Teste',
                             'tarefas': [{"titulo": 'Tarefa Teste',
                                          "descricao": '',
                                          "prioridade": 0,
                                          "data_inicio": '2005/09/10',
                                          "data_vencimento": '2005/09/10'}]}))
    ret = quadros.removeTarefaDoQuadro('Quadro Teste', 'Coluna Teste', 'Tarefa Teste')
    checaAssertiva(ret, 0)
    ret = quadros.consultaColuna('Quadro Teste', 'Coluna Teste')
    mensagemResultadoTeste(ret, (0, {'titulo': 'Coluna Teste',
                                     'tarefas': []}))
    ret = quadros.apagaQuadro('Quadro Teste')
    ret = apagaTarefa('Tarefa Teste')

    mensagemInicialTeste('Remove Tarefa de um Quadro Nao Existente')
    ret = quadros.consultaQuadro('Quadro Teste')
    checaAssertiva(ret, (1, None))
    ret = quadros.criaColuna('Quadro Teste', 'Coluna Teste')
    checaAssertiva(ret, 1)
    ret = criaTarefa('Tarefa Teste', '', 0, '2005/09/10', '2005/09/10')
    checaAssertiva(ret, 0)
    ret = quadros.adicionaTarefaAoQuadro('Quadro Teste', 'Coluna Teste', 'Tarefa Teste')
    checaAssertiva(ret, 1)
    ret = quadros.removeTarefaDoQuadro('Quadro Teste', 'Coluna Teste', 'Tarefa Teste')
    mensagemResultadoTeste(ret, 1)
    ret = apagaTarefa('Tarefa Teste')

    mensagemInicialTeste('Remove Tarefa de Quadro com Coluna Nao Existente')
    ret = quadros.criaQuadro('Quadro Teste')
    checaAssertiva(ret, 0)
    ret = criaTarefa('Tarefa Teste', '', 0, '2005/09/10', '2005/09/10')
    checaAssertiva(ret, 0)
    ret = quadros.adicionaTarefaAoQuadro('Quadro Teste', 'Coluna Teste', 'Tarefa Teste')
    checaAssertiva(ret, 2)
    ret = quadros.removeTarefaDoQuadro('Quadro Teste', 'Coluna Teste', 'Tarefa Teste')
    mensagemResultadoTeste(ret, 2)
    ret = quadros.apagaQuadro('Quadro Teste')
    ret = apagaTarefa('Tarefa Teste')

    mensagemInicialTeste('Remove Tarefa do Quadro com Tarefa Nao Existente')
    ret = quadros.criaQuadro('Quadro Teste')
    checaAssertiva(ret, 0)
    ret = quadros.criaColuna('Quadro Teste', 'Coluna Teste')
    checaAssertiva(ret, 0)
    ret = quadros.adicionaTarefaAoQuadro('Quadro Teste', 'Coluna Teste', 'Tarefa Teste')
    checaAssertiva(ret, 3)
    ret = quadros.removeTarefaDoQuadro('Quadro Teste', 'Coluna Teste', 'Tarefa Teste')
    mensagemResultadoTeste(ret, 3)
    ret = quadros.apagaQuadro('Quadro Teste')

    quadros.listaQuadros = []

    return

    quadros.listaQuadros = []
    
    mensagemInicialTeste('Update Tarefa Ok')
    ret = quadros.criaQuadro('Quadro Teste')
    checaAssertiva(ret, 0)
    ret = quadros.criaColuna('Quadro Teste', 'Backlog')
    checaAssertiva(ret, 0)
    ret = criaTarefa('Tarefa Teste', '', 0, '2005/09/10', '2005/09/10')
    checaAssertiva(ret, 0)
    ret = quadros.adicionaTarefaAoQuadro('Quadro Teste', 'Backlog', 'Tarefa Teste')
    checaAssertiva(ret, 0)
    ret = quadros.consultaColuna('Quadro Teste', 'Backlog')
    checaAssertiva(ret, (0, {'titulo': 'Backlog',
                             'tarefas': [{"titulo": 'Tarefa Teste',
                                          "descricao": '',
                                          "prioridade": 0,
                                          "data_inicio": '2005/09/10',
                                          "data_vencimento": '2005/09/10'}]}))
    ret = editaTarefa('Tarefa Teste', {"titulo": 'Tarefa Alterada',
                                       "descricao": '',
                                       "prioridade": 0,
                                       "data_inicio": '2005/09/10',
                                       "data_vencimento": '2005/09/10'})
    checaAssertiva(ret, 0)
    print(quadros.consultaColuna('Quadro Teste', 'Backlog'))
    ret = quadros.updateTarefa('Quadro Teste', 'Backlog', 'Tarefa Teste', 'Tarefa Alterada')
    checaAssertiva(ret, 0)
    ret = quadros.consultaColuna('Quadro Teste', 'Backlog')
    mensagemResultadoTeste(ret, (0, {'titulo': 'Backlog',
                             'tarefas': [{"titulo": 'Tarefa Alterada',
                                       "descricao": '',
                                       "prioridade": 0,
                                       "data_inicio": '2005/09/10',
                                       "data_vencimento": '2005/09/10'}]}))
    ret = quadros.apagaQuadro('Quadro Teste')
    ret = apagaTarefa('Tarefa Teste')

    '''mensagemInicialTeste('Mover Tarefa de um Quadro Nao Existente')
    ret = quadros.consultaQuadro('Quadro Teste')
    checaAssertiva(ret, (1, None))
    ret = quadros.criaColuna('Quadro Teste', 'Backlog')
    checaAssertiva(ret, 1)
    ret = quadros.criaColuna('Quadro Teste', 'Complete')
    checaAssertiva(ret, 1)
    ret = criaTarefa('Tarefa Teste', '', 0, '2005/09/10', '2005/09/10')
    checaAssertiva(ret, 0)
    ret = quadros.adicionaTarefaAoQuadro('Quadro Teste', 'Backlog', 'Tarefa Teste')
    checaAssertiva(ret, 1)
    ret = quadros.moverTarefaEntreColunas('Quadro Teste', 'Backlog', 'Complete', 'Tarefa Teste')
    mensagemResultadoTeste(ret, 1)
    ret = apagaTarefa('Tarefa Teste')

    mensagemInicialTeste('Mover Tarefa de Quadro com Coluna de Origem Nao Existente')
    ret = quadros.criaQuadro('Quadro Teste')
    checaAssertiva(ret, 0)
    ret = quadros.criaColuna('Quadro Teste', 'Complete')
    checaAssertiva(ret, 0)
    ret = criaTarefa('Tarefa Teste', '', 0, '2005/09/10', '2005/09/10')
    checaAssertiva(ret, 0)
    ret = quadros.adicionaTarefaAoQuadro('Quadro Teste', 'Backlog', 'Tarefa Teste')
    checaAssertiva(ret, 2)
    ret = quadros.moverTarefaEntreColunas('Quadro Teste', 'Backlog', 'Complete', 'Tarefa Teste')
    mensagemResultadoTeste(ret, 2)
    ret = quadros.apagaQuadro('Quadro Teste')
    ret = apagaTarefa('Tarefa Teste')

    mensagemInicialTeste('Mover Tarefa de Quadro com Coluna de Destino Nao Existente')
    ret = quadros.criaQuadro('Quadro Teste')
    checaAssertiva(ret, 0)
    ret = quadros.criaColuna('Quadro Teste', 'Backlog')
    checaAssertiva(ret, 0)
    ret = criaTarefa('Tarefa Teste', '', 0, '2005/09/10', '2005/09/10')
    checaAssertiva(ret, 0)
    ret = quadros.adicionaTarefaAoQuadro('Quadro Teste', 'Backlog', 'Tarefa Teste')
    checaAssertiva(ret, 0)
    ret = quadros.moverTarefaEntreColunas('Quadro Teste', 'Backlog', 'Complete', 'Tarefa Teste')
    mensagemResultadoTeste(ret, 3)
    ret = quadros.apagaQuadro('Quadro Teste')
    ret = apagaTarefa('Tarefa Teste')

    mensagemInicialTeste('Mover Tarefa de Quadro com Tarefa Nao Existente')
    ret = quadros.criaQuadro('Quadro Teste')
    checaAssertiva(ret, 0)
    ret = quadros.criaColuna('Quadro Teste', 'Backlog')
    checaAssertiva(ret, 0)
    ret = quadros.criaColuna('Quadro Teste', 'Complete')
    checaAssertiva(ret, 0)
    ret = quadros.adicionaTarefaAoQuadro('Quadro Teste', 'Backlog', 'Tarefa Teste')
    checaAssertiva(ret, 3)
    ret = quadros.moverTarefaEntreColunas('Quadro Teste', 'Backlog', 'Complete', 'Tarefa Teste')
    mensagemResultadoTeste(ret, 4)
    ret = quadros.apagaQuadro('Quadro Teste')'''

    quadros.listaQuadros = []

    return

def testaMoverTarefaEntreColunas():

    quadros.listaQuadros = []
    
    mensagemInicialTeste('Mover Tarefa Ok')
    ret = quadros.criaQuadro('Quadro Teste')
    checaAssertiva(ret, 0)
    ret = quadros.criaColuna('Quadro Teste', 'Backlog')
    checaAssertiva(ret, 0)
    ret = quadros.criaColuna('Quadro Teste', 'Complete')
    checaAssertiva(ret, 0)
    ret = criaTarefa('Tarefa Teste', '', 0, '2005/09/10', '2005/09/10')
    checaAssertiva(ret, 0)
    ret = quadros.adicionaTarefaAoQuadro('Quadro Teste', 'Backlog', 'Tarefa Teste')
    checaAssertiva(ret, 0)
    ret = quadros.consultaColuna('Quadro Teste', 'Backlog')
    checaAssertiva(ret, (0, {'titulo': 'Backlog',
                             'tarefas': [{"titulo": 'Tarefa Teste',
                                          "descricao": '',
                                          "prioridade": 0,
                                          "data_inicio": '2005/09/10',
                                          "data_vencimento": '2005/09/10'}]}))
    ret = quadros.consultaColuna('Quadro Teste', 'Complete')
    checaAssertiva(ret, (0, {'titulo': 'Complete',
                             'tarefas': []}))
    ret = quadros.moverTarefaEntreColunas('Quadro Teste', 'Backlog', 'Complete', 'Tarefa Teste')
    checaAssertiva(ret, 0)
    ret = quadros.consultaColuna('Quadro Teste', 'Backlog')
    checaAssertiva(ret, (0, {'titulo': 'Backlog',
                             'tarefas': []}))
    ret = quadros.consultaColuna('Quadro Teste', 'Complete')
    mensagemResultadoTeste(ret, (0, {'titulo': 'Complete',
                                     'tarefas': [{"titulo": 'Tarefa Teste',
                                                  "descricao": '',
                                                  "prioridade": 0,
                                                  "data_inicio": '2005/09/10',
                                                  "data_vencimento": '2005/09/10'}]}))
    ret = quadros.apagaQuadro('Quadro Teste')
    ret = apagaTarefa('Tarefa Teste')

    mensagemInicialTeste('Mover Tarefa de um Quadro Nao Existente')
    ret = quadros.consultaQuadro('Quadro Teste')
    checaAssertiva(ret, (1, None))
    ret = quadros.criaColuna('Quadro Teste', 'Backlog')
    checaAssertiva(ret, 1)
    ret = quadros.criaColuna('Quadro Teste', 'Complete')
    checaAssertiva(ret, 1)
    ret = criaTarefa('Tarefa Teste', '', 0, '2005/09/10', '2005/09/10')
    checaAssertiva(ret, 0)
    ret = quadros.adicionaTarefaAoQuadro('Quadro Teste', 'Backlog', 'Tarefa Teste')
    checaAssertiva(ret, 1)
    ret = quadros.moverTarefaEntreColunas('Quadro Teste', 'Backlog', 'Complete', 'Tarefa Teste')
    mensagemResultadoTeste(ret, 1)
    ret = apagaTarefa('Tarefa Teste')

    mensagemInicialTeste('Mover Tarefa de Quadro com Coluna de Origem Nao Existente')
    ret = quadros.criaQuadro('Quadro Teste')
    checaAssertiva(ret, 0)
    ret = quadros.criaColuna('Quadro Teste', 'Complete')
    checaAssertiva(ret, 0)
    ret = criaTarefa('Tarefa Teste', '', 0, '2005/09/10', '2005/09/10')
    checaAssertiva(ret, 0)
    ret = quadros.adicionaTarefaAoQuadro('Quadro Teste', 'Backlog', 'Tarefa Teste')
    checaAssertiva(ret, 2)
    ret = quadros.moverTarefaEntreColunas('Quadro Teste', 'Backlog', 'Complete', 'Tarefa Teste')
    mensagemResultadoTeste(ret, 2)
    ret = quadros.apagaQuadro('Quadro Teste')
    ret = apagaTarefa('Tarefa Teste')

    mensagemInicialTeste('Mover Tarefa de Quadro com Coluna de Destino Nao Existente')
    ret = quadros.criaQuadro('Quadro Teste')
    checaAssertiva(ret, 0)
    ret = quadros.criaColuna('Quadro Teste', 'Backlog')
    checaAssertiva(ret, 0)
    ret = criaTarefa('Tarefa Teste', '', 0, '2005/09/10', '2005/09/10')
    checaAssertiva(ret, 0)
    ret = quadros.adicionaTarefaAoQuadro('Quadro Teste', 'Backlog', 'Tarefa Teste')
    checaAssertiva(ret, 0)
    ret = quadros.moverTarefaEntreColunas('Quadro Teste', 'Backlog', 'Complete', 'Tarefa Teste')
    mensagemResultadoTeste(ret, 3)
    ret = quadros.apagaQuadro('Quadro Teste')
    ret = apagaTarefa('Tarefa Teste')

    mensagemInicialTeste('Mover Tarefa de Quadro com Tarefa Nao Existente')
    ret = quadros.criaQuadro('Quadro Teste')
    checaAssertiva(ret, 0)
    ret = quadros.criaColuna('Quadro Teste', 'Backlog')
    checaAssertiva(ret, 0)
    ret = quadros.criaColuna('Quadro Teste', 'Complete')
    checaAssertiva(ret, 0)
    ret = quadros.adicionaTarefaAoQuadro('Quadro Teste', 'Backlog', 'Tarefa Teste')
    checaAssertiva(ret, 3)
    ret = quadros.moverTarefaEntreColunas('Quadro Teste', 'Backlog', 'Complete', 'Tarefa Teste')
    mensagemResultadoTeste(ret, 4)
    ret = quadros.apagaQuadro('Quadro Teste')

    quadros.listaQuadros = []

    return

testaQuadros()  