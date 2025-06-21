# tarefas.py

__all__ = [
    "criaTarefa", "consultaTarefa", "consultaId", "consultaTituloPorId",
    "editaTarefa", "apagaTarefa",
    "consultaTodasTarefas",  
    "limpaTarefas", "ambienteDeTesteTarefas",
]


from datetime import datetime
from copy import copy

# -------------------------
# Estruturas globais
# -------------------------

tarefas = []          # lista de dicionários
_next_id: int = 1                 # auto‑incremento interno


# -------------------------
# Funções de acesso
# -------------------------


# Relacionada aos testes
def limpaTarefas() -> None:
    """Esvazia a lista em memória **e** reseta o contador de IDs.
    Usado em setUp() dos testes."""
    global _next_id
    tarefas.clear()
    _next_id = 1


def ambienteDeTesteTarefas() -> None:
    """Povoa a lista *tarefas* com 1 tarefa para o consultaTarefa() inicial."""
    limpaTarefas()
    exemplo1 = {
        "id": _gera_id(),
        "titulo": "Tarefa Teste 1",
        "descricao": "Descricao 1",
        "prioridade": 1,
        "data_inicio": "2025/01/01",
        "data_vencimento": "2025/01/05",
    }
    
    tarefas.append(exemplo1)

def consultaTarefa(titulo: str) -> tuple[int, dict]:
    """0 + copia da tarefa se existe; 1, {} caso contrário."""
    for t in tarefas:
        if t["titulo"] == titulo:
            return 0, t.copy()  
    return 1, {}


def consultaTituloPorId(id_tarefa: int) -> tuple[int, str]:
    """
    0, titulo  → id existe
    1, ""      → id não existe
    """
    for t in tarefas:
        if t["id"] == id_tarefa:
            return 0, t["titulo"]
    return 1, ""

def consultaId(titulo: str) -> tuple[int, int]:
    """0, id se achar; 1 se não achar."""
    for t in tarefas:
        if t["titulo"] == titulo:
            return 0, t["id"]
    return 1, -1

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
        "id": _gera_id(),
        "titulo": titulo.strip(),
        "descricao": descricao.strip(),
        "prioridade": prioridade,
        "data_inicio": data_inicio.strip(),
        "data_vencimento": data_vencimento.strip(),
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

    tarefa_ref = None
    for t in tarefas:
        if t["id"] == tarefa["id"]:
            tarefa_ref = t
            break

    tarefa_ref["titulo"] = novo_titulo
    tarefa_ref["descricao"] = nova_descricao
    tarefa_ref["prioridade"] = nova_prioridade
    tarefa_ref["data_inicio"] = nova_data_inicio
    tarefa_ref["data_vencimento"] = nova_data_vencimento
    return 0


def apagaTarefa(titulo: str) -> int:
    if titulo.strip() == "":
        return 2  # Título vazio
    if len(titulo) > 50:
        return 3  # Título muito longo

    for t in list(tarefas):  # iteração segura
        if t["titulo"] == titulo:
            tarefas.remove(t)
            return 0
    return 1
# ----------  Para uso do persistência ----------
def consultaTodasTarefas() -> list[dict]:  
    """
    Retorna cópias das tarefas em memória.

    """
    return [t.copy() for t in tarefas]

# -------------------------
# Auxiliar
# -------------------------

def validaDatas(inicio: str, fim: str) -> bool:
    try:
        d1 = datetime.strptime(inicio, "%Y/%m/%d")
        d2 = datetime.strptime(fim, "%Y/%m/%d")
        return d1 <= d2
    except ValueError:
        return False
    
def _gera_id() -> int:
    global _next_id
    valor = _next_id
    _next_id += 1
    return valor
