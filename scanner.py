from lox_token import Token
from token_type import TokenType, keywords

class Scanner:
    source: str
    tokens: list[Token] = []

    start: int = 0
    current: int = 0
    line: int = 0

    def __init__(self, source: str) -> None:
        self.source = source

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))

        for token in self.tokens:
            print(f"TOKEN: {token}")
        return self.tokens

    def scan_token(self):
        c: chr = self.advance()
        match c:
            case '(': 
                self.add_token(TokenType.LEFT_PAREN)
            case ')': 
                self.add_token(TokenType.RIGHT_PAREN)
            case '{': 
                self.add_token(TokenType.LEFT_BRACE)
            case '}': 
                self.add_token(TokenType.RIGHT_BRACE)
            case ',': 
                self.add_token(TokenType.COMMA)
            case '.': 
                self.add_token(TokenType.DOT)
            case '-': 
                self.add_token(TokenType.MINUS)
            case '+': 
                self.add_token(TokenType.PLUS)
            case ';': 
                self.add_token(TokenType.SEMICOLON)
            case '*': 
                self.add_token(TokenType.STAR)
            case '!':
                token = TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG
                self.add_token(token)
            case '=':
                token = TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL
                self.add_token(token)
            case '<':
                token = TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS
                self.add_token(token)
            case '>':
                token = TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER
                self.add_token(token)
            case '/':
                if self.match('/'):
                    while self.peek() != '\n' and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token(TokenType.SLASH)
            case ' ':
                pass
            case '\r':
                pass
            case '\t':
                pass
            case '\n':
                self.line += 1
            case '"':
                self.string()
            case _:
                if self.is_digit(c):
                    self.number()
                elif self.is_alpha(c):
                    self.identifier()
                else:
                    pass
                    # error(self.line, "Unexpected character")

    def string(self) -> None:
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.is_at_end():
            print("Unterminated string")
            return
        self.advance()
        value: str = self.source[self.start + 1: self.current - 1]
        self.add_token_with_literal(TokenType.STRING, value)

    def number(self) -> None:
        while self.is_digit(self.peek()):
            self.advance()
        if self.peek() == '.' and self.is_digit(self.peek_next()):
            self.advance()
        while self.is_digit(self.peek()):
            self.advance()
        self.add_token_with_literal(TokenType.NUMBER, float(self.source[self.start: self.current]))

    def identifier(self):
        while self.is_alphanumeric(self.peek()):
            self.advance()
        text: str = self.source[self.start: self.current]
        token_type: TokenType = keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(token_type)
        

    def match(self, expected: chr) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self) -> chr:
        if self.is_at_end():
            return '\0'

        return self.source[self.current]

    def peek_next(self) -> chr:
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def is_digit(self, c: chr) -> bool:
        return c >= '0' and c <= '9'

    def is_alpha(self, c: chr) -> bool:
        return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or (c == '_')

    def is_alphanumeric(self, c: chr) -> bool:
        return self.is_digit(c) or self.is_alpha(c)

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def advance(self) -> chr:
        current_char = self.source[self.current]
        self.current += 1
        return current_char

    def add_token(self, token_type: TokenType) -> None:
        self.add_token_with_literal(token_type, None)

    def add_token_with_literal(self, token_type: TokenType, literal: object) -> None:
        text: str = self.source[self.start: self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))