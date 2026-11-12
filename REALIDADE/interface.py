# Arquivo para cuidar da interface
import tkinter
from tkinter import ttk, messagebox # TK com temas para ficar mais bonito
import sistema # para fazer o sistema.estoque
from sistema import CATEGORIAS, adicionar_produto, salvar_dados, ler_arquivo, controle_estoque

janela = tkinter.Tk()
janela.title("Depósito de Materiais de Construção")
janela.geometry("1000x800")

label_titutlo = tkinter.Label(
    janela, text="Sistema de Controle de Estoque", font=("Arial", 16, "bold") # tupla pra informar a fonte, tamanho e bold para negrito
)
label_titutlo.pack(pady=20)  # pack serve para fixar a janela na tela ; e pady=20 dá um espaço em cima e embaixo

janela_cadastro = ttk.LabelFrame(janela, text=" Cadastro de Material ")
janela_cadastro.pack(fill="x", padx=20, pady=10)

janela_movimentacao = ttk.LabelFrame(janela, text="Movimentação de estoque (Entrada / Saída)")
janela_movimentacao.pack(fill="x", padx=20, pady=10)

#ID movimentado
label_mov_id = ttk.Label(janela_movimentacao, text="ID do Material:")
label_mov_id.grid(row=0, column=0, padx=10, pady=5, sticky="w")

texto_mov_id = ttk.Entry(janela_movimentacao, width=10)
texto_mov_id.grid(row=0, column=1, padx=5, pady=5, sticky="w")

# Quantidade que está entrando ou saindo
label_mov_qtd = ttk.Label(janela_movimentacao, text="Quantidade:")
label_mov_qtd.grid(row=0, column=2, padx=10, pady=5, sticky="w")
texto_mov_qtd = ttk.Entry(janela_movimentacao, width=12)
texto_mov_qtd.grid(row=0, column=3, padx=5, pady=5, sticky="w")

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

texto_categoria = ttk.Combobox(janela_cadastro, values=CATEGORIAS, state="readonly", width=15) # combobox = caixa de escolha e readonly para o usuario nao alterar
texto_categoria.grid(row=1, column=1, padx=10, pady=5, sticky="w")

label_quantidade = ttk.Label(janela_cadastro, text="Quantidade:")
label_quantidade.grid(row=1, column=2, padx=10, pady=5, sticky="w")

texto_quantidade = ttk.Entry(janela_cadastro, width=12)
texto_quantidade.grid(row=1, column=3, padx=10, pady=5, sticky="w")

# Linha 2 para o preço
label_preco = ttk.Label(janela_cadastro, text="Preço Unitário (R$):")
label_preco.grid(row=2, column=0, padx=10, pady=5, sticky="w")

texto_preco = ttk.Entry(janela_cadastro, width=15)
texto_preco.grid(row=2, column=1, padx=10, pady=5, sticky="w")



# Notificação específica da movimentação
label_notificacao_mov = tkinter.Label(janela_movimentacao, text="", font=("Arial", 10, "italic"))
label_notificacao_mov.grid(row=1, column=0, columnspan=6, pady=5)

def mostrar_notificacao(mensagem, cor="green"):
    label_notificacao.config(text=mensagem, fg=cor)
    # Depois de 3500ms ou 3,5 segundos
    janela.after(3500, lambda: label_notificacao.config(text=""))

#Agora tem que criar a função callback para interagir como um intermediador com o sistema

def realizar_cadastro():
    id_digitado = texto_id.get()
    nome_digitado = texto_nome.get()
    categoria_digitada = texto_categoria.get()
    quantidade_digitada = texto_quantidade.get()
    preco_digitado = texto_preco.get()

    if not id_digitado or not nome_digitado or not categoria_digitada or not quantidade_digitada or not preco_digitado:
        mostrar_notificacao("Preencha todos os campos obrigatórios!", cor="red")
        return

    # 2. Converte quantidade e preço com segurança (evita travar se digitarem texto)
    try:
        quantidade_convertida = int(quantidade_digitada)
        preco_convertido = float(preco_digitado.replace(",","."))
    except ValueError:
        mostrar_notificacao("Quantidade e Preço devem ser numéricos!", cor="red")
        return
    
    sucesso = adicionar_produto(id_digitado,nome_digitado,categoria_digitada,quantidade_convertida,preco_convertido)
    # Adiconar agora na memoria
    if sucesso:
        salvar_dados()
        atualizar_tabela()

        mostrar_notificacao(f"✓ Material '{nome_digitado}' cadastrado com sucesso!", cor="green")

        #Limpar os campos da tela
        texto_id.delete(0, "end")
        texto_nome.delete(0, "end")
        texto_categoria.set("")
        texto_quantidade.delete(0, "end")
        texto_preco.delete(0, "end")
    else:
       mostrar_notificacao("Alguma informação inválida, revise os campos!", cor="red")

def mostrar_notificacao_mov(mensagem, cor="green"):
    label_notificacao_mov.config(text=mensagem, fg=cor)
    janela.after(3500, lambda: label_notificacao_mov.config(text=""))

def movimentar(tipo):
    id_digitado = texto_mov_id.get().strip()
    quantidade_digitada = texto_mov_qtd.get().strip()

    if not id_digitado or not quantidade_digitada:
        mostrar_notificacao_mov("Preencha o ID e a Quantidade!", cor="red")
        return
    try: 
        quantidade_movimentada = int(quantidade_digitada)
        if quantidade_movimentada <= 0:
            mostrar_notificacao_mov("A quantidade deve ser maior que 0!", cor="red")
            return
    except ValueError:
        mostrar_notificacao_mov("A quantidade deve ser um valor inteiro!", cor="red")
        return

    # AGORA PARA SAÍDA, invertemos o sinal para subtrair
    fator = 1 if tipo == "entrada" else -1
    quantidade_final = quantidade_movimentada * fator

    sucesso = controle_estoque(id_digitado, quantidade_final)
    if sucesso:
        atualizar_tabela()
        texto_mov_id.delete(0, "end")
        texto_mov_qtd.delete(0, "end")
        acao = "adicionadas" if tipo == "entrada" else "retiradas"
        mostrar_notificacao_mov(f"✓ Sucesso! {quantidade_movimentada} unidades {acao}.", cor="green")
    else:
        mostrar_notificacao_mov("❌ Falha: ID não existe ou estoque insuficiente!", cor="red")

def dar_entrada():
    movimentar("entrada")
def dar_saida():
    movimentar("saida")
    
# Botão Entrada
botao_entrada = ttk.Button(janela_movimentacao, text="Entrada", command=dar_entrada)
botao_entrada.grid(row=0, column=4, padx=10, pady=5)
# Botão Saída
botao_saida = ttk.Button(janela_movimentacao, text="Baixa / Saída", command=dar_saida)
botao_saida.grid(row=0, column=5, padx=10, pady=5)

botao_cadastrar = ttk.Button(janela_cadastro, text="Cadastro de Material", command=realizar_cadastro)
botao_cadastrar.grid(row=3, column=2, columnspan=2, padx=10, pady=10)
#o columspan da uma largura ao botao

label_notificacao = tkinter.Label(janela_cadastro, text="", font=("Arial", 10, "italic"))
label_notificacao.grid(row=4, column=0, columnspan=4, pady=5)



# Fazer a tabela para ver o estoque, usar o Treeview

quadro_tabela = ttk.LabelFrame(janela, text=" Estoque de Materiais ")
quadro_tabela.pack(fill="both", expand=True, padx=20, pady=10)
# o Fill = both enche toda a linha para criar proxima

# PAINEL DE BUSCAR / FILTRO (fica no topo da tabela)
painel_filtros = ttk.Frame(quadro_tabela)
painel_filtros.pack(fill="x", padx=5, pady=5)

# Campo de Busca (Nome ou ID)
label_busca = ttk.Label(painel_filtros, text="Buscar (Nome ou ID):")
label_busca.grid(row=0, column=0, padx=5, pady=5, sticky="w")

texto_busca = ttk.Entry(painel_filtros, width=20)
texto_busca.grid(row=0, column=1, padx=5, pady=5)

# Filtro por Categoria
label_filtro_cat = ttk.Label(painel_filtros, text="Categoria:")
label_filtro_cat.grid(row=0, column=2, padx=5, pady=5, sticky="w")

# Tupla com 'Todas' + as categorias existentes
opcoes_categorias = ("Todas",) + CATEGORIAS
combobox_filtro_categoria = ttk.Combobox(painel_filtros, values=opcoes_categorias, state="readonly", width=14)
combobox_filtro_categoria.set("Todas") # Começa com Todas
combobox_filtro_categoria.grid(row=0, column=3, padx=5, pady=5)

def filtrar_tabela():
    termo = texto_busca.get().strip().lower()
    categoria_selecionada = combobox_filtro_categoria.get()

    # Limpa as linhas atuais da tabela
    for item in tabela.get_children():
        tabela.delete(item)

    # Percorre o estoque aplicando as condições
    for produto in sistema.estoque:
        # 1. Checa se o termo está no ID ou no Nome
        bate_busca = (not termo) or (termo in produto["nome"].lower()) or (termo == str(produto["id"]).lower())
        
        # 2. Checa se bate com a categoria
        bate_categoria = (categoria_selecionada == "Todas" or categoria_selecionada == "") or (produto["categoria"] == categoria_selecionada)

        if bate_busca and bate_categoria:
            tabela.insert("", "end", values=(
                produto["id"],
                produto["nome"],
                produto["categoria"],
                produto["quantidade"],
                f"R$ {produto['preco']:.2f}"
            ))

def limpar_filtro():
    texto_busca.delete(0, "end")
    combobox_filtro_categoria.set("Todas")
    atualizar_tabela() # Mostra todos novamente

# Botões
botao_filtrar = ttk.Button(painel_filtros, text="🔍 Filtrar", command=filtrar_tabela)
botao_filtrar.grid(row=0, column=4, padx=5, pady=5)

botao_limpar_filtro = ttk.Button(painel_filtros, text="🔄 Mostrar Todos", command=limpar_filtro)
botao_limpar_filtro.grid(row=0, column=5, padx=5, pady=5)

colunas = ("id", "nome", "categoria", "quantidade", "preco")
tabela = ttk.Treeview(quadro_tabela, columns=colunas, show="headings")
# Configurando o heading = titulo de cada coluna
tabela.heading("id", text="ID")
tabela.heading("nome", text="Nome do Material")
tabela.heading("categoria", text="Categoria")
tabela.heading("quantidade", text="Quantidade")
tabela.heading("preco", text="Preço (R$)")
# Configurando a largura de cada coluna
tabela.column("id", width=50, anchor="center")
tabela.column("nome", width=250)
tabela.column("categoria", width=120, anchor="center")
tabela.column("quantidade", width=90, anchor="center")
tabela.column("preco", width=100, anchor="center")
tabela.pack(fill="both", expand=True, padx=5, pady=5)

def atualizar_tabela():
    # 1. limpar as linhas antigas
    for item in tabela.get_children(): # get_children é pegar os IDs que a Treeview gera a cada linha ex: 'I001', 'I002'
        tabela.delete(item)

    # 2. inserir cada produto no estoque da tabela
    for produto in sistema.estoque:
        tabela.insert("", "end", values=( 
            # Usar insert inves de apend porque tabela não é uma lista, é um componente gráfico
            produto["id"],
            produto["nome"],
            produto["categoria"],
            produto["quantidade"],
            f"R$ {produto['preco']:.2f}"
        ))


ler_arquivo()
atualizar_tabela()
janela.mainloop() # sempre ficar no final ja que mantem tudo acima aberto tipo while true




