
import json, os

__all__ = ["salva_estado", "carrega_estado"]

def salva_estado(data, filename):
    '''
    Nome: salva_estado

    Objetivo: Salvar a estrutura de dados fornecida em um arquivo JSON no diretório "data/".

    Acoplamento:
        - data, list: Lista de dados a serem salvos. Deve ser serializável em JSON.
        - filename, string: Nome do arquivo no qual os dados serão salvos.
        - Retorno:
            * True: Se os dados foram salvos com sucesso
            * False: Se os dados não forem uma lista ou ocorrer erro de tipo

    AE:
        - O parâmetro data deve ser do tipo list.
        - O diretório "data/" deve existir previamente no sistema de arquivos.
        - O nome do arquivo deve ser válido para o sistema operacional.

    AS:
        - A função chamadora deve verificar o valor de retorno para garantir que o salvamento foi bem-sucedido.

    Descrição:
        Serializa os dados passados no parâmetro `data` em formato JSON e salva no arquivo especificado por `filename`, dentro do diretório "data/".

    Hipóteses:
        - Os dados são compatíveis com o formato JSON (valores primitivos, listas, dicionários).
        - O diretório "data/" existe e tem permissões de escrita.

    Restrições:
        - Apenas listas podem ser salvas. Tipos diferentes são rejeitados.
        - O salvamento sobrescreve qualquer arquivo existente com o mesmo nome.
    '''
    path = "data/"+filename
    if type(data) is not list:
        return False
    with open(path,"w") as f:
        json.dump(data, f, indent=2)

    return True

def carrega_estado(filename):
    '''
    Nome: carrega_estado

    Objetivo: Carregar dados de um arquivo JSON do diretório "data/".

    Acoplamento:
        - filename, string: Nome do arquivo de onde os dados serão carregados.
        - Retorno:
            * list: Conteúdo carregado do arquivo, se o mesmo existir
            * []: Lista vazia, se o arquivo não existir (primeira execução por ex.)

    AE:
        - O nome do arquivo deve referenciar um arquivo JSON válido existente no diretório "data/".

    AS:
        - A função chamadora deve verificar se o retorno está vazio para saber se a carga foi bem-sucedida.

    Descrição:
        Lê o conteúdo de um arquivo JSON localizado no diretório "data/" e o converte novamente para estrutura de dados Python (list, dict, etc.).

    Hipóteses:
        - O conteúdo do arquivo está em formato JSON válido.
        - O diretório "data/" contém o arquivo desejado, salvo anteriormente por `salva_estado`.

    Restrições:
        - Se o arquivo não existir, a função retorna uma lista vazia.
        - O arquivo deve estar bem formatado como JSON para que a leitura funcione corretamente.
    '''
    path = "data/"+filename
    if os.path.exists(path):
        with open(path, "r") as f:
            data = json.load(f)
        return data
    else:
        return []