import json
import os

class Estoque:
    def __init__(self, filename='estoque.json'):
        self.filename = filename
        self.produtos = self.carregar_dados()

    def carregar_dados(self):
        """Carrega os dados do arquivo JSON."""
        if not os.path.exists(self.filename):
            return {}
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            print("Erro ao ler o arquivo de dados. Iniciando estoque vazio.")
            return {}

    def salvar_dados(self):
        """Salva os dados atuais no arquivo JSON."""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.produtos, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Erro ao salvar dados: {e}")

    def adicionar_produto(self, nome, quantidade, preco, categoria):
        """Adiciona um novo produto ou atualiza a quantidade se já existir."""
        if nome in self.produtos:
            self.produtos[nome]['quantidade'] += quantidade
        else:
            self.produtos[nome] = {
                'quantidade': quantidade,
                'preco': preco,
                'categoria': categoria
            }
        self.salvar_dados()
        return True

    def remover_produto(self, nome):
        """Remove um produto do estoque."""
        if nome in self.produtos:
            del self.produtos[nome]
            self.salvar_dados()
            return True
        return False

    def atualizar_quantidade(self, nome, quantidade_delta):
        """
        Atualiza a quantidade de um produto.
        quantidade_delta positivo para entrada, negativo para saída.
        """
        if nome not in self.produtos:
            return False, "Produto não encontrado."

        nova_qtd = self.produtos[nome]['quantidade'] + quantidade_delta
        if nova_qtd < 0:
            return False, "Quantidade insuficiente em estoque."

        self.produtos[nome]['quantidade'] = nova_qtd
        self.salvar_dados()
        return True, "Quantidade atualizada com sucesso."

    def listar_produtos(self):
        """Retorna a lista de produtos formatada."""
        return self.produtos
