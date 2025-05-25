import time
import os
import random
import json

vidas = 3
nivel = 1
max_niveis = 50
inventario = []

# Arquivo para salvar progresso
save_file = "cursr_save.json"

def limpar_tela():
    os.system('clear')

def suspense():
    for _ in range(3):
        print(".", end='', flush=True)
        time.sleep(0.3)
    print()

def caveira():
    print("""
       .-''''-.
     .'        '.
    /            \\
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
    print(f"\033[1;31mVocê perdeu uma vida!\033[m Vidas restantes: {vidas}")
    if vidas <= 0:
        print("=== GAME OVER ===")
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
            print("\033[1;32mProgresso carregado com sucesso!\033[m")
    except FileNotFoundError:
        print("Nenhum progresso salvo encontrado. Iniciando novo jogo.")

def escolha(msg, opcoes):
    print(msg)
    for i, opcao in enumerate(opcoes, 1):
        print(f"\033[1;32m{i}) {opcao}\033[m")
    while True:
        opcao = input("Escolha: ")
        if opcao in [str(i) for i in range(1, len(opcoes)+1)]:
            return int(opcao)
        else:
            print("Escolha inválida.")

def adicionar_item(item):
    inventario.append(item)
    print(f"\033[1;34mVocê encontrou: {item}\033[m")

def fase(nivel):
    limpar_tela()
    print(f"\033[1;35m=== NÍVEL {nivel} ===\033[m")
    
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
    print(evento)
    suspense()
    
    opcao = escolha("O que você faz?", opcoes)

    # Consequências variadas
    if "chave" in evento and opcao == 1:
        adicionar_item("Chave enferrujada")
    elif "porta" in evento:
        if opcao == 1 and random.random() < 0.4:
            print("A porta quebrou e você se feriu!")
            perdeu_vida()
    elif "figura" in evento:
        if opcao == 1:
            print("A figura era hostil!")
            perdeu_vida()
        else:
            print("Você se esconde com sucesso.")
    elif "kit médico" in evento:
        if opcao == 1:
            global vidas
            vidas += 1
            print(f"\033[1;32mVocê recuperou uma vida! Vidas: {vidas}\033[m")
        else:
            adicionar_item("Kit Médico")
    else:
        if random.random() < 0.2:
            print("Um perigo inesperado te feriu!")
            perdeu_vida()
        else:
            print("Você passou sem problemas.")

    time.sleep(1)
    salvar_progresso()

def final():
    limpar_tela()
    print(f"\033[1;33mVocê sobreviveu até o final com {vidas} vida(s) restante(s)!\033[m")
    print("=== PARABÉNS, VENCEDOR! ===")
    print("=== SEU INVENTÁRIO ===")
    for item in inventario:
        print(f" - {item}")
    print("=== SEU RANK ===")
    print(f"Níveis concluídos: {nivel-1}/{max_niveis}")
    caveira()
    salvar_progresso()
    exit()

def main():
    limpar_tela()
    caveira()
    carregar = escolha("Deseja carregar o progresso salvo?", ["Sim", "Não"])
    if carregar == 1:
        carregar_progresso()
    else:
        print("Novo jogo iniciado.")
    time.sleep(2)

    global nivel
    while nivel <= max_niveis:
        fase(nivel)
        nivel += 1
    final()

if __name__ == "__main__":
    main()
