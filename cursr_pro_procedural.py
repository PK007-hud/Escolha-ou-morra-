import time
import os
import random
import json

vidas = 3
nivel = 1
max_niveis = 50
inventario = ["Kit Médico", "Binóculos"]

save_file = "cursr_save.json"

def limpar_tela():
    os.system('clear')

def suspense():
    for _ in range(3):
        print(".", end='', flush=True)
        time.sleep(0.3)
    print()

def caveira():
    print(r"""
       .-''''-.
     .'        '.
    /            \
   |              |
   |,  .-.  .-.  ,|
   | )(_o/  \o_)( |
   |/     /\     \|
   (_     ^^     _)
    \__|IIIIII|__/
     | \IIIIII/ |
     \          /
      `--------`
    """)

def perdeu_vida():
    global vidas
    vidas -= 1
    print(f"\033[1;31mVocê perdeu uma vida!\033[m Vidas restantes: {vidas}", flush=True)
    if vidas <= 0:
        print("=== GAME OVER ===", flush=True)
        salvar_progresso()
        exit()
    time.sleep(1)

def salvar_progresso():
    data = {
        "vidas": vidas,
        "nivel": nivel,
        "inventario": inventario
    }
    with open(save_file, 'w') as f:
        json.dump(data, f)

def carregar_progresso():
    global vidas, nivel, inventario
    try:
        with open(save_file, 'r') as f:
            data = json.load(f)
            vidas = data["vidas"]
            nivel = data["nivel"]
            inventario = data["inventario"]
            print("\033[1;32mProgresso carregado com sucesso!\033[m", flush=True)
    except FileNotFoundError:
        print("Nenhum progresso salvo encontrado. Iniciando novo jogo.", flush=True)

def escolha(msg, opcoes):
    print(msg, flush=True)
    for i, opcao in enumerate(opcoes, 1):
        print(f"\033[1;32m{i}) {opcao}\033[m", flush=True)
    print("\033[1;33mDigite 'inv' para abrir o inventário a qualquer momento.\033[m", flush=True)
    while True:
        opcao = input("Escolha: ")
        if opcao.lower() == "inv":
            abrir_inventario()
            continue
        if opcao in [str(i) for i in range(1, len(opcoes)+1)]:
            return int(opcao)
        else:
            print("Escolha inválida.", flush=True)

def abrir_inventario():
    print("\033[1;36m=== INVENTÁRIO ===\033[m", flush=True)
    for item in inventario:
        print(f" - {item}", flush=True)
    print("===================", flush=True)
    usar = input("Quer usar algum item? (sim/não): ").strip().lower()
    if usar == "sim":
        item = input("Qual item quer usar? ").strip()
        usar_item(item)

def usar_item(item):
    global vidas
    if item not in inventario:
        print("Você não possui esse item.", flush=True)
        return
    if item.lower() == "kit médico":
        vidas += 1
        inventario.remove("Kit Médico")
        print(f"\033[1;32mVocê usou o Kit Médico e recuperou uma vida! Vidas: {vidas}\033[m", flush=True)
    elif item.lower() == "binóculos":
        print("Você usa os Binóculos para observar a área ao longe...", flush=True)
        time.sleep(1)
        print("Parece seguro ou perigoso, dependendo da situação!", flush=True)

def adicionar_item(item):
    inventario.append(item)
    print(f"\033[1;34mVocê encontrou: {item}\033[m", flush=True)

def fase(nivel):
    limpar_tela()
    print(f"\033[1;35m=== NÍVEL {nivel} ===\033[m", flush=True)

    eventos = [
        ("Você encontra uma chave enferrujada.", ["Pegar a chave", "Ignorar"]),
        ("Uma porta bloqueia seu caminho.", ["Forçar a porta", "Procurar outro caminho"]),
        ("Você vê uma figura ao longe.", ["Chamar por ajuda", "Se esconder"]),
        ("Há um lago profundo à frente.", ["Nadar através", "Dar a volta"]),
        ("Você ouve um grito assustador.", ["Investigar", "Correr para longe"]),
        ("Um velho livro está no chão.", ["Ler o livro", "Deixá-lo aí"]),
        ("Uma mochila abandonada está aqui.", ["Abrir", "Ignorar"]),
        ("O teto está desmoronando.", ["Correr rápido", "Se proteger atrás de um objeto"]),
        ("Há duas portas: uma vermelha e uma azul.", ["Entrar na vermelha", "Entrar na azul"]),
        ("Você encontra um kit médico.", ["Usar para recuperar vida", "Guardar para depois"]),
    ]

    evento, opcoes = random.choice(eventos)

    if "figura" in evento and "Binóculos" in inventario:
        usar = input("Quer usar os Binóculos para identificar? (sim/não): ").strip().lower()
        if usar == "sim":
            usar_item("binóculos")

    if "porta" in evento and "Chave enferrujada" in inventario:
        print("Você usa a Chave Enferrujada para destrancar a porta e passa sem problemas!", flush=True)
        return

    print(evento, flush=True)
    suspense()

    opcao = escolha("O que você faz?", opcoes)

    if "chave" in evento and opcao == 1:
        adicionar_item("Chave enferrujada")
    elif "porta" in evento:
        if opcao == 1:
            print("Você força a porta...", flush=True)
            if random.random() < 0.4:
                print("A porta quebrou e você se feriu!", flush=True)
                perdeu_vida()
            else:
                print("Você conseguiu forçar a porta sem se machucar.", flush=True)
    elif "figura" in evento:
        if opcao == 1:
            print("A figura era hostil!", flush=True)
            perdeu_vida()
        else:
            print("Você se esconde com sucesso.", flush=True)
    elif "kit médico" in evento:
        if opcao == 1:
            global vidas
            vidas += 1
            print(f"\033[1;32mVocê recuperou uma vida! Vidas: {vidas}\033[m", flush=True)
        else:
            adicionar_item("Kit Médico")
    else:
        if random.random() < 0.2:
            print("Um perigo inesperado te feriu!", flush=True)
            perdeu_vida()
        else:
            print("Você passou sem problemas.", flush=True)

    time.sleep(1)
    salvar_progresso()

def final():
    limpar_tela()
    print(f"\033[1;33mVocê sobreviveu até o final com {vidas} vida(s) restante(s)!\033[m", flush=True)
    print("=== PARABÉNS, VENCEDOR! ===", flush=True)
    print("=== SEU INVENTÁRIO ===", flush=True)
    for item in inventario:
        print(f" - {item}", flush=True)
    print("=== SEU RANK ===", flush=True)
    print(f"Níveis concluídos: {nivel-1}/{max_niveis}", flush=True)
    caveira()
    salvar_progresso()
    exit()

def main():
    limpar_tela()
    caveira()
    print("DEBUG: main entrou", flush=True)
    carregar = escolha("Deseja carregar o progresso salvo?", ["Sim", "Não"])
    print(f"DEBUG: Carregou = {carregar}", flush=True)
    if carregar == 1:
        carregar_progresso()
    else:
        print("Novo jogo iniciado.", flush=True)
    time.sleep(2)

    global nivel
    while nivel <= max_niveis:
        fase(nivel)
        nivel += 1
    final()

if __name__ == "__main__":
    main()
