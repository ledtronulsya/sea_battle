from dot import Dot
from helper_classes import Direction


class Ship:
    """Класс корабля"""
    def __init__(self, length: int, head: Dot, direction: Direction) -> None:
        self.length = length
        self.head = head
        self.dir = direction
        self.hp = length

    @property
    def is_alive(self):
        """Возвращает булевое значение, потоплен корабль или нет"""
        return self.hp > 0 
    
    @staticmethod
    def get_neightbour_dots(dot: Dot, dr: Direction, ax: int = 0) -> tuple[Dot, Dot]:
        """Возвраащет соседние точки. Если ax=0, возвращет две соседних, 
        не соответствующих направлению корабля (если корабль вертикальный, вернет соседей по горизонтали,
        и наоборото). Если ax=1, вернет точки, соответствущие направлению корабля"""
        if ax == 0:
            dot1 = Dot(dot.x - 1 * dr.horizontal, dot.y - 1 * dr.vertical)
            dot2 = Dot(dot.x + 1 * dr.horizontal, dot.y + 1 * dr.vertical)
        elif ax == 1:
            dot1 = Dot(dot.x - 1 * dr.vertical, dot.y - 1 * dr.horizontal)
            dot2 = Dot(dot.x + 1 * dr.vertical, dot.y + 1 * dr.horizontal)
        return dot1, dot2

    def get_around_dots(self) -> list[Dot]:
        """Возвращает точки, окружающие корабль"""
        dots = self.dots()
        dots_around = []
        for dot in dots:
            dots_around.extend(self.get_neightbour_dots(dot, self.dir))
        doth = self.get_neightbour_dots(dots[0], self.dir, ax=1)[0]
        dott = self.get_neightbour_dots(dots[-1], self.dir, ax=1)[1]
        dots_around.extend([doth, dott, *self.get_neightbour_dots(doth, self.dir), 
                            *self.get_neightbour_dots(dott, self.dir)])
        return dots_around

    def __len__(self):
        """Возвращает длину корабля"""
        return self.length
    
    def dots(self) -> list[Dot]:
        """Возвращает клетки, которые занимает корабль"""
        ship_dots = []
        for i in range(len(self)):
            ship_dots.append(
                self.head + (self.dir.vertical * i, self.dir.horizontal * i)
            )
        return ship_dots
    
    def hit(self):
        """Производит попадание по точку корабля"""
        self.hp -= 1
    
    def __str__(self) -> str:
        if self.dir == Direction(vertical=True):
            return f"Ship({len(self)}, {repr(self.head)}, vertical=True, {self.hp})"
        return f"Ship({len(self)}, {repr(self.head)}, horizontal=True, {self.hp})"
    
    def __repr__(self):
        return str(self)