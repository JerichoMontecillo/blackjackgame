"""
module collections allows namedtuple to be used for Card class

module random allows to get a random value to put the cut card location, allows to get a
random integer for variation

module player imports Player class
"""

from collections import namedtuple
from random import randint, random

class Deck:
    """
    A class used to represent a deck of cards

    Attributes
    ----------
    card : namedtuple
        represents a Card that makes up the Deck

    suits : list
        represents the four suits in a deck of cards

    ranks : list
        represents the 13 types/values in a deck of cards

    cards : list
        a list containing the namedtuples Card

    discards : list
        a list containing cards that have been used during the runtime

    cut_card_location : int
        an int representing a random number within the closer end of the entire stack of cards to
        show when the deck should be reshuffled
    
    Methods
    -------
    deck_shuffle()
        adds cards in discard list into the cards list and shuffles them
        when the cut_card_location is reached

    discard_hands(person)
        takes a Person class and takes the cards in currentHand, adds them
        to the discard list and clears their hand
    """
    Card = namedtuple("Card", ["rank", "suit"])
    suits = "Clubs Hearts Spades Diamonds".split()  # ['Clubs', 'Hearts', 'Spades', Diamonds']
    ranks = ["Ace"] + [str(x) for x in range(2, 11)] + "J Q K".split()

    def __init__(self):
        """
        Parameters
        ----------
        Values are always the same so they are made during initialization
        """
        self.cards = []
        self.discards = []
        for suit in self.suits:
            for rank in self.ranks:
                self.cards.append(self.Card(rank, suit))
        self.cut_card_location = randint(335, 355)

    def deck_shuffle(self):
        """
        Combines the cards list and discards list and shuffles them
        """
        self.cards = self.cards + self.discards
        random_value = random()
        self.cards.shuffle(random_value)
        return self.cards

    def discard_hands(self, person):
        """
        Takes a person's cards and adds them to the discards list and
        clears the person's hand

        Parameters
        ----------
        player : Person
            Any Person class
        """
        self.discards = self.discards + person.current_hand
        person.current_hand.clear()
