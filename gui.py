import tkinter as tk
from tkinter import ttk, messagebox
from estoque import Estoque

class EstoqueGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Estoque de Materiais de Construção")
        self.root.geometry("700x500")

        self.sistema = Estoque()

        # Layout Principal
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Área de Formulário (Topo) ---
        self.form_frame = ttk.LabelFrame(self.main_frame, text="Cadastro / Edição", padding="10")
        self.form_frame.pack(fill=tk.X, pady=(0, 20))

        # Grid do Formulário
        ttk.Label(self.form_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.ent_nome = ttk.Entry(self.form_frame)
        self.ent_nome.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(self.form_frame, text="Qtd:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.ent_qtd = ttk.Entry(self.form_frame, width=10)
        self.ent_qtd.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)

        ttk.Label(self.form_frame, text="Preço:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.ent_preco = ttk.Entry(self.form_frame)
        self.ent_preco.grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(self.form_frame, text="Categoria:").grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
        self.ent_cat = ttk.Entry(self.form_frame)
        self.ent_cat.grid(row=1, column=3, padx=5, pady=5, sticky=tk.EW)

        self.btn_add = ttk.Button(self.form_frame, text="Adicionar/Atualizar", command=self.adicionar)
        self.btn_add.grid(row=2, column=0, columnspan=4, pady=10)

        self.form_frame.columnconfigure(1, weight=1)
        self.form_frame.columnconfigure(3, weight=1)

        # --- Área da Tabela (Meio) ---
        self.table_frame = ttk.Frame(self.main_frame)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ('nome', 'quantidade', 'preco', 'categoria')
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show='headings')

        self.tree.heading('nome', text='Nome')
        self.tree.heading('quantidade', text='Qtd')
        self.tree.heading('preco', text='Preço (R$)')
        self.tree.heading('categoria', text='Categoria')

        self.tree.column('nome', width=200)
        self.tree.column('quantidade', width=80, anchor=tk.CENTER)
        self.tree.column('preco', width=100, anchor=tk.CENTER)
        self.tree.column('categoria', width=150)

        # Scrollbar para a tabela
        self.scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # --- Área de Ações (Baixo) ---
        self.actions_frame = ttk.Frame(self.main_frame, padding="10")
        self.actions_frame.pack(fill=tk.X)

        self.btn_entrada = ttk.Button(self.actions_frame, text="Entrada (+)", command=lambda: self.movimentar(1))
        self.btn_entrada.pack(side=tk.LEFT, padx=5)

        self.btn_saida = ttk.Button(self.actions_frame, text="Saída (-)", command=lambda: self.movimentar(-1))
        self.btn_saida.pack(side=tk.LEFT, padx=5)

        self.btn_remover = ttk.Button(self.actions_frame, text="Remover Item", command=self.remover)
        self.btn_remover.pack(side=tk.RIGHT, padx=5)

        self.atualizar_tabela()

    def atualizar_tabela(self):
        """Sincroniza a Treeview com os dados do Estoque."""
        # Limpa a tabela
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Popula com dados atuais
        produtos = self.sistema.listar_produtos()
        for nome, info in produtos.items():
            self.tree.insert('', tk.END, values=(
                nome,
                info['quantidade'],
                f"{info['preco']:.2f}",
                info['categoria']
            ))

    def adicionar(self):
        nome = self.ent_nome.get().strip()
        try:
            qtd = int(self.ent_qtd.get())
            preco = float(self.ent_preco.get())
            cat = self.ent_cat.get().strip()

            if not nome or not cat:
                raise ValueError("Nome e Categoria são obrigatórios.")

            self.sistema.adicionar_produto(nome, qtd, preco, cat)
            self.atualizar_tabela()
            self.limpar_campos()
            messagebox.showinfo("Sucesso", f"Material '{nome}' atualizado!")
        except ValueError as e:
            messagebox.showerror("Erro de Entrada", f"Dados inválidos: {e}")

    def movimentar(self, direcao):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Por favor, selecione um item na tabela.")
            return

        item_values = self.tree.item(selected[0])['values']
        nome = item_values[0]

        try:
            # Abre uma janelinha simples para perguntar a quantidade
            # Para simplificar, vamos usar um diálogo de entrada
            qtd_str = self.pedir_quantidade(f"Quantidade de {direcao if direcao==1 else 'saída'} para {nome}:")
            if qtd_str is None: return

            qtd = int(qtd_str)
            if qtd <= 0:
                messagebox.showerror("Erro", "A quantidade deve ser maior que zero.")
                return

            delta = qtd if direcao == 1 else -qtd
            sucesso, msg = self.sistema.atualizar_quantidade(nome, delta)

            if sucesso:
                self.atualizar_tabela()
                messagebox.showinfo("Sucesso", "Estoque atualizado!")
            else:
                messagebox.showerror("Erro", msg)

        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um número inteiro válido.")

    def remover(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione um item para remover.")
            return

        nome = self.tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirmação", f"Tem certeza que deseja remover {nome} do sistema?"):
            if self.sistema.remover_produto(nome):
                self.atualizar_tabela()
                messagebox.showinfo("Sucesso", "Item removido!")
            else:
                messagebox.showerror("Erro", "Não foi possível remover o item.")

    def limpar_campos(self):
        self.ent_nome.delete(0, tk.END)
        self.ent_qtd.delete(0, tk.END)
        self.ent_preco.delete(0, tk.END)
        self.ent_cat.delete(0, tk.END)

    def pedir_quantidade(self, titulo):
        """Cria uma janela pequena para input de quantidade."""
        janela = tk.Toplevel(self.root)
        janela.title("Quantidade")
        janela.geometry("250x120")
        janela.transient(self.root) # Fica na frente da principal
        janela.grab_set() # Bloqueia a principal até fechar esta

        ttk.Label(janela, text=titulo).pack(pady=10)
        ent = ttk.Entry(janela)
        ent.pack(pady=5)
        ent.focus_set()

        resultado = [None]

        def confirmar():
            resultado[0] = ent.get()
            janela.destroy()

        ttk.Button(janela, text="Confirmar", command=confirmar).pack(pady=10)

        self.root.wait_window(janela)
        return resultado[0]

if __name__ == "__main__":
    root = tk.Tk()
    app = EstoqueGUI(root)
    root.mainloop()
