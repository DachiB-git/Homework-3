
blackIcons = {"Pawn" : "♙", "Rook" : "♖", "Knight" : "♘", "Bishop" : "♗", "King" : "♔", "Queen" : "♕" }
whiteIcons = {"Pawn" : "♟", "Rook" : "♜", "Knight" : "♞", "Bishop" : "♝", "King" : "♚", "Queen" : "♛" }

import re
class Piece:
    def __init__(self, color, board, position):
        self.__color = color if color in ('White',"Black") else ""
        self._board = board
        self.__position = position
    @property
    def color(self):
        return self.__color
    @property
    def position(self):
        return self.__position
    @position.setter
    def position(self,new_position):
        if type(new_position) == tuple:
            (l,n) = new_position
            if re.fullmatch('[A-H][1-8]',f"{l}{n}"):
                self.__position = new_position
    def checkMove(self, dest):
        return False

    def move(self, dest):
        return False

    def getName(self):
        return self.__class__.__name__

    def getIcon(self):
        match(self.color):
            case 'White':
                return whiteIcons.get(self.getName())
            case "Black":
                return blackIcons.get(self.getName())
            case _:
                return None
class Knight(Piece):
    def __init__(self, color, board, position):
        super(Knight, self).__init__(color, board, position)
    def checkMove(self, dest):
        dest_to_cord = self._board.letters.index(dest[0]) * 8 + (dest[1] - 1)
        self_to_cord = self._board.letters.index(self.position[0]) * 8 + (self.position[1] - 1)
        enemy_piece = self._board.getPiece(f"{dest[0]}{dest[1]}")
        if enemy_piece and enemy_piece.getName() == "King":
            return False
        if enemy_piece:
            return abs(dest_to_cord - self_to_cord) in (6, 10, 15, 17) and enemy_piece.color != self.color
        else:
            return abs(dest_to_cord - self_to_cord) in (6, 10, 15, 17)

    def move(self, dest):
        if self.checkMove(dest):
            self.position = dest
            return True
        else:
            return False
class Rook(Piece):
    def __init__(self, color, board, position):
        super(Rook, self).__init__(color, board, position)
    def checkMove(self, dest):
        enemy_piece = self._board.getPiece(f"{dest[0]}{dest[1]}")
        if enemy_piece and enemy_piece.getName() == "King":
            return False
        if self.position[0] == dest[0]:
            if all(self._board.getPiece(f"{dest[0]}{i}") is None for i in range(min(self.position[1]+1,dest[1]),max(self.position[1]+1,dest[1]))):
                return not enemy_piece or enemy_piece.color != self.color
        elif self.position[1] == dest[1]:
            start_i = self._board.letters.index(self.position[0])
            end_i = self._board.letters.index(dest[0])
            print(start_i,end_i)
            if all(self._board.getPiece(f"{self._board.letters[i]}{self.position[1]}") is None
                   for i in range(min(start_i,end_i),max(start_i,end_i))
                   if self._board.getPiece(f"{self._board.letters[i]}{self.position[1]}") != self):
                return not enemy_piece or enemy_piece.color != self.color


    def move(self, dest):
        if self.checkMove(dest):
            self.position = dest
            return True
        else:
            return False
        
class Bishop(Piece):
    def __init__(self, color, board, position):
        super(Bishop, self).__init__(color, board, position)
    def checkMove(self, dest):
        enemy_piece = self._board.getPiece(f"{dest[0]}{dest[1]}")
        self_letter_index = self._board.letters.index(self.position[0])
        dest_letter_index = self._board.letters.index(dest[0])
        if enemy_piece and enemy_piece.getName() == "King":
            return False
        if dest[0] != self.position[0]:
            vertical_diff = abs(self_letter_index - dest_letter_index)
            lower = min(self_letter_index,dest_letter_index)
            if not enemy_piece or enemy_piece.color != self.color:
                if abs(dest[1]-self.position[1]) == 1:
                    return True
                else:
                    return all(self._board.getPiece(f'{self._board.letters[i]}{self.position[1] - (i - lower) * (1 if dest[1] < self.position[1] else -1)}') is None
                        for i in range(lower,max(self_letter_index,dest_letter_index)) if self._board.getPiece(f'{self._board.letters[i]}{self.position[1] - (i - lower) * (1 if dest[1] < self.position[1] else -1)}') != self) and \
                        abs(dest[1]-self.position[1]) == vertical_diff
            else:
                return False
        else:
            return False

    def move(self, dest):
        if self.checkMove(dest):
            self.position = dest
            return True
        else:
            return False
        
class Queen(Piece):
    def __init__(self, color, board, position):
        super(Queen, self).__init__(color, board, position)
    def checkMove(self, dest):
        print(Bishop.checkMove(self,dest))
        return Bishop.checkMove(self,dest) or Rook.checkMove(self,dest)

    def move(self, dest):
        if self.checkMove(dest):
            self.position = dest
            return True
        else:
            return False

class King(Piece):
    def __init__(self, color, board, position):
        super(King, self).__init__(color, board, position)
    def checkMove(self, dest):
        dest_to_cord = self._board.letters.index(dest[0]) * 8 + (dest[1] - 1)
        self_to_cord = self._board.letters.index(self.position[0]) * 8 + (self.position[1] - 1)
        enemy_piece = self._board.getPiece(f"{dest[0]}{dest[1]}")
        if enemy_piece and enemy_piece.getName() == "King":
            return False
        if not enemy_piece or enemy_piece.color != self:
            return abs(self_to_cord-dest_to_cord) in (7,8,9,1)

    def move(self, dest):
        if self.checkMove(dest):
            self.position = dest
            return True
        else:
            return False

class Pawn(Piece):
    def __init__(self,color,board,position):
        self.hasMoved = False
        super(Pawn, self).__init__(color,board,position)

    def checkMove(self, dest):
        dest_to_cord = self._board.letters.index(dest[0]) * 8 + (dest[1] - 1)
        self_to_cord = self._board.letters.index(self.position[0]) * 8 + (self.position[1] - 1)
        enemy_piece = self._board.getPiece(f"{dest[0]}{dest[1]}")
        if enemy_piece and enemy_piece.getName() == "King":
            return False
        if not enemy_piece:
            if self.hasMoved:
                return dest_to_cord - self_to_cord == (8 if self.color == "Black" else -8)
            else:
                path_letter = self._board.letters[self._board.letters.index(dest[0])+(1,-1)[self.color == 'Black']]
                check_tile = self._board.getPiece(f"{path_letter}{dest[1]}") \
                if dest_to_cord-self_to_cord == (16 if self.color == "Black" else -16) else None
                return dest_to_cord - self_to_cord in ((8,16) if self.color == 'Black' else (-8,-16)) and not check_tile
        elif enemy_piece.color != self.color:
            return dest_to_cord - self_to_cord in ((7,9) if self.color == "Black" else (-7,-9))
    def promotionCheck(self):
        self_to_cord = self._board.letters.index(self.position[0]) * 8 + (self.position[1] - 1)
        if self_to_cord in (range(0,8) if self.color == 'White' else range(56,64)):
            new_piece = None
            while not new_piece:
                print('Choose a piece for promotion:')
                name = input()
                for piece in self._board.pieces:
                    if piece.__name__ == name:
                        new_piece = piece(self.color,self._board,self.position)
                        self._board.board[self_to_cord] = new_piece


    def move(self, dest):
        if self.checkMove(dest):
            self.position = dest
            self.hasMoved = True
            return True
        else:
            return False

