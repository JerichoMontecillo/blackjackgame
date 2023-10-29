"""
module deck allows for use of the Deck class used in runtime

module player allows for use of Player and Dealer classes which make up the queue

module random allows for use of shuffle which allows the Deck to be shuffled when needed

module time allows for terminal output to be delayed to make it easier to read

import sys used to exit code
"""

from random import shuffle, randint
from time import sleep
import pickle
from .deck import Deck
from .player import Player, Dealer


class Game:
    """
    A class used to represent the Game

    Attributes
    ----------
    new_deck : Deck
        an entire deck of cards

    queue : list
        list of Players which gets iterated on during runtime

    Methods
    -------
    duplicate_deck(deck, n)
        takes a Deck object and an int
        creates n - 1 duplications of the Deck and combines them

    add_queue(person)
        takes a Person object and appends them into the queue

    add_to_file(player_list)
        takes a list of Person objects and adds their information to 
        blackjackgame.player_balances.pkl

    check_file(person)
        takes a person's name and checks to see if they have a past balance

    run()
        runs the game BlackJack
    """

    def __init__(self):
        """
        Parameters
        ----------
        No Parameters
        """
        self.new_deck = Deck()
        self.queue = []

    def duplicate_deck(self, deck, repeat):
        """
        takes a Deck, copies it n - 1 times and combines them all together
        """

        copy_deck = Deck()
        for _ in range(repeat - 1):
            deck.cards += copy_deck.cards

    def add_queue(self, person):
        """
        takes a Person and adds them to the end of the queue
        """

        self.queue.append(person)

    def add_to_file(self, player_list):
        """
        takes everyone and adds their information to blackjackgame.player_balances.pkl,
        """

        try:
            with open("blackjackgame/player_balances.pkl", "rb") as client_info:
                new_clients = []
                found = False
                for _, info in enumerate(pickle.load(client_info)):
                    for _, player in enumerate(player_list):
                        if info.name == player.name:
                            new_clients.append(player)
                            found = True
                    if found is False:
                        new_clients.append(info)
                for _, player in enumerate(player_list):
                    if player not in new_clients:
                        new_clients.append(player)
            client_info.close()

            with open("blackjackgame/player_balances.pkl", "wb") as write_info:
                pickle.dump(new_clients, write_info)
            write_info.close()

        except EOFError:
            with open("blackjackgame/player_balances.pkl", "wb") as write_info:
                pickle.dump(player_list, write_info)
                write_info.close()

    def check_file(self, player):
        """
        checks to see if player has a past balance
        """

        try:
            with open("blackjackgame/player_balances.pkl", "rb") as client_info:
                found = False
                for _, info in enumerate(pickle.load(client_info)):
                    if player == info.name:
                        found = True
                        print("Looks like you have a balance here.")
                        sleep(1.000)
                        print(f"You have {info.balance}\n")
                        sleep(1.000)
                        new_player = Player(info.name, info.balance)
            client_info.close()
            if found:
                return new_player
            return -1
        except EOFError:
            return Player(player, 10000)

    def run(self):
        """
        all the logic for BlackJack, stops when no more players or players responds with
        'n' to wanting to play again
        """

        print("Welcome to terminal Blackjack!")
        sleep(1.000)
        player_amount = int(input("How many players at the table? "))

        # Deck duplicate and shuffle
        self.duplicate_deck(self.new_deck, 8)
        shuffle(self.new_deck.cards)

        # Cut Cards
        length = len(self.new_deck.cards)
        self.new_deck.cards = self.new_deck.cards[length // 2:] + self.new_deck.cards[:length // 2]

        # Place random card in cut card location
        random_card = Deck()
        self.new_deck.cards.insert(self.new_deck.cut_card_location,
                                   random_card.cards[randint(0, 51)])

        # Adds players into the queue and checking if they have a balance already
        for player in range(player_amount):
            name = input(f"What is player {player + 1}'s name? ")
            person = self.check_file(name)
            if person == -1:
                self.queue.append(Player(name, 10000))
            else:
                self.queue.append(person)

        self.add_queue(Dealer("Dealer", 100000000000000000000))

        # Gets bets from all players
        for player in self.queue:
            player.is_turn = True
            if player.is_dealer is True:
                player.end_turn()
                continue
            while player.is_turn:
                bet = int(input(f"{player.name}, how much would you like to bet?"
                                "(Bet 0 to leave) "))
                player.add_bet(bet)

        play_again = " "
        while len(self.queue) > 1:
            # Use same bet as last round
            if play_again == "y":
                print("\n")
                self.queue[-1].is_hidden = True  # Hide the dealer's cards when starting over

                # Shuffle deck if it reaches cut card location
                if self.new_deck.cut_card_location < len(self.new_deck.discards):
                    self.new_deck = self.new_deck.deck_shuffle()

                for player in self.queue:
                    player.start_turn()
                    if player.is_dealer:
                        player.end_turn()
                        continue
                    if player.doubled_down:
                        player.doubled_down = False
                        player.current_bet = player.current_bet / 2
                    bet_option = input(f"{player.name}, would you like to use the"
                                       f"same bet as the previous round? (${player.current_bet})" 
                                       "(y/n) ").lower()
                    if bet_option == "n":
                        while player.is_turn:
                            new_bet = int(input(f"{player.name}, how much would you like to bet?"
                                                "(Bet 0 to leave) "))
                            print("\n")
                            player.is_turn = player.add_bet(new_bet)
            elif play_again == "n":
                print("Leaving table...")
                sleep(1.000)
                for player in self.queue:
                    if player.is_dealer:
                        continue
                    print(f"Goodbye {player.name}, your total balance is {player.balance} ")
                    sleep(1.000)
                self.add_to_file(self.queue[0:-1])
                return -1

            # Takes players out of the queue if they do not have any bet
            for player in self.queue:
                if player.current_bet == 0 and player.is_dealer is False:
                    print(f"Goodbye {player.name}, your total balance is {player.balance}\n")
                    sleep(1.000)
                    self.queue.remove(player)
                    self.add_to_file(player)
                if len(self.queue) < 2:
                    return -1

            # Deal the cards
            for player in self.queue:  # First Set
                player.draw_card(self.new_deck)

            for player in self.queue:  # Second Set
                player.draw_card(self.new_deck)

            # Display Cards and prompt actions
            for player in self.queue:
                player.start_turn()

                if player.is_dealer is False:  # Display Dealer cards
                    self.queue[-1].print_cards()

                while player.is_turn:
                    if player.is_dealer:  # Reveals dealer's final cards
                        player.is_hidden = False
                        while player.check_value() < 17:
                            player.draw_card(self.new_deck)
                        player.print_cards()
                        if player.check_value() == 21:
                            print("Dealer got Blackjack!")
                            sleep(1.000)
                        player.end_turn()
                        continue

                    player.print_cards()

                    if player.check_value() == 21:  # Blackjack off the first two cards
                        print("Blackjack!")
                        sleep(1.000)
                        player.end_turn()
                        continue

                    if player.check_value() < 21:  # Double Down
                        option = input("Would you like to double down? (y/n) ").lower()
                    if option == "y":
                        player.double_down()
                        if player.doubled_down:
                            player.draw_card(self.new_deck)
                            player.print_cards()
                            if player.check_value() == 21:
                                print("Blackjack!")
                                sleep(1.000)
                            if player.check_value() > 21:
                                print("Busted!")
                                sleep(1.000)
                                player.end_turn()
                                continue
                            print("This is your final hand.")
                            sleep(1.000)
                            print(f"You have ${player.balance} remaining\n")
                            sleep(1.000)
                            player.end_turn()
                            continue
                        print("Not enough funds")
                        sleep(1.000)

                    while player.is_turn:  # Hit
                        option = input("Would you like to hit? (y/n) ").lower()
                        if option == "n":  # No hit, stand
                            player.stand()
                            print("This is your final hand.\n")
                            sleep(1.000)
                            player.end_turn()
                            continue
                        player.draw_card(self.new_deck)
                        if player.check_value() == 21:
                            print("Blackjack!")
                            sleep(1.000)
                        player.print_cards()
                        if player.check_value() > 21:
                            print("Busted!\n")
                            sleep(1.000)
                            player.end_turn()

            # Check Values
            for player in self.queue:
                if player.is_dealer:
                    continue
                if player.check_value() < 22:
                    if (self.queue[-1].check_value() > 21
                        or self.queue[-1].check_value() < player.check_value()):
                        player.win_hand()
                    elif player.check_value() == self.queue[-1].check_value():
                        player.tie_hand()
                    else:
                        player.lose_hand()
                else:
                    player.lose_hand()
                print(f"{player.name} has ${player.balance} remaining.\n")
                sleep(1.000)

            # Discard hands
            for person in self.queue:
                self.new_deck.discard_hands(person)

            # Prompt play again
            play_again = input("Would you like to go again? (y/n) ").lower()
