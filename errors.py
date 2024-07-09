class NoCardsLeftError(Exception):
    "Used for when there are no cards left in the deck."

class NotSupportedError(Exception):
    "Used for when a deck cannot be built off of a `DeckType` input."

class NotCompatibleError(Exception):
    "Used for when two objects cannot be compared. (ie. a string and an integer)"