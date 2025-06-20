"""
Neste espaço se encontram as funções utilizadas para criação da UI - ui.py
(versão sem classes/POO)
"""

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from entidades.quadros import *
from entidades.tarefas import *

# Variáveis globais de estado
root = None
quadro_atual = None
lista_quadros = None
titulo_quadro = None
colunas_frame = None
filtro_prioridade = None

def inicializar_ui():
    """Função principal que inicia a interface"""
    global root
    
    root = tk.Tk()
    root.title("Organizer - Sistema Kanban")
    root.geometry("1000x600")
    
    # Configuração do tema
    style = ttk.Style()
    style.theme_use('clam')
    
    # Adiciona dados de teste se não existirem
    inicializar_dados_teste()
    
    # Criar widgets
    criar_menu_quadros()
    criar_area_quadro()
    criar_controles()
    
    # Carregar dados iniciais
    atualizar_lista_quadros()
    
    root.mainloop()

def inicializar_dados_teste():
    """Adiciona dados de teste para visualização"""
    if not consultaTodosQuadros():
        criaQuadro("Projeto Acadêmico", "Tarefas da faculdade")
        criaQuadro("Pessoal", "Tarefas pessoais")
        
        criaColuna("Projeto Acadêmico", "A Fazer")
        criaColuna("Projeto Acadêmico", "Em Progresso")
        criaColuna("Projeto Acadêmico", "Feito")
        
        criaColuna("Pessoal", "A Fazer")
        criaColuna("Pessoal", "Concluído")
        
        # Adiciona algumas tarefas de teste
        criaTarefa("Estudar Python", "Módulos e Tkinter", 2, "2023-06-15", "2023-06-20")
        criaTarefa("Fazer relatório", "Relatório do projeto", 1, "2023-06-10", "2023-06-15")
        criaTarefa("Compras mercado", "Leite, ovos, pão", 3, "2023-06-12", "2023-06-12")
        
        adicionaTarefaAoQuadro("Projeto Acadêmico", "A Fazer", "Estudar Python")
        adicionaTarefaAoQuadro("Projeto Acadêmico", "Em Progresso", "Fazer relatório")
        adicionaTarefaAoQuadro("Pessoal", "A Fazer", "Compras mercado")

def criar_menu_quadros():
    """Painel lateral com lista de quadros"""
    global lista_quadros
    
    painel_quadros = ttk.Frame(root, padding="10", width=200)
    painel_quadros.pack(side="left", fill="y")
    
    ttk.Label(painel_quadros, text="Quadros").pack()
    lista_quadros = tk.Listbox(painel_quadros)
    lista_quadros.pack(expand=True, fill="both")
    lista_quadros.bind("<<ListboxSelect>>", selecionar_quadro)
    
    ttk.Button(painel_quadros, 
             text="+ Novo Quadro", 
             command=criar_novo_quadro).pack(pady=5)

def criar_area_quadro():
    """Área principal com colunas kanban"""
    global titulo_quadro, colunas_frame
    
    area_quadro = ttk.Frame(root, padding="10")
    area_quadro.pack(expand=True, fill="both")
    
    # Cabeçalho do quadro
    titulo_quadro = ttk.Label(area_quadro, 
                             text="Selecione um quadro",
                             font=('Helvetica', 14, 'bold'))
    titulo_quadro.pack()
    
    # Container para colunas
    colunas_frame = ttk.Frame(area_quadro)
    colunas_frame.pack(expand=True, fill="both")

def criar_controles():
    """Barra de controles e filtros"""
    global filtro_prioridade
    
    controles = ttk.Frame(root, padding="10")
    controles.pack(fill="x")
    
    # Filtro por prioridade
    ttk.Label(controles, text="Filtrar por:").pack(side="left")
    filtro_prioridade = ttk.Combobox(controles, 
                                    values=["Todas", "Urgente", "Alta", "Normal", "Baixa"])
    filtro_prioridade.pack(side="left", padx=5)
    filtro_prioridade.set("Todas")
    
    # Botão de salvar
    ttk.Button(controles, 
             text="Salvar Tudo", 
             command=salvar_estado).pack(side="right")

def atualizar_lista_quadros():
    """Carrega a lista de quadros disponíveis"""
    lista_quadros.delete(0, tk.END)
    quadros = consultaTodosQuadros()
    for quadro in quadros:
        lista_quadros.insert(tk.END, quadro['titulo'])

def selecionar_quadro(event):
    """Callback quando um quadro é selecionado"""
    global quadro_atual
    
    selection = lista_quadros.curselection()
    if not selection:
        return
        
    nome_quadro = lista_quadros.get(selection[0])
    quadro_atual = nome_quadro
    mostrar_quadro(nome_quadro)

def mostrar_quadro(nome_quadro):
    """Exibe as colunas e tarefas de um quadro"""
    # Limpa colunas existentes
    for widget in colunas_frame.winfo_children():
        widget.destroy()
    
    # Atualiza título
    titulo_quadro.config(text=nome_quadro)
    
    # Busca dados do quadro
    status, quadro = consultaQuadro(nome_quadro)
    if status != 0:
        messagebox.showerror("Erro", "Quadro não encontrado")
        return
        
    # Cria uma coluna para cada coluna do quadro
    for coluna in quadro['colunas']:
        criar_coluna_ui(coluna)

def criar_coluna_ui(coluna):
    """Cria a UI para uma coluna kanban"""
    frame_coluna = ttk.Frame(colunas_frame, padding="5", 
                           relief="groove", borderwidth=1)
    frame_coluna.pack(side="left", expand=True, fill="both", padx=5)
    
    # Título da coluna
    ttk.Label(frame_coluna, text=coluna['titulo'], 
             font=('Helvetica', 10, 'bold')).pack()
    
    # Lista de tarefas
    canvas = tk.Canvas(frame_coluna)
    scrollbar = ttk.Scrollbar(frame_coluna, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Adiciona tarefas
    for tarefa in coluna['tarefas']:
        criar_tarefa_ui(scrollable_frame, tarefa)
    
    # Botão para adicionar tarefa
    ttk.Button(frame_coluna, 
             text="+ Adicionar Tarefa",
             command=lambda c=coluna['titulo']: adicionar_tarefa(c)).pack()

def criar_tarefa_ui(parent, tarefa):
    """Cria o widget de uma tarefa individual"""
    # Determina a cor com base na prioridade
    cores = {
        0: '#FFCDD2',  # Urgente (vermelho claro)
        1: '#FFE0B2',  # Alta (laranja claro)
        2: '#FFF9C4',  # Normal (amarelo claro)
        3: '#C8E6C9',  # Baixa (verde claro)
        4: '#E0F7FA'   # Nenhuma (azul claro)
    }
    cor_fundo = cores.get(tarefa['prioridade'], '#FFFFFF')
    
    frame = tk.Frame(parent, bg=cor_fundo, padx=5, pady=5, 
                    relief="ridge", borderwidth=1)
    frame.pack(fill="x", pady=2)
    
    # Título da tarefa
    tk.Label(frame, text=tarefa['titulo'], font=('Helvetica', 9, 'bold'),
            bg=cor_fundo, anchor="w").pack(fill="x")
    
    # Descrição (se existir)
    if tarefa['descricao']:
        tk.Label(frame, text=tarefa['descricao'], bg=cor_fundo,
                anchor="w").pack(fill="x")
    
    # Data de vencimento
    tk.Label(frame, text=f"Venc: {tarefa['data_vencimento']}", 
            bg=cor_fundo, anchor="w").pack(fill="x")
    
    # Botões de ação
    botoes_frame = tk.Frame(frame, bg=cor_fundo)
    botoes_frame.pack(fill="x")
    
    tk.Button(botoes_frame, text="Editar", bg='white',
             command=lambda t=tarefa['titulo']: editar_tarefa(t)).pack(side="left")
    tk.Button(botoes_frame, text="Mover", bg='white',
             command=lambda t=tarefa['titulo']: mover_tarefa(t)).pack(side="left", padx=5)
    tk.Button(botoes_frame, text="Excluir", bg='white',
             command=lambda t=tarefa['titulo']: excluir_tarefa(t)).pack(side="right")

# Funções de ação
def criar_novo_quadro():
    nome = simpledialog.askstring("Novo Quadro", "Nome do quadro:")
    if nome:
        resultado = criaQuadro(nome)
        if resultado == 0:
            atualizar_lista_quadros()
            messagebox.showinfo("Sucesso", "Quadro criado com sucesso!")
        else:
            messagebox.showerror("Erro", "Não foi possível criar o quadro")

def adicionar_tarefa(nome_coluna):
    messagebox.showinfo("Info", f"Adicionar tarefa à coluna {nome_coluna} - Implemente esta função")

def editar_tarefa(titulo_tarefa):
    messagebox.showinfo("Info", f"Editar tarefa {titulo_tarefa} - Implemente esta função")

def mover_tarefa(titulo_tarefa):
    messagebox.showinfo("Info", f"Mover tarefa {titulo_tarefa} - Implemente esta função")

def excluir_tarefa(titulo_tarefa):
    if messagebox.askyesno("Confirmar", f"Excluir a tarefa '{titulo_tarefa}'?"):
        resultado = apagaTarefa(titulo_tarefa)
        if resultado == 0:
            mostrar_quadro(quadro_atual)
            messagebox.showinfo("Sucesso", "Tarefa excluída!")
        else:
            messagebox.showerror("Erro", "Não foi possível excluir a tarefa")

def salvar_estado():
    messagebox.showinfo("Info", "Salvar estado - Implemente esta função")

if __name__ == "__main__":
    inicializar_ui()