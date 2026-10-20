
ARQUIVO_DADOS = "dados_estoque.txt"
CATEGORIAS = ("Alvenaria", "Elétrica", "Hidráulica", "Pintura", "Ferramentas") #Tuplas
estoque = [] # produtos ficarao aqui
import os #verificar se tem arquivo ou criar um novo

def salvar_dados():
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as database: # o "w" significa write e o with garante que feche o arquivo depois, encoding = utf-8 é para os acentos brasileiros
        for produto in estoque:
            linha = f"{produto['id']};{produto['nome']};{produto['categoria']};{produto['quantidade']};{produto['preco']}\n"
            database.write(linha)
        print("Dados salvos com sucesso no arquivo!")

def ler_arquivo():
    global estoque # transforma a lista estoque em global, ou seja serve para todas
    if not os.path.exists(ARQUIVO_DADOS):
        print("Arquivo de dados não encontrado. Criando um do zero.")
        return
    
    estoque = [] # para nao duplicar os dados 

    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as database: # 'r' = read ou seja ler        print("Dados carregados com sucesso."))
        for linha in database:
            linha_limpa = linha.strip()
            if linha_limpa:
                partes_do_produto = linha_limpa.split(";")
                produto = {
                    "id": partes_do_produto[0],
                    "nome": partes_do_produto[1],
                    "categoria": partes_do_produto[2],
                    "quantidade": int(partes_do_produto[3]),
                    "preco": float(partes_do_produto[4]),
                }
                estoque.append(produto)
    print("Dados carregados com sucesso apartir do arquivo .TXT")







#usar .strip para tirar espacos em branco e .title para melhorar a visualizacao com letras maisuculas
#def para indicar que se trata de uma funcao / subprograma
def adicionar_produto(id_produto, nome, categoria, quantidade, preco):
    if preco <=0 or quantidade <0:
        print("Erro! Preço deve ser maior que 0 ou quantidade está menor que 0")
        return False
    
    nome_arrumado = nome.strip().title()
    produto = {
        "id": id_produto,
        "nome": nome_arrumado,
        "categoria": categoria,
        "quantidade": int(quantidade),
        "preco": float(preco),
    }
    estoque.append(produto)
    print(f"Produto '{nome_arrumado}' foi adicionado com sucesso!")
    return True

# Agora funcao para listar o estoque todo
def listar_estoque():
    if len(estoque) < 1:
        print("Erro! Estoque está vazio, cadastre um produto antes.")
        return False
    else:
        for produto in estoque:
            print(f"ID: {produto['id']} | Nome: {produto['nome']} || Categoria: {produto['categoria']} || Qtd: {produto['quantidade']} || Preço: R$ {produto['preco']:.2f}")

def controle_estoque(id_produto, quantidade_movimentada):
    for produto in estoque:
        if produto['id'] == str(id_produto):
            nova_quantidade = produto['quantidade'] + quantidade_movimentada
            if nova_quantidade < 0:
                print("Erro! Quantidade insuficiente no estoque")
                return False
            else:
                produto['quantidade'] = nova_quantidade
                salvar_dados()
                print(f"Estoque do  {produto['nome']} atualizado: {nova_quantidade} unidades")
                return True
    print(f"\nERRO: ID não encontrado, tente novamente\n")
    return False


def buscar_produto(item_buscado):
    item_buscado = item_buscado.lower()
    resultados = []
    for produto in estoque:
        if item_buscado in produto['nome'].lower():
            resultados.append(produto)
    return resultados





# 1. Adiciona um produto
adicionar_produto("1", "Saco de cimento", "Alvenaria", 14, 49.90)
adicionar_produto("2", "Argamassa", "Alvenaria", 14, 49.90)

# 2. Salva no TXT
salvar_dados()

# 3. Lê de volta do TXT para testar
ler_arquivo()

# 4. Mostra o estoque na tela
listar_estoque()


# Teste para entrada de saida de produtos
controle_estoque("1", -4)
listar_estoque()
# ver se da erro
controle_estoque("1", -50)
listar_estoque()

controle_estoque("1", 20)
listar_estoque()

busca = buscar_produto("cimento")
print("Resultado da busca por 'cimento':", busca)