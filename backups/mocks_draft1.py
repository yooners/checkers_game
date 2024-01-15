"""
Stub and mock implementations of the Checkers class
"""

from enum import Enum
PieceColor = Enum("PieceColor", ["BLACK", "RED"])
"""
Enum type for representing piece colors.
"""


class BoardStub:
    """
    Stub implementation of Board class
    """

    def __init__(self, size, p1_name = "Player 1", p2_name = "Player 2"):
        self.dims = (size * 2) + 2
        self._board = [[None] * self.dims for _ in range(self.dims)]
        self.p1_name = p1_name
        self.p2_name = p2_name
        self.curr_player = 1
        self._winner = None

    def _init_pieces(self):
        pass
    
    def __str__(self):
        return "BOARD"

    def get_piece(self, coordinates):
        row, col = coordinates
        return self._board[row][col]

    def player_legal_moves(self, player):
        return (self._board[0][0], (1, 1))
   
    def get_winner(self):
        return self.p1_name


class PieceStub:
    """
    Stub implementation of Piece class
    """

    def __init__(self, player, x, y, type, board):
        self.player = player
        self.x = x
        self.y = y
        self.type = type
        self.board = board

    def __str__(self):
        return self.type

    def move(self, location, player): 
        pass

    def get_legal_moves(self):
        return [(1, 1), (2, 2)]

    def is_legal_move(self, move):
        return True



class BoardMock:
    """
    Mock implementation of Board class

    Expected behaviors:
    - Plays on a checkers board where n = 1
    - Each player starts with 1 piece and 1 king
    - Does not include jumps for now
    - Game ends if it's player x's turn but they have no legal moves
    """

    def __init__(self, size = 1, p1_name = "black", p2_name = "red"):
        self.dims = (size * 2) + 2
        self._board = [[None] * self.dims for _ in range(self.dims)]
        self.p1_name = p1_name
        self.p2_name = p2_name
        self.p1, self.p2 = self._init_pieces()
        self.curr_player = 1
        self._winner = None

    def _init_pieces(self):
        p1_pieces = []
        p2_pieces = []
        p1_pieces.append(PieceMock(self.p1_name, 3, 0, "piece", self))
        p1_pieces.append(PieceMock(self.p1_name, 3, 2, "king", self))
        p2_pieces.append(PieceMock(self.p2_name, 0, 1, "piece", self))
        p2_pieces.append(PieceMock(self.p2_name, 0, 3, "king", self))
        self._board[0][1] = p2_pieces[0]
        self._board[0][3] = p2_pieces[1]
        self._board[3][0] = p1_pieces[0]
        self._board[3][2] = p1_pieces[1]
        return p1_pieces, p2_pieces
    
    def __str__(self):
        return "BOARD"

    def get_piece(self, coordinates):
        row, col = coordinates
        return self._board[row][col]

    def player_legal_moves(self, player):
        moves = []
        if player == self.p1_name:
            if self.p1 != []:
                for piece in self.p1:
                    all_moves = piece.get_legal_moves()
                    for move in all_moves:
                        moves.append((piece, move))
        if player == self.p2_name:
            if self.p2 != []:
                for piece in self.p2:
                    all_moves = piece.get_legal_moves()
                    for move in all_moves:
                        moves.append((piece, move))
        return moves

   
    def get_winner(self):
        if self.player_legal_moves(self.p1_name) == [] and self.curr_player == 1:
            return "red wins!"
        if self.player_legal_moves(self.p2_name) == [] and self.curr_player == 2:
            return "black wins!"
        return None


class PieceMock:
    """
    Mock implementation of Piece class
    """

    def __init__(self, player, x, y, type, board):
        self.player = player
        self.x = x
        self.y = y
        self.type = type
        self.board = board

    def __str__(self):
        return self.type

    def move(self, location): 
        if (location[0] >= self.board.dims or location[1] >= self.board.dims
        or not self.is_legal_move(location)):
            raise ValueError("not a valid move") 
        else:
            self.board._board[self.x][self.y] = None
            self.x = location[0]
            self.y = location[1]
            self.board._board[self.x][self.y] = self
            if self.board.curr_player == 1:
                self.board.curr_player = 2
            elif self.board.curr_player == 2:
                self.board.curr_player = 1


    def get_legal_moves(self):
        legal_moves = []
        left = right = left_back = right_back = 0
        if self.player == "black":
            if self.x - 1 >= 0 and self.y - 1 >= 0:
                left = self.board._board[self.x - 1][self.y - 1]
            if self.x - 1 >= 0 and self.y + 1 < self.board.dims:
                right = self.board._board[self.x - 1][self.y + 1]
            if self.type == "king":
                if self.x + 1 < self.board.dims and self.y - 1 >= 0:
                    left_back = self.board._board[self.x + 1][self.y - 1]
                if self.x + 1 < self.board.dims and self.y + 1 < self.board.dims:
                    right_back = self.board._board[self.x + 1][self.y + 1]
            
            if left is None:
                legal_moves.append((self.x - 1, self.y - 1))
            if right is None:
                legal_moves.append((self.x - 1, self.y + 1))
            if left_back is None:
                legal_moves.append((self.x + 1, self.y - 1))
            if right_back is None:
                legal_moves.append((self.x + 1, self.y + 1))   

        if self.player == "red":
            if self.x + 1 < self.board.dims and self.y - 1 >= 0:
                left = self.board._board[self.x + 1][self.y - 1]
            if self.x + 1 < self.board.dims and self.y + 1 < self.board.dims:
                right = self.board._board[self.x + 1][self.y + 1]
            if self.type == "king":
                if self.x - 1 >= 0 and self.y - 1 >= 0:
                    left_back = self.board._board[self.x - 1][self.y - 1]
                if self.x - 1 >= 0 and self.y + 1 >= 0:
                    right_back = self.board._board[self.x - 1][self.y + 1]
            
            if left is None:
                legal_moves.append((self.x + 1, self.y - 1))
            if right is None:
                legal_moves.append((self.x + 1, self.y + 1))
            if left_back is None:
                legal_moves.append((self.x - 1, self.y - 1))
            if right_back is None:
                legal_moves.append((self.x - 1, self.y + 1))  
        return legal_moves

                
    def is_legal_move(self, move):
        return move in self.get_legal_moves()