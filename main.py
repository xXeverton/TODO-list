# main.py 

from entidades.tarefas import *
from entidades.quadros import *
from ui.ui import *

def main() -> None:

    carregaTarefas()
    carregaQuadros()


    inicializar_ui()  

    # Após fechar janela
    salvaTarefas()
    salvaQuadros()

if __name__ == "__main__":
    main()


