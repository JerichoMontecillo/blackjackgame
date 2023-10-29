"""
module dictionary allows to use Dict function to map values

module time allows for delaying the terminal output
"""

from time import sleep
from .dictionary import Dict


class Player:
    """
    A class used to represent a Player at the blackjack table

    Attributes
    ----------
    name : string
        Player's name

    balance : int
        Player's balance

    current_bet : int
        How much the Player is betting at any current time (default is 0)

    current_hand : list
        Player's current cards

    is_turn : bool
        True when it's the Player's turn (default is False)

    is_dealer : bool
        Always False for Player classes

    doubled_down : bool
        True when the Player has doubled down (default is False)

    Methods
    -------
    empty_hand()
        clears the Player's hand

    add_balance(winnings)
        adds money to the Players balance

    subtract_balance(losings)
        subtracts money to the Players balance

    add_bet(bet)
        makes sure that the Player has enough money to make their bet

    doubled_down()
        makes sure that the Player has enough money to double down

    draw_card()
        adds a card to the Player's hand

    print_cards()
        outputs the Player's cards on the terminal

    check_value()
        adds up the values of all the cards in a hand

    start_turn()
        starts a Player's turn

    end_turn()
        ends a Player's turn

    stand()
        the Player is standing and will draw no more cards

    win_hand()
        adds money to the Player's balance and displays win message in terminal

    lose_hand()
        displays lose message in terminal

    tie_hand()
        adds bet amount to Player's balance and displays tie message
    """

    def __init__(self, name, balance):
        """
        Parameters
        name: string
            name of the Player

        balance: int
            initial balance of the Player
        """

        self.name = name
        self.balance = balance
        self.current_bet = 0
        self.current_hand = []
        self.is_turn = False
        self.is_dealer = False
        self.doubled_down = False

    def empty_hand(self):
        """
        empties the list current_hand
        """

        self.current_hand = []

    def add_balance(self, winnings):
        """
        adds money to the Player's balance

        Parameters
        ----------
        winnings : int
            how much money the Player wins
        """

        self.balance = self.balance + winnings

    def subtract_balance(self, losings):
        """
        subtracts money from the Player's balance

        Parameters
        ----------
        losings: int
            how much money the Player loses
        """

        self.balance = self.balance - losings

    def add_bet(self, bet):
        """
        changes value of current_bet to bet if the Player has enough money

        Parameters
        ----------
        bet : int
            how much money the Player is betting
        """

        if bet < 0:  # Negative Bet
            print("Bet amount out of range.")
            sleep(1.000)
            self.is_turn = True
        elif bet > self.balance:  # Bet too high
            print("Not enough funds.")
            sleep(1.000)
            self.is_turn = True
        elif bet == 0:  # Stop playing
            print("Leaving Table...")
            sleep(1.000)
            self.is_turn = False
        else:
            self.current_bet = bet
            self.subtract_balance(bet)
            self.is_turn = False

    def double_down(self):
        """
        changes value of current_bet if the player has enough money to double down
        """

        if self.current_bet <= self.balance:
            self.subtract_balance(self.current_bet)
            self.current_bet = self.current_bet * 2
            self.doubled_down = True
        else:
            self.doubled_down = False

    def draw_card(self, deck):
        """
        adds a card to the Player's current_hand

        Parameters
        ----------
        deck : Deck
            takes a Card from the Deck made in runtime
        """

        self.current_hand.append(deck.cards[0])
        deck.discards.append(deck.cards[0])
        deck.cards.pop(0)

    def print_cards(self):
        """
        prints cards from current_hand onto the terminal
        """

        print(f"{self.name}'s cards: ")
        for _, card in enumerate(self.current_hand):
            print(card.rank, Dict.get(card.suit))
            sleep(0.500)

    def check_value(self):
        """
        adds values of all the cards in current_hand and returns the total
        """

        value = 0
        number_of_aces = 0
        for _, card in enumerate(self.current_hand):
            if card.rank == "Ace":
                value = value + 10
                number_of_aces = number_of_aces + 1
            value = value + Dict.get(card.rank)
            for _ in range(number_of_aces):
                if value > 21:
                    value = value - 10
                    number_of_aces = number_of_aces - 1
        return value

    def start_turn(self):
        """
        starts the Player's turn
        """

        self.is_turn = True
        print(f"It is {self.name}'s turn")
        sleep(1.000)

    def end_turn(self):
        """
        ends the Player's turn
        """

        self.is_turn = False

    def stand(self):
        """
        prints that the Player is standing and ends their turn
        """

        print(f"{self.name} stands and ends their turn")
        sleep(1.000)
        self.end_turn()

    def win_hand(self):
        """
        adds money to Player's balance and prints winning message
        """

        self.add_balance(2 * self.current_bet)
        print(f"{self.name} wins with their hand and wins {self.current_bet}.")
        sleep(1.000)

    def lose_hand(self):
        """
        prints losing message and gives donation if negative
        """

        print(f"{self.name} loses with their hand and loses {self.current_bet}.")
        sleep(1.000)

        if self.balance <= 0:
            self.balance = 10000
            print("Uh oh, looks like we took all your money!")
            sleep(1.000)
            print("But it seems like someone donated $10000 to you :D")
            sleep(1.000)

    def tie_hand(self):
        """
        adds money to Player's balance equal to how much they bet and prints winning message
        """

        self.add_balance(self.current_bet)
        print(f"{self.name} ties with the dealer.")
        sleep(1.000)


class Dealer(Player):
    """
    A class used to represent the Dealer which inherits from Player class

    Attributes
    ----------
    name : string
        always Dealer

    balance : int
        always 0

    current_bet : int
        always 0

    current_hand : list
        Dealer's current cards

    is_turn : bool
        True when it's the Dealers's turn (default is False)

    is_dealer : bool
        Always True for Dealer classes

    doubled_down : bool
        Always False

    is_hidden : bool
        True at the start, False when it is the Dealer's turn to draw cards

    Methods
    -------
    print_cards()
        prints the Dealer's cards
    """

    def __init__(self, name, balance):
        """
        Parameters
        ----------
        name: string
            always Dealer

        balance : int
            always 0
        """

        super().__init__(name, balance)
        self.is_dealer = True
        self.is_hidden = True

    def print_cards(self):
        """
        prints Dealer's cards into the terminal, and hides the second card if is_hidden is True
        """

        if self.is_hidden:
            print(
                f"Dealer's cards: {self.current_hand[0].rank}"
                f"{Dict.get(self.current_hand[0].suit)} **")
            sleep(1.000)

        else:
            print("Dealer's cards: ")
            for _, card in enumerate(self.current_hand):
                print(card.rank, Dict.get(card.suit))
                sleep(0.200)
