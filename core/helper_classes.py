from typing import NamedTuple


class Direction(NamedTuple):
    """Именованный кортеж направления корабля"""
    vertical: bool = False
    horizontal: bool = False
    # TODO: exp if vert == hor == True


class DotSymbol(NamedTuple):
    """Класс символа точки на поле"""
    simple: str = "О"
    hit: str = "X"
    miss: str = "T"
    ship: str = "■"
    around: str = "▒"

SYMBOLS_DICT = {
    DotSymbol.simple: "О",
    DotSymbol.hit: "X",
    DotSymbol.miss: "T",
    DotSymbol.ship: "■",
    DotSymbol.around: "▒",

}