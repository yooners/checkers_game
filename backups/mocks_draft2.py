"""
Improved stub and mock implementation of Checkers Board.
"""

import copy
from checkers import PieceColor, PieceType

class BoardStub1:
    """
    Stub implementation of board class.
    """

    def __init__(self, size = 1, p1_name = "Player 1", p2_name = "Player 2"):
        # int: The dimensions of the board
        self.dims = (size * 2) + 2
        # list[list[Optional[Piece]]]: The board itself
        self._board = [[None] * self.dims for _ in range(self.dims)]
        # Initializes Pieces onto the board in-place
        # Lists of Pieces corresponding to each player
        self.p1, self.p2 = self._init_pieces()
        # str: the names of each player, dependent on game
        self.p1_name = p1_name
        self.p2_name = p2_name
        # int: Integer corresponding to the player identifier
        self.curr_player = 1
        # Optional[int]: The identifier of the winner (if any) on the board
        self._winner = None
        # Counts the number of moves taken on the board
        self.move_counter = 0
        # Counts the number of moves without a capture
        self.draw_counter = 0

        self.p1_legal_moves = [(self._board[0][0], [(1, 1)])]
        self.p2_legal_moves = [(self._board[0][0], [(1, 1)])]

    def _init_pieces(self):
        p1_pieces = []
        p2_pieces = []
        p1_pieces.append(PieceStub1(PieceColor.BLACK, 3, 0, PieceType.PIECE, self))
        p1_pieces.append(PieceStub1(PieceColor.BLACK, 3, 2, PieceType.KING, self))
        p2_pieces.append(PieceStub1(PieceColor.RED, 0, 1, PieceType.PIECE, self))
        p2_pieces.append(PieceStub1(PieceColor.RED, 0, 3, PieceType.KING, self))
        self._board[0][1] = p2_pieces[0]
        self._board[0][3] = p2_pieces[1]
        self._board[3][0] = p1_pieces[0]
        self._board[3][2] = p1_pieces[1]
        return p1_pieces, p2_pieces
    
    def __str__(self):
        return "BOARD"
    
    #
    #PUBLIC METHODS
    #

    def get_piece(self, coordinates):
        row, col = coordinates
        return self._board[row][col]

    def player_legal_moves(self, player):
        if player == 'Player 1':
            return self.p1_legal_moves
        if player == 'Player 2':
            return self.p2_legal_moves
    
    def set_player_legal_moves(self, player, moves):
        if player == 'Player 1':
            self.p1_legal_moves = moves
        if player == 'Player 2':
            self.p2_legal_moves = moves
    
    def move(self, old_loc, new_loc):
        assert old_loc[0] >= 0 and old_loc[0] < self.dims and old_loc[1] >= 0 \
            and old_loc[1] < self.dims
        assert new_loc[0] >= 0 and new_loc[0] < self.dims and new_loc[1] >= 0 \
            and new_loc[1] < self.dims

        self._board[new_loc[0]][new_loc[1]] = self._board[old_loc[0]][old_loc[1]]
        self._board[old_loc[0]][old_loc[1]] = None
   
    def get_winner(self):
        return self.p1_name

    def is_done(self):
        return False

    def to_piece_grid(self):
        return copy.deepcopy(self._board)


class PieceStub1:
    """
    Stub implementation of Piece class
    """

    def __init__(self, color=PieceColor.BLACK, col=0, row=0, \
                 type=PieceType.PIECE, board=None):
        self.color = color
        #int: The x position of the piece
        self.row = row
        #int: The y position of the piece
        self.col = col
        #str: The type of piece it is
        self.type = type
        #list[list[Optional[Piece]]]: The board itself
        self.board = board

    def __str__(self):
        return "PIECE"
    
    def __repr__(self):
        return f"(PIECE, ({self.row}, {self.col}))"
    
    def _phantom_step(self, location):
        """
        Used purely in DFS, to change the coordinates and type without 
        affecting the main board.

        Args:
            location (tuple(int, int)): location to move to 
        
        returns None
        """
        r, c = location
        self.row = r
        self.col = c
    
    #
    #PUBLIC METHODS
    #

    def move(self, location): 
        pass

    def get_legal_moves(self):
        return [[(1, 1), (2, 2)], [(1, 1), (3, 3)]]

    def is_legal_move(self, move):
        return True


class BoardMock1:
    """
    Mock implementation of board class. Expected behaviors:
    - Plays on a checkers board where n = 1
    - Each player starts with 1 piece and 1 king
    - Moves do not include jumps
    - Game ends if it's player x's turn but they have no legal moves
    """

    def __init__(self, size = 1, p1_name = "Player 1", p2_name = "Player 2"):
        # int: The size parameter passed to __init__
        self.size = size
        # int: The dimensions of the board
        self.dims = (size * 2) + 2
        # list[list[Optional[Piece]]]: The board itself
        self._board = [[None] * self.dims for _ in range(self.dims)]
        # Initializes Pieces onto the board in-place
        # Lists of Pieces corresponding to each player
        self.p1, self.p2 = self._init_pieces()
        # str: the names of each player, dependent on game
        self.p1_name = p1_name
        self.p2_name = p2_name
        # int: Integer corresponding to the player identifier
        self.curr_player = 1
        # Optional[int]: The identifier of the winner (if any) on the board
        self._winner = None
        # Counts the number of moves taken on the board
        self.move_counter = 0
        # Counts the number of moves without a capture
        self.draw_counter = 0

    def _init_pieces(self):
        p1_pieces = []
        p2_pieces = []
        p1_pieces.append(PieceMock1(PieceColor.BLACK, 3, 0, PieceType.PIECE, self))
        p1_pieces.append(PieceMock1(PieceColor.BLACK, 3, 2, PieceType.KING, self))
        p2_pieces.append(PieceMock1(PieceColor.RED, 0, 1, PieceType.PIECE, self))
        p2_pieces.append(PieceMock1(PieceColor.RED, 0, 3, PieceType.KING, self))
        self._board[0][1] = p2_pieces[0]
        self._board[0][3] = p2_pieces[1]
        self._board[3][0] = p1_pieces[0]
        self._board[3][2] = p1_pieces[1]
        return p1_pieces, p2_pieces
    
    def __str__(self):
        return "BOARD"
    
    #
    #PUBLIC METHODS
    #

    def get_piece(self, coordinates):
        row, col = coordinates
        return self._board[row][col]

    def player_legal_moves(self, player):
        moves = []
        if player == self.p1_name:
            if self.p1 != []:
                for piece in self.p1:
                    all_moves = piece.get_legal_moves()
                    moves.append((piece, all_moves))
        if player == self.p2_name:
            if self.p2 != []:
                for piece in self.p2:
                    all_moves = piece.get_legal_moves()
                    moves.append((piece, all_moves))
        return moves
   
    def get_winner(self):
        if self.player_legal_moves(self.p1_name) == [] and self.curr_player == 1:
            return "red wins!"
        if self.player_legal_moves(self.p2_name) == [] and self.curr_player == 2:
            return "black wins!"
        return None

    def is_done(self):
        if self.get_winner() is None:
            return False
        return True

    def to_piece_grid(self):
        return copy.deepcopy(self._board)
    
    def move_manual(self, old_loc, new_loc):
        assert old_loc[0] >= 0 and old_loc[0] < self.dims and old_loc[1] >= 0 \
            and old_loc[1] < self.dims
        assert new_loc[0] >= 0 and new_loc[0] < self.dims and new_loc[1] >= 0 \
            and new_loc[1] < self.dims

        self._board[new_loc[0]][new_loc[1]] = self._board[old_loc[0]][old_loc[1]]
        self._board[old_loc[0]][old_loc[1]] = None
        self._board[new_loc[0]][new_loc[1]].row = new_loc[0]
        self._board[new_loc[0]][new_loc[1]].col = new_loc[1]


class PieceMock1:
    """
    Mock implementation of Piece class
    """

    def __init__(self, color, col, row, type, board):
        self.color = color
        #int: The x position of the piece
        self.row = row
        #int: The y position of the piece
        self.col = col
        #str: The type of piece it is
        self.type = type
        #list[list[Optional[Piece]]]: The board itself
        self.board = board

    def _phantom_step(self, location):
        """
        Used purely in DFS, to change the coordinates and type without 
        affecting the main board.

        Args:
            location (tuple(int, int)): location to move to 
        
        returns None
        """
        r, c = location
        self.row = r
        self.col = c


    def __repr__(self):
        return f'{self.color}, ({self.row},{self.col})'

    #
    #PUBLIC METHODS
    #

    def move(self, location): 
        if (location[0][0][0] >= self.board.dims or location[0][0][1] >= self.board.dims
        or not self.is_legal_move(location)):
            raise ValueError("not a valid move") 
        else:
            self.board._board[self.row][self.col] = None
            self.row = location[0][0]
            self.col = location[0][1]
            self.board._board[self.row][self.col] = self
            if self.board.curr_player == 1:
                self.board.curr_player = 2
            elif self.board.curr_player == 2:
                self.board.curr_player = 1

    def get_legal_moves(self):
        legal_moves = []
        left = right = left_back = right_back = 0
        if self.color == PieceColor.BLACK:
            if self.row - 1 >= 0 and self.col - 1 >= 0:
                left = self.board._board[self.row - 1][self.col - 1]
            if self.row - 1 >= 0 and self.col + 1 < self.board.dims:
                right = self.board._board[self.row - 1][self.col + 1]
            if self.type == PieceType.KING:
                if self.row + 1 < self.board.dims and self.col - 1 >= 0:
                    left_back = self.board._board[self.row + 1][self.col - 1]
                if self.col + 1 < self.board.dims and self.row + 1 < self.board.dims:
                    right_back = self.board._board[self.row + 1][self.col + 1]
            
            if left is None:
                legal_moves.append([(self.row - 1, self.col - 1)])
            if right is None:
                legal_moves.append([(self.row - 1, self.col + 1)])
            if left_back is None:
                legal_moves.append([(self.row + 1, self.col - 1)])
            if right_back is None:
                legal_moves.append([(self.row + 1, self.col + 1)])   

        if self.color == PieceColor.RED:
            if self.row + 1 < self.board.dims and self.col - 1 >= 0:
                left = self.board._board[self.row + 1][self.col - 1]
            if self.col + 1 < self.board.dims and self.row + 1 < self.board.dims:
                right = self.board._board[self.row + 1][self.col + 1]
            if self.type == PieceType.KING:
                if self.row - 1 >= 0 and self.col - 1 >= 0:
                    left_back = self.board._board[self.row - 1][self.col - 1]
                if self.row - 1 >= 0 and self.col + 1 < self.board.dims:
                    right_back = self.board._board[self.row - 1][self.col + 1]
            
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
        return f'{self.color}, ({self.row},{self.col})'
    