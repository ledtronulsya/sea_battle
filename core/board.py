from dot import Dot
from ship import Ship
from exceptions import *
from helper_classes import DotSymbol, Direction, SYMBOLS_DICT


class Board:
    """Класс игрового поля"""
    def __init__(self, is_hidden: bool = False, rows: int = 6, columns: int = 6) -> None:
        self.is_hidden = is_hidden
        self.rows, self.columns =rows, columns
        self.field = [[Dot(i + 1, j + 1) for j in range(columns + 1)] for i in range(rows + 1)]
        self.ships = []
    

    def add_headers(self):
        """Добавляет числа на первой строке и первом столбце"""
        self.field[0] = [" "] + list(map(str, range(1, self.columns + 1)))
        
    
    def add_ship(self, ship: Ship):
        """Добавляет корабль на поле"""
        if self.out(ship.head) or self.out(ship.dots()[-1]):
            raise ShipOutOfBoudsException
        self.ships.append(ship)
        self.contour(ship)
    

    def set_symbol(self, dot, symb):
        """Устаанвливает символ на поле"""
        if not self.out(dot):
            self.field[dot.x - 1][dot.y - 1].mark(symb)
    
    @staticmethod
    def get_neightbour_dots(dot: Dot, ship: Ship) -> tuple[Dot, Dot]:
        """Возвраащет соседние точки"""
        dot1 = Dot(dot.x - 1 * ship.dir.horizontal, dot.y - 1 * ship.dir.vertical)
        dot2 = Dot(dot.x + 1 * ship.dir.horizontal, dot.y + 1 * ship.dir.vertical)
        return dot1, dot2

    def contour(self, ship: Ship):
        """Помечает точки вокруг корабля, в которые нельзя ставить другие корабли"""
        dots = ship.dots()
        for dot in ship.dots():
            self.set_symbol(dot, DotSymbol.ship)
            dot1, dot2 = self.get_neightbour_dots(dot, ship)
            self.set_symbol(dot1, DotSymbol.around)
            self.set_symbol(dot2, DotSymbol.around)
        doth = Dot(dots[0].x - 1 * ship.dir.vertical, dots[0].y - 1 * ship.dir.horizontal)
        doth1, doth2 = self.get_neightbour_dots(doth, ship)
        self.set_symbol(doth, DotSymbol.around)
        self.set_symbol(doth1, DotSymbol.around)
        self.set_symbol(doth2, DotSymbol.around)
        doth = Dot(dots[-1].x + 1 * ship.dir.vertical, dots[-1].y + 1 * ship.dir.horizontal)
        doth1, doth2 = self.get_neightbour_dots(doth, ship)
        self.set_symbol(doth, DotSymbol.around)
        self.set_symbol(doth1, DotSymbol.around)
        self.set_symbol(doth2, DotSymbol.around)


    @property
    def ships_alive(self):
        """Возвращает число живых кораблей"""
        return len([ship for ship in self.ships if ship.is_alive])

    def __repr__(self):
        """Вывод доски в консоль"""
        row_pattern = "{} | {} | {} | {} | {} | {} | {} |"
        first_row = row_pattern.format(" ", *range(1, self.columns + 1))
        rows = [first_row]
        for x, i in enumerate(self.field, 1):
            symbols = []
            for dot in i:
                if not self.is_hidden:
                    symbols.append(dot.symbol)
                elif dot.symbol in (DotSymbol.ship, DotSymbol.around):
                    symbols.append(DotSymbol.simple)
                else:
                    symbols.append(dot.symbol)
            symbols = [SYMBOLS_DICT[s] for s in symbols]
            row = row_pattern.format(x, *symbols)
            rows.append(row)
        return '\n'.join(rows)
    
    def out(self, dot: Dot) -> bool:
        """Возвращает флаг, вышла ли точка за границы поля"""
        return not (1 <= dot.x <= self.rows and 1 <= dot.y <= self.columns)
    
    def find_ship_with_dot(self, dot: Dot) -> Ship | None:
        """Ищет корабль, имеющие точку dot"""
        for ship in self.ships:
            if dot in ship.dots():
                return ship
        return None

    def shot(self, dot: Dot):
        """Делает выстрел"""
        if self.out(dot):
            raise OutOfBoundException(dot)
        if self.field[dot.x - 1][dot.y - 1].used:
            raise AlreadyMarkedDotException(dot)
        ship = self.find_ship_with_dot(dot)
        if ship is None:
            self.field[dot.x - 1][dot.y - 1].mark(DotSymbol.miss)
            return False
        self.field[dot.x - 1][dot.y - 1].mark(DotSymbol.hit)
        return True


# b = Board()
# s = Ship(3, Dot(2, 2), Direction(vertical=True))
# b.add_ship(s)
# b.shot(Dot(2, 2))
# b.shot(Dot(2, 3))
# print(b)
        

        
