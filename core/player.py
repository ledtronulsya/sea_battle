from board import Board
from random import randint
from dot import Dot
from exceptions import *


class Player:
    """Класс игрока"""
    def __init__(self, player_board: Board, opponent_board: Board, log: bool = True):
        self.player_board = player_board
        self.opponent_board = opponent_board
        self.log = log

    def ask(self) -> Dot:
        """Спрашивет игрока, в какую клеетку произвести выстрел"""
    
    def move(self):
        while True:
            try:
                dot = self.ask()
                return self.opponent_board.shot(dot)
            except (OutOfBoundException, AlreadyMarkedDotException) as error:
                if self.log:
                    print(error)


class User(Player):
    """Класс пользователя"""

    def ask(self) -> Dot:
        x, y = map(int, input("Введите строку и столбец ячейки через пробел: ").split())
        return Dot(x, y)


class AI(Player):
    """Класс игрового бота"""

    def ask(self) -> Dot:
        return Dot(randint(1, self.opponent_board.rows), randint(1, self.opponent_board.columns))
