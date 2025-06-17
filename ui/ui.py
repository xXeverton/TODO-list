"""
Neste espaço se encontra as funções utilizadas para criação da UI - ui.py
"""

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from entidades.quadros import *
from entidades.tarefas import *

class OrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Organizer - Sistema Kanban")
        self.root.geometry("1000x600")
        
        # Adiciona alguns dados de teste se não existirem
        self.inicializar_dados_teste()
        
        # Configuração do tema
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Variáveis de estado
        self.quadro_atual = None
        
        # Criar widgets
        self.criar_menu_quadros()
        self.criar_area_quadro()
        self.criar_controles()
        
        # Carregar dados iniciais
        self.atualizar_lista_quadros()
    
    def inicializar_dados_teste(self):
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
    
    def criar_menu_quadros(self):
        """Painel lateral com lista de quadros"""
        self.painel_quadros = ttk.Frame(self.root, padding="10", width=200)
        self.painel_quadros.pack(side="left", fill="y")
        
        ttk.Label(self.painel_quadros, text="Quadros").pack()
        self.lista_quadros = tk.Listbox(self.painel_quadros)
        self.lista_quadros.pack(expand=True, fill="both")
        self.lista_quadros.bind("<<ListboxSelect>>", self.selecionar_quadro)
        
        ttk.Button(self.painel_quadros, 
                 text="+ Novo Quadro", 
                 command=self.criar_novo_quadro).pack(pady=5)
    
    def criar_area_quadro(self):
        """Área principal com colunas kanban"""
        self.area_quadro = ttk.Frame(self.root, padding="10")
        self.area_quadro.pack(expand=True, fill="both")
        
        # Cabeçalho do quadro
        self.titulo_quadro = ttk.Label(self.area_quadro, 
                                     text="Selecione um quadro",
                                     font=('Helvetica', 14, 'bold'))
        self.titulo_quadro.pack()
        
        # Container para colunas
        self.colunas_frame = ttk.Frame(self.area_quadro)
        self.colunas_frame.pack(expand=True, fill="both")
    
    def criar_controles(self):
        """Barra de controles e filtros"""
        self.controles = ttk.Frame(self.root, padding="10")
        self.controles.pack(fill="x")
        
        # Filtro por prioridade
        ttk.Label(self.controles, text="Filtrar por:").pack(side="left")
        self.filtro_prioridade = ttk.Combobox(self.controles, 
                                            values=["Todas", "Urgente", "Alta", "Normal", "Baixa"])
        self.filtro_prioridade.pack(side="left", padx=5)
        self.filtro_prioridade.set("Todas")
        
        # Botão de salvar
        ttk.Button(self.controles, 
                 text="Salvar Tudo", 
                 command=self.salvar_estado).pack(side="right")
    
    def atualizar_lista_quadros(self):
        """Carrega a lista de quadros disponíveis"""
        self.lista_quadros.delete(0, tk.END)
        quadros = consultaTodosQuadros()
        for quadro in quadros:
            self.lista_quadros.insert(tk.END, quadro['titulo'])
    
    def selecionar_quadro(self, event):
        """Callback quando um quadro é selecionado"""
        selection = self.lista_quadros.curselection()
        if not selection:
            return
            
        nome_quadro = self.lista_quadros.get(selection[0])
        self.quadro_atual = nome_quadro
        self.mostrar_quadro(nome_quadro)
    
    def mostrar_quadro(self, nome_quadro):
        """Exibe as colunas e tarefas de um quadro"""
        # Limpa colunas existentes
        for widget in self.colunas_frame.winfo_children():
            widget.destroy()
        
        # Atualiza título
        self.titulo_quadro.config(text=nome_quadro)
        
        # Busca dados do quadro
        status, quadro = consultaQuadro(nome_quadro)
        if status != 0:
            messagebox.showerror("Erro", "Quadro não encontrado")
            return
            
        # Cria uma coluna para cada coluna do quadro
        for coluna in quadro['colunas']:
            self.criar_coluna_ui(coluna)
    
    def criar_coluna_ui(self, coluna):
        """Cria a UI para uma coluna kanban"""
        frame_coluna = ttk.Frame(self.colunas_frame, padding="5", 
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
            self.criar_tarefa_ui(scrollable_frame, tarefa)
        
        # Botão para adicionar tarefa
        ttk.Button(frame_coluna, 
                 text="+ Adicionar Tarefa",
                 command=lambda: self.adicionar_tarefa(coluna['titulo'])).pack()
    
    def criar_tarefa_ui(self, parent, tarefa):
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
                 command=lambda t=tarefa['titulo']: self.editar_tarefa(t)).pack(side="left")
        tk.Button(botoes_frame, text="Mover", bg='white',
                 command=lambda t=tarefa['titulo']: self.mover_tarefa(t)).pack(side="left", padx=5)
        tk.Button(botoes_frame, text="Excluir", bg='white',
                 command=lambda t=tarefa['titulo']: self.excluir_tarefa(t)).pack(side="right")
    
    # Métodos para ações - versões simplificadas para teste
    def criar_novo_quadro(self):
        nome = simpledialog.askstring("Novo Quadro", "Nome do quadro:")
        if nome:
            resultado = criaQuadro(nome)
            if resultado == 0:
                self.atualizar_lista_quadros()
                messagebox.showinfo("Sucesso", "Quadro criado com sucesso!")
            else:
                messagebox.showerror("Erro", "Não foi possível criar o quadro")
    
    def adicionar_tarefa(self, nome_coluna):
        messagebox.showinfo("Info", f"Adicionar tarefa à coluna {nome_coluna} - Implemente esta função")
    
    def editar_tarefa(self, titulo_tarefa):
        messagebox.showinfo("Info", f"Editar tarefa {titulo_tarefa} - Implemente esta função")
    
    def mover_tarefa(self, titulo_tarefa):
        messagebox.showinfo("Info", f"Mover tarefa {titulo_tarefa} - Implemente esta função")
    
    def excluir_tarefa(self, titulo_tarefa):
        if messagebox.askyesno("Confirmar", f"Excluir a tarefa '{titulo_tarefa}'?"):
            resultado = apagaTarefa(titulo_tarefa)
            if resultado == 0:
                self.mostrar_quadro(self.quadro_atual)
                messagebox.showinfo("Sucesso", "Tarefa excluída!")
            else:
                messagebox.showerror("Erro", "Não foi possível excluir a tarefa")
    
    def salvar_estado(self):
        messagebox.showinfo("Info", "Salvar estado - Implemente esta função")

if __name__ == "__main__":
    root = tk.Tk()
    app = OrganizerApp(root)
    root.mainloop()