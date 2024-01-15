"""
Classes for implementing Checkers (working).

Examples:
    1) Create a new Checkers board::
        b1 = Checkers(3)

    2) Given a Checkers board with a game in progress, check whether a given
    move is feasible::
        piece1 = b1.board.get_piece((1,2))
        piece1.is_legal_move([(2,3)])

    3) Given a piece at a specific position in the board, obtain all the
    valid moves for that piece::
        piece1.get_legal_moves()

    4) Obtain the list of all possible moves a player can make on the board.
        b1.player_legal_moves(PieceColor.BLACK)

    5) Check whether there is a winner and, if so, who the winner is.
	    b1.get_winner()
"""

import copy
from enum import Enum

PieceColor = Enum("PieceColor", ["BLACK", "RED"])
PieceType = Enum("PieceType", ["PIECE", "KING"])

class Board:
    """
    Class for representing a board for a board game
    """


    def __init__(self, num_rows, num_cols):
        """
        Constructor

        Args:
            num_rows (int): Number of rows on the board
            num_cols (int): Number of columns on the board
        """
        self.rows = num_rows
        self.cols = num_cols
        self.board = [[None] * num_cols for _ in range(num_rows)]


    def to_piece_grid(self):
        """ Returns the board as a list of list of Pieces

        Not suitable for JSON serialization, but can be useful
        to display the board in a GUI or TUI.

        Returns:
            list[list[Piece]]: A list of lists with the same
            dimensions as the board. In each row, the values
            in the list will be None (no piece), or Piece.
        """
        return copy.deepcopy(self.board)
        

    def get_piece(self, coordinates):
        """ 
        Gets piece at given coordinates (row_idx, col_idx).

        Args:
            coordinates (tuple(int)): Location on board (row_idx, col_idx)
        
        Raises:
            ValueError: if coordinates are not on the board, or if there is no
            piece at this location

        Returns:
            Piece: the piece at the specified location
        """
        r, c = coordinates
        if r >= self.rows or c >= self.cols:
            raise ValueError("Coordinates not on board!")
        if self.board[r][c] is None:
            raise ValueError("No piece here!")
        else:
            return self.board[r][c]
        

class Checkers:
    """
    Class for representing a Checkers game
    """

    def __init__(self, size):
        """
        Constructor

        Args:
            size (int): Number of rows where pieces are initialized. Dimensions
                of board will be a square of side length ((size * 2) + 2)
        """
        # int: The size parameter passed to __init__
        self.size = size

        # int: The dimensions of the board
        self.dims = (size * 2) + 2

        # Initializes the board instance
        self.board = Board(self.dims, self.dims)

        # Creates grid attribute to access the board conveniently
        self.grid = self.board.board

        # PieceColor: the color of each player on the board
        self.p1_color = PieceColor.BLACK
        self.p2_color = PieceColor.RED

        # Initializes Pieces onto the board in-place
        # Lists of Pieces corresponding to each player
        self.p1, self.p2 = self._init_pieces()

        # int: Integer corresponding to the player identifier
        self.curr_player = 1

        # Optional[int]: The identifier of the winner (if any) on the board
        self._winner = None

        # Counts the number of moves taken on the board
        self.move_counter = 0

        # Counts the number of moves without a capture
        self.draw_counter = 0

        # Keeps track of if draw has been initiated
        self.initiated_draw = False


    def _init_pieces(self):
        """
        Initializes pieces of both teams on a board in-place, and returns a 
        tuple of two lists of the initialized Piece objects
            
        Args:
            (None)

        Returns: 
            Initialised Piece objects (Tuple([List[Piece], List[Piece]]))
        """
        p1_pieces = []
        p2_pieces = []
        #player 1
        for row in range((self.dims - 2)//2):
            curr_row = self.dims - 1 - row
            for col in range(self.dims):
                if (curr_row + col) % 2 != 0:
                    piece = Piece(PieceColor.BLACK, curr_row, col, self)
                    p1_pieces.append(piece)
                    self.grid[curr_row][col] = piece
        #player 2
        for row in range((self.dims - 2)//2):
            for col in range(self.dims):
                if (row + col) % 2 != 0:
                    piece = Piece(PieceColor.RED, row, col, self)
                    p2_pieces.append(piece)
                    self.grid[row][col] = piece
        return (p1_pieces, p2_pieces)
    

    def _player_has_jump(self, legal_moves):
        """
        Checks if given player with sequence of moves contains a jump. Used for 
        player_legal_moves

        Args:
            moves (list(tuple(Piece, list(list(tuple(int, int))))))): 
        
        Returns:
            If given player's moves contains a jump (bool)
        """
        for piece_move in legal_moves:
            piece, move = piece_move
            r, c = move[0][0]
            if abs(piece.row - r) == 2 or abs(piece.col - c) == 2:
                return True           
        return False
    

    def _move_has_jump(self, piece, move):
        """
        Checks if given list of moves contains a jump

        Args:
            piece (Piece): piece object for which the moves pertain
            move list(list(tuple(int, int))): list of all possible moves for the
            piece

        Returns:
            If given list of moves contains a jump (bool)
        """
        r, c = move[0][0]
        return abs(piece.row - r) == 2 or abs(piece.col - c) == 2


    def _only_jumps(self, legal_moves):
        """
        Removes all pieces with non-jumps, creating a new list 

        Args:
            legal moves (list[tuple(Piece, list(list(tuple(int, int))))]):
            list of tuples of pieces and their respective moves

        Returns:
            Legal moves of only pieces with jumps (list[tuple(Piece, 
            list(list(tuple(int, int))))]: )
        """
        only_jumps = []
        for piece_move in legal_moves:
            piece, move = piece_move
            if self._move_has_jump(piece, move):
                only_jumps.append(piece_move)
        return only_jumps


    #
    #PUBLIC METHODS
    #
    def offer_draw(self):
        """
        Mechanism to offer a draw

        Args:
            None

        Returns None
        """
        self.initiated_draw = True


    def accept_draw(self):
        """
        Mechanism to accept draw. Ends the game in a draw. 
        
        Args:
            None
        
        Returns None
            """
        if self.initiated_draw:
            self.draw_counter = 80
            self.get_winner()


    def player_legal_moves(self, color):
        """ 
        Gets all possible legal moves for each piece of the given player color.

        Args:
            color (PieceColor): Color of player (PieceColor.BLACK or 
            PieceColor.RED)

        Raises:
            ValueError: if a valid PieceColor is not inputed

        Returns:
            A list of tuples. In each tuple, the first element is the piece to 
            move, and the second element is a list containing the move sequences 
            (list[tuple(Piece, list(list(tuple(int, int))))])
        """
        legal_moves = []
        if color == self.p1_color:
            for piece in self.p1: 
                if piece.get_legal_moves() != []:
                    legal_moves.append((piece, piece.get_legal_moves()))
        elif color == self.p2_color:
            for piece in self.p2:
                if piece.get_legal_moves() != []:
                    legal_moves.append((piece, piece.get_legal_moves()))
        
        if self._player_has_jump(legal_moves):
            legal_moves = self._only_jumps(legal_moves)

        return legal_moves


    def get_winner(self):
        """ 
        Checks for a winner, and returns the winner name

        Args:
            None

        Raise:
            None

        Returns:
            Winner name (str)
        """ 
        if not self.player_legal_moves(self.p1_color) and self.curr_player == 1:
            return "Red has won!"
        elif not self.player_legal_moves(self.p2_color) and self.curr_player \
        == 2:
            return "Black has won!"
        elif self.draw_counter >= 79:
            return "It's a draw!"
        else:
            return None
        

    def is_done(self):
        """ 
        Checks if a game is done (either one player wins, or the game is drawn,
        after the threshold of number of "actionless" moves is reached)

        Args:
            None

        Raise:
            None

        Returns:
            Whether the game is done or not (bool)
        """
        if self.get_winner() is None:
            return False
        return True


class Piece:
    """
    Class for representing a Piece
    """

    def __init__(self, color, row, col, game, type = PieceType.PIECE):
        """
        Constructor

        Args:
            color (PieceColor): Which color the piece is
            c (int): The column position of the piece
            r (int): The row position of the piece
            type (PieceType): The type of piece it is - KING or PIECE
            game (Checkers): The checkers game that the piece belongs to
        """
        #PieceColor: The player who controls the piece
        self.color = color

        #int: The column position of the piece
        self.col = col

        #int: The row position of the piece
        self.row = row

        #PieceType: The type of piece it is
        self.type = type

        #list[list[Optional[Piece]]]: The board itself
        self.game = game


    def __repr__(self):
        """
        Returns a string representation of the piece
        """
        return f'{self.type}, ({self.row}, {self.col})'
    

    def __str__(self):
        """
        Returns a string representation of the piece
        """
        return f'{self.type}, ({self.row}, {self.col})'
    

    def _remove_piece(self):
        """
        Removes piece from board after it's been jumped over 

        Args:
            None

        Returns None
        """
        self.game.grid[self.row][self.col] = None
        if self in self.game.p1: 
            self.game.p1.remove(self)
        else:
            self.game.p2.remove(self)
    
    
    def _phantom_step(self, location):
        """
        Used purely in DFS, to change the coordinates and type without 
        affecting the main board.

        Args:
            location: location to move to (tuple(int, int))
        
        returns None
        """
        r, c = location
        self.row = r
        self.col = c
    

    def _temporary_step(self, location):
        """
        Used purely in DFS, to change the coordinates and type that does 
        affect the main board.

        Args:
            location: location to move to (tuple(int, int))
        
        returns None
        """
        r, c = location

        self.game.board.board[r][c] = self
        self.game.board.board[self.row][self.col] = None

        self.row = r
        self.col = c


    def _step(self, location):
        """
        Moves the Piece to the new location. Updates board.
        
        Args:
            location: location to move to (tuple(int, int))
        
        returns None
        """
        r, c = location
        #check if it's a jump, if it is, remove piece
        if self._is_jump(location):
            piece_c = ((self.col + c)//2)
            piece_r = ((self.row + r)//2)
            piece = self.game.board.get_piece((piece_r, piece_c))
            piece._remove_piece()
        #remove old location
        self.game.grid[self.row][self.col] = None
        #change within board 
        self.row = r
        self.col = c
        #move to new position in board
        self.game.grid[r][c] = self
        #change to king type once it reaches the ends of the board
        if r == 0 or r == self.game.dims - 1:
            self.type = PieceType.KING
    

    def _is_jump(self, location):
        """
        Checks if the step/move is a jump.

        Args:
            location (tuple): Coordinates of the jump
        
        Returns: 
            If it's a jump or not (bool)
        """
        r, c = location
        return abs(r - self.row) == 2 or abs(c - self.col) == 2
    
    
    #
    #PUBLIC METHODS
    #
    def move(self, location): 
        """ 
        Moves a player's piece to a certain location if the move is legal,
        and updates information on board

        Args:
            location (List(tuple(int,int))): Coordinates of steps in move
            color (PieceColor): The color making the move

        Raise:
            IndexError: If the location is out of the board
            ValueError: If the player is not a valid player

        Returns None
        """  
        total_p1_pieces = len(self.game.p1)
        total_p2_pieces = len(self.game.p2)
        
        #move the piece, removing pieces along the way
        for loc in location:
            self._step(loc) 
          
        # change the turn 
        if self.color == PieceColor.BLACK:
            self.game.curr_player = 2
            if len(self.game.p2) < total_p2_pieces:
                self.game.draw_counter = 0
            else:
                self.game.draw_counter += 1

        if self.color == PieceColor.RED:
            self.game.curr_player = 1
            if len(self.game.p1) < total_p1_pieces:
                self.game.draw_counter = 0
            else:
                self.game.draw_counter += 1

        #add to move counter
        self.game.move_counter += 1


    def get_legal_moves(self):
        """ 
        Returns list of list of tuples, representing each location that is a 
        legal move

        Args:
            enemies_captured (list): list of enemies captured thus far

        Raise:
            None

        Returns: 
            List of legal move locations, including intermediates
            (list(list(tuple(int, int)))
        """
        movable_loc = []
        contains_jump = False
        if self.type == PieceType.PIECE:
            if self.color == PieceColor.BLACK:
                direction = [(-1, -1), (-1, 1)]
            if self.color == PieceColor.RED:
                direction = [(1, -1), (1, 1)]
        else:
            direction = [(1, -1), (1, 1), (-1, -1), (-1, 1)]

        for dir in direction:
            dr, dc = dir
            neighbor_c = self.col + dc
            neighbor_r = self.row + dr
            
            #if "neighbor" is out of board, skip to next direction
            if (neighbor_c >= self.game.dims or neighbor_c < 0) or \
                (neighbor_r >= self.game.dims or neighbor_r < 0):
                continue
            neighbor = self.game.grid[neighbor_r][neighbor_c]

            #if neighbor is enemy tile 
            if neighbor is not None and neighbor.color != self.color:
                #if next tile is within board
                if (neighbor_c + dc >= self.game.dims or neighbor_c + dc < 0) \
                or (neighbor_r + dr >= self.game.dims or neighbor_r + dr < 0):
                    continue
                next_tile = self.game.grid[neighbor_r + dr][neighbor_c + dc]  
                #recursive case: enemy neighbor + empty tile in that direction, initialise jump
                if next_tile is None:
                    contains_jump = True
                    for move in self.legal_move_dfs(direction, set()):
                        movable_loc.append(move)
            elif neighbor is None:
                movable_loc.append([(neighbor_r, neighbor_c)])
        
        if contains_jump:
            movable_loc = self.only_jumps(movable_loc)

        return movable_loc
    
    
    def legal_move_dfs(self, direction, enemies_captured = set()):
        """
        DFS to find the jumps in a jump sequence

        Args:
            direction(list)

        Returns:
            List of movable locations from the piece's current location
            (list(list(tuple(int, int)))

        """
        og_c = self.col
        og_r = self.row
        movable_loc = []

        #begin DFS
        for dir in direction:
            dr, dc = dir
            neighbor_c = self.col + dc
            neighbor_r = self.row + dr

            #if "neighbor" is out of board, skip to next direction
            if (neighbor_c >= self.game.dims or neighbor_c < 0) or \
                (neighbor_r >= self.game.dims or neighbor_r < 0):
                continue
            neighbor = self.game.grid[neighbor_r][neighbor_c]

            #case 1: enemy neighbor
            if neighbor is not None and neighbor.color != self.color:
                if (neighbor_c + dc >= self.game.dims or neighbor_c + dc < 0) or \
                (neighbor_r + dr >= self.game.dims or neighbor_r + dr < 0):
                    continue
                next_tile = self.game.grid[neighbor_r + dr][neighbor_c + dc]  

                #case 1b: enemy neighbor + empty tile in that direction, (phantom) jump!
                if next_tile is None and neighbor not in enemies_captured:
                    enemies_captured.add(neighbor)

                    #self phantom steps there, then recurse
                    self._phantom_step((neighbor_r + dr, neighbor_c + dc))
                    to_add = [(neighbor_r + dr, neighbor_c + dc)]
                    e_c2 = enemies_captured
                    curr_len = len(movable_loc)
                    for move in self.legal_move_dfs(direction, e_c2):
                        movable_loc.append(to_add + move)
                    if curr_len == len(movable_loc):
                        movable_loc.append(to_add)
                    self.col = og_c
                    self.row = og_r

            #case 2: no way to move/no more jumps, skip that neighbor
        return movable_loc
    

    def only_jumps(self, movable_loc):
        """
        Removes all non jumps from a list of moves
        
        Args:
            movable_loc: List(List(tuple): List of legal move locations, 
            including intermediates

        Returns: 
            List of legal move locations, including intermediates, without jumps
            (list(list(tuple(int, int)))
        """

        new_list = []
        for move in movable_loc:
            r, c = move[0]
            if abs(self.row - r) > 1 and abs(self.col - c) > 1:
                new_list.append(move)
        return new_list
    

    def is_legal_move(self, move): 
        """ 
        Checks if a move (including intermediate steps) is legal

        Args:
            move (List(tuple(int,int))): The move that is being made including
            intermediate coordinates reached

        Returns:
            If the move is legal (bool)
        """
        return move in self.get_legal_moves()
