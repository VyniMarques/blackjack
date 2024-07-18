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

    # FIXME O ÁS vale sempre 1 (Deveria valer 1 ou 11)
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


def game():
    start_hand = deal(cards)
    dealer_hand = deal(cards)

    op = input(str("Jogar Blackjack? S/N ")).lower()

    while True:
        if op == "s":
            print(start_hand, "=", sum_cards(start_hand))
            op2 = input(str("Comprar outra carta? S/N ")).lower()
            if op2 == "s":
                start_hand = buy_card(start_hand)
                if sum_cards(start_hand) == 22:
                    print("Estorou!")
                else:
                    print(start_hand, "=", sum_cards(start_hand))
            elif op2 == "n":
                dealer_result = dealer_play(dealer_hand)

                # print(f"Dealer: {dealer_result}")
                # print("Dealer Estourou" if dealer_result == 22 else f"Dealer: {dealer_result}")
                # print("Você Estourou" if sum_cards(start_hand) == 22 else f"Sua mão: {sum_cards(start_hand)}")
                # FIXME : Valores maiores que 21 são tratados como 22

                if (
                    dealer_result > sum_cards(start_hand)
                    and dealer_result != 22
                    and sum_cards(start_hand) != 22
                ):
                    if dealer_result > sum_cards(start_hand):
                        print("Dealer ganhou")
                        break
                    elif dealer_result < sum_cards(start_hand):
                        print("Voce ganhou")
                        break
                    else:
                        print("Empate")
                        break
                elif dealer_result == 22 and sum_cards(start_hand) != 22:
                    # print("Dealer Estourou" if dealer_result == 22 else f"Dealer: {dealer_result}")
                    # print("Você Estourou" if sum_cards(start_hand) == 22 else f"Sua mão: {sum_cards(start_hand)}")
                    print("Dealer estourou! Você ganhou!")
                    break
                elif dealer_result == 22 and sum_cards(start_hand) == 22:
                    # print("Dealer Estourou" if dealer_result == 22 else f"Dealer: {dealer_result}")
                    # print("Você Estourou" if sum_cards(start_hand) == 22 else f"Sua mão: {sum_cards(start_hand)}")
                    print("Ambos perderam")
                    break
                elif dealer_result != 22 and sum_cards(start_hand) == 22:
                    # print("Dealer Estourou" if dealer_result == 22 else f"Dealer: {dealer_result}")
                    # print("Você Estourou" if sum_cards(start_hand) == 22 else f"Sua mão: {sum_cards(start_hand)}")
                    print("Dealer ganhou")
                    break
        else:
            break


game()
