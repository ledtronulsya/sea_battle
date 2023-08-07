class NamedTuple(dict):
    """Класс, позволяюший получать значения из словаря через точку"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class HitFlag(NamedTuple):
    """Класс флага для попадания/убийства"""
    def __init__(self, kill=False, hit=False):
        self["kill"] = kill
        self["hit"] = hit
    

class Direction(NamedTuple):
    """Именованный кортеж направления корабля"""
    def __init__(self, vertical=False, horizontal=False):
        self["vertical"] = vertical
        self["horizontal"] = horizontal


DotSymbol = NamedTuple({
    "simple": "□",
    "hit": "⊠",
    "miss": "T",
    "ship": "■",
    "around":"▦",
})

