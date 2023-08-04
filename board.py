from pieces import *

class Board:
    letters = ['A','B','C','D','E','F','G','H']
    pieces = [Rook,Knight,Bishop,Queen,King,Bishop,Knight,Rook]
    def __init__(self):
        self.board = []
        self.placePieces()

    def placePieces(self):
        white_back_row = [piece("White", self, ("H", i+1)) for i,piece in enumerate(Board.pieces)]
        white_pawns = [Pawn("White", self, ('G', i)) for i in range(1,9)]
        black_back_row = [piece("Black",self,("A",i+1)) for i,piece in enumerate(Board.pieces)]
        black_pawns = [Pawn("Black", self, ('B', i))for i in range(1,9)]
        self.board = black_back_row + black_pawns + ([None] * 32) + white_pawns + white_back_row
    def setPiece(self, position, piece):
        self.board[position[0]],self.board[position[1]]= None, piece

    def getPiece(self, position):
        return self.board[Board.letters.index(position[0]) * 8 + (int(position[1])-1)]
    def makeMove(self, startPosition, endPosition, player):
        moving_piece = self.getPiece(startPosition)
        if moving_piece:
            start_pos = Board.letters.index(startPosition[0]) * 8 + (int(startPosition[1])-1)
            end_pos = Board.letters.index(endPosition[0]) * 8 + (int(endPosition[1])-1)
            if moving_piece.color == player:
                if moving_piece.move((endPosition[0],int(endPosition[1]))):
                    self.setPiece((start_pos,end_pos),moving_piece)
                    if(moving_piece.getName() == 'Pawn'):
                        moving_piece.promotionCheck()
                    return True
                else:
                    print("INVALID move. Path is blocked or illegal move!")
                    return False
            else:
                print(f"INVALID move. Piece should be {player}!")
                return False
        else:
            print("INVALID move. The tile is empty!")
            return False
    def displayBoard(self):
        board_display = "   " + ' '.join(f"({i})"for i in range(1,9))
        for j in range(64):
            if (not j % 8):
                board_display += f'\n({Board.letters[j//8]})'
            board_display += f" {self.board[j].getIcon()} " if self.board[j] else ' ☐ '

        print(board_display)
