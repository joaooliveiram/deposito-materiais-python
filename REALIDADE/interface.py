# Arquivo para cuidar da interface
import tkinter
from tkinter import ttk # TK com temas para ficar mais bonito

janela = tkinter.Tk()
janela.title("Depósito de Materiais de Construção")
janela.geometry("1000x800")

label_titutlo = tkinter.Label(
    janela, text="Sistema de Controle de Estoque", font=("Arial", 16, "bold") # tupla pra informar a fonte, tamanho e bold para negrito
)
label_titutlo.pack(pady=20)  # pack serve para fixar a janela na tela ; e pady=20 dá um espaço em cima e embaixo

janela_cadastro = ttk.LabelFrame(janela, text=" Cadastro de Material ")
janela_cadastro.pack(fill="x", padx=20, pady=10)

# Importar as funcoes e categorias do sistema.py

from sistema import CATEGORIAS

# L A B E L s
# Linha 0 com ID e Nome

label_id = ttk.Label(janela_cadastro, text="ID")
label_id.grid(row=0, column=0, padx=10, pady=5, sticky="w") # W para West para ficar do lado esquerdo

texto_id = ttk.Entry(janela_cadastro, width=9)
texto_id.grid(row=0, column=1, padx=5, pady=5, sticky="w")

label_nome = ttk.Label(janela_cadastro, text="Nome do Material: ")
label_nome.grid(row=0, column=2, padx=10, pady=5, sticky="w")

texto_nome = ttk.Entry(janela_cadastro, width=35)
texto_nome.grid(row=0, column=3, padx=10, pady=10)

# Linha 1 com Categoria e Quantidade
label_categoria = ttk.Label(janela_cadastro, text="Categoria:")
label_categoria.grid(row=1, column=0, padx=10, pady=5, sticky="w")

combo_categoria = ttk.Combobox(janela_cadastro, values=CATEGORIAS, state="readonly", width=15) # combobox = caixa de escolha e readonly para o usuario nao alterar
combo_categoria.grid(row=1, column=1, padx=10, pady=5, sticky="w")

label_quantidade = ttk.Label(janela_cadastro, text="Quantidade:")
label_quantidade.grid(row=1, column=2, padx=10, pady=5, sticky="w")

texto_quantidade = ttk.Entry(janela_cadastro, width=12)
texto_quantidade.grid(row=1, column=3, padx=10, pady=5, sticky="w")

# Linha 2 para o preço
label_preco = ttk.Label(janela_cadastro, text="Preço Unitário (R$):")
label_preco.grid(row=2, column=0, padx=10, pady=5, sticky="w")

texto_preco = ttk.Entry(janela_cadastro, width=15)
texto_preco.grid(row=2, column=1, padx=10, pady=5, sticky="w")




janela.mainloop() # sempre ficar no final ja que mantem tudo acima aberto tipo while true





