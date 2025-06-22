# tarefas.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from servicos.persistencia import *

__all__ = [
    "criaTarefa", "consultaTarefa", "consultaId", "consultaTituloPorId",
    "editaTarefa", "apagaTarefa",
    "consultaTodasTarefas",  
    "limpaTarefas", "ambienteDeTesteTarefas", "carregaTarefas","salvaTarefas"
]

from datetime import datetime
from copy import copy

# -------------------------
# Estruturas globais
# -------------------------

tarefas = []          # lista de dicionários
_next_id: int = 1     # auto-incremento interno

# -------------------------
# Funções de acesso
# -------------------------

def limpaTarefas() -> int:
    '''
    Nome: limpaTarefas

    Objetivo:
        Esvaziar completamente a lista de tarefas em memória e reiniciar
        o contador de IDs para o estado inicial, garantindo ambiente limpo
        para testes.

    Acoplamento:
        - Retorno:
            * 0: indica que a operação foi concluída com sucesso.

    AE:
        - Não há parâmetros de entrada.

    AS:
        - A lista global `tarefas` fica vazia.
        - O contador global `_next_id` é resetado para 1.

    Descrição:
        - Executa `tarefas.clear()` para remover todos os elementos.
        - Atualiza `_next_id = 1`.
        - Usado tipicamente em `setUp()` de testes automatizados.

    Hipóteses:
        - A lista `tarefas` existe e está acessível globalmente.

    Restrição:
        - Deve ser chamado somente em contexto de teste; não persiste em disco.
    '''
    global _next_id
    tarefas.clear()
    _next_id = 1
    return 0


def ambienteDeTesteTarefas() -> None:
    '''
    Nome: ambienteDeTesteTarefas

    Objetivo:
        Preparar um ambiente mínimo de teste com uma tarefa pré-definida,
        facilitando a validação de operações de consulta.

    Acoplamento:
        - Retorno:
            * None (efeito colateral em memória).

    AE:
        - Não há parâmetros de entrada.

    AS:
        - Após a execução, existe exatamente uma tarefa na lista
          com título "Tarefa Teste 1" e ID gerado automaticamente.

    Descrição:
        - Chama `limpaTarefas()` para reiniciar estado.
        - Cria um dicionário de exemplo e o adiciona a `tarefas`.

    Hipóteses:
        - Função usada apenas em casos de teste unitário.

    Restrição:
        - Apaga permanentemente qualquer tarefa existente antes de popular.
    '''
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


def carregaTarefas() -> int:
    '''
    Nome: carregaTarefas

    Objetivo:
        Carregar a lista de tarefas do arquivo 'tarefas.json' para a memória
        e ajustar o contador de IDs para continuar a numeração corretamente.

    Acoplamento:
        - Retorno:
            * 0: indica que a carga (ou ausência de arquivo) foi processada.

    AE:
        - Arquivo 'tarefas.json' pode existir ou não; trata ambos os casos.

    AS:
        - `tarefas` recebe a lista carregada.
        - `_next_id` torna-se (maior ID presente + 1).

    Descrição:
        - Invoca `carrega_estado("tarefas.json")`.
        - Calcula novo `_next_id` com base nos IDs existentes.

    Hipóteses:
        - O JSON no arquivo corresponde à estrutura de tarefa esperada.

    Restrição:
        - Não realiza validações além de carregar e ajustar contador.
    '''
    global tarefas, _next_id
    tarefas = carrega_estado("tarefas.json")
    _next_id = max((t["id"] for t in tarefas), default=0) + 1
    return 0


def salvaTarefas() -> int:
    '''
    Nome: salvaTarefas

    Objetivo:
        Persistir o estado atual da lista de tarefas em 'tarefas.json',
        permitindo recuperação em execuções futuras.

    Acoplamento:
        - Retorno:
            * 0: indica que o arquivo foi gravado sem erros.

    AE:
        - A lista `tarefas` deve estar corretamente montada.

    AS:
        - O arquivo JSON é sobrescrito com o conteúdo de `tarefas`.

    Descrição:
        - Chama `salva_estado(tarefas, 'tarefas.json')`.

    Hipóteses:
        - `salva_estado` funciona conforme especificado no módulo de persistência.

    Restrição:
        - Não retorna erro detalhado, sempre devolve 0.
    '''
    salva_estado(tarefas, 'tarefas.json')
    return 0


def consultaTarefa(titulo: str) -> tuple[int, dict]:
    '''
    Nome: consultaTarefa

    Objetivo:
        Recuperar uma cópia da tarefa cujo título corresponda ao parâmetro,
        garantindo que alterações posteriores não afetem o original.

    Acoplamento:
        - titulo, string: título da tarefa a buscar.
        - Retorno:
            * (0, cópia_da_tarefa) se encontrado.
            * (1, {})                 se não encontrado.

    AE:
        - `titulo` não deve ser None.

    AS:
        - Retorna apenas cópia (`t.copy()`), não referência direta.

    Descrição:
        - Percorre cada tarefa em `tarefas` comparando `t["titulo"]`.

    Hipóteses:
        - Não existem títulos duplicados.

    Restrição:
        - Complexidade O(n) em número de tarefas.
    '''
    for t in tarefas:
        if t["titulo"] == titulo:
            return 0, t.copy()
    return 1, {}


def consultaTituloPorId(id_tarefa: int) -> tuple[int, str]:
    '''
    Nome: consultaTituloPorId

    Objetivo:
        Obter o título de uma tarefa a partir do seu ID numérico.

    Acoplamento:
        - id_tarefa, int: identificador da tarefa.
        - Retorno:
            * (0, titulo) se existir tarefa com aquele ID.
            * (1, "")     se não existir.

    AE:
        - `id_tarefa` deve ser inteiro válido.

    AS:
        - Não altera estado de `tarefas`.

    Descrição:
        - Varre `tarefas` em busca de correspondência em `t["id"]`.

    Hipóteses:
        - IDs são únicos e gerados apenas por `_gera_id()`.
    '''
    for t in tarefas:
        if t["id"] == id_tarefa:
            return 0, t["titulo"]
    return 1, ""


def consultaId(titulo: str) -> tuple[int, int]:
    '''
    Nome: consultaId

    Objetivo:
        Recuperar o ID de uma tarefa com base em seu título.

    Acoplamento:
        - titulo, string: nome da tarefa.
        - Retorno:
            * (0, id)   se encontrar.
            * (1, -1)   se não encontrar.

    AE:
        - `titulo` não deve ser string vazia.

    AS:
        - Não modifica `tarefas`.

    Descrição:
        - Percorre `tarefas` e retorna `t["id"]` no match.
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
        Adicionar uma nova tarefa na lista, validando título, descrição,
        prioridade e período (data de início ≤ data de vencimento).

    Acoplamento:
        - titulo, string: não vazio, ≤50 caracteres, único.
        - descricao, string: ≤250 caracteres.
        - prioridade, int: valor entre 0 e 4.
        - data_inicio, string "YYYY/MM/DD".
        - data_vencimento, string "YYYY/MM/DD".
        - Retorno:
            * 0 – sucesso.
            * 1 – título duplicado.
            * 2 – título vazio.
            * 3 – prioridade inválida.
            * 4 – datas inválidas (formato ou lógica).
            * 5 – título muito longo.
            * 6 – descrição muito longa.

    AE:
        - Formato de data compatível com `validaDatas()`.

    AS:
        - Em caso de sucesso, cria dict com `_gera_id()` e adiciona a `tarefas`.

    Descrição:
        - Valida cada parâmetro sequencialmente; no primeiro erro,
          retorna o código correspondente.
        - Se tudo OK, constrói a tarefa e `append()`.

    Hipóteses:
        - A função `_gera_id()` gera IDs únicos e crescentes.

    Restrição:
        - Não persiste em disco; caller deve chamar `salvaTarefas()`.
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
        Modificar campos específicos de uma tarefa existente sem alterar seu ID,
        com retornos específicos para cada tipo de validação.

    Acoplamento:
        - titulo_antigo, string: tarefa a ser editada.
        - novas_infos, dict: possíveis chaves {"titulo","descricao",
          "prioridade","data_inicio","data_vencimento"}.
        - Retorno:
            * 0 – sucesso.
            * 1 – tarefa não encontrada ou título duplicado.
            * 2 – novo título vazio.
            * 3 – prioridade inválida.
            * 4 – datas inválidas.
            * 5 – título muito longo.
            * 6 – descrição muito longa.
            * 7 – nenhuma alteração solicitada.

    AE:
        - `novas_infos` não pode ser vazio se a tarefa existir.

    AS:
        - Campos atualizados em memória; ID permanece inalterado.

    Descrição:
        - Chama `consultaTarefa()`.
        - Verifica e aplica cada campo de `novas_infos`.
        - Retorna imediatamente no primeiro erro encontrado.

    Hipóteses:
        - Usuário sabe quais campos deseja alterar.

    Restrição:
        - Não salva automaticamente; caller deve chamar `salvaTarefas()`.
    '''
    codigo, tarefa = consultaTarefa(titulo_antigo)
    if codigo != 0:
        return 1
    if not novas_infos:
        return 7

    novo_titulo = novas_infos.get("titulo", tarefa["titulo"]).strip()
    nova_descricao = novas_infos.get("descricao", tarefa["descricao"])
    nova_prioridade = novas_infos.get("prioridade", tarefa["prioridade"])
    nova_data_inicio = novas_infos.get("data_inicio", tarefa["data_inicio"])
    nova_data_vencimento = novas_infos.get("data_vencimento", tarefa["data_vencimento"])

    if novo_titulo == "":
        return 2
    if len(novo_titulo) > 50:
        return 5
    if novo_titulo != titulo_antigo and consultaTarefa(novo_titulo)[0] == 0:
        return 1
    if len(nova_descricao) > 250:
        return 6
    if nova_prioridade not in [0, 1, 2, 3, 4]:
        return 3
    if not validaDatas(nova_data_inicio, nova_data_vencimento):
        return 4

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
    '''
    Nome: apagaTarefa

    Objetivo:
        Excluir permanentemente uma tarefa identificada por título,
        validando parâmetros de entrada e retornando códigos de erro.

    Acoplamento:
        - titulo, string: tarefa a ser removida.
        - Retorno:
            * 0 – sucesso.
            * 1 – tarefa não encontrada.
            * 2 – título vazio.
            * 3 – título muito longo (>50).

    AE:
        - `titulo.strip()` não pode ser vazio.

    AS:
        - Remove o elemento de `tarefas` se encontrado.

    Descrição:
        - Valida string.
        - Itera sobre cópia de `tarefas` para remoção segura.

    Hipóteses:
        - Títulos únicos garantem remoção de item correto.

    Restrição:
        - Caller deve invocar `salvaTarefas()` para persistir.
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
        Fornecer ao chamador uma lista de cópias independentes de todas
        as tarefas presentes em memória, preservando encapsulamento.

    Acoplamento:
        - Retorno:
            * lista de dicionários (cópias).

    AE:
        - Nenhum.

    AS:
        - Alterações na lista retornada não afetam `tarefas`.

    Descrição:
        - Retorna `[t.copy() for t in tarefas]`.

    Hipóteses:
        - Dicionário de tarefa contém apenas tipos primitivos.

    Restrição:
        - Complexidade O(n).
    '''
    return [t.copy() for t in tarefas]

# -------------------------
# Auxiliar
# -------------------------

def validaDatas(inicio: str, fim: str) -> bool:
    try:
        d1 = datetime.strptime(inicio, "%Y/%m/%d")
        d2 = datetime.strptime(fim,    "%Y/%m/%d")
        return d1 <= d2
    except ValueError:
        return False
    
def _gera_id() -> int:
    global _next_id
    valor = _next_id
    _next_id += 1
    return valor
