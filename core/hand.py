from typing import List, Any
from core.card import Card, CardType
from core.deck import Deck

class Hand:
    "Represents a player's hand. Use `can_play_on()` with the top-most card to get a list of cards that can be played on the stack."
    
    def __init__(self) -> None:
        self._cards: List[Card] = []

    
    @property
    def cards(self) -> List[Card]:
        "Returns a list of cards in the current hand."
        return self._cards

    
    def __getitem__(self, index: int) -> Any:
        return self._cards[index]
    

    def pick_up(self, deck: Deck) -> None:
        "Append a new `Card` to this current hand."
        
        self._cards.append(deck.draw())

    
    def can_play_on(self, current: Card) -> List[Card]:
        "Returns a list of cards that can be played with the current card on the top of the stack."

        if current.type in (CardType.Wild, CardType.WildPlus4):
            ...
        
        def playable(card: Card) -> bool:
            "Run checks to see if the card can be placed on top of the stack, returning `True` if it's playable and `False` if not."

            checks = [
                card == current,                                    # card is the exact same
                card.type == current.type,                          # card type is the same
                card.colour and card.colour == current.colour,      # card colour is the same
                card.number and card.number == current.number,      # card number is the same
                card.type == CardType.WildPlus4,                    # card is a wild +4 card
                card.type == CardType.Wild                          # card is a wild card
            ]

            return any(checks)
        
        return [card for card in self._cards if playable(card)]