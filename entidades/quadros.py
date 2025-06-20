# -*- coding: utf-8 -*-

#Modelo Quadro = {'titulo': '',
#                 'descricao': '',
#                 'colunas': []}

#Modelo Coluna = {'codigo': ,
#                 'titulo': '',
#                 'tarefas': []}

import random
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from entidades.tarefas import *
 
__all__ = ['ambienteDeTesteQuadro', 'apagaTodosOsQuadros', 'consultaQuadro', 'criaQuadro', 'apagaQuadro', 'consultaColuna', 'criaColuna', 'apagaColuna', 'editaColuna', 'consultaTodosQuadros', 'adicionaTarefaAoQuadro',
           'adicionaTarefaAoQuadro', 'removeTarefaDoQuadro', 'moverTarefaEntreColunas']

listaQuadros = []
listaColunas = []
listaCodigos = []

#Funcao privadas

def copiaQuadro(quadro):

    copia = {'titulo': '',
             'descricao': '',
             'colunas': []}

    copia['titulo'] = quadro['titulo']
    copia['descricao'] = quadro['descricao']
    copia['colunas'] = quadro['colunas'].copy()

    return copia

def copiaColuna(coluna):
    
    copia = {'titulo': '',
             'tarefas': []}
    
    copia['titulo'] = coluna['titulo']
    copia['tarefas'] = coluna['tarefas'].copy()

    return copia

def buscaQuadro(nomeQuadro):
    for quadro in listaQuadros:
        if quadro['titulo'] == nomeQuadro:
            return quadro
    return None

def buscaColuna(chave, identificador):
    for coluna in listaColunas:
        if coluna[chave] == identificador:
            return coluna
    return None

def buscaColunaNoQuadro(quadro, chave, identificador):
    for idColuna in quadro['colunas']:
        coluna = buscaColuna('codigo', idColuna)
        if coluna[chave] == identificador:
            return coluna
    return None

def indexTarefa(coluna, nomeTarefa):
    for (pos, tarefa) in enumerate(coluna['tarefas']):
        if tarefa['titulo'] == nomeTarefa:
            return pos
    return -1

def geraCodigoUnico(lista):

    random.random
    codigo = random.randint(0, 255)
    while codigo in lista:
        codigo = random.randint(0, 255)

    lista.append(codigo)
    return codigo

#Funcoes de acesso

#Nome: ambienteDeTesteQuadro
def ambienteDeTesteQuadro():
    #

    global listaQuadros, listaColunas, listaCodigos

    listaQuadros.clear()
    listaColunas.clear()

    colunaTeste11 = {'codigo': 0,
                     'titulo': 'ColunaTeste1.1',
                     'tarefas': [1, 2, 3]}
    colunaTeste12 = {'codigo': 1,
                     'titulo': 'ColunaTeste1.2',
                     'tarefas': [3, 4, 5]}
    colunaTeste13 = {'codigo': 2,
                     'titulo': 'ColunaTeste1.3',
                     'tarefas': [6, 7, 8]}
    quadroTeste1 = {'titulo': 'Quadro Teste 1',
                    'descricao': 'Descricao 1',
                    'colunas': [0, 1, 2]}
    
    colunaTeste21 = {'codigo': 3,
                     'titulo': 'ColunaTeste2.1',
                     'tarefas': [9, 10, 11]}
    colunaTeste22 = {'codigo': 4,
                     'titulo': 'ColunaTeste2.2',
                     'tarefas': [12, 13, 14]}
    colunaTeste23 = {'codigo': 5,
                     'titulo': 'ColunaTeste2.3',
                     'tarefas': [15, 16, 17]}
    quadroTeste2 = {'titulo': 'Quadro Teste 2',
                    'descricao': 'Descricao 2',
                    'colunas': [3, 4, 5]}
    
    colunaTeste31 = {'codigo': 6,
                     'titulo': 'ColunaTeste3.1',
                     'tarefas': [18, 19, 20]}
    colunaTeste32 = {'codigo': 7,
                     'titulo': 'ColunaTeste3.2',
                     'tarefas': [21, 22, 23]}
    colunaTeste33 = {'codigo': 8,
                     'titulo': 'ColunaTeste3.3',
                     'tarefas': [24, 25, 26]}
    quadroTeste3 = {'titulo': 'Quadro Teste 3',
                    'descricao': 'Descricao 3',
                    'colunas': [6, 7, 8]}
    
    listaQuadros = [quadroTeste1, quadroTeste2, quadroTeste3]
    listaColunas = [colunaTeste11, colunaTeste12, colunaTeste13, colunaTeste21, colunaTeste22, colunaTeste23, colunaTeste31, colunaTeste32, colunaTeste33]
    listaCodigos = [0, 1, 2, 3, 4, 5, 6, 7, 8]

def apagaTodosOsQuadros():
    listaQuadros.clear()
    listaCodigos.clear()
    listaColunas.clear()

def consultaQuadro(nome: str) -> tuple[int, list]:
    
    if nome == '':
        return 1, None
    
    for quadro in listaQuadros:
        if quadro['titulo'] == nome:
            return 0, copiaQuadro(quadro)
    
    return 1, None

def criaQuadro(nome: str, descricao: str = '') -> int:

    if nome == '':
        return 2

    for quadro in listaQuadros:
        if nome == quadro['titulo']:
            return 1

    novoQuadro = {'titulo': nome,
                  'descricao': descricao,
                  'colunas': []}

    listaQuadros.append(novoQuadro)

    return 0

def apagaQuadro(nome: str) -> int:
    
    for (pos, quadro) in enumerate(listaQuadros):
        if quadro['titulo'] == nome:
            listaQuadros.pop(pos)
            return 0
    
    return 1

def consultaColuna(nome_quadro: str, nome_coluna: str) -> tuple[int, list]:

    quadro = buscaQuadro(nome_quadro)
    if quadro == None:
        return 1, None

    coluna = buscaColunaNoQuadro(quadro, 'titulo', nome_coluna)
    if coluna == None:
        return 2, None

    return 0, copiaColuna(coluna)

def criaColuna(nome_quadro: str, nome_coluna: str) -> int:
    
    if nome_coluna == '':
        return 2
    
    quadro = buscaQuadro(nome_quadro)
    if quadro == None:
        return 1
    
    coluna = buscaColunaNoQuadro(quadro, 'titulo', nome_coluna)
    if coluna != None:
        return 3

    # for codigoColuna in quadro['colunas']:
    #     coluna = buscaColuna('codigo', codigoColuna)
    #     if coluna['titulo'] == nome_coluna:
    #         return 3
                
    novaColuna = {'codigo': geraCodigoUnico(listaCodigos),
                  'titulo': nome_coluna,
                  'tarefas': []}

    #quadro['colunas'].append(novaColuna)
    quadro['colunas'].append(novaColuna['codigo'])
    listaColunas.append(novaColuna)

    return 0

def apagaColuna(nome_quadro: str, nome_coluna: str) -> int:
    
    quadro = buscaQuadro(nome_quadro)
    if quadro == None:
        return 1

    coluna = buscaColunaNoQuadro(quadro, 'titulo', nome_coluna)
    if coluna == None:
        return 2

    quadro['colunas'].remove(coluna['codigo'])
    listaCodigos.remove(coluna['codigo'])
    listaColunas.remove(coluna)
        
    return 0

def editaColuna(nome_quadro: str, nome_coluna_antigo: str, nome_coluna_novo: str) -> int:
    
    if nome_coluna_novo == '':
        return 3

    quadro = buscaQuadro(nome_quadro)
    if quadro == None:
        return 1

    idColunaVelha = -1
    for idColuna in quadro['colunas']:
        coluna = buscaColunaNoQuadro(quadro, 'codigo', idColuna)
        if coluna['titulo'] == nome_coluna_antigo:
            idColunaVelha = idColuna
        elif coluna['titulo'] == nome_coluna_novo:
            return 4
        
    if idColunaVelha == -1:
        return 2
    
    buscaColuna('codigo', idColunaVelha)['titulo'] = nome_coluna_novo

    return 0

def consultaTodosQuadros() -> list:
    
    quadros = []
    
    for quadro in listaQuadros:
        quadros.append(copiaQuadro(quadro))
    
    return quadros

def adicionaTarefaAoQuadro(nome_quadro: str, nome_coluna: str, tarefa: str) -> int:
    
    quadro = buscaQuadro(nome_quadro)
    if quadro == None:
        return 1
    
    coluna = buscaColunaNoQuadro(quadro, 'titulo', nome_coluna)
    if coluna == None:
        return 2
    
    novaTarefa = consultaTarefa(tarefa)
    if novaTarefa[0] == 0:
        coluna['tarefas'].append(novaTarefa[1])
        return 0
    return 3

def removeTarefaDoQuadro(nome_quadro: str, nome_coluna: str, tarefa: str) -> int:

    quadro = buscaQuadro(nome_quadro)
    if quadro == None:
        return 1
    
    coluna = buscaColunaNoQuadro(quadro, 'titulo', nome_coluna)
    if coluna == None:
        return 2
    
    for (pos, tarefaAtual) in enumerate(coluna['tarefas']):
        if tarefaAtual['titulo'] == tarefa:
            coluna['tarefas'].pop(pos)
            return 0       
    return 3

def moverTarefaEntreColunas(nome_quadro: str, origem: str, destino: str, titulo_tarefa: str) -> int:

    quadro = buscaQuadro(nome_quadro)
    if quadro == None:
        return 1
    
    colunaOrigem = buscaColunaNoQuadro(quadro, 'titulo', origem)
    if colunaOrigem == None:
        return 2
    
    colunaDestino = buscaColunaNoQuadro(quadro, 'titulo', destino)
    if colunaDestino == None:
        return 3
    
    indexT = indexTarefa(colunaOrigem, titulo_tarefa)
    if indexT < 0:
        return 4

    tarefa = colunaOrigem['tarefas'].pop(indexT)
    colunaDestino['tarefas'].append(tarefa)

    return 0