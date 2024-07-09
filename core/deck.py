from card import Card, CardType, Colour
from ..errors import NoCardsLeftError, NotSupportedError
from enum import Enum

class DeckSize(Enum):
    "An enum to represent the size of the deck to be used. Corresponds to the gamemode being played."

    Normal = 0
    
    ... # can make extra modes which have different deck compositions

class Deck:
    """
    Represents a deck of cards in Uno.
    
    Parameters
    ----------

        - size: `DeckSize` - the size of the deck selected. Corresponds to gamemode.
            
            - `DeckSize.Normal` - standard deck size in a normal game of Uno.

    
    Other game modes will be supported in future.

    
    Raises:
    -------

        - `TypeError`: `size` parameter did not match typehint to `DeckSize` enum.

        - `NotSupported`: `size` is not a supported `DeckSize`.
    """
    
    def __init__(self, size: DeckSize = DeckSize.Normal):
        if not isinstance(size, DeckSize):
            raise TypeError('size parameter is not of type DeckSize.')

        self.deck = []

        # build decks
        match size:
            case DeckSize.Normal:
                for current in Colour: # represents enum values for colours
                    self.deck += [Card(colour = current, number = 0)] # add 0
                        
                    # add one zero card
                    self.deck += [
                        Card(
                            colour = current, # get the attribute from the value
                            number = 0
                        )
                    ]

                    # add the other 9 cards in pairs of two
                    for i in range(9):
                        self.deck += [
                            Card(colour = current, number = i),
                            Card(colour = current, number = i)
                        ]

                    for i in range(1, 4): # 2 of each: Skip, +2 and Reverse
                        self.deck += [
                            Card(colour = current, type = CardType(i)),
                            Card(colour = current, type = CardType(i))
                        ]

                    # 4 Wild cards
                    self.deck += [
                        Card(type = CardType.Wild)
                        for _ in range(4)
                    ]

                    # 4 Wild +4 cards
                    self.deck += [
                        Card(type = CardType.WildPlus4)
                        for _ in range(4)
                    ]

            case _: # catch any unsupported gamemodes
                raise NotSupportedError("this mode is not supported.")
            
    
    def draw(self) -> Card:
        "Pick up a card from the deck. Raises a `NoCardsLeft` error if no cards are left in the deck."

        if not self.deck:
            raise NoCardsLeftError('no cards are left in the deck.')
        
        return self.deck.pop()