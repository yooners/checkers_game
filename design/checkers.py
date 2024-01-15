"""
Classes for implementing Checkers (design).

Examples:
    1) Create a new Checkers game:
        game = Checkers(3)

    2) Given a Checkers board with a game in progress, check whether a given
    move is feasible::
        piece1 = game.board.get_piece((1,2))
        piece1.is_legal_move((2,3))

    3) Given a piece at a specific position in the board, obtain all the
    valid moves for that piece::
        piece1.get_legal_moves()

    4) Obtain the list of all possible moves a player can make on the board.
        game.player_legal_moves("Player 1")

    5) Check whether there is a winner and, if so, who the winner is.
	game.get_winner()
"""
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
        raise NotImplementedError

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
        raise NotImplementedError


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
        #did we use this?

        # Optional[int]: The identifier of the winner (if any) on the board
        self._winner = None
        #did we use this?

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
                (Tuple([List[Piece], List[Piece]]))
        """
        raise NotImplementedError
    
    
    def _player_has_jump(self, legal_moves):
        """
        Checks if given player with sequence of moves contains a jump. Used for 
        player_legal_moves

        Args:
            moves (list(tuple(Piece, list(list(tuple(int, int))))))): 
        
        Returns:
            If given player's moves contains a jump (bool)
        """
        raise NotImplementedError

    
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
        raise NotImplementedError


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
        raise NotImplementedError
        

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
        raise NotImplementedError
    

    def accept_draw(self):
        """
        Mechanism to accept draw. Ends the game in a draw. 
        
        Args:
            None
        
        Returns None
            """
        raise NotImplementedError

    def player_legal_moves(self, color):
        """ 
        Gets all possible legal moves for each piece of the given player color.

        Args:
            color (PieceColor): Color of player (PieceColor.BLACK or 
            PieceColor.RED)

        Raises:
            ValueError: if a valid PieceColor is not inputed

        Returns:
            list[tuple(Piece, list(list(tuple(int, int))))]:a list of tuples.
            In each tuple, the first element is the piece to move, and the
            second element is list of all possible moves for that piece
        """
        raise NotImplementedError
   
    def get_winner(self):
        """ 
        Checks for a winner, and returns the winner name

        Args:
            None

        Raise:
            None

        Returns:
            Optional[str]: Winner name
        """
        raise NotImplementedError


    def is_done(self):
        """ 
        Checks if a game is done (either one player wins, or the game is drawn,
        after the threshold of number of "actionless" moves is reached)

        Args:
            None

        Raise:
            None

        Returns:
            Bool: Whether the game is done or not
        """
        raise NotImplementedError


class Piece:
    """
    Class for representing a Piece
    """

    def __init__(self, color, row, col, game, type = PieceType.PIECE):
        """
        Constructor

        Args:
            color (PieceColor): Which color the piece is
            row (int): The row the piece is on
            col (int): he column the piece is on
            type (PieceType): The type of piece it is - KING or PIECE
            game (Checkers): The checkers game that the piece belongs to
        """
        #str: The player who controls the piece
        self.color = color

        #int: The row the piece is on
        self.row = row

        #int: The column the piece is on
        self.col = col
        
        #str: The type of piece it is
        self.type = type

        #list[list[Optional[Piece]]]: The board itself
        self.game = game


    def __repr__(self):
        """
        Returns a string representation of the piece
        """
        raise NotImplementedError

    def __str__(self):
        """
        Returns a string representation of the piece
        """
        raise NotImplementedError
    

    def _remove_piece(self):
        """
        Removes piece from board after it's been jumped over 

        Args:
            None

        Returns None
        """
        raise NotImplementedError

    def _phantom_step(self, location):
        """
        Used purely in DFS, to change the coordinates and type without 
        affecting the main board.

        Args:
            location: location to move to (tuple(int, int))
        
        returns None
        """
        raise NotImplementedError

    def _temporary_step(self, location):
        """
        Used purely in DFS, to change the coordinates and type that does 
        affect the main board.

        Args:
            location: location to move to (tuple(int, int))
        
        returns None
        """
        raise NotImplementedError
    
    def _step(self, location):
        """
        Moves the Piece to the new location. Updates board.
        
        Args:
            location: location to move to (tuple(int, int))
        
        returns None
        """
        raise NotImplementedError

    def _is_jump(self, location):
        """
        Checks if the step/move is a jump.

        Args:
            location (tuple): Coordinates of the jump
        
        Returns: 
            If it's a jump or not (bool)
        """
        raise NotImplementedError

    #
    #PUBLIC METHODS
    #

    def move(self, locations): 
        """ 
        Moves a player's piece to a certain location if the move is legal,
        and updates information on board

        Args:
            locations (List(tuple(int,int))): Series of row, col coordinates of
            the steps in the move

        Raise:
            ValueError: If the locations inputed are not valid or illegal

        Returns: (None)
        """
        raise NotImplementedError
       

    def get_legal_moves(self):
        """ 
        Returns a list of legal moves for the piece, showing each intermediate
        coordinate in each move.

        Args:
            None

        Raise:
            None

        Outputs: List(List(tuple): List of legal move coordinates, including 
        intermediates
        """
        raise NotImplementedError


    def legal_move_dfs(self, direction, enemies_captured = set()):
        """
        DFS to find the jumps in a jump sequence

        Args:
            direction(list)

        Returns:
            List of movable locations from the piece's current location
            (list(list(tuple(int, int)))
        """
        raise NotImplementedError
    

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
        raise NotImplementedError
    

    def is_legal_move(self, move):
        
        """ 
        Checks if a move (including intermediate steps) is legal

        Args:
            move (List(tuple(int,int))): The move that is being made including
            intermediate coordinates reached

        Returns:
            bool: True if the move is legal, False otherwise
        """
        raise NotImplementedError
    
