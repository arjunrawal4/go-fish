import random
import sys
import os
import operator
from time import sleep

rows, columns = os.popen('stty size', 'r').read().split()
nice_values = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
values = [0,1,2,3,4,5,6,7,8,9,10,11,12]

colors = ['♥', '♦', '♠', '♣']

class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color
    def __str__(self):
        return nice_values[self.value] + self.color
    def __eq__(self, other):
        return self.value == other.value

class Player:
    def __init__(self, name, score, hand):
        self.name = name
        self.score = score
        self.hand = hand
        
    def print_hand(self):
        print(self.name + "\'s Deck: ",  end='')
        print_deck(self.hand)

    def __str__(self):
        return self.name

def new_deck():
    deck = [Card(value, color) for value in values for color in colors]
    random.shuffle(deck)
    return deck
    
def deal(deck):
    p1_cards = deck[:7]
    p2_cards = deck[7:14]
    draw_pile = deck[14:]
    return(p1_cards,p2_cards,draw_pile)

def print_deck(deck):
    for c in deck:
        print(str(c)+',', end='')
    print('\n')

def possible_choices(deck):
    vals = []
    for c in deck:
        vals.append(c.value)
    return vals

def go_fish(hand,pile):
    if pile == []:
        print("No more cards left!")
        exit(0)
    else:
        hand.append(pile.pop(0))

def ask(card,requester,giver,pile):
    print(str(requester)+" is asking for " + str(nice_values[card.value])+'\'s')
    sleep(0.3)
    count = 0
    taken = []
    for c in giver.hand:
        if c.value == card.value:
            count += 1
            requester.hand.append(c)
            taken.append(c)
    for t in taken:
        giver.hand.remove(t)
    if count == 0:
        print(str(giver)+" says Go Fish!")
        sleep(0.5)
        go_fish(requester.hand,pile)
    else :
        print("You gained some cards!")
        check_hand(requester)
        sleep(0.3)
        print("You can pick again!")
        requester.print_hand()
        if requester.hand:
            query = input("What card would you like to ask for?\n")
            while query not in nice_values or nice_values.index(query) not in possible_choices(requester.hand):
                print("Please choose a value from A,2,3,4,5,6,7,8,9,10,J,Q, and K that is in your hand")
                query = input("What card would you like to ask for?\n")
            ask(Card(nice_values.index(query), colors[0]), requester, giver, pile)
    check_hand(requester)


def ask_cpu(card, requester, giver, pile):
    print(str(requester)+" is asking for " +
          str(nice_values[card.value])+'\'s')
    count = 0
    taken = []
    for c in giver.hand:
        if c.value == card.value:
            count += 1
            requester.hand.append(c)
            taken.append(c)
    for t in taken:
        giver.hand.remove(t)
    if count == 0:
        print("Go Fish!")
        go_fish(requester.hand, pile)
        input("Press enter to continue\n")
    else:
        print("The AI took some cards!")
        check_hand(requester)
        giver.print_hand()
        if requester.hand:
            ask_cpu(random.choice(requester.hand), requester, giver, pile)
    check_hand(requester)

def check_hand(player):
    player.hand.sort(key=lambda x: [x.value])
    quads = [x for x in player.hand if player.hand.count(x) >= 4]
    player.hand = [x for x in player.hand if player.hand.count(x) < 4]
    if quads:
        player.score += 1
        print("\n"+str(player) + " scored 1 point for getting a set of " + str(nice_values[quads[0].value])+"\'s\n")

def game_status(player1, player2,draw_pile):
    player1.print_hand()
    # player2.print_hand()
    # print("Draw Pile: ",  end='')
    # print_deck(draw_pile)
    print("Score:")
    print("\t"+str(player1) + ": " + str(player1.score))
    print("\t"+str(player2) + ": " + str(player2.score))

def run_game(p1,p2,dp):
    while dp:
        if p1.hand:
            query = input("What card would you like to ask for?\n")
            while query not in nice_values or nice_values.index(query) not in possible_choices(p1.hand):
                print("Please choose a value from A,2,3,4,5,6,7,8,9,10,J,Q, and K that is in your hand")
                query = input("What card would you like to ask for?\n")
            ask(Card(nice_values.index(query), colors[0]), p1, p2, dp)
            game_status(p1, p2, dp)
        sleep(0.5)
        print("\n"+'*' * int(rows)+"\n")
        print(str(p2)+"\'s turn\n\n")
        input("Press enter to continue\n")

        if p2.hand and dp:
            ask_cpu(random.choice(p2.hand), p2, p1, dp)
            game_status(p1, p2, dp)

        print("\n"+'*' * int(rows)+"\n")
        print(str(p1)+"\'s turn\n\n")

    print('*' * int(rows))
    print('*' * int(rows))
    print('*' * int(rows))

    print("GAME OVER!\n\n")
    print("Final score is:")

    print("\t"+str(p1) + ": " + str(p1.score))
    print("\t"+str(p2) + ": " + str(p2.score))
    if p1.score > p2.score : 
        print("You Win! Congratulations!")
    elif p1.score == p2.score :
        print("You Tied! But you can do better...!")
    else:
        print("Yikes, you lost to a computer!")

def main(): 

    user = input("What's your name?\n")
    print("\nWelcome, "+user+"!")
    input("Press Enter to continue\n")
    print("Ready to play Go Fish???")
    response = input("Enter n for No, anything else for Yes!\n")
    if response == 'n':
        print("OK, come back when you feel ready!")
        exit(0)

    p1 = Player(user,0,[])
    p2 = Player("AI", 0, [])

    deck = new_deck()
    print("Shuffling the deck...\n\n")
    sleep(0.5)
    p1.hand,p2.hand,dp = deal(deck)
    print("Dealing out the cards...\n\n")
    sleep(0.5)

    check_hand(p1)
    check_hand(p2)
    print("Here are your cards!...")
    p1.print_hand()


    print('*' * int(rows))
    print('*' * int(rows))
    print('*' * int(rows))
    print("GAME IS STARTING!\n\n")


    run_game(p1,p2,dp)

main()
