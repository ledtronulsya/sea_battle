import sys
from core.board import Board
from core.dot import Dot
from core.ship import Ship
from core.player import User, AI
from random import choice, randint
from core.exceptions import *
from core.helper_classes import Direction, HitFlag
from time import sleep

# Правила игры: 1 трехпалубный, 2 двухпалубных и 4 однопалубных корабля
RULES = [3, 2, 2, 1, 1, 1, 1]


class Game:
    """Класс игры"""
    def __init__(self) -> None:
        player_board = self.random_board()
        while player_board is None:
            player_board = self.random_board()
        self.player_board = player_board

        ai_board = self.random_board(is_hidden=True)
        while ai_board is None:
            ai_board = self.random_board(is_hidden=True)
        self.opponent_board = ai_board

        self.player = User(self.player_board, self.opponent_board)
        self.ai = AI(self.opponent_board, self.player_board, log=False)

    def random_board(self, is_hidden: bool = False) -> Board | None:
        """Генерирует случайное поле"""
        board = Board(is_hidden=is_hidden)
        for rule in RULES:
            for i in range(1000):
                try:
                    dr = choice([Direction(vertical=True), Direction(horizontal=True)])
                    x, y = randint(1, board.rows), randint(1, board.columns)
                    head = Dot(x, y)
                    board.add_ship(Ship(rule, head, dr))
                    break
                except (ShipOutOfBoudsException, ShipCollideException):
                    continue
            if i == 999:
                return None
        return board

    def start(self):
        """Начало игры"""
        self.greet()
        self.loop()

    def greet(self):
        """Приветствие игрока"""
        print("""Привет! Это игра 'Морской бой'. 
Поля игрока и противника создаются случайным образом. Вы ходите первым.
Чтобы сделать ход, нужно ввести координаты точки, по которой вы хотите произвести выстрел.
Координаты точки задаются двумя числами, записанными через пробел - номером строки и номером столбца.""")
    
    def loop(self):
        """Игровой цикл"""
        player_move = True
        while True:
            self._print()
            if player_move:
                player_move = self.process_move_result(self.player.move())
            else:
                sleep(2)
                player_move = self.process_move_result(self.ai.move(), False)
            
            check_result = self.check_game()
            if check_result:
                self._print()
                self._exit()
    
    @staticmethod
    def process_move_result(res, player=True) -> bool:
        """Вывод информации в зависимости от того, кто ходил, и от того, попал ли ходивший.
        Возвращает флаг, делает ли следующий игрое игрок"""
        if player:
            if not res:
                print("Вы промахнулись! Ход переходит к противнику")
                return False
            if res == HitFlag(kill=True):
                print("Корабль потоплен! Ход остается у вас")
            else:
                print("Вы попали! Ход остается у вас")
            return True
        else:
            if not res:
                print("Противник промахнулся! Ход переходит к вам")
                return True
            if res == HitFlag(kill=True):
                print("Противник потопил корабль! Ход остается у него")
            else:
                print("Противник попал! Ход остается у него")
            return False
    
    def check_game(self) -> bool:
        """Проверяет, выиграл ли кто-то из игроков после хода"""
        if self.player_board.ships_alive == 0:
            print("--- Противник выиграл! ---")
            return True
        if self.opponent_board.ships_alive == 0:
            print("--- Вы выиграли! ---")
            return True
        return False

    def _print(self):
        """Выводит в консоль поля"""
        player = repr(self.player_board).split("\n")
        ai = repr(self.opponent_board).split("\n")
        for p, o in zip(player, ai):
            print(p + '\t' + o)
    
    def _exit(self):
        """Выход из игры"""
        print("Приятно было провести время!")
        sleep(2)
        sys.exit(0)