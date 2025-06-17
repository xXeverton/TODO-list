# tarefas.py

__all__ = ["criaTarefa", "consultaTarefa", "editaTarefa", "apagaTarefa", "limpaTarefas"]

from datetime import datetime

tarefas = []  # Lista em memória de tarefas

# Tem que colocar aquele formato de descricoes ainda para TODAS AS FUNCOES!

def limpaTarefas():
    tarefas.clear()  # Limpa a lista de tarefas para testes


def consultaTarefa(titulo: str) -> tuple[int, dict]:
    for tarefa in tarefas:
        if tarefa["titulo"] == titulo:
            return 0, tarefa
    return 1, {}


def criaTarefa(titulo: str, descricao: str, prioridade: int, data_inicio: str, data_vencimento: str) -> int:
    if titulo.strip() == "":
        return 2  # Título vazio
    if len(titulo) > 50:
        return 5  # Título muito longo
    if consultaTarefa(titulo)[0] == 0:
        return 1  # Título duplicado
    if len(descricao) > 250:
        return 6  # Descrição muito grande
    if prioridade not in [0, 1, 2, 3, 4]:
        return 3  # Prioridade inválida
    if not validaDatas(data_inicio, data_vencimento):
        return 4  # Data inválida

    nova = {
        "titulo": titulo.strip(),
        "descricao": descricao.strip(),
        "prioridade": prioridade,
        "data_inicio": data_inicio.strip(),
        "data_vencimento": data_vencimento.strip()
    }
    tarefas.append(nova)
    return 0


def editaTarefa(titulo_antigo: str, novas_infos: dict) -> int:
    codigo, tarefa = consultaTarefa(titulo_antigo)
    if codigo != 0:
        return 1  # Tarefa não encontrada

    if not novas_infos:
        return 7  # Nenhuma informação a alterar

    novo_titulo = novas_infos.get("titulo", tarefa["titulo"]).strip()
    nova_descricao = novas_infos.get("descricao", tarefa["descricao"])
    nova_prioridade = novas_infos.get("prioridade", tarefa["prioridade"])
    nova_data_inicio = novas_infos.get("data_inicio", tarefa["data_inicio"])
    nova_data_vencimento = novas_infos.get("data_vencimento", tarefa["data_vencimento"])

    if novo_titulo == "":
        return 2  # Novo título vazio
    if len(novo_titulo) > 50:
        return 5  # Novo título muito longo
    if novo_titulo != titulo_antigo and consultaTarefa(novo_titulo)[0] == 0:
        return 1  # Título duplicado
    if len(nova_descricao) > 250:
        return 6  # Descrição muito grande
    if nova_prioridade not in [0, 1, 2, 3, 4]:
        return 3  # Prioridade inválida
    if not validaDatas(nova_data_inicio, nova_data_vencimento):
        return 4  # Data inválida

    tarefa["titulo"] = novo_titulo
    tarefa["descricao"] = nova_descricao
    tarefa["prioridade"] = nova_prioridade
    tarefa["data_inicio"] = nova_data_inicio
    tarefa["data_vencimento"] = nova_data_vencimento
    return 0


def apagaTarefa(titulo: str) -> int:
    if titulo.strip() == "":
        return 2  # Título vazio
    if len(titulo) > 50:
        return 3  # Título muito longo

    for tarefa in tarefas:
        if tarefa["titulo"] == titulo:
            tarefas.remove(tarefa)
            return 0  # Sucesso

    return 1  # Tarefa não encontrada


def validaDatas(inicio: str, fim: str) -> bool:
    try:
        d1 = datetime.strptime(inicio, "%Y/%m/%d")
        d2 = datetime.strptime(fim, "%Y/%m/%d")
        return d1 <= d2
    except ValueError:
        return False
