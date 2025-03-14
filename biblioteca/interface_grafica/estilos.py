
AZUL_CLARO = "#6b8cae"  # bordas
AZUL_ESCURO = "#4a6a8a"  #  hover
VERMELHO = "#c27c7c"     
VERMELHO_ESCURO = "#a35f5f"  
VERDE = "#7caa8c"       
VERDE_ESCURO = "#5d8a6f" 
BRANCO = "#f7f3e9"       
PRETO = "#e8d5b5"        
CINZA_CLARO = "#f0ece2"  
CINZA_ESCURO = "#b8a88e" 


COR_FUNDO = PRETO  
COR_FUNDO_TRANSPARENTE = "rgba(232, 213, 181, 0.95)" 
COR_CARTAO = "rgba(224, 204, 170, 0.95)"  
COR_TEXTO = "#594a3c"  
COR_BORDA = "#c4b59e"  

# Estilo suave para as janelas principais
estilo_janela_principal = f"""
    QMainWindow, QWidget, QFrame {{
        background-color: {PRETO};
        color: {COR_TEXTO};
    }}
    QLabel {{
        color: {COR_TEXTO};
    }}
"""

# Estilo para tela de login
estilo_tela_login = f"""
    QMainWindow, QWidget, QFrame, QLabel {{
        background-color: {PRETO};
        color: {COR_TEXTO};
    }}
"""

# Estilo para tela inicial com scroll area
estilo_tela_inicial = f"""
    QMainWindow, QWidget, QFrame, QLabel, QScrollArea, QScrollBar {{
        background-color: {PRETO};
        color: {COR_TEXTO};
    }}
    QScrollArea {{
        border: 1px solid {COR_BORDA};
        border-radius: 8px;
    }}
    QScrollArea > QWidget > QWidget {{
        background-color: {PRETO};
    }}
    QScrollArea > QWidget {{
        background-color: {PRETO};
    }}
"""

# Estilo para o conteúdo da scroll area
estilo_scroll_content = f"""
    background-color: {PRETO};
    color: {COR_TEXTO};
"""

# Estilo para a scroll area na busca
estilo_scroll_area_busca = f"""
    QScrollArea {{
        background-color: {PRETO};
        color: {COR_TEXTO};
        border: 1px solid {COR_BORDA};
        border-radius: 8px;
    }}
"""

# Estilo para o frame de informações do livro
estilo_frame_info_livro = f"""
    background-color: {COR_CARTAO};
    color: {COR_TEXTO};
    border: 1px solid {COR_BORDA};
    border-radius: 10px;
    padding: 15px;
"""

# Estilo para cartões/painéis (como o painel de login)
estilo_cartao = f"""
    QFrame#frame_login {{
        background-color: {COR_CARTAO};
        border-radius: 12px;
        border: 1px solid {COR_BORDA};
    }}
    QFrame#frame_conteudo {{
        background-color: {COR_CARTAO};
        border-radius: 12px;
        border: 1px solid {COR_BORDA};
    }}
"""

# Estilo para títulos grandes
estilo_titulo = f"""
    QLabel[titulo=true] {{
        color: {COR_TEXTO};
        font-size: 24pt;
        font-weight: bold;
    }}
"""

# Estilo para botões de login/criar conta (azul)
estilo_botoes_login = f"""
    QPushButton {{
        background-color: {AZUL_CLARO};
        color: {BRANCO};
        border-radius: 8px;
        padding: 8px;
        font-weight: bold;
        border: none;
    }}
    QPushButton:hover {{
        background-color: {AZUL_ESCURO};
    }}
"""

# Estilo para botões de voltar/cancelar (vermelho)
estilo_botoes_voltar = f"""
    QPushButton {{
        background-color: {VERMELHO};
        color: {BRANCO};
        border-radius: 8px;
        padding: 8px;
        font-weight: bold;
        border: none;
    }}
    QPushButton:hover {{
        background-color: {VERMELHO_ESCURO};
    }}
"""

# Estilo para botões de adicionar/salvar (verde)
estilo_botoes_adicionar = f"""
    QPushButton {{
        background-color: {VERDE};
        color: {BRANCO};
        border-radius: 8px;
        padding: 8px;
        font-weight: bold;
        border: none;
    }}
    QPushButton:hover {{
        background-color: {VERDE_ESCURO};
    }}
"""

# Estilo para botões de editar (azul)
estilo_botoes_editar = f"""
    QPushButton {{
        background-color: {AZUL_CLARO};
        color: {BRANCO};
        border-radius: 8px;
        padding: 10px;
        font-size: 12pt;
        font-weight: bold;
        border: none;
    }}
    QPushButton:hover {{
        background-color: {AZUL_ESCURO};
    }}
"""

# Estilo para botões de excluir (vermelho)
estilo_botoes_excluir = f"""
    QPushButton {{
        background-color: {VERMELHO};
        color: {BRANCO};
        border-radius: 8px;
        padding: 10px;
        font-size: 12pt;
        font-weight: bold;
        border: none;
    }}
    QPushButton:hover {{
        background-color: {VERMELHO_ESCURO};
    }}
"""

# Estilo para labels de informação
estilo_label_info = f"""
    font-size: 10pt; 
    font-weight: bold;
    color: {COR_TEXTO};
"""

# Estilo para campos de texto 
estilo_campo_texto = f"""
    QLineEdit {{
        border: 1px solid {COR_BORDA};
        border-radius: 8px;
        padding: 8px;
        background-color: {BRANCO};
        color: {COR_TEXTO};
    }}
    QLineEdit:focus {{
        border: 1px solid {AZUL_CLARO};
        background-color: {BRANCO};
    }}
"""

# Estilo específico para campos de login
estilo_campo_login = f"""
    QLineEdit {{
        border: 1px solid {COR_BORDA};
        border-radius: 8px;
        padding: 8px;
        background-color: {BRANCO};
        color: {COR_TEXTO};
    }}
    QLineEdit:focus {{
        border: 1px solid {AZUL_CLARO};
        background-color: {BRANCO};
    }}
"""

# Configurações de tabela
estilo_cabecalho_tabela = f"""
    QHeaderView::section {{
        background-color: {COR_CARTAO};
        color: {COR_TEXTO};
        font-weight: bold;
        padding: 8px;
        border: 1px solid {COR_BORDA};
    }}
"""

# Estilo para a tabela
estilo_tabela = f"""
    QTableView {{
        background-color: {BRANCO};
        alternate-background-color: {CINZA_CLARO};
        color: {COR_TEXTO};
        gridline-color: {COR_BORDA};
        border: 1px solid {COR_BORDA};
        border-radius: 8px;
    }}
    QTableView::item:selected {{
        background-color: {AZUL_CLARO};
        color: {BRANCO};
    }}
"""

# Estilo para scroll bars
estilo_scrollbar = f"""
    QScrollBar:vertical {{
        border: none;
        background: {CINZA_CLARO};
        width: 10px;
        margin: 0px 0px 0px 0px;
        border-radius: 5px;
    }}
    QScrollBar::handle:vertical {{
        background: {CINZA_ESCURO};
        min-height: 20px;
        border-radius: 5px;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}
"""
