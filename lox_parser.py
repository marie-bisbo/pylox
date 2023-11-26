from lox_token import Token
from expression import *
from token_type import TokenType

class Parser:
    tokens: list[Token]
    current: int = 0

    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens

    def expression(self) -> Expression:
        return self.equality()

    def equality(self) -> Expression:
        pass

    def match(self, *types: TokenType) -> bool:
        for type in types:
            pass

    def check(self) -> bool:
        pass

    def advance(self) -> Token:
        pass

    def is_at_end(self) -> bool:
        pass

    def peek(self) -> Token:
        pass

    def previous(self) -> Token:
        pass