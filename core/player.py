from core.board import Board
from random import randint
from core.dot import Dot
from core.exceptions import *


class Player:
    """Класс игрока"""
    def __init__(self, player_board: Board | None = None, opponent_board: Board | None = None, log: bool = True):
        self.player_board = player_board
        self.opponent_board = opponent_board
        self.log = log

    def ask(self) -> Dot:
        """Спрашивет игрока, в какую клеетку произвести выстрел"""
    
    def set_player_board(self, player_board: Board):
        """Устанавливает поле игрока"""
        self.player_board = player_board
    
    def set_opponent_board(self, opponent_board: Board):
        """Устанавливат поле противника"""
        self.opponent_board = opponent_board
    
    def move(self):
        while True:
            try:
                dot = self.ask()
                return self.opponent_board.shot(dot)
            except (OutOfBoundException, AlreadyMarkedDotException) as error:
                if self.log:
                    print(error)
            except ValueError as error:
                if self.log:
                    print("Координаты введены некорректно!")


class User(Player):
    """Класс пользователя"""

    def ask(self) -> Dot:
        x, y = map(int, input(
            "Введите строку и столбец ячейки, которую вы хотите открыть, через пробел: "
        ).split())
        return Dot(x, y)


class AI(Player):
    """Класс игрового бота"""

    def ask(self) -> Dot:
        return Dot(randint(1, self.opponent_board.rows), randint(1, self.opponent_board.columns))
