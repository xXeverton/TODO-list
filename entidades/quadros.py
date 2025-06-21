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
from servicos.persistencia import *
 
__all__ = ['ambienteDeTesteQuadro', 'apagaTodosOsQuadros', 'consultaQuadro', 'criaQuadro', 'apagaQuadro', 'consultaColuna', 'criaColuna', 'apagaColuna', 'editaColuna', 'consultaTodosQuadros',
           'consultaTodasColunas', 'adicionaTarefaAoQuadro', 'adicionaTarefaAoQuadro', 'removeTarefaDoQuadro', 'moverTarefaEntreColunas', 'carregaQuadros', 'salvaQuadros']

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

def copiaColunaComId(coluna):
    
    copia = {'codigo': 0,
             'titulo': '',
             'tarefas': []}
    
    copia['titulo'] = coluna['titulo']
    copia['tarefas'] = coluna['tarefas'].copy()
    copia['codigo'] = coluna['codigo']

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

def indexTarefa(coluna, tituloTarefa):
    codigoTarefaDesejada = consultaTarefa(tituloTarefa)
    if codigoTarefaDesejada[0] == 0:
        codigoTarefaDesejada = codigoTarefaDesejada[1]['id']
        for (pos, codigoTarefa) in enumerate(coluna['tarefas']):
            if codigoTarefa == codigoTarefaDesejada:
                return pos
    return -1

def geraCodigoUnico(lista):

    random.random
    codigo = random.randint(0, 255)
    while codigo in lista:
        codigo = random.randint(0, 255)

    lista.append(codigo)
    return codigo

def apagaColunaPorCodigo(codigo):
    for coluna in listaColunas:
        if coluna['codigo'] == codigo:
            listaColunas.remove(coluna)
            for codigoTarefa in coluna['tarefas']:
                tarefa = consultaTituloPorId(codigoTarefa)
                if tarefa[0] == 0:
                    apagaTarefa(tarefa[1])
            return

#Funcoes de acesso

def ambienteDeTesteQuadro():
    '''
    Nome: ambienteDeTesteQuadro

    Objetivo: manualmente atualiza os dados para um estado propricio para testes

    Acoplamento: Retorno: 0

    AE: NA

    AS: A função chamadora deve tratar o retorno e agir de acordo antes de operar sobre as colunas e tarefas.

    Descrição: A função apaga os dados atuais e manualmente coloca na memoria 3 quadros testes, cada um com 3 colunas, que por sua vez possuem tres tarefas que nao existem.\n
    Hipoteses: Essa função espera ser chamada somente pelo testeQuadros, com o unico intuito de testar o modulo quadros. Ela tambem considera que todos os dados presentes 
    atualmente na memoria ja foram salvos ou podem ser apagados

    Restrição: Essa função apaga permanentemente TODOS os dados atuais guardados na mémoria sobre quadros e colunas, sem nenhuma maneira de recuperá-los por esse módulo. 
    '''

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

    return 0

def apagaTodosOsQuadros():
    '''
    Nome: apagaTodosOsQuadros

    Acoplamento: 
        - Retorno: 0

    AE: NA

    AS: A função chamadora deve tratar o retorno e agir de acordo antes de operar sobre as colunas e tarefas.

    Descrição: Essa função apaga manualmente todas as informações sobre os dados dos quadros.

    Hipoteses: Essa função espera ser chamada somente pelo testeQuadros ou na saida do aplicativo. E que todos os dados atuais podem ser apagados ou 
    foram salvos pelo modulo persistencia

    Restrição: Essa função apaga permanentemente TODOS os dados atuais guardados na mémoria sobre quadros e colunas, sem nenhuma maneira de recuperá-los por esse módulo. 
    '''

    global listaQuadros, listaColunas, listaCodigos

    listaQuadros.clear()
    listaCodigos.clear()
    listaColunas.clear()

    return 0

def consultaQuadro(nome: str) -> tuple[int, list]:
    
    '''
    Nome: consultaQuadro

    Objetivo: Procura na memória o quadro com o nome especificado e retorna suas informações relevantes

    Acoplamento:
        - Nome, string: O nome do quadro a ser consultado
        - Retorno: Uma tupla nos seguintes formatos:
            * (0, Lista): Se o quadro foi encontrado e suas informações relevantes
            * (1, None): Se o quadro não existe ou não foi encontrado

    AE:
        - Nome não deve ser uma string vazia
        - Nome deve ser o nome de um quadro presente na memoria

    AS: A função chamadora deve primeiro confirmar que a função achou o quadro antes de tentar acessar suas informações

    Descrição: Essa função fornece as informações relevantes do quadro identificado pelo nome.

    Hipoteses: 
        - Essa função espera que o nome do quadro passado como parametro seja igual ao nome armazenado do quadro. 
        - Não existem dois quadros com o mesmo nome

    Restrição: Se um quadro não foi encontrado com o mesmo nome, a função considera que não existe o quadro pesquisado. 
    '''

    if nome == '':
        return 1, None
    
    for quadro in listaQuadros:
        if quadro['titulo'] == nome:
            return 0, copiaQuadro(quadro)
    
    return 1, None

def criaQuadro(nome: str, descricao: str = '') -> int:

    '''
    Nome: criaQuadro

    Objetivo: Cria um quadro na memoria

    Acoplamento:
        - Nome, string: O nome do quadro que sera criado
        - Descricao, string: A descricao do quadro que sera criado (opcional)
        - Retorno:
            * 0: Se o quadro foi criado com sucesso
            * 1: Se já existir um quadro com o mesmo nome
            * 2: Se o nome do quadro for uma string vazia

    AE:
        - Nome não deve ser uma string vazia
        - Nome não deve ser o nome de um quadro presente na memoria

    AS: A função chamadora deve tratar o erro antes de fazer qualquer operação com o quadro criado

    Descrição: Essa função cria um quadro com o nome especificado, descrição, se essa for passada, e uma lista vazia que guarda os codigos das colunas do quadro. 

    Hipoteses: 
        - Um quadro não pode ser criado se já existir um quadro com o mesmo nome
        - Um quadro não pode ser criado com uma coluna já existente
        - Um quadro deve ter um nome válido, diferente da string vazia

    Restrição: A função deve guardar o quadro e suas informações em uma lista encapsulada do módulo. 
    '''

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
    
    '''
    Nome: apagaQuadro

    Objetivo: Apaga o quadro com o nome especificado

    Acoplamento:
        - Nome, string: O nome do quadro que sera excluido
        - Retorno:
            * 0: Se o quadro foi apagado com sucesso
            * 1: Se não foi encontrado um quadro com o mesmo nome passado

    AE:
        - O parametro nome deve estar escrito igual o nome do quadro que deseja ser apagado

    AS: 
        - A função chamadora deve tratar o codigo de erro retornado

    Descrição: Apaga o quadro com o nome especificado e todas suas informações da memoria, não podendo mais ser acessadas por qualquer outro metodo.

    Hipoteses: 
        - A informação do quadro apagado foi salvado em algum lugar externo anteriormente a chamada dessa função caso deseja se manter esses dados
        - Não existe quadros com nomes repetidos

    Restrição: A função deve apagar as colunas do quadro. 
    '''

    quadro = buscaQuadro(nome)
    if quadro == None:
        return 1
    
    for codigo in quadro['colunas']:
        apagaColunaPorCodigo(codigo)
    listaQuadros.remove(quadro)
    
    return 0

def consultaColuna(nome_quadro: str, nome_coluna: str) -> tuple[int, list]:

    '''
    Nome: consultaColuna

    Objetivo: Procura na mémoria o quadro e a coluna especificada e retorna a informações relevantes da coluna 

    Acoplamento:
        - nome_quadro, string: O nome do quadro a qual a coluna pertence
        - nome_coluna, string: O nome da coluna da qual deseja saber suas informações
        - Retorno: Uma tupla nos seguintes formatos:
            * (0, InfoColuna): Se o quadro e a coluna foram encontrados e suas informações relevantes
            * (1, None): Se o quadro não existe ou não foi encontrado
            * (2, None): Se a coluna não existe ou não foi encontrado

    AE:
        - O parametro nome_quadro deve estar escrito igual o nome do quadro guardado na memória a qual a coluna pertence 
        - O parametro nome_coluna deve estar escrito igual o nome da coluna guardado na memória da qual deseja saber suas informaçõe

    AS: 
        - A função chamadora deve tratar o codigo de erro retornado antes de tentar acessar as informações da coluna
        - Não existe colunas com nomes repetidos
        - Não existe quadros com nomes repetidos

    Descrição: Consulta a coluna com o nome especificado no quadro tambem especificado. As informações retornadas são: o nome da coluna, e o codigo das tarefas daquela coluna

    Hipoteses: 
        - Caso a função não encontre a coluna especificada, deve se assumir que ela não existe
        - 

    Restrição: A consulta da coluna só poderá acontecer se o quadro especificado existir. 
    '''

    quadro = buscaQuadro(nome_quadro)
    if quadro == None:
        return 1, None

    coluna = buscaColunaNoQuadro(quadro, 'titulo', nome_coluna)
    if coluna == None:
        return 2, None

    return 0, copiaColuna(coluna)

def criaColuna(nome_quadro: str, nome_coluna: str) -> int:
    
    '''
    Nome: criaColuna

    Objetivo: Cria na memoria e adiciona a um quadro uma coluna com o nome especificado 

    Acoplamento:
        - nome_quadro, string: O nome do quadro no qual a coluna será inserida
        - nome_coluna, string: O nome da coluna que será criada
        - Retorno:
            * 0: Se a coluna foi criada com sucesso
            * 1: Se o quadro não existe ou não foi encontrado
            * 2: Se o nome da coluna foi uma string vazia
            * 3: Se já existir uma coluna no mesmo quadro com o mesmo nome da coluna que será criada

    AE:
        - O parametro nome_quadro deve estar escrito igual o nome do quadro guardado na memória a qual a coluna irá ser inserida 
        - O parametro nome_coluna não deve ser o mesmo que uma outra coluna no mesmo quadro especificado
        - O parametro nome_coluna não deve ser uma string vazia

    AS: 
        - A função chamadora deve tratar o codigo de erro retornado antes de tentar fazer operações com a coluna

    Descrição: Cria na memoria e adiciona a um quadro uma coluna com o nome especificado, um codigo gerado automaticamente e uma lista vazia para o codigo de suas tarefas,
    se, e somente se, existir o quadro especificado e o nome da coluna for valido, isso é, não repetido por uma outra coluna nesse mesmo quadro e não vazio.

    Hipoteses: 
        - Caso a função não encontre o quadro especificado, ela deve assumir que ele não existe
        - Não existe colunas com nomes repetidos
        - Não existe quadros com nomes repetidos

    Restrição: A cria coluna só poderá criar a coluna se o quadro especificado existir, se não existir uma coluna nesse quadro com o mesmo nome e o nome da coluna for valido. 
    '''

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
    
    '''
    Nome: apagaColuna

    Objetivo: Procura na memoria e apaga, se for encontrado, as informações de uma coluna e a remove de em um quadro.

    Acoplamento:
        - nome_quadro, string: O nome do quadro do qual a coluna será removida
        - nome_coluna, string: O nome da coluna que será apagada
        - Retorno:
            * 0: Se a coluna foi apagada com sucesso
            * 1: Se o quadro não existe ou não foi encontrado
            * 2: Se a coluna não existe ou não foi encontrado

    AE:
        - O parametro nome_quadro deve estar escrito igual o nome do quadro guardado na memória a qual a coluna pertence 
        - O parametro nome_coluna deve ser o mesmo que uma coluna no quadro especificado

    AS: 
        - A função chamadora deve tratar o codigo de erro retornado.

    Descrição: Remove da memoria e remove de um quadro uma coluna com o nome especificado. Todas as tarefas pertencentes aquela coluna são apagadas tambem.

    Hipoteses: 
        - Caso a função não encontre o quadro especificado, ela deve assumir que ele não existe
        - Caso a função não encontre a coluna especificada, ela deve assumir que ela não existe
        - Não existe colunas com nomes repetidos
        - Não existe quadros com nomes repetidos

    Restrição: A apaga coluna só poderá apagar uma coluna se o quadro especificado existir, se a coluna existir e pertencer a esse quadro. 
    '''

    quadro = buscaQuadro(nome_quadro)
    if quadro == None:
        return 1

    coluna = buscaColunaNoQuadro(quadro, 'titulo', nome_coluna)
    if coluna == None:
        return 2

    for codigoTarefa in coluna['tarefas']:
        tarefa = consultaTituloPorId(codigoTarefa)
        if tarefa[0] == 0:
            apagaTarefa(tarefa[1])
    
    quadro['colunas'].remove(coluna['codigo'])
    listaCodigos.remove(coluna['codigo'])
    listaColunas.remove(coluna)
        
    return 0

def editaColuna(nome_quadro: str, nome_coluna_antigo: str, nome_coluna_novo: str) -> int:
    
    '''
    Nome: editaColuna

    Objetivo: Procura na memoria e modifica, se for encontrado, o nome de uma coluna de um quadro especificado.

    Acoplamento:
        - nome_quadro, string: O nome do quadro do qual a coluna pertence
        - nome_coluna_antigo, string: O nome antigo da coluna que será editada, isso é o nome atual na memória
        - nome_coluna_novo, string: O novo nome que será atribuido a coluna editada
        - Retorno:
            * 0: Se a coluna foi editada com sucesso
            * 1: Se o quadro não existe ou não foi encontrado
            * 2: Se a coluna antiga não existe ou não foi encontrado
            * 3: Se o novo nome desejado da coluna é uma string vazia
            * 4: Se existe uma coluna no mesmo quadro com o nome desejado da coluna

    AE:
        - O parametro nome_quadro deve estar escrito igual o nome do quadro guardado na memória a qual a coluna pertence 
        - O parametro nome_coluna_antigo deve ser o mesmo que uma coluna no quadro especificado
        - O parametro nome_coluna_novo não pode ser o mesmo que o nome de uma coluna existente neste quadro

    AS: 
        - A função chamadora deve tratar o codigo de erro retornado antes de operar sobre a nova coluna.

    Descrição: Procura na memoria e modifica, se for encontrado, o nome de uma coluna de um quadro especificado sem alterar os dados das tarefas da coluna.

    Hipoteses: 
        - Caso a função não encontre o quadro especificado, ela deve assumir que ele não existe
        - Caso a função não encontre a coluna especificada, ela deve assumir que ela não existe
        - Não existe colunas com nomes repetidos
        - Não existe quadros com nomes repetidos

    Restrição: A edita coluna só poderá editar uma coluna se o quadro especificado existir, se a coluna existir e pertencer a esse quadro e se uma coluna
    com o mesmo nome do nome desejado não existir. 
    '''

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
    
    '''
    Nome: consultaTodosQuadros

    Objetivo: Retorna a lista com todas as informações presentes de todos os quadros.

    Acoplamento:
        - Retorno:
            * []: Não existe nenhum quadro na memória
            * [quadro1, quadro2, ..., quadroN]: As informações de todos os quadros na memoria sem nenhuma ordem especifica

    AE:
        - NA

    AS: 
        - A função chamadora deve tratar o retorno e agir de acordo.

    Descrição: Percorre todos os quadros e retorna uma copia de todas informações de todos os quadros.

    Hipoteses: 
        - NA

    Restrição: A consultaTodosQuadros() deve retornar todas as informações de todos os quadros presentes atualmente na memória
    '''

    quadros = []
    
    for quadro in listaQuadros:
        quadros.append(copiaQuadro(quadro))
    
    return quadros

def consultaTodasColunas() -> list:

    '''
    Nome: consultaTodasColunas

    Objetivo: Retorna a lista com todas as informações presentes de todos as colunas atualmente na memória.

    Acoplamento:
        - Retorno:
            * []: Não existe nenhuma coluna na memória
            * [coluna1, coluna2, ..., colunaN]: As informações de todos as colunas na memoria sem nenhuma ordem especifica

    AE:
        - NA

    AS: 
        - A função chamadora deve tratar o retorno e agir de acordo.

    Descrição: Percorre todos as colunas e retorna uma copia de todas informações de todos as colunas. Mesmo aquelas que não pertencem a nenhum quadro.

    Hipoteses: 
        - NA

    Restrição: A consultaTodasColunas() deve retornar todas as informações de todos as colunas presentes atualmente na memória
    '''

    colunas = []

    for coluna in listaColunas:
        colunas.append(copiaColunaComId(coluna))

    return colunas

def adicionaTarefaAoQuadro(nome_quadro: str, nome_coluna: str, tarefa: str) -> int:
    
    '''
    Nome: adicionaTarefaAoQuadro

    Objetivo: Adiciona em uma coluna de um quadro a tarefa especificada.

    Acoplamento:
        - Retorno:
            * 0: Se a tarefa foi adicionada com sucesso
            * 1: Se o quadro não existe ou não foi encontrado
            * 2: Se a coluna não existe ou não foi encontrada
            * 3: Se a tarefa não existe ou não foi encontrada

    AE:
        - O parametro nome_quadro deve estar escrito igual o nome do quadro guardado na memória a qual a coluna irá ser inserida 
        - O parametro nome_coluna não deve ser o mesmo que uma outra coluna no mesmo quadro especificado
        - O parametro tarefa deve ser uma tarefa presente na memória

    AS: 
        - A função chamadora deve tratar o retorno e agir de acordo antes de operar sobre as colunas e tarefas.

    Descrição: Procura a coluna presente no quadro e adiciona o codigo da tarefa na lista tarefas da coluna.

    Hipoteses: 
        - Caso a função não encontre o quadro especificado, ela deve assumir que ele não existe
        - Caso a função não encontre a coluna especificada, ela deve assumir que ela não existe
        - Não existe colunas com nomes repetidos
        - Não existe quadros com nomes repetidos
        - Não existe tarefas com codigos repetidos

    Restrição: A adicionaTarefaAoQuadro() só pode adicionar uma tarefa a uma coluna se: a tarefa, a coluna e o quadro existirem e forem encontrados
    '''

    quadro = buscaQuadro(nome_quadro)
    if quadro == None:
        return 1
    
    coluna = buscaColunaNoQuadro(quadro, 'titulo', nome_coluna)
    if coluna == None:
        return 2
    
    novaTarefa = consultaTarefa(tarefa)
    if novaTarefa[0] == 0:
        coluna['tarefas'].append(novaTarefa[1]['id'])
        return 0
    return 3

def removeTarefaDoQuadro(nome_quadro: str, nome_coluna: str, tarefa: str) -> int:

    '''
    Nome: removeTarefaDoQuadro

    Objetivo: Remove uma tarefa de uma coluna de um quadro e apaga a tarefa da memoria.

    Acoplamento:
        - Retorno:
            * 0: Se a tarefa foi adicionada com sucesso
            * 1: Se o quadro não existe ou não foi encontrado
            * 2: Se a coluna não existe ou não foi encontrada
            * 3: Se a tarefa não existe ou não foi encontrada

    AE:
        - O parametro nome_quadro deve estar escrito igual o nome do quadro guardado na memória a qual a coluna irá ser inserida 
        - O parametro nome_coluna não deve ser o mesmo que uma outra coluna no mesmo quadro especificado
        - O parametro tarefa deve ser uma tarefa presente na memória e na coluna deste quadro

    AS: 
        - A função chamadora deve tratar o retorno e agir de acordo antes de operar sobre as colunas e tarefas.

    Descrição: Procura a coluna presente no quadro e remove o codigo da tarefa na lista tarefas da coluna e apaga a tarefa da memória.

    Hipoteses: 
        - Caso a função não encontre o quadro especificado, ela deve assumir que ele não existe
        - Caso a função não encontre a coluna especificada, ela deve assumir que ela não existe
        - Não existe colunas com nomes repetidos
        - Não existe quadros com nomes repetidos
        - Não existe tarefas com codigos repetidos

    Restrição: A removeTarefaDoQuadro() só pode remover uma tarefa de uma coluna se: a tarefa, a coluna e o quadro existirem e forem encontrados
    '''

    quadro = buscaQuadro(nome_quadro)
    if quadro == None:
        return 1
    
    coluna = buscaColunaNoQuadro(quadro, 'titulo', nome_coluna)
    if coluna == None:
        return 2
    
    for (pos, codigoTarefa) in enumerate(coluna['tarefas']):
        nometarefa = consultaTituloPorId(codigoTarefa)
        if nometarefa[0] == 0:
            if nometarefa[1] == tarefa:
                coluna['tarefas'].pop(pos)
                apagaTarefa(tarefa)
                return 0
       
    return 3

def moverTarefaEntreColunas(nome_quadro: str, origem: str, destino: str, titulo_tarefa: str) -> int:

    '''
    Nome: moverTarefaEntreColunas

    Objetivo: Move uma tarefa de uma coluna de um quadro para uma outra coluna do mesmo quadro.

    Acoplamento:
        - Retorno:
            * 0: Se a tarefa foi movida com sucesso
            * 1: Se o quadro não existe ou não foi encontrado
            * 2: Se a coluna de origem não existe ou não foi encontrada
            * 3: Se a coluna de destino não existe ou não foi encontrada
            * 4: Se a tarefa não existe ou não foi encontrada

    AE:
        - O parametro nome_quadro deve estar escrito igual o nome do quadro guardado na memória a qual a coluna irá ser inserida 
        - O parametro origem deve ser o mesmo que de uma coluna presente no mesmo quadro especificado
        - O parametro destino deve ser o mesmo que de uma coluna presente no mesmo quadro especificado
        - O parametro tarefa deve ser uma tarefa presente na memória e na coluna origem deste quadro

    AS: 
        - A função chamadora deve tratar o retorno e agir de acordo antes de operar sobre as colunas e tarefas.

    Descrição: Procura a coluna de origem presente no quadro e remove o codigo da tarefa na lista tarefas da coluna de origem e procura a coluna de destino e 
    adiciona o codigo da tarefa na lista tarefas da coluna de origem.

    Hipoteses: 
        - Caso a função não encontre o quadro especificado, ela deve assumir que ele não existe
        - Caso a função não encontre as colunas especificadas, ela deve assumir que elas não existem
        - Não existe colunas com nomes repetidos
        - Não existe quadros com nomes repetidos
        - Não existe tarefas com codigos repetidos

    Restrição: A moverTarefaEntreColunas() só pode mover uma tarefa de uma coluna se: a tarefa, a coluna de origem, a coluna de destino e o quadro existirem e forem encontrados
    '''

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

def carregaQuadros():

    '''
    Nome: iniciaQuadros

    Objetivo: Carrega o estado da memória e seta a lista quadros, colunas e codigos com os valores armazenados.

    Acoplamento:
        - Retorno:
            * 0: Se o estado foi carregado corretamente

    AE:
        - NA

    AS: 
        - A função chamadora deve tratar o retorno e agir de acordo antes de operar sobre as colunas e tarefas.

    Descrição: Chama o módulo persistência e carrega o estado da memória com o valor de retorno e seta a lista quadros, colunas e codigos com os valores armazenados.

    Hipoteses: 
        - Essa função será chamada no inicio do programa para carregar o estado anterior dos quadros

    Restrição: 
    '''

    global listaQuadros, listaColunas, listaCodigos

    listaQuadros = carrega_estado('quadros.json')
    listaColunas = carrega_estado('colunas.json')

    for coluna in listaColunas:
        listaCodigos.append(coluna['codigo'])
    
    return 0

def salvaQuadros():

    '''
    Nome: salvaQuadros

    Objetivo: Salva o estado da memória em um json.

    Acoplamento:
        - Retorno:
            * 0: Se o estado foi salvo corretamente

    AE:
        - NA

    AS: 
        - A função chamadora deve tratar o retorno e agir de acordo antes de operar sobre as colunas e tarefas.

    Descrição: Chama o módulo persistência e salva o estado da memória com o valor das listas atuais em um json com o módulo persistência.

    Hipoteses: 
        - Essa função será chamada no final da execução do programa para salvar o estado atual dos quadros

    Restrição: 
    '''

    global listaQuadros, listaColunas

    salva_estado(listaQuadros, 'quadros.json')
    salva_estado(listaColunas, 'colunas.json')
    
    return 0