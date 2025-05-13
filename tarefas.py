# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
""" 

#Lista de todas as tarefas criadas
listaTarefas = []


def titulo_valido(titulo: str):
    #Retorna 0 caso o titulo seja valido ou um numero diferente de 0 se for invalido
    
    if (titulo.strip() == ""):        
        #Titulo vazio
        return 2 
    
    if len(titulo) > 50:
        #Titulo excede limite de caractere
        return 5
    
    for tarefa in listaTarefas:
        if tarefa["titulo"] == titulo:
            #Titulo duplicado
            return 1
    
    #Titulo valido
    return 0

def validaIntervalo(data_inicio: str, data_vencimento: str):
    #Função recebe duas datas existentes e avalia se estão no formato correto e se a data de inicio é
    #depois da data de vencimento
    
    data1 = data_inicio.split("/")
    data2 = data_vencimento.split("/")
    
    if len(data1[2]) != 4 and len(data2[2]) != 4:
        #Data no formato incorreto (Ex: dd/mm/aa, aa/mm/dd)
        return 4
    
    for i in range(3):
        data1[i] = int(data1[i])
        data2[i] = int(data2[i])
    
    for i in range(2, -1, -1):
        if data1[i] > data2[i]:
            #Data inicial depois da final
            return 4
        if data1[i] < data2[i]:
            #Data Valida
            return 0
        
    #Data Valida
    return 0

def criaTarefa(titulo: str, descricao: str, prioridade: int, data_inicio: str, data_vencimento: str) -> int:
    #Cria uma tarefa em formato de dicionario
    #retorna 0 se não ocorreu erros, 1 se titulo for duplicado, 2 se for um titulo vazio, 3 prioridade invalida,
    #4 data invalida, 5 titulo excede limite de caractere e 6 descrição excede limite de caractere
    
    #Valida titulo
    statusTitulo = titulo_valido(titulo)
    
    if statusTitulo:
        #Titulo Invalido
        return statusTitulo
    
    if len(descricao) > 250:
        #Descrição excede limite de caractere
        return 6
    
    if prioridade < 0 or prioridade > 4:
        #Prioridade invalida
        return 3
    
    #Valida data
    statusData = validaIntervalo(data_inicio, data_vencimento)
    
    if statusData:
        #Data Invalida
        return statusData
    
    novaTarefa = {"titulo": titulo, 
                  "descricao": descricao,
                  "prioridade": prioridade,
                  "data_inicio": data_inicio,
                  "data_vencimento": data_vencimento}
    
    listaTarefas.append(novaTarefa)
    
    return 0
    
