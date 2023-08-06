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
        if self.hp == 0:
            return True
        return False 




if __name__ == "__main__":
    s = Ship(4, Dot(1, 1), Direction(horizontal=True))
    print(s.is_alive)
    print(len(s))
    print(s.dots())

