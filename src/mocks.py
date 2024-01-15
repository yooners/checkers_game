"""
Final stub and mock implementation of Checkers Board.
"""

import copy
from checkers import PieceColor, PieceType

class BoardStub:
    """
    Real implementation of a board class.
    """

    def __init__(self, num_rows, num_cols):
        self.rows = num_rows
        self.cols = num_cols
        self.board = [[None] * num_cols for _ in range(num_rows)]

    def to_piece_grid(self):
        #only for TUI
        return copy.deepcopy(self.board)

    def get_piece(self, coordinates):
        row, col = coordinates
        return self.board[row][col]

class CheckersStub:
    """
    Stub implementation of checkers class. Expected behaviors:
    - Plays on a checkers board where n = 1
    - Each player starts with 1 piece and 1 king
    - Moves do not include jumps
    - Game ends if it's player x's turn but they have no legal moves
    """

    def __init__(self,size=1):
        # int: The size parameter passed to __init__
        self.size = size

        self.dims = (size * 2) + 2
        self.board = BoardStub(self.dims, self.dims)
        self.grid = self.board.board
        self.p1_color = PieceColor.BLACK
        self.p2_color = PieceColor.RED
        self.p1, self.p2 = self._init_pieces()
        self.curr_player = 1
        self._winner = None
        self.move_counter = 0
        self.draw_counter = 0   

    def _init_pieces(self):
        p1_pieces = []
        p2_pieces = []
        p1_pieces.append(PieceStub(self.p1_color, 3, 0, self))
        p1_pieces.append(PieceStub(self.p1_color, 3, 2, self, PieceType.KING))
        p2_pieces.append(PieceStub(self.p2_color, 0, 1, self))
        p2_pieces.append(PieceStub(self.p2_color, 0, 3, self, PieceType.KING))
        self.grid[0][1] = p2_pieces[0]
        self.grid[0][3] = p2_pieces[1]
        self.grid[3][0] = p1_pieces[0]
        self.grid[3][2] = p1_pieces[1]
        return p1_pieces, p2_pieces

    def player_legal_moves(self, color):
        moves = []
        if color == self.p1_color:
            if self.p1 != []:
                for piece in self.p1:
                    all_moves = piece.get_legal_moves()
                    if piece.get_legal_moves() != []:
                        moves.append((piece, all_moves))
        if color == self.p2_color:
            if self.p2 != []:
                for piece in self.p2:
                    all_moves = piece.get_legal_moves()
                    if piece.get_legal_moves() != []:
                        moves.append((piece, all_moves))
        return moves
   
    def get_winner(self):
        return None

    def is_done(self):
        if self.get_winner() is None:
            return False
        return True

    def move_manual(self, old_loc, new_loc):
        assert old_loc[0] >= 0 and old_loc[0] < self.dims and old_loc[1] >= 0 \
            and old_loc[1] < self.dims
        assert new_loc[0] >= 0 and new_loc[0] < self.dims and new_loc[1] >= 0 \
            and new_loc[1] < self.dims

        self.grid[new_loc[0]][new_loc[1]] = self.grid[old_loc[0]][old_loc[1]]
        self.grid[old_loc[0]][old_loc[1]] = None
        self.grid[new_loc[0]][new_loc[1]].row = new_loc[0]
        self.grid[new_loc[0]][new_loc[1]].col = new_loc[1]

class PieceStub:
    """
    Mock class for representing a checkers piece
    """

    def __init__(self, color, row, col, game, type = PieceType.PIECE):
        self.color = color
        self.row = row
        self.col = col
        self.type = type
        self.game = game
    
    def _phantom_step(self, location):
        r, c = location
        self.row = r
        self.col = c

    def move(self, location):
        if (location[0][0] >= self.game.dims or location[0][1] >= self.game.dims
        or not self.is_legal_move(location)):
            raise ValueError("not a valid move") 
        else:
            self.game.grid[self.row][self.col] = None
            self.row = location[0][0]
            self.col = location[0][1]
            self.game.grid[self.row][self.col] = self
            if self.game.curr_player == 1:
                self.game.curr_player = 2
            elif self.game.curr_player == 2:
                self.game.curr_player = 1

    def get_legal_moves(self):
        return [[(2,1), (1,2)], [(2,3), (1,2)], [(2,3), (1,4)]]

    def is_legal_move(self, move):
        return move in self.get_legal_moves()

    def __repr__(self):
        if self.type == PieceType.PIECE:
            return f'PIECE({self.row},{self.col})'
        if self.type == PieceType.KING:
            return f'KING({self.row},{self.col})'
        return "ERROR"


class BoardMock:
    """
    Real implementation of a board class.
    """

    def __init__(self, num_rows, num_cols):
        self.rows = num_rows
        self.cols = num_cols
        self.board = [[None] * num_cols for _ in range(num_rows)]

    def to_piece_grid(self):
        #only for TUI
        return copy.deepcopy(self.board)

    def get_piece(self, coordinates):
        r, c = coordinates
        if r >= self.rows or c >= self.cols:
            raise ValueError("Coordinates not on board!")
        if self.board[r][c] is None:
            raise ValueError("No piece here!")
        else:
            return self.board[r][c]
        #row, col = coordinates
        #return self.board[row][col]


class CheckersMock:
    """
    Mock implementation of checkers class. Expected behaviors:
    - Each player starts with 1 piece and 1 king
    - Moves do not include jumps
    - Game ends if it's player x's turn but they have no legal moves
    """

    def __init__(self,size):
        # int: The size parameter passed to __init__
        self.size = size

        self.dims = (size * 2) + 2
        self.board = BoardMock(self.dims, self.dims)
        self.grid = self.board.board
        self.p1_color = PieceColor.BLACK
        self.p2_color = PieceColor.RED
        self.p1, self.p2 = self._init_pieces()
        self.curr_player = 1
        self._winner = None
        self.move_counter = 0
        self.draw_counter = 0   

    def _init_pieces(self):
        p1_pieces = []
        p2_pieces = []
        p1_pieces.append(PieceMock(self.p1_color, self.dims-1, 0, self))
        p1_pieces.append(PieceMock(self.p1_color, self.dims-1, 2, self, PieceType.KING))
        p2_pieces.append(PieceMock(self.p2_color, 0, 1, self))
        p2_pieces.append(PieceMock(self.p2_color, 0, 3, self, PieceType.KING))
        self.grid[0][1] = p2_pieces[0]
        self.grid[0][3] = p2_pieces[1]
        self.grid[self.dims-1][0] = p1_pieces[0]
        self.grid[self.dims-1][2] = p1_pieces[1]
        return p1_pieces, p2_pieces

    def player_legal_moves(self, color):
        moves = []
        if color == self.p1_color:
            if self.p1 != []:
                for piece in self.p1:
                    all_moves = piece.get_legal_moves()
                    if piece.get_legal_moves() != []:    
                        moves.append((piece, all_moves))
        if color == self.p2_color:
            if self.p2 != []:
                for piece in self.p2:
                    all_moves = piece.get_legal_moves()
                    if piece.get_legal_moves() != []:
                        moves.append((piece, all_moves))
        return moves
   
    def get_winner(self):
        if self.player_legal_moves(self.p1_color) == [] and self.curr_player == 1:
            return "red wins!"
        if self.player_legal_moves(self.p2_color) == [] and self.curr_player == 2:
            return "black wins!"
        return None

    def is_done(self):
        if self.get_winner() is None:
            return False
        return True

    def move_manual(self, old_loc, new_loc):
        assert old_loc[0] >= 0 and old_loc[0] < self.dims and old_loc[1] >= 0 \
            and old_loc[1] < self.dims
        assert new_loc[0] >= 0 and new_loc[0] < self.dims and new_loc[1] >= 0 \
            and new_loc[1] < self.dims

        self.grid[new_loc[0]][new_loc[1]] = self.grid[old_loc[0]][old_loc[1]]
        self.grid[old_loc[0]][old_loc[1]] = None
        self.grid[new_loc[0]][new_loc[1]].row = new_loc[0]
        self.grid[new_loc[0]][new_loc[1]].col = new_loc[1]

class PieceMock:
    """
    Mock class for representing a checkers piece
    """

    def __init__(self, color, row, col, game, type = PieceType.PIECE):
        self.color = color
        self.row = row
        self.col = col
        self.type = type
        self.game = game
    

    def _phantom_step(self, location):
        r, c = location
        self.row = r
        self.col = c


    def move(self, location): 
        if (location[0][0] >= self.game.dims or location[0][1] >= self.game.dims
        or not self.is_legal_move(location)):
            raise ValueError("not a valid move") 
        else:
            self.game.grid[self.row][self.col] = None
            self.row = location[0][0]
            self.col = location[0][1]
            self.game.grid[self.row][self.col] = self
            if self.game.curr_player == 1:
                self.game.curr_player = 2
            elif self.game.curr_player == 2:
                self.game.curr_player = 1

    def get_legal_moves(self):
        legal_moves = []
        left = right = left_back = right_back = 0
        if self.color == PieceColor.BLACK:
            if self.row - 1 >= 0 and self.col - 1 >= 0:
                left = self.game.grid[self.row - 1][self.col - 1]
            if self.row - 1 >= 0 and self.col + 1 < self.game.dims:
                right = self.game.grid[self.row - 1][self.col + 1]
            if self.type == PieceType.KING:
                if self.row + 1 < self.game.dims and self.col - 1 >= 0:
                    left_back = self.game.grid[self.row + 1][self.col - 1]
                if self.col + 1 < self.game.dims and self.row + 1 < self.game.dims:
                    right_back = self.game.grid[self.row + 1][self.col + 1]
            
            if left is None:
                legal_moves.append([(self.row - 1, self.col - 1)])
            if right is None:
                legal_moves.append([(self.row - 1, self.col + 1)])
            if left_back is None:
                legal_moves.append([(self.row + 1, self.col - 1)])
            if right_back is None:
                legal_moves.append([(self.row + 1, self.col + 1)])   

        if self.color == PieceColor.RED:
            if self.row + 1 < self.game.dims and self.col - 1 >= 0:
                left = self.game.grid[self.row + 1][self.col - 1]
            if self.col + 1 < self.game.dims and self.row + 1 < self.game.dims:
                right = self.game.grid[self.row + 1][self.col + 1]
            if self.type == PieceType.KING:
                if self.row - 1 >= 0 and self.col - 1 >= 0:
                    left_back = self.game.grid[self.row - 1][self.col - 1]
                if self.row - 1 >= 0 and self.col + 1 < self.game.dims:
                    right_back = self.game.grid[self.row - 1][self.col + 1]
            
            if left is None:
                legal_moves.append([(self.row + 1, self.col - 1)])
            if right is None:
                legal_moves.append([(self.row + 1, self.col + 1)])
            if left_back is None:
                legal_moves.append([(self.row - 1, self.col - 1)])
            if right_back is None:
                legal_moves.append([(self.row - 1, self.col + 1)])
        return legal_moves

    def is_legal_move(self, move):
        return move in self.get_legal_moves()


    def __repr__(self):
        if self.type == PieceType.PIECE:
            return f'PIECE({self.row},{self.col})'
        if self.type == PieceType.KING:
            return f'KING({self.row},{self.col})'
        return "ERROR"