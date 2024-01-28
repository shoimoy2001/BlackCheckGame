import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10, 'Jack': 10,
          'Queen': 10, 'King': 10, 'Ace': 11}

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n ' + card.__str__()
        return 'The deck has:' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        single_card = self.deck.pop()
        return single_card

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips:
    def __init__(self, total):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

class Player:
    def __init__(self, name):
        self.name = name
        self.chips = Chips(0)  # Default total chips set to 100

def buy_chips(player):
    while True:
        try:
            buy_amount = int(input(f"{player.name}, how many chips would you like to buy? "))
        except ValueError:
            print('Sorry, the amount must be an integer!')
        else:
            player.chips.total += buy_amount
            print(f"You bought {buy_amount} chips. Your total chips: {player.chips.total}")
            break

def take_bet(player):
    while True:
        try:
            player.chips.bet = int(input(f"{player.name}, how many chips would you like to bet? "))
        except ValueError:
            print('Sorry, a bet must be an integer!')
        else:
            if player.chips.bet > player.chips.total:
                print(f"Sorry, your bet can't exceed {player.chips.total}")
            else:
                break

def hit(deck, hand):
    card = deck.deal()
    hand.add_card(card)
    if hand.value > 21 and hand.aces:
        hand.adjust_for_ace()

def hit_or_stand(deck, hand):
    global playing
    while True:
        user_input = input("Do you want to Hit or Stand? Enter 'H' or 'S': ").lower()
        if user_input == 'h':
            hit(deck, hand)
        elif user_input == 's':
            playing = False
        else:
            print("Invalid Input")
            continue
        break

def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')

def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)

def player_busts(player, dealer, chips):
    print("Player busts! You lose!")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print("Dealer busts! Player wins.")
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    print("Dealer wins! You lose.")
    chips.lose_bet()

def push(player, dealer):
    print("It's a tie! Push.")

while True:
    player_name = input("Enter your name: ")
    player = Player(player_name)

    print(f"Welcome to Blackjack, {player.name}! Get as close to 21 as you can without going over.")
    print("Dealer hits until she reaches 17. Aces count as 1 or 11.")

    buy_chips(player)

    while True:
        deck = Deck()
        deck.shuffle()

        player_hand = Hand()
        player_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())

        dealer_hand = Hand()
        dealer_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

        take_bet(player)

        show_some(player_hand, dealer_hand)

        playing = True

        while playing:
            hit_or_stand(deck, player_hand)
            show_some(player_hand, dealer_hand)

            if player_hand.value > 21:
                player_busts(player_hand, dealer_hand, player.chips)
                break

        if player_hand.value <= 21:
            while dealer_hand.value < 17:
                hit(deck, dealer_hand)

            show_all(player_hand, dealer_hand)

            if dealer_hand.value > 21:
                dealer_busts(player_hand, dealer_hand, player.chips)
            elif dealer_hand.value > player_hand.value:
                dealer_wins(player_hand, dealer_hand, player.chips)
            elif dealer_hand.value < player_hand.value:
                player_wins(player_hand, dealer_hand, player.chips)
            else:
                push(player_hand, dealer_hand)

        print(f"\n{player.name}'s total chips: {player.chips.total}")

        if player.chips.total == 0:
            print(f"Sorry, {player.name}! You're out of chips. Thanks for playing.")
            break

        while True:
            new_game = input("Do you want to play another hand? Enter 'Y' or 'N': ").lower()
            if new_game == 'y':
                break
            elif new_game == 'n':
                print(f"Thanks for playing, {player.name}!")
                break
            else:
                print("Invalid input. Please enter 'Y' or 'N'.")
                continue
        if new_game != 'y':
            break
