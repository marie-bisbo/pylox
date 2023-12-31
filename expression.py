from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from lox_token import Token


class Visitor(ABC):
    @abstractmethod
    def visit_binary_expression(self, expression: Binary) -> Any:
        pass

    @abstractmethod
    def visit_grouping_expression(self, expression: Grouping) -> Any:
        pass

    @abstractmethod
    def visit_literal_expression(self, expression: Literal) -> Any:
        pass

    @abstractmethod
    def visit_unary_expression(self, expression: Unary) -> Any:
        pass

    def parenthesize(self, name: str, *expressions: Expression) -> str:
        expression_string = " ".join(
            expression.accept(self) for expression in expressions
        )

        return f"({name} {expression_string})"


class AstPrinter(Visitor):
    def print_ast(self, expression: Expression) -> str:
        return expression.accept(self)

    def visit_binary_expression(self, expression: Binary) -> str:
        return self.parenthesize(
            expression.operator.lexeme, expression.left, expression.right
        )

    def visit_grouping_expression(self, expression: Grouping) -> str:
        return self.parenthesize("group", expression.expression)

    def visit_literal_expression(self, expression: Literal) -> str:
        return "nil" if expression.value is None else str(expression.value)

    def visit_unary_expression(self, expression: Unary) -> str:
        return self.parenthesize(expression.operator.lexeme, expression.right)


@dataclass
class Expression(ABC):
    @abstractmethod
    def accept(cls, visitor: Visitor) -> Any:
        pass


@dataclass
class Binary(Expression):
    left: Expression
    operator: Token
    right: Expression

    def accept(cls, visitor: Visitor) -> None:
        return visitor.visit_binary_expression(cls)


@dataclass
class Grouping(Expression):
    expression: Expression

    def accept(cls, visitor: Visitor) -> None:
        return visitor.visit_grouping_expression(cls)


@dataclass
class Literal(Expression):
    value: object

    def accept(cls, visitor: Visitor) -> None:
        return visitor.visit_literal_expression(cls)


@dataclass
class Unary(Expression):
    operator: Token
    right: Expression

    def accept(cls, visitor: Visitor) -> None:
        return visitor.visit_unary_expression(cls)
