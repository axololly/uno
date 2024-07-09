from __future__ import annotations
from enum import Enum
from errors import NotCompatibleError

class Colour(Enum):
    Red = 1
    Green = 2
    Yellow = 3
    Blue = 4

class CardType(Enum):
    Normal = 0
    Skip = 1
    Plus2 = 2
    Reverse = 3
    WildPlus4 = 4
    Wild = 5


class Card:
    def __init__(
        self,
        /,
        colour: Colour = None,
        number: int = None,
        type: CardType = CardType.Normal
    ):
        # check colour is Colour enum
        if colour:
            if not isinstance(colour, Colour):
                raise TypeError('colour parameter is not of type Colour.')

        # check number is an integer
        if number: # if number is not None
            if not isinstance(number, int): # if number is not an integer
                raise TypeError('number parameter is given but it is not integer.')
            
            if not 0 <= number < 10: # if number is not valid
                raise ArithmeticError('not a valid card number. Number must be a single digit between 1 and 9.')
        
        # check type is CardType
        if not isinstance(type, CardType):
            raise TypeError('type parameter is not of type CardType.')
        
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

        self.colour = colour
        self.number = number
        self.type = type

    
    def __hash__(self) -> int:
        return hash((self.colour, self.number, self.type))

    def __eq__(self, other: Card) -> bool:
        if not isinstance(other, Card): # if the other object is not a 
            raise NotCompatibleError(f'Card instance cannot be compared with item of type {type(other)}.')

        return all([
            self.colour == other.colour,
            self.number == other.number,
            self.type == other.type
        ])