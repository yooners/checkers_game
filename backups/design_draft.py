"""
Classes for implementing Checkers (design).

Examples:
    1) Create a new Checkers board::
        b1 = Board(3)

    2) Given a Checkers board with a game in progress, check whether a given
    move is feasible::
        piece1 = b1.get_piece((1,2))
        piece1.is_legal_move((2,3))

    3) Given a piece at a specific position in the board, obtain all the
    valid moves for that piece::
        piece1.get_legal_moves()

    4) Obtain the list of all possible moves a player can make on the board.
        b1.player_legal_moves("Player 1")

    5) Check whether there is a winner and, if so, who the winner is.
	    b1.get_winner()
"""
import copy
from enum import Enum
PieceColor = Enum("PieceColor", ["BLACK", "RED"])
PieceType = Enum("PieceType", ["PIECE", "KING"])


class Board:
    """
    Class for representing a Checkers game
    """

    def __init__(self, size, p1_name = "Player 1", p2_name = "Player 2"):
        """
        Constructor

        Args:
            size (int): Number of rows where pieces are initialized. Dimensions
                of board will be a square of side length ((size * 2) + 2)
            p1_name (str): Name of player 1
            p2_name (str): Name of player 2
        """

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
        """
        Initializes pieces of both teams on a board in-place, and returns a 
        tuple of two lists of the initialized Piece objects
            Args:
                (None)

            Returns: 
                (Tuple([List[Piece], List[Piece]]))
        """
        raise NotImplementedError
    
    def __str__(self):
        """
        Returns a string representation of the board
        """
        raise NotImplementedError
    
    #
    #PUBLIC METHODS
    #

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

    def player_legal_moves(self, player):
        """ 
        Gets all possible legal moves for each piece of the given player.

        Args:
            player (str): Name of player

        Raises:
            ValueError: if the player name is not valid

        Returns:
            list[tuple(Piece, list(tuple(int, int)))]:a list of tuples. In each
            tuple, the first element is the piece to move, and the second
            element is a tuple containing the row-column coordinates of the new 
            position after moving.  
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

class Piece:
    """
    Class for representing a Piece
    """

    def __init__(self, color, x, y, board, type = PieceType.PIECE):
        """
        Constructor

        Args:
            color (PieceColor): Which color the piece is
            x (int): The x position of the piece
            y (int): The y position of the piece
            type (PieceType): The type of piece it is - KING or PIECE
            board (Board): The board on which the piece is on
        """
        #str: The player who controls the piece
        self.color = color

        #int: The x position of the piece
        self.x = x

        #int: The y position of the piece
        self.y = y

        #str: The type of piece it is
        self.type = type

        #list[list[Optional[Piece]]]: The board itself
        self.board = board

    def __str__(self):
        """
        Returns a string representation of the piece
        """
        raise NotImplementedError

    #
    #PUBLIC METHODS
    #

    def move(self, location): 
        """ 
        Moves a player's piece to a certain location if the move is legal,
        and updates information on board

        Args:
            location (List(tuple(int,int))): Coordinates of steps in move

        Raise:
            IndexError: If the location is out of the board
            ValueError: If the player is not a valid player

        Returns: (None)
        """
        raise NotImplementedError
        # Pls increment self.board.move_counter after every full move thnx
        # Also increment self.board.draw_counter if no captures happen, u dont
        #   have to think of the logic urself, we can do it together
        #   Count total pieces, if it doesnt go down after a move, increment?

    def get_legal_moves(self):
        """ 
        Returns list of list of tuples, representing each location that is a 
        legal move

        Args:
            None

        Raise:
            None

        Outputs: List(List(tuple): List of legal move locations, including 
        intermediates
        """
        raise NotImplementedError

    def is_legal_move(self, move):
        """ 
        Checks if the final location where the move is to be made is legal

        Args:
            move (tuple(int,int)): The move that is being made

        Raise:
            IndexError: If the move location is out of the board

        Returns:
            bool: True if the move is legal, False if the move is illegal
        """
        raise NotImplementedError