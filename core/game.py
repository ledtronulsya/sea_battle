import sys
from board import Board
from dot import Dot
from ship import Ship
from player import User, AI
from random import choice, randint
from exceptions import *
from helper_classes import Direction
import os
from time import sleep

# Правила игры: 1 трехпалубный, 2 двухпалубных и 4 однопалубных корабля
RULES = [3, 2, 2, 1, 1, 1, 1]


class Game:
    """Класс игры"""
    def __init__(self) -> None:
        self.player_board = self.random_board()
        self.opponent_board = self.random_board(is_hidden=True)
        self.player = User(self.player_board, self.opponent_board)
        self.ai = AI(self.opponent_board, self.player_board)

    def random_board(self, is_hidden: bool = False) -> Board:
        """Генерирует случайное поле"""
        board = Board(is_hidden=is_hidden)
        for rule in RULES:
            while True:
                try:
                    dr = choice([Direction(vertical=True), Direction(horizontal=True)])
                    dr_flag = dr == Direction.vertical
                    x, y = randint(1, board.rows - rule * dr_flag), randint(1, board.columns - (1 - dr_flag))
                    head = Dot(x, y)
                    board.add_ship(Ship(rule, head, dr))
                    break
                except ShipOutOfBoudsException:
                    continue
        return board

    def start(self):
        """Начало игры"""
        self.greet()
        self.loop()

    def greet(self):
        """Приветствие игрока"""
        print("""Привет! Сыграем в морской бой?""")
    
    def loop(self):
        """Игровой цикл"""
        player_move = True
        while True:
            self._print()

            if player_move:
                player_move = self.process_move_result(self.player.move())
            else:
                player_move = self.process_move_result(self.ai.move(), False)
                sleep(2)
            
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
            print("Вы попали! Ход остается у вас")
            return True
        else:
            if not res:
                print("Противник промахнулся! Ход переходт к вам")
                return True
            print("Противник попал! Ход остается у него")
            return False
    
    def check_game(self) -> bool:
        """Проверяет, выиграл ли кто-то из игроков после хода"""
        if self.player_board.ships_alive == 0:
            print("Противник выиграл!")
            return True
        if self.opponent_board.ships_alive == 0:
            print("Вы выиграли!")
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
        sys.exit(0)


if __name__ == "__main__":
    g = Game()
    g.start()
