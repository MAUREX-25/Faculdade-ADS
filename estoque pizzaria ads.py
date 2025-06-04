from tabulate import tabulate
import os

ARQUIVO_ESTOQUE = "estoque.txt"

estoque = {
    1: {"nome": "Frango", "quantidade": "20 Kg", "preco": 50.00},
    2: {"nome": "Queijos", "quantidade": "10 Kg", "preco": 30.00, "tipo": ["Mussarela", "Provolone", "Cheddar"], "borda": "Catupiry"},
    3: {"nome": "Opções de Molhos", "quantidade": "10 Kg", "preco": 15.00, "tipo": ["Tradicional", "Picante", "Agridoce"], "borda": "Cheddar"},
    4: {"nome": "Tipo de Massa", "quantidade": "10 UNI", "preco": 25.00, "tipo": ["Tradicional", "Sem Glúten"], "borda": "Requeijão"},
    5: {"nome": "Calabresa", "quantidade": "7 Kg", "preco": 20.00, "tipo": ["Artesanal", "Defumada", "Pepperoni"], "borda": "Cream Cheese"},
    6: {"nome": "Ingredientes Extras", "quantidade": "5 Kg", "preco": 6.50, "tipo": ["Azeitona", "Milho", "Orégano", "Alho Frito"], "borda": "Sem Borda recheada"}
}

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def carregar_estoque():
    if not os.path.exists(ARQUIVO_ESTOQUE):
        return
    with open(ARQUIVO_ESTOQUE, "r", encoding="utf-8") as f:
        for linha in f:
            partes = linha.strip().split("|")
            if len(partes) == 6:
                id_str, nome, quantidade, preco, tipo_str, borda = partes
                id_item = int(id_str)
                tipo_lista = tipo_str.split(", ") if tipo_str else []
                estoque[id_item] = {
                    "nome": nome,
                    "quantidade": quantidade,
                    "preco": float(preco)
                }
                if tipo_lista:
                    estoque[id_item]["tipo"] = tipo_lista
                if borda and borda != "-":
                    estoque[id_item]["borda"] = borda

def salvar_estoque():
    with open(ARQUIVO_ESTOQUE, "w", encoding="utf-8") as f:
        for id_item, dados in estoque.items():
            tipo_str = ", ".join(dados.get("tipo", []))
            borda = dados.get("borda", "-")
            f.write(f"{id_item}|{dados['nome']}|{dados['quantidade']}|{dados['preco']:.2f}|{tipo_str}|{borda}\n")

def mostrar_estoque():
    print("\nEstoque Atual:")
    if not estoque:
        print("Estoque vazio.")
    else:
        tabela = [[
            id_item,
            dados["nome"],
            dados.get("quantidade", "-"),
            f"R$ {dados.get('preco', 0):.2f}",
            ", ".join(dados.get("tipo", [])) if dados.get("tipo") else "-",
            dados.get("borda", "-")
        ] for id_item, dados in estoque.items()]
        print(tabulate(
            tabela,
            headers=["ID", "Ingrediente", "Quantidade", "Preço", "Tipo", "Borda"],
            tablefmt="grid",
            colalign=("center", "center", "center", "center", "center", "center")
        ))
    input("\nPressione Enter para continuar...")
    limpar_tela()

def validar_quantidade(quantidade_str):
    partes = quantidade_str.strip().split(maxsplit=1)
    if not partes:
        return False
    numero = partes[0].replace(",", ".")
    try:
        float(numero)
        return True
    except ValueError:
        return False

def adicionar_item():
    while True:
        nome = input("Nome do ingrediente: ").strip().title()
        while True:
            quantidade = input("Quantidade (ex: 10 KG, 5 UNI): ").strip().upper()
            if validar_quantidade(quantidade):
                break
            print("Quantidade inválida. Digite um número seguido da unidade (ex: 10 KG)")

        try:
            preco = float(input("Preço (ex: 12.50): ").strip().replace(",", "."))
        except ValueError:
            print("Preço inválido.")
            continue

        tipo_raw = input("Tipos (se houver, separados por vírgula): ").strip()
        tipo_lista = [t.strip().title() for t in tipo_raw.split(",") if t.strip()] if tipo_raw else []

        borda = input("Borda (se houver): ").strip().title()
        borda = borda if borda else "-"

        novo_id = max(estoque.keys(), default=0) + 1

        estoque[novo_id] = {
            "nome": nome,
            "quantidade": quantidade,
            "preco": preco,
        }
        if tipo_lista:
            estoque[novo_id]["tipo"] = tipo_lista
        if borda and borda != "-":
            estoque[novo_id]["borda"] = borda

        salvar_estoque()
        print(f"{nome} adicionado/atualizado com sucesso (ID: {novo_id}).")

        cont = input("Deseja adicionar outro item? (s/n): ").strip().lower()
        if cont != 's':
            break
    limpar_tela()

def remover_item():
    while True:
        ids_str = input("Digite os IDs dos ingredientes a remover (separados por vírgula): ").strip()
        ids = [int(i.strip()) for i in ids_str.split(",") if i.strip().isdigit()]
        for id_item in ids:
            if id_item in estoque:
                nome = estoque[id_item]["nome"]
                del estoque[id_item]
                print(f"{nome} (ID: {id_item}) removido com sucesso.")
            else:
                print(f"ID {id_item} não encontrado.")
        salvar_estoque()
        cont = input("Deseja remover mais itens? (s/n): ").strip().lower()
        if cont != 's':
            break
    limpar_tela()

def escolher_opcao(nome_categoria):
    for id_item, dados in estoque.items():
        if dados["nome"] == nome_categoria:
            opcoes = dados.get("tipo", [])
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
    return None

def escolher_multiplos_ingredientes(nome_categoria):
    for id_item, dados in estoque.items():
        if dados["nome"] == nome_categoria and "tipo" in dados:
            opcoes = dados["tipo"]
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
    return []

def escolher_borda():
    bordas = sorted({dados.get("borda") for dados in estoque.values() if dados.get("borda") and dados["borda"] != "-"})
    if not bordas:
        return "Sem borda"

    print("\nEscolha a borda:")
    print("0. Sem borda")
    for i, borda in enumerate(bordas, 1):
        print(f"{i}. {borda}")

    while True:
        escolha = input("Número da borda: ").strip()
        if escolha == "0":
            return "Sem borda"
        elif escolha.isdigit() and 1 <= int(escolha) <= len(bordas):
            return bordas[int(escolha) - 1]
        print("Opção inválida.")

def escolher_ingredientes_principais():
    opcoes = [(id_item, dados["nome"]) for id_item, dados in estoque.items() if dados["nome"] not in ["Tipo de Massa", "Opções de Molhos", "Ingredientes Extras"]]
    print("\nEscolha os ingredientes principais (digite os números separados por vírgula):")
    for i, (id_item, nome) in enumerate(opcoes, 1):
        print(f"{i}. {nome}")
    while True:
        escolha = input("Digite os números: ").strip()
        numeros = [n.strip() for n in escolha.split(",") if n.strip().isdigit()]
        validos = [opcoes[int(n) - 1][0] for n in numeros if 1 <= int(n) <= len(opcoes)]
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

    for id_item in ingredientes_escolhidos:
        nome = estoque[id_item]["nome"]
        if "tipo" in estoque[id_item]:
            tipo_escolhido = escolher_multiplos_ingredientes(nome)
            ingredientes_com_tipos.append(f"{nome} ({', '.join(tipo_escolhido)})")
        else:
            ingredientes_com_tipos.append(nome)
        total += estoque[id_item]["preco"]

    if massa:
        for id_item, dados in estoque.items():
            if dados["nome"] == "Tipo de Massa":
                total += dados["preco"]
                break
    if molho:
        for id_item, dados in estoque.items():
            if dados["nome"] == "Opções de Molhos":
                total += dados["preco"]
                break
    if extras:
        for id_item, dados in estoque.items():
            if dados["nome"] == "Ingredientes Extras":
                total += dados["preco"] * len(extras)
                break

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

if __name__ == "__main__":
    menu()