# ui.py — Kanban interface v6 (procedural, dialogs always on top)
from __future__ import annotations
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from datetime import datetime
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from entidades.tarefas import *
from entidades.quadros import *

__all__ = ["inicializar_ui"]

# globals
root: tk.Tk | None = None
quadro_atual: str | None = None
lista_quadros_lb: tk.Listbox | None = None
colunas_canvas: tk.Canvas | None = None
colunas_frame: ttk.Frame | None = None
scroll_x: ttk.Scrollbar | None = None
scroll_y: ttk.Scrollbar | None = None
titulo_lbl: ttk.Label | None = None
btn_nova_coluna: ttk.Button | None = None

DATE_FMT = "%Y/%m/%d"

# —— Dialog wrappers to force topmost ——
def _askstring(title: str, prompt: str, **kwargs) -> str | None:
    if root: root.attributes('-topmost', True)
    res = simpledialog.askstring(title, prompt, parent=root, **kwargs)
    if root: root.attributes('-topmost', False)
    return res

def _askinteger(title: str, prompt: str, **kwargs) -> int | None:
    if root: root.attributes('-topmost', True)
    res = simpledialog.askinteger(title, prompt, parent=root, **kwargs)
    if root: root.attributes('-topmost', False)
    return res

def _askyesno(title: str, msg: str) -> bool:
    if root: root.attributes('-topmost', True)
    res = messagebox.askyesno(title, msg, parent=root)
    if root: root.attributes('-topmost', False)
    return res

def _showerror(title: str, msg: str) -> None:
    if root: root.attributes('-topmost', True)
    messagebox.showerror(title, msg, parent=root)
    if root: root.attributes('-topmost', False)

def _showinfo(title: str, msg: str) -> None:
    if root: root.attributes('-topmost', True)
    messagebox.showinfo(title, msg, parent=root)
    if root: root.attributes('-topmost', False)


# —— Bootstrap ——
def inicializar_ui() -> None:
    """
    Nome: inicializar_ui

    Objetivo: Inicia a interface gráfica do sistema Kanban, carregando dados e configurando os elementos visuais.

    Acoplamento: Retorno: None

    AE: carregaTarefas, carregaQuadros, _menu_quadros, _area_quadro, _barra_inferior, _atualiza_lista_quadros

    AS: Deve ser chamada apenas uma vez no início da aplicação.

    Descrição: Cria a janela principal, define seu layout e inicializa a interface com dados dos quadros e tarefas previamente salvos.

    Restrição: Não deve ser chamada em ambientes sem interface gráfica (headless).

    """
    carregaTarefas()
    carregaQuadros()
    global root
    root = tk.Tk()
    root.title("Organizer – Kanban")
    root.geometry("1100x650")
    ttk.Style().theme_use("clam")

    _menu_quadros()
    _area_quadro()
    _barra_inferior()
    _atualiza_lista_quadros()
    root.mainloop()


# —— Layout —— 
def _menu_quadros():
    """
    Nome: _menu_quadros

    Objetivo: Cria o menu lateral com a lista de quadros e botões para criar ou excluir quadros.

    Acoplamento: Retorno: None

    AE: root, lista_quadros_lb, _novo_quadro, _excluir_quadro

    AS: Espera que a variável global `root` esteja inicializada.

    Descrição: Monta o painel lateral esquerdo que lista todos os quadros existentes e fornece botões para criação e exclusão de quadros.

    Restrição: A função depende da existência da janela principal do tkinter.

    """
    global lista_quadros_lb
    painel = ttk.Frame(root, padding=10, width=220)
    painel.pack(side="left", fill="y")
    ttk.Label(painel, text="Quadros", font=("Helvetica", 11, "bold")).pack()
    lista_quadros_lb = tk.Listbox(painel)
    lista_quadros_lb.pack(expand=True, fill="both")
    lista_quadros_lb.bind("<<ListboxSelect>>", _on_select_quadro)
    ttk.Button(painel, text="+ Novo Quadro", command=_novo_quadro).pack(pady=5)
    ttk.Button(painel, text="✖ Excluir Quadro", command=_excluir_quadro).pack()

def _area_quadro():
    """
    Nome: _area_quadro

    Objetivo: Cria a área central da interface onde são exibidas as colunas e tarefas do quadro selecionado.

    Acoplamento: Retorno: None

    AE: root, colunas_canvas, colunas_frame, scroll_x, scroll_y, titulo_lbl, btn_nova_coluna

    AS: Deve ser chamada após `root` estar inicializado.

    Descrição: Define o layout e scroll da área principal onde as colunas de um quadro são apresentadas e manipuladas.

    Restrição: A janela principal (`root`) deve estar previamente criada.

    """
    global colunas_canvas, colunas_frame, scroll_x, scroll_y, titulo_lbl, btn_nova_coluna

    area = ttk.Frame(root, padding=10)
    area.pack(expand=True, fill="both")

    # ── header ──
    header = ttk.Frame(area)
    header.pack(fill="x")
    titulo_lbl = ttk.Label(header, text="Selecione um quadro",
                           font=("Helvetica", 14, "bold"))
    titulo_lbl.pack(side="left")
    btn_nova_coluna = ttk.Button(header, text="+ Nova Coluna",
                                 command=_nova_coluna, state="disabled")
    btn_nova_coluna.pack(side="right")

    # ── scrollable canvas frame ──
    canvas_frame = ttk.Frame(area)
    canvas_frame.pack(expand=True, fill="both")

    # create canvas
    colunas_canvas = tk.Canvas(canvas_frame, highlightthickness=0)
    # vertical scrollbar
    scroll_y = ttk.Scrollbar(canvas_frame, orient="vertical",
                             command=colunas_canvas.yview)
    # horizontal scrollbar
    scroll_x = ttk.Scrollbar(area, orient="horizontal",
                             command=colunas_canvas.xview)

    # wire them up
    colunas_canvas.configure(xscrollcommand=scroll_x.set,
                             yscrollcommand=scroll_y.set)

    # the inner frame that actually holds the columns
    colunas_frame = ttk.Frame(colunas_canvas)
    colunas_canvas.create_window((0, 0), window=colunas_frame, anchor="nw")

    # update scrollregion when inner frame changes
    colunas_frame.bind(
        "<Configure>",
        lambda e: colunas_canvas.configure(
            scrollregion=colunas_canvas.bbox("all")
        )
    )

    # pack everything
    colunas_canvas.pack(side="left", expand=True, fill="both")
    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(fill="x")


def _barra_inferior():
    """
    Nome: _barra_inferior

    Objetivo: Cria a barra inferior da interface com o botão para salvar os dados.

    Acoplamento: Retorno: None

    AE: root, _salvar_estado

    AS: Espera que a janela principal esteja criada e visível.

    Descrição: Adiciona um botão de "Salvar Tudo" na parte inferior da tela, permitindo persistência manual do estado atual.

    Restrição: Depende do root e das funções de salvamento estarem funcionais.

    """
    barra = ttk.Frame(root, padding=10)
    barra.pack(fill="x")
    ttk.Button(barra, text="Salvar Tudo", command=_salvar_estado).pack(side="right")


# —— Refresh —— 
def _atualiza_lista_quadros():
    """
    Nome: _atualiza_lista_quadros

    Objetivo: Atualiza visualmente a lista de quadros disponíveis na interface.

    Acoplamento: Retorno: None

    AE: lista_quadros_lb, consultaTodosQuadros

    AS: Lista de quadros precisa estar disponível via função `consultaTodosQuadros`.

    Descrição: Limpa a lista atual e repopula com os títulos dos quadros existentes.

    Restrição: `lista_quadros_lb` precisa estar inicializada.

    """
    lista_quadros_lb.delete(0, tk.END)
    for q in consultaTodosQuadros():
        lista_quadros_lb.insert(tk.END, q["titulo"])

def _on_select_quadro(event=None):
    """
    Nome: _on_select_quadro

    Objetivo: Atualiza a interface com as colunas e tarefas do quadro selecionado.

    Acoplamento: Retorno: None

    AE: lista_quadros_lb, quadro_atual, btn_nova_coluna, _mostrar_quadro

    AS: Depende da seleção feita pelo usuário na lista de quadros.

    Descrição: Detecta seleção de um quadro e atualiza a visualização do conteúdo correspondente na área central.

    Restrição: Lista deve conter quadros válidos.

    """
    global quadro_atual
    sel = lista_quadros_lb.curselection()
    if not sel: return
    quadro_atual = lista_quadros_lb.get(sel[0])
    btn_nova_coluna["state"] = "normal"
    _mostrar_quadro(quadro_atual)


# —— Display —— 
def _mostrar_quadro(nome: str):
    """
    Nome: _mostrar_quadro

    Objetivo: Exibe na interface todas as colunas e tarefas pertencentes a um quadro específico.

    Acoplamento: Retorno: None

    AE: consultaQuadro, consultaTodasColunas, _criar_coluna_ui, colunas_frame

    AS: Espera que o nome do quadro seja válido e existente.

    Descrição: Atualiza a área central da interface com o conteúdo completo do quadro, incluindo colunas e tarefas.

    Restrição: Quadro informado deve existir e estar bem formatado.

    """
    for w in colunas_frame.winfo_children():
        w.destroy()
    titulo_lbl.config(text=nome)
    st, quadro = consultaQuadro(nome)
    if st != 0:
        _showerror("Erro", "Quadro não encontrado")
        return
    for cod in quadro["colunas"]:
        col = next((c for c in consultaTodasColunas() if c["codigo"]==cod), None)
        if col:
            _criar_coluna_ui(col)

def _criar_coluna_ui(coluna: dict):
    """
    Nome: _criar_coluna_ui

    Objetivo: Gera a interface visual para uma coluna específica e suas tarefas.

    Acoplamento: Retorno: None

    AE: consultaTituloPorId, consultaTarefa, _criar_tarefa_ui

    AS: Espera que os dados da coluna estejam no formato correto e que os IDs de tarefas estejam válidos.

    Descrição: Cria um painel visual para uma coluna, incluindo seus botões de ação e as tarefas dentro dela.

    Restrição: Função assume estrutura específica de dicionário para a coluna.

    """
    frame = ttk.Frame(colunas_frame, padding=10,
                      relief="groove", borderwidth=1)
    frame.pack(side="left", pady=6, padx=8)
    frame.configure(width=300, height=600)
    frame.pack_propagate(False)
    ttk.Label(frame, text=coluna["titulo"],
              font=("Helvetica", 11, "bold")).pack(pady=(0,6))
    inner = ttk.Frame(frame); inner.pack(expand=True, fill="both")
    for tid in coluna["tarefas"]:
        st, title = consultaTituloPorId(tid)
        if st==0:
            task = consultaTarefa(title)[1]
            _criar_tarefa_ui(inner, task, coluna["titulo"])
    ttk.Button(frame, text="+ Tarefa",
               command=lambda c=coluna["titulo"]: _nova_tarefa(c)
              ).pack(pady=6)
    ttk.Button(frame, text="✎ Renomear Coluna",
               command=lambda c=coluna["titulo"]: _renomear_coluna(c)
              ).pack(pady=2)
    ttk.Button(frame, text="✖ Excluir Coluna",
               command=lambda c=coluna["titulo"]: _excluir_coluna(c)
              ).pack(pady=2)

def _criar_tarefa_ui(parent, tarefa: dict, nome_coluna: str):
    """
    Nome: _criar_tarefa_ui

    Objetivo: Cria os elementos visuais que representam uma tarefa na interface.

    Acoplamento: Retorno: None

    AE: tarefa, nome_coluna, _editar_tarefa, _mover_tarefa, _excluir_tarefa

    AS: Espera receber uma tarefa válida com os campos necessários preenchidos.

    Descrição: Cria um pequeno painel com as informações da tarefa e botões para edição, movimentação e exclusão.

    Restrição: Campos da tarefa devem estar corretamente preenchidos e formatados.

    """
    colors={0:"#FFCDD2",1:"#FFE0B2",2:"#FFF9C4",3:"#C8E6C9",4:"#E0F7FA"}
    bg=colors.get(tarefa["prioridade"],"white")
    frm=tk.Frame(parent,bg=bg,relief="ridge",borderwidth=1,padx=4,pady=4)
    frm.pack(fill="x", pady=2)
    tk.Label(frm,text=tarefa["titulo"],bg=bg,
             anchor="w",font=("Helvetica",9,"bold")).pack(fill="x")
    if tarefa["descricao"]:
        tk.Label(frm,text=tarefa["descricao"],bg=bg,
                 anchor="w").pack(fill="x")
    tk.Label(frm, text="Venc.: "+tarefa["data_vencimento"],
             bg=bg,anchor="w").pack(fill="x")
    btns=tk.Frame(frm,bg=bg); btns.pack(fill="x")
    tk.Button(btns,text="Editar",
              command=lambda t=tarefa["titulo"]: _editar_tarefa(t)
             ).pack(side="left")
    tk.Button(btns,text="Mover",
              command=lambda t=tarefa["titulo"],c=nome_coluna:
                    _mover_tarefa(t,c)
             ).pack(side="left",padx=3)
    tk.Button(btns,text="✖",
              command=lambda t=tarefa["titulo"]: _excluir_tarefa(t)
             ).pack(side="right")


# —— Actions —— 
def _novo_quadro():
    """
    Nome: _novo_quadro

    Objetivo: Solicita ao usuário o nome e cria um novo quadro.

    Acoplamento: Retorno: None

    AE: _askstring, criaQuadro, _atualiza_lista_quadros

    AS: Espera que o usuário forneça um nome único e válido.

    Descrição: Abre uma caixa de diálogo, coleta o nome do quadro e o cria, atualizando a interface após sucesso.

    Restrição: Não deve ser chamado se a persistência de quadros estiver indisponível.

    """
    nome=_askstring("Novo Quadro","Nome do quadro:")
    if nome and criaQuadro(nome)==0:
        _atualiza_lista_quadros()

def _excluir_quadro():
    """
    Nome: _excluir_quadro

    Objetivo: Exclui o quadro atualmente selecionado após confirmação do usuário.

    Acoplamento: Retorno: None

    AE: _askyesno, apagaQuadro, quadro_atual, _atualiza_lista_quadros

    AS: Um quadro precisa estar selecionado previamente.

    Descrição: Remove o quadro da memória e atualiza a interface para refletir a exclusão.

    Restrição: Exclusão é permanente e não pode ser desfeita via interface.

    """
    global quadro_atual
    if not quadro_atual: return
    if _askyesno("Excluir Quadro","Tem certeza?"):
        apagaQuadro(quadro_atual)
        quadro_atual=None
        btn_nova_coluna["state"]="disabled"
        _atualiza_lista_quadros()
        for w in colunas_frame.winfo_children(): w.destroy()
        titulo_lbl.config(text="Selecione um quadro")

def _nova_coluna():
    """
    Nome: _nova_coluna

    Objetivo: Adiciona uma nova coluna ao quadro atual.

    Acoplamento: Retorno: None

    AE: quadro_atual, _askstring, criaColuna, _mostrar_quadro

    AS: Requer que um quadro esteja selecionado.

    Descrição: Pede ao usuário o nome da nova coluna e, se fornecido corretamente, a adiciona ao quadro atual.

    Restrição: Coluna só pode ser adicionada a um quadro existente.

    """
    if not quadro_atual: return
    nome=_askstring("Nova Coluna","Nome da coluna:")
    if nome and criaColuna(quadro_atual,nome)==0:
        _mostrar_quadro(quadro_atual)

def _renomear_coluna(coluna:str):
    """
    Nome: _renomear_coluna

    Objetivo: Solicita novo nome e renomeia uma coluna existente.

    Acoplamento: Retorno: None

    AE: quadro_atual, _askstring, editaColuna, _mostrar_quadro

    AS: Espera que o quadro atual esteja carregado e a coluna exista.

    Descrição: Abre um prompt de edição e aplica as mudanças no nome da coluna.

    Restrição: Nome novo não pode ser nulo.

    """
    novo=_askstring("Renomear Coluna","Novo nome:", initialvalue=coluna)
    if novo and editaColuna(quadro_atual,coluna,novo)==0:
        _mostrar_quadro(quadro_atual)

def _excluir_coluna(coluna:str):
    """
    Nome: _excluir_coluna

    Objetivo: Exclui uma coluna de um quadro após confirmação.

    Acoplamento: Retorno: None

    AE: quadro_atual, _askyesno, apagaColuna, _mostrar_quadro

    AS: Coluna deve existir no quadro atual.

    Descrição: Remove permanentemente a coluna e atualiza a visualização.

    Restrição: Ação é destrutiva e requer confirmação do usuário.

    """
    if _askyesno("Excluir Coluna","Tem certeza?"):
        apagaColuna(quadro_atual,coluna)
        _mostrar_quadro(quadro_atual)

def _nova_tarefa(coluna:str):
    """
    Nome: _nova_tarefa

    Objetivo: Cria uma nova tarefa e a adiciona à coluna selecionada.

    Acoplamento: Retorno: None

    AE: quadro_atual, _askstring, _askinteger, criaTarefa, adicionaTarefaAoQuadro, _mostrar_quadro

    AS: Requer quadro e coluna ativos. Dados da tarefa devem ser válidos.

    Descrição: Solicita os dados da tarefa ao usuário, cria e insere no sistema.

    Restrição: Datas devem estar no formato correto. Prioridade entre 0–4.

    """
    if not quadro_atual: return
    titulo=_askstring("Nova Tarefa","Título:")
    if not titulo: return
    descricao=_askstring("Nova Tarefa","Descrição:", initialvalue="") or ""
    pri=_askinteger("Prioridade","0 (urgente) a 4 (nenhuma)",
                    minvalue=0,maxvalue=4)
    if pri is None: return
    hoje=datetime.today().strftime(DATE_FMT)
    ini=_askstring("Data Início",DATE_FMT, initialvalue=hoje) or hoje
    venc=_askstring("Data Vencimento",DATE_FMT, initialvalue=hoje) or hoje
    err = criaTarefa(titulo, descricao, pri, ini, venc)
    if err != 0:
        if err == 2:
            _showerror("Erro", "Título não pode ser vazio.")
        elif err == 5:
            _showerror("Erro", "Título não pode ter mais de 50 caracteres.")
        elif err == 1:
            _showerror("Erro", "Título já existe.")
        elif err == 3:
            _showerror("Erro", "Prioridade deve ser entre 0 e 4.")
        elif err == 4:
            _showerror("Erro", "Datas inválidas ou formato incorreto.")
        else:
            _showerror("Erro", "Falha ao criar tarefa — verifique os dados.")
        return
    adicionaTarefaAoQuadro(quadro_atual,coluna,titulo)
    _mostrar_quadro(quadro_atual)

def _editar_tarefa(titulo:str):
    """
    Nome: _editar_tarefa

     Objetivo: Permite editar os dados de uma tarefa já existente.

    Acoplamento: Retorno: None

    AE: consultaTarefa, _askstring, _askinteger, editaTarefa, _mostrar_quadro

    AS: Tarefa deve estar previamente cadastrada e acessível.

    Descrição: Abre caixas de diálogo para editar título, descrição, datas e prioridade da tarefa.

    Restrição: Campos devem ser preenchidos corretamente."

    """
    st,t=consultaTarefa(titulo)
    if st!=0: return
    novas={}
    nt=_askstring("Editar Tarefa","Novo título:", initialvalue=t["titulo"])
    if nt and nt!=t["titulo"]: novas["titulo"]=nt
    nd=_askstring("Editar Tarefa","Nova descrição:", initialvalue=t["descricao"])
    if nd is not None and nd!=t["descricao"]: novas["descricao"]=nd
    np=_askinteger("Editar Tarefa","Prioridade (0-4):", initialvalue=t["prioridade"])
    if np is not None and np!=t["prioridade"]: novas["prioridade"]=np
    ni=_askstring("Editar Tarefa","Data Início:", initialvalue=t["data_inicio"])
    if ni and ni!=t["data_inicio"]: novas["data_inicio"]=ni
    nv=_askstring("Editar Tarefa","Data Vencimento:", initialvalue=t["data_vencimento"])
    if nv and nv!=t["data_vencimento"]: novas["data_vencimento"]=nv
    if novas:
        editaTarefa(titulo,novas)
        _mostrar_quadro(quadro_atual)

def _mover_tarefa(titulo:str,origem:str):
    """
    Nome: _mover_tarefa

    Objetivo: Move uma tarefa de uma coluna para outra.

    Acoplamento: Retorno: None

    AE: consultaQuadro, consultaTodasColunas, _askstring, moverTarefaEntreColunas, _mostrar_quadro

    AS: Espera que a tarefa exista e que colunas de destino estejam disponíveis.

    Descrição: Pergunta a nova coluna destino e, se confirmada, move a tarefa.

    Restrição: A coluna destino deve ser diferente da origem e pertencer ao mesmo quadro.

    """
    st,q=consultaQuadro(quadro_atual)
    if st!=0: return
    dests=[c["titulo"] for c in consultaTodasColunas()
           if c["codigo"] in q["colunas"] and c["titulo"]!=origem]
    if not dests:
        _showinfo("Mover","Nenhuma coluna destino disponível.")
        return
    dst=_askstring("Mover Tarefa","Destino:", initialvalue=dests[0])
    if dst in dests:
        moverTarefaEntreColunas(quadro_atual,origem,dst,titulo)
        _mostrar_quadro(quadro_atual)

def _excluir_tarefa(titulo:str):
    """
    Nome: _excluir_tarefa

    Objetivo: Exclui uma tarefa existente após confirmação do usuário.

    Acoplamento: Retorno: None

    AE: _askyesno, apagaTarefa, _mostrar_quadro

    AS: Tarefa deve existir no quadro e coluna atuais.

    Descrição: Remove a tarefa permanentemente do sistema.

    Restrição: Ação irreversível.

    """
    if _askyesno("Excluir Tarefa","Tem certeza?"):
        apagaTarefa(titulo)
        _mostrar_quadro(quadro_atual)

def _salvar_estado():
    """
    Nome: _salvar_estado

    Objetivo: Salva todos os quadros e tarefas na persistência atual.

    Acoplamento: Retorno: None

    AE: salvaTarefas, salvaQuadros, _showinfo

    AS: Chamado quando o usuário desejar salvar manualmente o progresso.

    Descrição: Persiste os dados atuais da aplicação e informa sucesso.

    Restrição: Exige que os módulos de salvamento estejam funcionando.

    """
    salvaTarefas()
    salvaQuadros()
    _showinfo("Salvar","Estado gravado com sucesso")

if __name__ == "__main__":
    inicializar_ui()
