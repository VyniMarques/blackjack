import random
from tkinter import *

cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"] * 4


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


# Reseta as cartas para a quantidade inicial
def reset_deck():
    global cards
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"] * 4
    random.shuffle(cards)


# Comprar cartas
def buy_card(hand):
    hand.append(cards[0])
    cards.pop(0)
    return hand


# Somatorio das cartas
def sum_cards(hand):
    map_card = {"J": 10, "K": 10, "Q": 10, "A": 1}
    numbers = []

    for card in hand:
        if isinstance(card, int):
            numbers.append(card)
        elif card in map_card:
            numbers.append(map_card[card])
        else:
            numbers.append(card)

    # Resultado / Tratamento do Ás
    total = sum(numbers)
    if "A" in hand and total + 10 <= 21:
        total += 10
    if total > 21:
        total = 22
    return total


# Jogo do dealer
def dealer_play(dealer):
    total = sum_cards(dealer)
    if total == 22:
        return total
    elif int(total) < 17:
        dealer = buy_card(dealer)
        return dealer_play(dealer)
    elif total > 21:
        return total
    return int(total)


def start_game():
    global start_hand, dealer_hand
    start_hand = deal(cards)
    dealer_hand = deal(cards)
    update_display()
    result_label.config(text="")
    hit_button.config(state=NORMAL)
    stand_button.config(state=NORMAL)


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


# Opção de comprar mais cartas
def hit():
    global start_hand
    start_hand = buy_card(start_hand)
    if sum_cards(start_hand) == 22:
        result_label.config(text="Estourou!")
        update_display(show_full_dealer_hand=True)
        hit_button.config(state=DISABLED)
        stand_button.config(state=DISABLED)
    else:
        update_display()


# Opção de passar a vez / mostrar resultado
def stand():
    dealer_result = dealer_play(dealer_hand)
    player_result = sum_cards(start_hand)
    update_display(show_full_dealer_hand=True)
    hit_button.config(state=DISABLED)
    stand_button.config(state=DISABLED)
    if dealer_result == 22:
        result_label.config(text="Dealer estourou! Você ganhou!")
    elif player_result == 22:
        result_label.config(text="Você estourou!")
    elif dealer_result > player_result:
        result_label.config(text="Dealer ganhou")
    elif dealer_result < player_result:
        result_label.config(text="Você ganhou")
    else:
        result_label.config(text="Empate")


# ============================== Interface gráfica ==============================
root = Tk()
root.title("Blackjack ♠️♥️♦️♣️")
root.geometry("500x300")

start_hand = []
dealer_hand = []

player_hand_label = Label(root, text="Player Hand: ")
player_hand_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

dealer_hand_label = Label(root, text="Dealer Hand: ")
dealer_hand_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

result_label = Label(root, text="")
result_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

start_button = Button(root, text="Start Game", command=start_game)
start_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

hit_button = Button(root, text="Hit", command=hit)
hit_button.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

stand_button = Button(root, text="Stand", command=stand)
stand_button.grid(row=4, column=1, padx=10, pady=10, sticky="nsew")

# Configurar a grade para expandir conforme necessário
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_rowconfigure(4, weight=1)

root.mainloop()
