from core.dot import Dot


class OutOfBoundException(Exception):
    """Исключение, возникающее при попытке поставть точку вне поля"""
    def __init__(self, dot: Dot):
        msg = f"Точка с координатами ({dot.x}, {dot.y}) выходит за пределы поля"
        super().__init__(msg)


class AlreadyMarkedDotException(Exception):
    """Исключение, возникающее, когда игрок пытается выстрелить в ту точку, которая уже открыта"""
    def __init__(self, dot: Dot):
        msg = f"Вы уже стреляли в точку с координатами ({dot.x}, {dot.y})"
        super().__init__(msg)


class ShipOutOfBoudsException(Exception):
    """Исключение, возникающее, когда корабль не помещается в границы поля"""
    def __init__(self):
        msg = "Корабль частично или полностью выходит за границы поля"
        super().__init__(msg)


class ShipCollideException(Exception):
    """Исключение, возникающее, когда корабли на поле пересекаются или когда они расположены вплотную"""
    def __init__(self):
        msg = "Корабль пересекается с другим кораблем или стоит вплотную к нему"
        super().__init__(msg)