from board import Board
from random import randint
from dot import Dot


class Player:
    """Класс игрока"""
    def __init__(self, player_board: Board, opponent_board: Board, show_errors: bool = True):
        self.player_board = player_board
        self.opponent_board = opponent_board
        self.show_errors = show_errors

    def ask(self) -> Dot:
        """Спрашивет игрока, в какую клеетку произвести выстрел"""
    
    def move(self):
        while True:
            


class User(Player):
    """Класс пользователя"""

    def ask(self):
        pass


class AI(Player):
    """Класс игрового бота"""

    def ask(self) -> Dot:
        return Dot(randint(1, self.opponent_board.rows), randint(1, self.opponent_board.columns))
