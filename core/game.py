import sys


class Game:
    """Класс игры"""
    def __init__(self) -> None:
        self.cmds = {"exit": self._exit, "help": self._help}


    def random_board(self):
        """Генерирует случайное поле"""
        # TODO

    def start(self):
        """Начало игры"""
        self.greet()
        self.loop()

    def greet(self):
        """Приветствие игрока"""
        print("""Привет! Сыграем в морской бой? Для игры необходимо вводить команды. 
Чтобы узнать список команд, введи help""")
    
    def _help(self, args):
        """Выводит правидла игры"""
        print("""Доступные команды:
help - вывести правила игры
exit - выйти из игры
shot <row> <col> - произвести выстрел по точке (row, col), где row и col - числа от 1 до 6""")
    
    def loop(self):
        """Игровой цикл"""
        while True:
            cmd, *args = input().split()
            self.cmds[cmd](args)
    
    def _exit(self, args):
        """Выход из игры"""
        print("Приятно было провести время!")
        sys.exit(0)

g = Game()
g.start()
