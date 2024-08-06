import random
from tkinter import *
from tkinter import ttk
from pathlib import Path

ROOT_PATH = Path(__file__).parent

cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"] * 4
victories = 0
defeats = 0

game_history = []


# Salvar historico
def save_history(game_info):
    # Criando arquivo de historico
    file = ROOT_PATH / "historico.txt"
    if not file.exists():
        with open(file, "w", encoding="utf-8") as arquivo:
            arquivo.write("====== Historico de Partidas ======\n")
    with open(file, "a", encoding="utf-8") as arquivo:
        arquivo.write(game_info)


# Mostrar o historico
def show_history():
    if not game_history:  # Verifica se o histórico está vazio
        return

    history_window = Toplevel(root)
    history_window.title("Histórico de Jogos")
    history_window.geometry("400x300")

    history_text = Text(history_window, wrap=WORD)
    history_text.pack(expand=YES, fill=BOTH)

    for index, game in enumerate(game_history, 1):
        game_info = f"Jogo {index}:\n"
        game_info += f"Mão do Jogador: {game['player_hand']}\n"
        game_info += f"Mão do Dealer: {game['dealer_hand']}\n"
        game_info += f"Resultado: {game['result']}\n\n"
        history_text.insert(END, game_info)


# Embaralhar as cartas
def deal(cards):
    if len(cards) < 4:  # Verifica se há cartas suficientes para uma nova rodada
        reset_deck()
    hand = []
    for i in range(2):
        random.shuffle(cards)
        card = cards.pop()
        hand.append(card)
    return hand


# Resetar as cartas para a quantidade inicial
def reset_deck():
    global cards
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"] * 4
    random.shuffle(cards)


# Comprar cartas
def buy_card(hand):
    hand.append(cards[0])
    cards.pop(0)
    return hand


# Somar cartas
def sum_cards(hand):
    map_card = {"J": 10, "K": 10, "Q": 10, "A": 11}
    aces_count = 0
    total = 0

    for card in hand:
        if isinstance(card, int):
            total += card
        elif card in map_card:
            total += map_card[card]
            if card == "A":
                aces_count += 1  # Contabiliza quantos Áses existem na mão

    # Tratamento do Ás (ajusta o valor ao exceder 21)
    while total > 21 and aces_count > 0:
        total -= 10  # Reduz 10 do total, convertendo um Ás de 11 para 1
        aces_count -= 1

    return total


# Verificar mão inicial
def is_blackjack(hand):
    return sum_cards(hand) == 21 and len(hand) == 2


# Jogo do dealer
def dealer_play():
    global dealer_hand
    total = sum_cards(dealer_hand)

    # Continuar comprando enquanto o total for menor que 17
    while total < 17:
        dealer_hand = buy_card(dealer_hand)
        total = sum_cards(dealer_hand)
        update_display(
            show_full_dealer_hand=True
        )  # Atualiza a interface após cada compra
        root.update_idletasks()  # Garante que a interface seja atualizada

    return total


# Atualiza a interface
def update_display(show_full_dealer_hand=False):
    player_hand_label.config(
        text=f"Player Hand: {start_hand} = {sum_cards(start_hand)}"
    )
    if show_full_dealer_hand:
        dealer_hand_label.config(
            text=f"Dealer Hand: {dealer_hand} = {sum_cards(dealer_hand)}"
        )
    else:
        dealer_hand_label.config(text=f"Dealer Hand: {dealer_hand[0]}, ?")

    victories_label.config(text=f"Victories: {victories}")
    defeats_label.config(text=f"Defeats: {defeats}")


# Comprar mais cartas
def hit():
    global start_hand, defeats
    start_hand = buy_card(start_hand)
    player_total = sum_cards(start_hand)

    if player_total > 21:  # Verifica se o jogador estourou
        result = "Estourou!"
        defeats += 1
        result_label.config(text=result)
        update_display(show_full_dealer_hand=True)  # Atualiza a interface
        hit_button.config(state=DISABLED)
        stand_button.config(state=DISABLED)

        # Salva o histórico apenas uma vez por rodada
        game_history.append(
            {
                "player_hand": start_hand[:],
                "dealer_hand": dealer_hand[:],
                "result": result,
            }
        )
        save_history(
            f"Jogo:\nMão do Jogador: {start_hand}\nMão do Dealer: {dealer_hand}\nResultado: {result}\n\n"
        )
    elif player_total == 21:  # Se o jogador atingir 21, chama automaticamente o stand
        stand()
    else:
        update_display()


# Passar a vez
def stand():
    global victories, defeats
    dealer_result = dealer_play()
    player_result = sum_cards(start_hand)
    hit_button.config(state=DISABLED)
    stand_button.config(state=DISABLED)

    if dealer_result > 21:  # Verifica se o dealer estourou
        result = "Dealer estourou! Você ganhou!"
        victories += 1
    elif player_result > 21:  # Verifica se o jogador estourou
        result = "Você estourou!"
        defeats += 1
    elif dealer_result > player_result:
        result = "Dealer ganhou!"
        defeats += 1
    elif dealer_result < player_result:
        result = "Você ganhou!"
        victories += 1
    else:
        result = "Empate!"

    result_label.config(text=result)  # Atualiza a mensagem na interface
    update_display(show_full_dealer_hand=True)  # Atualiza a interface

    # Salva o histórico apenas uma vez por rodada
    game_history.append(
        {"player_hand": start_hand[:], "dealer_hand": dealer_hand[:], "result": result}
    )
    save_history(
        f"Jogo:\nMão do Jogador: {start_hand}\nMão do Dealer: {dealer_hand}\nResultado: {result}\n\n"
    )


# Começar o jogo
def start_game():
    global start_hand, dealer_hand, victories, defeats
    start_hand = deal(cards)
    dealer_hand = deal(cards)
    update_display()

    # Verificação de Blackjack
    if is_blackjack(start_hand):
        if is_blackjack(dealer_hand):
            result = "Empate com Blackjacks!"
        else:
            result = "Blackjack! Você ganhou!"
            victories += 1

        result_label.config(
            text=result
        )  # Atualiza a interface com a mensagem de Blackjack
        game_history.append(
            {
                "player_hand": start_hand[:],
                "dealer_hand": dealer_hand[:],
                "result": result,
            }
        )
        save_history(
            f"Jogo:\nMão do Jogador: {start_hand}\nMão do Dealer: {dealer_hand}\nResultado: {result}\n\n"
        )
        hit_button.config(state=DISABLED)
        stand_button.config(state=DISABLED)
        update_display(
            show_full_dealer_hand=True
        )  # Atualiza a interface com a mão completa do dealer
    elif is_blackjack(dealer_hand):
        result = "Dealer tem um Blackjack. Você perdeu!"
        defeats += 1
        result_label.config(text=result)
        game_history.append(
            {
                "player_hand": start_hand[:],
                "dealer_hand": dealer_hand[:],
                "result": result,
            }
        )
        save_history(
            f"Jogo:\nMão do Jogador: {start_hand}\nMão do Dealer: {dealer_hand}\nResultado: {result}\n\n"
        )
        hit_button.config(state=DISABLED)
        stand_button.config(state=DISABLED)
        update_display(
            show_full_dealer_hand=True
        )  # Atualiza a interface com a mão completa do dealer
    else:
        result_label.config(text="")
        hit_button.config(state=NORMAL)
        stand_button.config(state=NORMAL)


# ============================== Interface gráfica ==============================
root = Tk()
root.title("Blackjack ♠️♥️♦️♣️")
root.geometry("600x400")

photo = PhotoImage(file="media\\cards.png")
root.wm_iconphoto(False, photo)

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=10)
style.configure("TLabel", font=("Helvetica", 12))

start_hand = []
dealer_hand = []

player_hand_label = ttk.Label(root, text="Player Hand: ")
player_hand_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

dealer_hand_label = ttk.Label(root, text="Dealer Hand: ")
dealer_hand_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

result_label = ttk.Label(root, text="")
result_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

victories_label = ttk.Label(root, text="Victories: ")
victories_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

defeats_label = ttk.Label(root, text="Defeats: ")
defeats_label.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")

start_button = ttk.Button(root, text="Start Game", command=start_game)
start_button.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

hit_button = ttk.Button(root, text="Hit", command=hit)
hit_button.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")

stand_button = ttk.Button(root, text="Stand", command=stand)
stand_button.grid(row=5, column=1, padx=10, pady=10, sticky="nsew")

show_history_button = ttk.Button(root, text="Mostrar Histórico", command=show_history)
show_history_button.grid(row=6, column=0, padx=10, pady=10, sticky="nsew")


# Configurar a grade para expandir conforme necessário
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)
root.grid_rowconfigure(5, weight=1)
root.grid_rowconfigure(6, weight=1)

root.mainloop()
