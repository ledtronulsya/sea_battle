from core.helper_classes import DotSymbol


class Dot:
    """Класс точки на игровом поле"""
    def __init__(self, x: int, y: int, is_hidden: bool = False) -> None:
        self.x = x
        self.y = y
        self.symbol = DotSymbol.simple
        self.used = False
        self.is_hidden = is_hidden
    
    def __eq__(self, other) -> bool:
        """Проверка на идентичность точек"""
        return (self.x, self.y) == (other.x, other.y)
    
    def __add__(self, shift: tuple[int, int]):
        """Возвращает новую точку с измененными координатами"""
        return Dot(self.x + shift[0], self.y + shift[1])
    
    def __sub__(self, shift: tuple[int, int]):
        """Возвращает новую точку с измененными координатами"""
        return Dot(self.x - shift[0], self.y - shift[1])
    
    def __repr__(self):
        """Вывод точки в консоль"""
        return f"Dot({self.x}, {self.y})"
    
    def __str__(self):
        if self.is_hidden and self.symbol in (DotSymbol.ship, DotSymbol.around):
            return DotSymbol.simple
        return self.symbol
    
    def mark(self, symb):
        """Устанавливает флаг, что по точке был произведен выстрел"""
        self.symbol = symb
        if symb in (DotSymbol.hit, DotSymbol.miss):
            self.used = True