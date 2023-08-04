from board import Board
from pieces import *
import re
class Chess:
    def __init__(self):
        self.board = Board()
        self.currentPlayer = 'White'

    def swapPlayers(self):
        self.currentPlayer = {'Black': 'White', 'White': 'Black'}[self.currentPlayer]
    
    def isStringValidMove(self, moveStr):
        parts = moveStr.split()

        if moveStr and all(re.fullmatch('[A-K][1-8]',part) for part in parts) and parts[0] != parts[1]:
            return True
        else:
            return False
    def play(self):
        while(True):
            self.board.displayBoard()
            print(f"{self.currentPlayer}'s turn. Enter a move:")
            move = input()
            while not self.isStringValidMove(move):
                print(f"{self.currentPlayer}'s turn. Enter a move:")
                move = input()
            res = self.board.makeMove(*move.split(), self.currentPlayer)
            while (not res):
                print(f"{self.currentPlayer}'s turn. Enter a move:")
                move = input()
                res = self.board.makeMove(*move.split(), self.currentPlayer)
            self.swapPlayers()
            if(move == 'EXIT'):
                break

#
if __name__ == "__main__":
    game = Chess()
    game.play()

