# tarefas.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from servicos.persistencia import *

__all__ = [
    "criaTarefa", "consultaTarefa", "consultaId", "consultaTituloPorId",
    "editaTarefa", "apagaTarefa",
    "consultaTodasTarefas",
    "limpaTarefas", "ambienteDeTesteTarefas",
    "carregaTarefas", "salvaTarefas"
]

from datetime import datetime

# -------------------------------------------------------------------
# ESTRUTURAS GLOBAIS
# -------------------------------------------------------------------
tarefas: list[dict] = []    # lista que guarda as tarefas
_next_id: int = 1           # contador de auto-incremento para novos IDs


# -------------------------------------------------------------------
# FUNÇÕES DE ACESSO — CADA UMA COM ESPECIFICAÇÃO COMPLETA
# -------------------------------------------------------------------

def limpaTarefas() -> int:
    '''
    Nome: limpaTarefas

    Objetivo:
        Remover todas as tarefas da memória e reiniciar o contador de IDs,
        criando um “estado limpo” para uso em testes.

    Acoplamento:
        - Retorno:
            * 0 — sempre que a limpeza for concluída.

    AE (Assertivas de Entrada):
        • Nenhum parâmetro é exigido.

    AS (Assertivas de Saída):
        • A lista global `tarefas` fica vazia.
        • A variável global `_next_id` volta a ser 1.

    Descrição:
        1. Executa `tarefas.clear()`.
        2. Seta `_next_id = 1`.
        3. Retorna 0 para indicar sucesso.

    Hipóteses:
        • Não existe outra estrutura paralela que precise ser sincronizada.

    Restrição:
        • Deve ser chamada apenas em ambiente controlado (testes ou reset).
    '''
    global _next_id
    tarefas.clear()
    _next_id = 1
    return 0


def ambienteDeTesteTarefas() -> None:
    '''
    Nome: ambienteDeTesteTarefas

    Objetivo:
        Popular a memória com um conjunto mínimo (1 tarefa) para permitir
        testes de consulta e visualização sem depender da interface.

    Acoplamento:
        - Retorno: None (efeito colateral sobre a lista global).

    AE:
        • Nenhum parâmetro.

    AS:
        • Após a chamada, existe exatamente uma tarefa de ID 1 e título
          "Tarefa Teste 1".

    Descrição:
        1. Chama `limpaTarefas()` para resetar.
        2. Cria um dicionário exemplo com campos válidos.
        3. Adiciona o dicionário à lista `tarefas`.

    Hipóteses:
        • Função utilizada apenas no módulo de testes automatizados.

    Restrição:
        • Apaga permanentemente qualquer estado prévio das tarefas.
    '''
    limpaTarefas()
    exemplo = {
        "id": _gera_id(),
        "titulo": "Tarefa Teste 1",
        "descricao": "Descricao 1",
        "prioridade": 1,
        "data_inicio": "2025/01/01",
        "data_vencimento": "2025/01/05",
    }
    tarefas.append(exemplo)


def carregaTarefas() -> int:
    '''
    Nome: carregaTarefas

    Objetivo:
        Restaurar da camada de persistência (arquivo *tarefas.json*) todo o
        conteúdo de tarefas, ajustando o contador `_next_id`.

    Acoplamento:
        - Retorno:
            * 0 — arquivo lido (ou inexistente, mas operação concluída).

    AE:
        • Arquivo *tarefas.json* pode existir ou não. (Função trata ambos.)

    AS:
        • Lista `tarefas` contém objetos carregados.
        • `_next_id` = (maior id presente) + 1, garantindo IDs únicos.

    Descrição:
        1. Usa `carrega_estado("tarefas.json")` da camada de serviço.
        2. Substitui a lista global.
        3. Calcula o próximo ID disponível.

    Hipóteses:
        • O JSON armazena exatamente a estrutura que a aplicação grava.

    Restrição:
        • Não executa qualquer validação de schema.
    '''
    global tarefas, _next_id
    tarefas = carrega_estado("tarefas.json")
    _next_id = max((t["id"] for t in tarefas), default=0) + 1
    return 0


def salvaTarefas() -> int:
    '''
    Nome: salvaTarefas

    Objetivo:
        Grav ar o estado atual da lista `tarefas` em *tarefas.json* de forma
        totalmente substitutiva (snapshot).

    Acoplamento:
        - Retorno:
            * 0 — gravação concluída.

    AE:
        • Lista `tarefas` em RAM deve estar coerente.

    AS:
        • Conteúdo do arquivo *tarefas.json* reflete exatamente a memória
          após a chamada.

    Descrição:
        1. Chama `salva_estado(tarefas, "tarefas.json")`.
        2. Retorna 0.

    Hipóteses:
        • A camada de persistência cria o arquivo se ele não existir.

    Restrição:
        • Descartará o conteúdo anterior do arquivo sem merger.
    '''
    salva_estado(tarefas, "tarefas.json")
    return 0


def consultaTarefa(titulo: str) -> tuple[int, dict]:
    '''
    Nome: consultaTarefa

    Objetivo:
        Retornar uma **cópia** da tarefa com o título fornecido.

    Acoplamento:
        - titulo, str
        - Retorno:
            * (0, tarefa_dict) — tarefa encontrada (cópia profunda).
            * (1, {})          — título inexistente.

    AE:
        • `titulo` não é None.

    AS:
        • Lista original permanece inalterada.

    Descrição:
        - Percorre `tarefas`; compara `t["titulo"] == titulo`.
        - Se achar, devolve `t.copy()`; senão devolve código 1.
    '''
    for t in tarefas:
        if t["titulo"] == titulo:
            return 0, t.copy()
    return 1, {}


def consultaTituloPorId(id_tarefa: int) -> tuple[int, str]:
    '''
    Nome: consultaTituloPorId

    Objetivo:
        Obter o título associado a um ID numérico de tarefa.

    Acoplamento:
        - id_tarefa, int
        - Retorno:
            * (0, título) — id existente.
            * (1, "")     — id não localizado.

    AE:
        • id_tarefa ≥ 1

    AS:
        • Estado da lista permanece intacto.

    Descrição:
        - Loop na lista procurando campo "id".
    '''
    for t in tarefas:
        if t["id"] == id_tarefa:
            return 0, t["titulo"]
    return 1, ""


def consultaId(titulo: str) -> tuple[int, int]:
    '''
    Nome: consultaId

    Objetivo:
        Descobrir o ID de uma tarefa a partir do título.

    Acoplamento:
        - titulo, str
        - Retorno:
            * (0, id)  — sucesso.
            * (1, -1)  — título não existente.

    AE:
        • String não vazia.

    AS:
        • Sem efeitos colaterais.
    '''
    for t in tarefas:
        if t["titulo"] == titulo:
            return 0, t["id"]
    return 1, -1


def criaTarefa(titulo: str, descricao: str, prioridade: int,
               data_inicio: str, data_vencimento: str) -> int:
    '''
    Nome: criaTarefa

    Objetivo:
        Inserir nova tarefa na lista cumprindo todas as validações de negócio.

    Acoplamento:
        - titulo, str  : nome da tarefa.
        - descricao, str : até 250 caracteres.
        - prioridade, int: 0 (urgente) … 4 (nenhuma).
        - data_inicio, str  "YYYY/MM/DD".
        - data_vencimento, str "YYYY/MM/DD".
        - Retorno (códigos):
            * 0 — sucesso
            * 1 — título já existe
            * 2 — título vazio
            * 3 — prioridade fora do range
            * 4 — datas inválidas
            * 5 — título > 50 caracteres
            * 6 — descrição > 250 caracteres

    AE:
        • Datas devem seguir formato e `data_inicio ≤ data_vencimento`.

    AS:
        • Em sucesso, a nova tarefa é anexada e possui id único.

    Descrição:
        1. Valida título (não vazio, tamanho, duplicidade).
        2. Valida descrição, prioridade, datas.
        3. Gera novo id por `_gera_id()` e dá append.

    Hipóteses:
        • Prioridade 0 é mais alta.

    Restrição:
        • Não grava em disco (persistência é externa).
    '''
    if titulo.strip() == "":
        return 2
    if len(titulo) > 50:
        return 5
    if consultaTarefa(titulo)[0] == 0:
        return 1
    if len(descricao) > 250:
        return 6
    if prioridade not in [0, 1, 2, 3, 4]:
        return 3
    if not validaDatas(data_inicio, data_vencimento):
        return 4

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
    '''
    Nome: editaTarefa

    Objetivo:
        Alterar campos selecionados de uma tarefa existente, mantendo o ID.

    Acoplamento:
        - titulo_antigo, str
        - novas_infos, dict com quaisquer chaves válidas:
            {"titulo", "descricao", "prioridade",
             "data_inicio", "data_vencimento"}
        - Retorno:
            * 0 – sucesso
            * 1 – tarefa não encontrada OU novo título duplicado
            * 2 – novo título vazio
            * 3 – prioridade inválida
            * 4 – datas inválidas
            * 5 – novo título > 50
            * 6 – nova descrição > 250
            * 7 – dicionário vazio (nada a alterar)

    AE:
        • `novas_infos` não pode ser None.

    AS:
        • Em sucesso, tarefa é atualizada in-place.

    Descrição:
        - Localiza tarefa existente.
        - Mescla valores; valida cada regra como em `criaTarefa`.
        - Atualiza campos.

    Hipóteses:
        • Títulos continuam únicos após edição.

    Restrição:
        • Persistência não é automática.
    '''
    codigo, tarefa = consultaTarefa(titulo_antigo)
    if codigo != 0:
        return 1
    if not novas_infos:
        return 7

    novo_titulo = novas_infos.get("titulo", tarefa["titulo"]).strip()
    nova_desc   = novas_infos.get("descricao", tarefa["descricao"])
    nova_prio   = novas_infos.get("prioridade", tarefa["prioridade"])
    nova_ini    = novas_infos.get("data_inicio", tarefa["data_inicio"])
    nova_venc   = novas_infos.get("data_vencimento", tarefa["data_vencimento"])

    if novo_titulo == "":
        return 2
    if len(novo_titulo) > 50:
        return 5
    if novo_titulo != titulo_antigo and consultaTarefa(novo_titulo)[0] == 0:
        return 1
    if len(nova_desc) > 250:
        return 6
    if nova_prio not in [0, 1, 2, 3, 4]:
        return 3
    if not validaDatas(nova_ini, nova_venc):
        return 4

    tarefa["titulo"]          = novo_titulo
    tarefa["descricao"]       = nova_desc
    tarefa["prioridade"]      = nova_prio
    tarefa["data_inicio"]     = nova_ini
    tarefa["data_vencimento"] = nova_venc
    return 0


def apagaTarefa(titulo: str) -> int:
    '''
    Nome: apagaTarefa

    Objetivo:
        Excluir definitivamente a tarefa cujo título é informado.

    Acoplamento:
        - titulo, str
        - Retorno:
            * 0 – removida
            * 1 – título não encontrado
            * 2 – título vazio
            * 3 – título > 50 caracteres

    AE:
        • String título não é None.

    AS:
        • Lista interna perde o elemento correspondente.

    Descrição:
        - Valida tamanho/não-vazio.
        - Percorre lista (cópia) e remove a primeira ocorrência.

    Hipóteses:
        • Títulos são únicos.

    Restrição:
        • Persistência fica a cargo do chamador.
    '''
    if titulo.strip() == "":
        return 2
    if len(titulo) > 50:
        return 3
    for t in list(tarefas):
        if t["titulo"] == titulo:
            tarefas.remove(t)
            return 0
    return 1


def consultaTodasTarefas() -> list[dict]:
    '''
    Nome: consultaTodasTarefas

    Objetivo:
        Retornar uma **lista independente** contendo cópias de todas
        as tarefas atualmente em memória.

    Acoplamento:
        - Retorno: list[dict] — cada item é `t.copy()`.

    AE: Nenhuma.

    AS:
        • Alterar o retorno não afeta a estrutura interna.

    Descrição:
        - List-comprehension `[t.copy() for t in tarefas]`.
    '''
    return [t.copy() for t in tarefas]


# -------------------------------------------------------------------
# AUXILIARES 
# -------------------------------------------------------------------
def validaDatas(inicio: str, fim: str) -> bool:
    '''Valida formato YYYY/MM/DD e garante início ≤ fim.'''
    try:
        d1 = datetime.strptime(inicio, "%Y/%m/%d")
        d2 = datetime.strptime(fim, "%Y/%m/%d")
        return d1 <= d2
    except ValueError:
        return False

def _gera_id() -> int:
    global _next_id
    val = _next_id
    _next_id += 1
    return val
