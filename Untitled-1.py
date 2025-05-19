from tabulate import tabulate
import os

ARQUIVO_ESTOQUE = "estoque.txt"

# Formato correto do estoque:
estoque = {
    "Queijo": {"quantidade": "10 Kg", "preco": 30.00},
    "Molho De Tomate": {"quantidade": "10 Kg", "preco": 15.00},
    "Massa De Pizza": {"quantidade": "10 UNI", "preco": 25.00},
    "Calabresa": {"quantidade": "7 Kg", "preco": 20.00},
    "Azeitona": {"quantidade": "5 Kg", "preco": 12.00}
}

def carregar_estoque():
    if not os.path.exists(ARQUIVO_ESTOQUE):
        return
    with open(ARQUIVO_ESTOQUE, "r", encoding="utf-8") as f:
        for linha in f:
            partes = linha.strip().split("|")
            if len(partes) == 3:
                ingrediente, quantidade, preco = partes
                estoque[ingrediente] = {"quantidade": quantidade, "preco": float(preco)}

def salvar_estoque():
    with open(ARQUIVO_ESTOQUE, "w", encoding="utf-8") as f:
        for ingrediente, dados in estoque.items():
            f.write(f"{ingrediente}|{dados['quantidade']}|{dados['preco']:.2f}\n")

def mostrar_estoque():
    print("\nEstoque Atual:")
    if not estoque:
        print("Estoque vazio.")
        return
    tabela = [[ingrediente, dados["quantidade"], f"R$ {dados['preco']:.2f}"]
              for ingrediente, dados in estoque.items()]
    print(tabulate(tabela, headers=["Ingrediente", "Quantidade", "Preço"], tablefmt="grid"))

def adicionar_item():
    ingrediente = input("Nome do ingrediente a adicionar: ").strip().title()
    quantidade = input("Quantidade (ex: 5KG ou 10 UNI): ").strip().upper()
    try:
        preco = float(input("Preço (ex: 12.50): ").strip().replace(",", "."))
    except ValueError:
        print("Preço inválido.")
        return
    estoque[ingrediente] = {"quantidade": quantidade, "preco": preco}
    salvar_estoque()
    print(f"{ingrediente} adicionado/atualizado com {quantidade} por R$ {preco:.2f}.")

def remover_item():
    ingrediente = input("Nome do ingrediente a remover: ").strip().title()
    if ingrediente in estoque:
        del estoque[ingrediente]
        salvar_estoque()
        print(f"{ingrediente} removido do estoque.")
    else:
        print(f"{ingrediente} não encontrado no estoque.")

def menu():
    carregar_estoque()
    while True:
        print("\n==== ESTOQUE PIZZARIA ====")
        print("1. Ver estoque")
        print("2. Adicionar item")
        print("3. Remover item")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            mostrar_estoque()
        elif opcao == "2":
            adicionar_item()
        elif opcao == "3":
            remover_item()
        elif opcao == "4":
            print("Finalizando o programa...")
            break
        else:
            print("Opção inválida. Tente novamente.")

menu()