from dot import Dot
from ship import Ship
from exceptions import *
from helper_classes import DotSymbol, Direction


class Board:
    """Класс игрового поля"""
    def __init__(self, is_hidden: bool = False, rows: int = 6, columns: int = 6) -> None:
        self.is_hidden = is_hidden
        self.rows, self.columns = rows, columns
        self.field = [[Dot(i, j) for j in range(columns + 1)] for i in range(rows + 1)]
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
        self.ships.append(ship)
        self.contour(ship)
    
    def set_symbol(self, dot, symb):
        """Устаанвливает символ на поле"""
        if not self.out(dot):
            self.field[dot.x][dot.y].mark(symb)
    
    @staticmethod
    def get_neightbour_dots(dot: Dot, dr: Direction, ax: int = 0) -> tuple[Dot, Dot]:
        """Возвраащет соседние точки. Если ax=0, возвращет две соседних, 
        не соответствующих направлению корабля (если корабль вертикальный, вернет соседей по горизонтали).
        Если ax=1, вернет точки, соответствущих направлению корабля"""
        if ax == 0:
            dot1 = Dot(dot.x - 1 * dr.horizontal, dot.y - 1 * dr.vertical)
            dot2 = Dot(dot.x + 1 * dr.horizontal, dot.y + 1 * dr.vertical)
        elif ax == 1:
            dot1 = Dot(dot.x - 1 * dr.vertical, dot.y - 1 * dr.horizontal)
            dot2 = Dot(dot.x + 1 * dr.vertical, dot.y + 1 * dr.horizontal)
        return dot1, dot2

    def contour(self, ship: Ship):
        """Помечает точки вокруг корабля, в которые нельзя ставить другие корабли"""
        dots = ship.dots()
        dots_around = []
        for dot in ship.dots():
            self.set_symbol(dot, DotSymbol.ship)
            dots_around.extend(self.get_neightbour_dots(dot, ship.dir))
        doth = self.get_neightbour_dots(dots[0], ship.dir, ax=1)[0]
        dott = self.get_neightbour_dots(dots[-1], ship.dir, ax=1)[1]
        dots_around.extend([doth, dott, *self.get_neightbour_dots(doth, ship.dir), *self.get_neightbour_dots(dott, ship.dir)])
        #[self.set_symbol(d, DotSymbol.around) for d in dots_around]

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
        return True
        
