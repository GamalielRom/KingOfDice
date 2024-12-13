import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import matplotlib.pyplot as plt
import random

Cards = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "Jack": 11, "Queen": 11, "King": 11, "Ace": [1,10]}

Players = ["Player 1", "Player 2", "Player 3", "Player 4"]

Values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "King", "Queen", "Jack", "Ace" ]

Suits = ["Hearts", "Diamonds", "Clubs", "Spades"]

Deck = [f"{value} of {suit}" for value in Values for suit in Suits]

bet = 100

print("Card and values")
for card, value in Cards.items():
    print(f"{card}: {value}")

def throw_dice():
    return[random.randint(1,6) for _ in range(3)] #3 Dices rolled in a range of 1 to 6


def calculate_hand(hand):
    total = 0
    for card in  hand:
        card_value = card.split()[0]
        if card_value == "Ace":
            total  += max(Cards[card_value])
        else:
            total += Cards[card_value]
    return total

def remove_players(differences):
    max_difference = max(differences.values())
    players_to_remove = [player for player, diff in differences.items() if diff == max_difference]
    return players_to_remove


def simulate_game():
    Players_copy = Players.copy()  
    Deck_copy = Deck.copy() 
    total_bet = len(Players) * bet
    total_winnings = 0

    while len(Players_copy) > 1:  # Continue until only one player remains
        dices = throw_dice()
        dice_sum = sum(dices)

        random.shuffle(Deck_copy)
        players_hand = {player: [Deck_copy.pop(), Deck_copy.pop()] for player in Players_copy}

        differences = {}

        for player, hand in players_hand.items():
            hand_value = calculate_hand(hand)
            difference = abs(hand_value - dice_sum)
            differences[player] = difference
            
        players_to_remove = remove_players(differences)

        for player in players_to_remove:
            if player in Players_copy:
                Players_copy.remove(player)
        

        if len(players_to_remove) > 1:
            print("\nMultiple players removed due to the highest equal difference")
        else:
            print("\nPlayer with the highest difference eliminated")
    if len(Players_copy) == 1:
        total_winnings = bet
        return Players_copy[0], total_bet, total_winnings
    return None, total_bet, 0
 


def calculate_experimental_probability(rounds = 100):
    win_count = {player: 0 for player in Players}
    total_bets = 0
    total_winnings = 0

    for _ in range(rounds):
        Winner, total_bet, total_winning = simulate_game()
        total_bets += total_bet
        total_winnings += total_winning
        if Winner:
            win_count[Winner] += 1
    
    probabilities = {player: win_count[player] / rounds * 100 for player in Players}

    if total_bets > 0:
        house_edge = (total_bets - total_winnings) / total_bets * 100
    else:
        house_edge = 0

    return probabilities, house_edge

probabilities, house_edge  = calculate_experimental_probability(rounds = 100)

for player, probability in probabilities.items():
    print(f"{player} has a probability of winning: {probability: .2f}")

print(f"\n House Edge: {house_edge: .2f}%")

if __name__ == "__main__":
    while len(Players) > 1:
        print("\n Starting the new round!")

        dices = throw_dice()
        dice_sum = sum(dices)
        print(f"Result for the dices: {dices}, sum {dice_sum}")

        random.shuffle(Deck)
        players_hand = {player: [Deck.pop(), Deck.pop()] for player in Players}

        differences = {}

        print("Hand Players")
        for player, hand in players_hand.items():
            hand_value = calculate_hand(hand)
            difference = abs(hand_value - dice_sum)
            differences[player] = difference
            print(f"{player}: {hand} - Hand Value {hand_value} - Dice Sum: {dice_sum} - Difference: {difference}")
        
        player_to_remove = remove_players(differences)

        for player in player_to_remove:
            if player in Players:
                Players.remove(player)
        if len(player_to_remove) > 1:
            print("\n Multiple players removed due the highest equal difference")
        else: 
            print("\n Player with the highest difference eliminated")
        print(f"Players eliminated: {player_to_remove}")

        if len(Players) == 1:
            print(f"\n {Players[0]} Is the Winner!")
            break

#Using Tkinter to demostrate a graph and probabilities
players = list(probabilities.keys())
probs_to_win = list(probabilities.values())

root = tk.Tk()
root.title("King of the dice Simulation")

fig, ax = plt.subplots()
ax.bar(players, probs_to_win, color='darkblue')
ax.set_title('Probabilities of each player to win')
ax.set_xlabel('Player')
ax.set_ylabel('Probability (%)')

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack()

text = tk.Text(root)
text.pack()

text.insert(tk.END, "Probabilidades de ganar:\n")
for player, probability in probabilities.items():
    text.insert(tk.END, f"{player}: {probability:.2f}%\n")
text.insert(tk.END, f"\nHouse Edge: {house_edge:.2f}%\n")
root.mainloop()







