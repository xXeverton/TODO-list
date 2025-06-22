# main.py – ponto de entrada bem simples

from entidades.tarefas import carregaTarefas, salvaTarefas
from entidades.quadros import carregaQuadros, salvaQuadros

# importa depois de carregar dados para que a UI leia o estado já populado
aut_ui = None

def main() -> None:
    global aut_ui
    carregaTarefas()
    carregaQuadros()

    # Importação tardia evita ciclos
    import ui.ui as ui_module  # pacote ui/ com ui.py
    aut_ui = ui_module
    ui_module.inicializar_ui()  # bloqueia até fechar janela

    # Após fechar janela
    salvaTarefas()
    salvaQuadros()

if __name__ == "__main__":
    main()
