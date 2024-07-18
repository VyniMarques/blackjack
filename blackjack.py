import random
from tkinter import *

cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K", "A"] * 4


def deal(cards):
    hand = []
    for i in range(2):
        random.shuffle(cards)
        card = cards.pop()
        hand.append(card)
    return hand


def buy_card(hand):
    hand.append(cards[0])
    cards.pop(0)
    return hand


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

    total = sum(numbers)
    if total > 21:
        total = 22
    return total


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


def update_display():
    player_hand_label.config(
        text=f"Player Hand: {start_hand} = {sum_cards(start_hand)}"
    )
    dealer_hand_label.config(text=f"Dealer Hand: {dealer_hand[0]}, ?")


def hit():
    global start_hand
    start_hand = buy_card(start_hand)
    if sum_cards(start_hand) == 22:
        result_label.config(text="Estourou!")
    update_display()


def stand():
    dealer_result = dealer_play(dealer_hand)
    player_result = sum_cards(start_hand)
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
    update_display()


root = Tk()
root.title("Blackjack")
root.geometry("300x300")

start_hand = []
dealer_hand = []

player_hand_label = Label(root, text="Player Hand: ")
player_hand_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

dealer_hand_label = Label(root, text="Dealer Hand: ")
dealer_hand_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

result_label = Label(root, text="")
result_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

start_button = Button(root, text="Start Game", command=start_game)
start_button.grid(row=3, column=0, padx=10, pady=10)

hit_button = Button(root, text="Hit", command=hit)
hit_button.grid(row=4, column=0, padx=10, pady=10)

stand_button = Button(root, text="Stand", command=stand)
stand_button.grid(row=4, column=1, columnspan=2, padx=10, pady=10)

root.mainloop()
