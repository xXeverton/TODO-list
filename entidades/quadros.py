# -*- coding: utf-8 -*-

#Modelo Quadro = {'titulo': '',
#                 'descricao': '',
#                 'colunas': []}

#Modelo Coluna = {'titulo': '',
#                 'tarefas': []}

from .tarefas import *
 

listaQuadros = []

def copiaQuadro(quadro):

    copia = {'titulo': '',
             'descricao': '',
             'colunas': []}

    copia['titulo'] = quadro['titulo']
    copia['descricao'] = quadro['descricao']
    for coluna in quadro['colunas']:
        copia['colunas'].append(coluna.copy())

    return copia

def indexQuadro(nomeQuadro):
    for (pos, quadro) in enumerate(listaQuadros):
        if quadro['titulo'] == nomeQuadro:
            return pos
    return -1

def indexColuna(indexQ, nomeColuna):
    for (pos, coluna) in enumerate(listaQuadros[indexQ]['colunas']):
        if coluna['titulo'] == nomeColuna:
            return pos
    return -1

def indexTarefa(indexQ, indexC, nomeTarefa):
    for (pos, tarefa) in enumerate(listaQuadros[indexQ]['colunas'][indexC]['tarefas']):
        if tarefa['titulo'] == nomeTarefa:
            return pos
    return -1

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

def criaColuna(nome_quadro: str, nome_coluna: str) -> int:
    
    if nome_coluna == '':
        return 2
    
    for quadro in listaQuadros:
        if quadro['titulo'] == nome_quadro:

            for coluna in quadro['colunas']:
                if coluna['titulo'] == nome_coluna:
                    return 3
                
            novaColuna = {'titulo': nome_coluna,
                          'tarefas': []}

            quadro['colunas'].append(novaColuna)

            return 0

    return 1

def apagaColuna(nome_quadro: str, nome_coluna: str) -> int:
    
    for quadro in listaQuadros:
        if quadro['titulo'] == nome_quadro:

            for (pos, coluna) in enumerate(quadro['colunas']):
                if coluna['titulo'] == nome_coluna:
                    quadro['colunas'].pop(pos)
                    return 0

            return 2

    return 1

def consultaColuna(nome_quadro: str, nome_coluna: str) -> tuple[int, list]:

    for quadro in listaQuadros:
        if quadro['titulo'] == nome_quadro:

            for coluna in quadro['colunas']:
                if coluna['titulo'] == nome_coluna:
                    return 0, coluna

            return 2, None

    return 1, None

def editaColuna(nome_quadro: str, nome_coluna_antigo: str, nome_coluna_novo: str) -> int:
    
    if nome_coluna_novo == '':
        return 3

    for quadro in listaQuadros:
        if quadro['titulo'] == nome_quadro:

            posColunaAntiga = -1
            for (pos, coluna) in enumerate(quadro['colunas']):
                if coluna['titulo'] == nome_coluna_antigo:
                    posColunaAntiga = pos
                elif coluna['titulo'] == nome_coluna_novo:
                    return 4
                
            if posColunaAntiga == -1:
                return 2
            
            quadro['colunas'][posColunaAntiga]['titulo'] = nome_coluna_novo

            return 0

    return 1

def consultaTodosQuadros() -> list:
    
    quadros = []
    
    for quadro in listaQuadros:
        quadros.append(copiaQuadro(quadro))
    
    return quadros

def adicionaTarefaAoQuadro(nome_quadro: str, nome_coluna: str, tarefa: str) -> int:
    
    for quadro in listaQuadros:
        if quadro['titulo'] == nome_quadro:

            for coluna in quadro['colunas']:
                if coluna['titulo'] == nome_coluna:
                    novaTarefa = consultaTarefa(tarefa)
                    if novaTarefa[0] == 0:
                        coluna['tarefas'].append(novaTarefa[1])
                        return 0
                    return 3

            return 2

    return 1

def removeTarefaDoQuadro(nome_quadro: str, nome_coluna: str, tarefa: str) -> int:
    for quadro in listaQuadros:
        if quadro['titulo'] == nome_quadro:

            for coluna in quadro['colunas']:
                if coluna['titulo'] == nome_coluna:

                    for (pos, tarefaAtual) in enumerate(coluna['tarefas']):
                        if tarefaAtual['titulo'] == tarefa:
                            coluna['tarefas'].pop(pos)
                            return 0
                        
                    return 3

            return 2

    return 1

def moverTarefaEntreColunas(nome_quadro: str, origem: str, destino: str, titulo_tarefa: str) -> int:

    indexQ = indexQuadro(nome_quadro)
    if indexQ < 0:
        return 1
    
    indexCO = indexColuna(indexQ, origem)
    if indexCO < 0:
        return 2
    
    indexCD = indexColuna(indexQ, destino)
    if indexCD < 0:
        return 3
    
    indexT = indexTarefa(indexQ, indexCO, titulo_tarefa)
    if indexT < 0:
        return 4

    tarefa = listaQuadros[indexQ]['colunas'][indexCO]['tarefas'].pop(indexT)
    listaQuadros[indexQ]['colunas'][indexCD]['tarefas'].append(tarefa)

    return 0