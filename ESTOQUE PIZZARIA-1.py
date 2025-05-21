from tabulate import tabulate
import os

ARQUIVO_ESTOQUE = "estoque.txt"

estoque = {
    "Frango": {"quantidade": "20 Kg", "preco": 50.00},
    "Queijos": {"quantidade": "10 Kg", "preco": 30.00, "tipo": ["Mussarela", "Provolone", "Cheddar"], "borda": "Catupiry"},
    "Opções de Molhos": {"quantidade": "10 Kg", "preco": 15.00, "tipo": ["Tradicional", "Picante", "Agridoce"], "borda": "Cheddar"},
    "Tipo de Massa": {"quantidade": "10 UNI", "preco": 25.00, "tipo": ["Tradicional", "Sem Glúten"], "borda": "Requeijão"},
    "Calabresa": {"quantidade": "7 Kg", "preco": 20.00, "tipo": ["Artesanal", "Defumada", "Pepperoni"], "borda": "Cream Cheese"},
    "Ingredientes Extras": {"quantidade": "5 Kg", "preco": 6.50, "tipo": ["Azeitona", "Milho", "Orégano", "Alho Frito"], "borda": "Sem Borda recheada"}
}

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def carregar_estoque():
    if not os.path.exists(ARQUIVO_ESTOQUE):
        return
    with open(ARQUIVO_ESTOQUE, "r", encoding="utf-8") as f:
        for linha in f:
            partes = linha.strip().split("|")
            if len(partes) == 5:
                nome, quantidade, preco, tipo_str, borda = partes
                tipo_lista = tipo_str.split(", ") if tipo_str else []
                estoque[nome] = {
                    "quantidade": quantidade,
                    "preco": float(preco)
                }
                if tipo_lista:
                    estoque[nome]["tipo"] = tipo_lista
                if borda:
                    estoque[nome]["borda"] = borda

def salvar_estoque():
    with open(ARQUIVO_ESTOQUE, "w", encoding="utf-8") as f:
        for nome, dados in estoque.items():
            tipo_str = ", ".join(dados.get("tipo", []))
            borda = dados.get("borda", "")
            f.write(f"{nome}|{dados['quantidade']}|{dados['preco']:.2f}|{tipo_str}|{borda}\n")

def mostrar_estoque():
    print("\nEstoque Atual:")
    if not estoque:
        print("Estoque vazio.")
    else:
        tabela = [[
            nome,
            dados.get("quantidade", "-"),
            f"R$ {dados.get('preco', 0):.2f}",
            ", ".join(dados.get("tipo", [])) if dados.get("tipo") else "-",
            dados.get("borda", "-")
        ] for nome, dados in estoque.items()]
        print(tabulate(
            tabela,
            headers=["Ingrediente", "Quantidade", "Preço", "Tipo", "Borda"],
            tablefmt="grid",
            colalign=("center", "center", "center", "center", "center")
        ))
    input("\nPressione Enter para continuar...")
    limpar_tela()

def adicionar_item():
    while True:
        nome = input("Nome do ingrediente: ").strip().title()
        quantidade = input("Quantidade (ex: 10 KG, 5 UNI): ").strip().upper()

        try:
            preco = float(input("Preço (ex: 12.50): ").strip().replace(",", "."))
        except ValueError:
            print("Preço inválido.")
            continue

        tipo_raw = input("Tipos (se houver, separados por vírgula): ").strip()
        tipo_lista = [t.strip().title() for t in tipo_raw.split(",") if t.strip()] if tipo_raw else []

        borda = input("Borda (se houver): ").strip().title()
        borda = borda if borda else None

        estoque[nome] = {
            "quantidade": quantidade,
            "preco": preco,
        }
        if tipo_lista:
            estoque[nome]["tipo"] = tipo_lista
        if borda:
            estoque[nome]["borda"] = borda

        salvar_estoque()
        print(f"{nome} adicionado/atualizado com sucesso.")

        cont = input("Deseja adicionar outro item? (s/n): ").strip().lower()
        if cont != 's':
            break
    limpar_tela()

def remover_item():
    while True:
        nomes = input("Digite os nomes dos ingredientes a remover (separados por vírgula): ").strip().split(",")
        for nome in nomes:
            nome = nome.strip().title()
            if nome in estoque:
                del estoque[nome]
                print(f"{nome} removido com sucesso.")
            else:
                print(f"{nome} não encontrado.")
        salvar_estoque()
        cont = input("Deseja remover mais itens? (s/n): ").strip().lower()
        if cont != 's':
            break
    limpar_tela()

def escolher_opcao(nome_categoria):
    opcoes = estoque.get(nome_categoria, {}).get("tipo", [])
    if not opcoes:
        return None

    print(f"\nEscolha {nome_categoria.lower()}:")
    for i, opcao in enumerate(opcoes, 1):
        print(f"{i}. {opcao}")

    while True:
        escolha = input("Digite o número desejado: ").strip()
        if escolha.isdigit() and 1 <= int(escolha) <= len(opcoes):
            return opcoes[int(escolha) - 1]
        print("Opção inválida.")

def escolher_multiplos_ingredientes(nome_categoria):
    opcoes = estoque.get(nome_categoria, {}).get("tipo", [])
    escolhidos =[]
    if not opcoes:
        return escolhidos

    print(f"\nEscolha os {nome_categoria.lower()} (digite os números separados por vírgula):")
    for i, opcao in enumerate(opcoes, 1):
        print(f"{i}. {opcao}")

    while True:
        escolha = input("Digite os números: ").strip()
        numeros = [n.strip() for n in escolha.split(",") if n.strip().isdigit()]
        validos = [opcoes[int(n) - 1] for n in numeros if 1 <= int(n) <= len(opcoes)]
        if validos:
            return validos
        print("Entrada inválida. Tente novamente.")

def escolher_borda():
    bordas = sorted({dados.get("borda") for dados in estoque.values() if dados.get("borda")})
    if not bordas:
        return "Sem borda"

    print("\nEscolha a borda:")
    for i, borda in enumerate(bordas, 1):
        print(f"{i}. {borda}")

    while True:
        escolha = input("Número da borda: ").strip()
        if escolha.isdigit() and 1 <= int(escolha) <= len(bordas):
            return bordas[int(escolha) - 1]
        print("Opção inválida.")

def escolher_ingredientes_principais():
    opcoes = [nome for nome in estoque if nome not in ["Tipo de Massa", "Opções de Molhos", "Ingredientes Extras"]]
    print("\nEscolha os ingredientes principais (digite os números separados por vírgula):")
    for i, ingrediente in enumerate(opcoes, 1):
        print(f"{i}. {ingrediente}")

    while True:
        escolha = input("Digite os números: ").strip()
        numeros = [n.strip() for n in escolha.split(",") if n.strip().isdigit()]
        validos = [opcoes[int(n) - 1] for n in numeros if 1 <= int(n) <= len(opcoes)]
        if validos:
            return validos
        print("Entrada inválida. Tente novamente.")

def fazer_pedido():
    print("=== FAZER PEDIDO ===")
    massa = escolher_opcao("Tipo de Massa")
    molho = escolher_opcao("Opções de Molhos")
    ingredientes_escolhidos = escolher_ingredientes_principais()
    extras = escolher_multiplos_ingredientes("Ingredientes Extras")
    borda = escolher_borda()

    ingredientes_com_tipos = []
    total = 0

    for nome in ingredientes_escolhidos:
        tipo_escolhido = escolher_multiplos_ingredientes(nome)
        ingredientes_com_tipos.append(f"{nome} ({tipo_escolhido})")
        total += estoque[nome]["preco"]

    if massa:
        total += estoque["Tipo de Massa"]["preco"]
    if molho:
        total += estoque["Opções de Molhos"]["preco"]
    if extras:
        total += estoque["Ingredientes Extras"]["preco"] * len(extras)

    print("\n=== RESUMO DO PEDIDO ===\n")
    tabela = [
        ["Massa", massa or "-"],
        ["Molho", molho or "-"],
        ["Ingredientes", ", ".join(ingredientes_com_tipos) if ingredientes_com_tipos else "-"],
        ["Extras", ", ".join(extras) if extras else "-"],
        ["Borda", borda or "-"],
        ["Total Estimado", f"R$ {total:.2f}"]
    ]
    print(tabulate(tabela, headers=["Item", "Escolha"], tablefmt="fancy_grid", colalign=("center", "center")))
    input("\nPressione Enter para voltar ao menu...")
    limpar_tela()

def menu():
    carregar_estoque()
    limpar_tela()
    while True:
        print("==== ESTOQUE PIZZARIA ====")
        print("1. Ver estoque")
        print("2. Adicionar item")
        print("3. Remover item")
        print("4. Fazer pedido")
        print("5. Encerrar programa")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            limpar_tela()
            mostrar_estoque()
        elif opcao == "2":
            limpar_tela()
            adicionar_item()
        elif opcao == "3":
            limpar_tela()
            remover_item()
        elif opcao == "4":
            limpar_tela()
            fazer_pedido()
        elif opcao == "5":
            print("Encerrando o programa. Até logo!")
            break
        else:
            print("Opção inválida.")
            input("\nPressione Enter para continuar...")
            limpar_tela()

menu()
