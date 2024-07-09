# UNO in Python

This is to document my journey in programming the game of UNO inside Python.

## Overview

In UNO, there are two different types of cards:
- Normal cards
    -
    These are cards with no special properties and that don't affect how the game progresses. Cards in this category are like a Red 5 or a Yellow 7: they don't change anything about the game and are simply cards that can be played.

- Special cards
    -
    Here's the fun part: special cards. These include skips, +2's and my personal favourites: the Wild Cards and the +4's. These are special cards that affect how the game progresses because a player can receive an influx of cards that means the game takes longer to play.


## First Steps

Let's start from the beginning. How are we going to represent a card? We have two options:
```py
class Card:
    def __init__(self, colour: str, number: int):
        self.colour = colour
        self.number = number
```

This works, but we can leverage enums for a similar output just with better typehints and less opportunity for errors to arise. This does come at a cost, which is more boilerplate code, but with our new system, we can discern between normal cards and different types of special cards.
```py
from enum import Enum

class Colour(Enum):
    Red = 1
    Green = 2
    Yellow = 3
    Blue = 4

class CardType(Enum):
    Normal = 1
    Skip = 2
    Plus2 = 3
    Wild = 4
    WildPlus4 = 5


class Card:
    def __init__(
        self,
        colour: Colour,
        number: int = None,
        type: CardType = CardType.Normal
    ):
        ...
```

Now we have fixed inputs and more discernable parameters. However, that doesn't stop _anything_ being thrown into the `__init__` of the card class, so we can add some type checks to make sure nothing goes wrong.

```py
class Card:
    def __init__(
        self,
        /,
        colour: Colour = None,
        number: int = None,
        type: CardType = CardType.Normal
    ):
        # check colour is Colour enum
        if not isinstance(colour, Colour):
            raise TypeError('colour parameter is not of type Colour.')

        # check number is an integer
        if number: # if number is not None
            if not isinstance(number, int): # if number is not an integer
                raise TypeError('number parameter is given but it is not integer.')
        
        if not isinstance(type, CardType):
            raise TypeError('type parameter is not of type CardType.')

        ...

        self.colour = colour
        self.number = number
        self.type = type
```

Ta-da! We have a way to store information about a card. The `isinstance` checks are used to check if the parameters are instances of the types we typehinted to, hence enforcing the types. We do this because Python is a dynamically-typed language, meaning types can be inferred but not enforced. The rest of the code has also been commented.


### Further Type Checking

The `...` represents:
```py
class Card:
    def __init__(self, ...):
        ...

        def raise_type_error(missing_param: str, expected_type: str):
            "Raise a `TypeError` for parameters with incorrect types."
            message = f"{missing_param} must be {expected_type}. Card is of type {type} and requires this parameter to be {expected_type}."
            raise TypeError(message)
        
        # check colour and number based on card type
        match type:
            # normal cards should have both a colour and a number
            case CardType.Normal:
                if not colour:
                    raise ValueError('missing colour parameter. Card is normal type and requires this parameter.')

                if not number:
                    raise ValueError('missing number parameter. Card is normal type and requires this parameter.')
        
            # skips and +2's shouldn't have numbers

            case CardType.Skip:
                if number: raise_type_error('number', 'None')
            
            case CardType.Plus2:
                if number: raise_type_error('number', 'None')

            # wild cards shouldn't have either a number or a colour

            case CardType.Wild:
                if colour: raise_type_error('colour', 'None')
                if number: raise_type_error('number', 'None')
            
            case CardType.WildPlus4:
                if colour: raise_type_error('colour', 'None')
                if number: raise_type_error('number', 'None')
```

Here, we have a function to raise a custom error message in the same format each time, then we can use `match` and `case` again for each card to enforce which attributes ecah type of card should have.


## Grouping the Cards

We have a way to represent one card, but what about the deck of cards all players draw from? We can use a second class for that, appropriately called `Deck`.

To accompany future gamemodes besides the basic one, we can use _another_ `Enum` (recurring theme by now) to represent different gamemodes.

```py
from enum import Enum

class DeckSize:
    Normal = 0
    ... # represents future sizes we could add
```

```py
class Deck:
    def __init__(self, size: DeckSize):
        if not isinstance(size, DeckSize):
            raise TypeError('size parameter is not of type DeckSize.')
        
        match size:
            case DeckSize.Normal:
                ...

            case _:
                raise NotImplementedError('this mode is not supported yet.') # catch any added DeckSize values that aren't supported
```

Using `match` and `case`, we can match the size to a corresponding deck size on the enum then build the deck accordingly.


## Standard Deck Contents

For this project, I've used [this website](https://www.asmodee.co.uk/blogs/news/UNO-rules) to source the contents of a normal deck of cards in UNO.

![Standard Deck Content](./deck%20content.png)

We can see here that there is one `0` card and 2 of each card going from `1` to `9`, as shown in the visual.

![Visual of Normal Cards](./normal%20cards.png)

There also is:
- 2 reverse cards
- 2 skip cards
- 2 +2 cards
- 4 +4 cards
- 4 wild cards

## Building the Deck

We can build the deck as follows.

Imports for reference:
```py
from card import Card, Colour, CardType
```

1. Define a `deck` list to hold the cards.
```py
deck = []
```

2. Add a zero card and a pair of cards from 1 to 9 for each colour in the deck.
```py
for current in Colour: # current colour of cards
    # add one zero card
    deck += [
        Card(
            colour = current, # get the attribute from the value
            number = 0
        )
    ]

    # add the other 9 cards in pairs of two
    for i in range(9):
        deck += [
            Card(colour = current, number = i),
            Card(colour = current, number = i)
        ]

    ...
```

3. Add the special cards to the mix.
```py
    ...

    for i in range(1, 4): # Skip, +2 and Reverse
        deck += [
            Card(colour = current, type = CardType(i)),
            Card(colour = current, type = CardType(i))
        ]

    # 4 Wild cards
    deck += [
        Card(type = CardType.Wild)
        for _ in range(4)
    ]

    # 4 Wild +4 cards
    deck += [
        Card(type = CardType.WildPlus4)
        for _ in range(4)
    ]
```

## Using the Deck

We want to be able to do 2 things:
- shuffle the deck
- draw from the deck

The first is simple. We can use the `shuffle()` method in the `random` library to shuffle our deck for us.
```py
from random import shuffle

class Deck:
    def __init__(self, ...):
        ...

        shuffle(self.deck) # Shuffles the list in place        
```

And the second is also incredibly easy. We can just pop the last item off the list and because the list is already shuffled, this is equivalent to selecting a random card.
```py
class Deck:
    ...

    def draw(self) -> Card:
        return self.deck.pop() # get last card ()
```

I personally prefer this method for the O(1) time complexity when removing the last element. I think it's neat, considering its constant time complexity and that it's only one line long. I could've used `.pop()` and `random.randint()` or `random.choice()` and `.remove()` but I think this one is the best.


## Creating a Hand

Now, players want to be able to play the game, but all we have is a deck of cards. To represent the cards a player has, we can make a `Hand` class. Yes, more OOP. I promise it'll make sense soon.

```py
class Hand:
    ...
```

For this class, we don't need any parameters since all hands are empty by default.
```py
class Hand:
    "Represents a player's hand. Use `can_play_on()` with the top-most card to get a list of cards that can be played on the stack."
    
    def __init__(self) -> None:
        self._cards: List[Card] = []
```

### Getting the Cards

We can privatise the list of cards by prefixing it with an underscore. This lets us use a `@property` decorator to get the cards in a read-only fashion.

```py
class Hand:
    ...

    @property
    def cards(self) -> List[Card]:
        "Returns a list of cards in the current hand."
        return self._cards
```

### Picking up Cards

Since there's no specific universal deck of cards, we can take the deck as a parameter and use the `.draw()` method to get a card.

```py
class Hand:
    ...

    def pick_up(self, deck: Deck) -> None:
        "Append a new `Card` to this current hand."
        self._cards.append(deck.draw())
```

## Legality

In any game, the most important part is being able to discern legal moves from illegal moves. It's what makes the game fun because your friends can't instantly cheat and win the game. Where would be the fun in that?

### Examples of Legal Moves in Games

| Game | Move |
|:-:   |:-   |
| Chess | pushing a pawn two squares at the start of the game |
| Connect 4 | placing a column in a column that is not filled |
| Tic-Tac-Toe | placing a piece in an open square |
| 15 Puzzle | moving a square neighbouring the open space into the open space |

### Legality in the Game of Uno

In Uno, normal cards can be played when their colour or their number matches the card in play (at the top of the stack). Of course, some cards have special properties like skiping turns, reversing the direction of play and forcing players to pick up cards, but these can be integrated in the highest level class that controls everything about the game, so we don't need to worry about it here.

## Coding Legality

This can go in our `Hand` class because it represents the cards the player's holding anyway, so it makes sense to include a method to that class to get all legal moves (cards that can be played).

```py
from typing import List

class Hand:
    ...

    def can_play_on(card: Card) -> List[Card]:
        ...
```

### List of Cases

- The cards are the same (there can be 2 of each normal card except the `0`)
- The type of cards are the same

For our checks, we can create an inner function called `playable()` that creates a list of all the following checks and 