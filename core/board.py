from core.dot import Dot
from core.ship import Ship
from core.exceptions import *
from core.helper_classes import DotSymbol, Direction, HitFlag


class Board:
    """Класс игрового поля"""
    def __init__(self, is_hidden: bool = False, rows: int = 6, columns: int = 6) -> None:
        self.is_hidden = is_hidden
        self.rows, self.columns = rows, columns
        self.field = [[Dot(i, j, is_hidden) for j in range(columns + 1)] for i in range(rows + 1)]
        self.add_headers()
        self.ships = []

    def add_headers(self):
        """Добавляет чисел на первой строке и первом столбце"""
        self.field[0] = [" "] + list(range(1, self.columns + 1))
        for row in range(1, self.rows + 1):
            self.field[row][0] = row

    def add_ship(self, ship: Ship):
        """Добавляет корабль на поле"""
        if self.out(ship.head) or self.out(ship.dots()[-1]):
            raise ShipOutOfBoudsException
        all_ship_dots = ship.dots() + ship.get_around_dots()
        for dot in all_ship_dots:
            if not self.out(dot) and not self.find_ship_with_dot(dot) is None:
                raise ShipCollideException
        self.ships.append(ship)
        if not self.is_hidden:
            [self.set_symbol(dot, DotSymbol.ship) for dot in ship.dots()]
            self.contour(ship)
    
    def set_symbol(self, dot, symb):
        """Устаанвливает символ на поле"""
        if not self.out(dot):
            self.field[dot.x][dot.y].mark(symb)

    def contour(self, ship: Ship):
        """Помечает точки вокруг корабля, в которые нельзя ставить другие корабли"""
        for dot in ship.get_around_dots():
            if not self.out(dot) and self.field[dot.x][dot.y].symbol == DotSymbol.simple:
                self.field[dot.x][dot.y].mark(DotSymbol.around)

    @property
    def ships_alive(self) -> int:
        """Возвращает число живых кораблей"""
        return len([ship for ship in self.ships if ship.is_alive])

    def __repr__(self) -> str:
        """Вывод доски в консоль"""
        return '\n'.join([" | ".join(map(str, row)) + " |" for row in self.field])
    
    def out(self, dot: Dot) -> bool:
        """Возвращает флаг, вышла ли точка за границы поля"""
        return not (1 <= dot.x <= self.rows and 1 <= dot.y <= self.columns)
    
    def find_ship_with_dot(self, dot: Dot) -> Ship | None:
        """Ищет корабль, имеющий точку dot"""
        for ship in self.ships:
            if dot in ship.dots():
                return ship
        return None

    def shot(self, dot: Dot) -> bool:
        """Делает выстрел"""
        if self.out(dot):
            raise OutOfBoundException(dot)
        if self.field[dot.x][dot.y].used:
            raise AlreadyMarkedDotException(dot)
        ship = self.find_ship_with_dot(dot)
        if ship is None:
            self.field[dot.x][dot.y].mark(DotSymbol.miss)
            return False
        self.field[dot.x][dot.y].mark(DotSymbol.hit)
        ship.hit()
        return HitFlag(kill=True) if not ship.is_alive else HitFlag(hit=True) 
        
