import sys
import copy
from checkers import Board, PieceColor, PieceType, Piece

#KIV, may remove if not needed
DIRECTIONS = {
    "UPL": (-1, -1),
    "UPR": (-1, 1),
    "DOL": (1, -1),
    "DOR": (1, 1)
}

class CheckersTest:
    """
    Class for representing a Checkers game to test a specific stage
    """

    def __init__(self, size = 5):
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

    def _init_pieces(self):
        """
        Initializes pieces of both teams on a board in-place, and returns a 
        tuple of two lists of the initialized Piece objects
            Args:
                (None)

            Returns: 
                (Tuple([List[Piece], List[Piece]]))
        """
        p1_pieces = []
        p2_pieces = []
        p1_pieces.append(Piece(self.p1_color, 9, 4, self))
        #p1_pieces.append(Piece(self.p1_color, 4, 3, self))
        #p1_pieces.append(Piece(self.p1_color, 4, 1, self))
        #uhm this is kinda screwed btw 
        '''for i in range(0, self.dims - 1, 2):
            for i2 in range(self.dims - 1, 0, -2):
                p2_pieces.append(Piece(self.p2_color, i, i2, self))
                self.grid[i][i2] = p2_pieces[i]'''
        
        p2_pieces.append(Piece(self.p2_color, 4, 1, self))
        p2_pieces.append(Piece(self.p2_color, 4, 3, self))
        p2_pieces.append(Piece(self.p2_color, 4, 5, self))
        p2_pieces.append(Piece(self.p2_color, 6, 3, self))
        p2_pieces.append(Piece(self.p2_color, 6, 5, self))
        p2_pieces.append(Piece(self.p2_color, 2, 5, self))
        p2_pieces.append(Piece(self.p2_color, 2, 3, self))
        p2_pieces.append(Piece(self.p2_color, 2, 1, self))
        p2_pieces.append(Piece(self.p2_color, 1, 2, self))
        p2_pieces.append(Piece(self.p2_color, 8, 1, self))
        p2_pieces.append(Piece(self.p2_color, 8, 3, self))
        p2_pieces.append(Piece(self.p2_color, 8, 5, self))
        p1_pieces.append(Piece(self.p1_color, 9, 4, self))
        #self.grid[4][3] = p1_pieces[1]
        #self.grid[4][1] = p1_pieces[2]
        self.grid[4][1] = p2_pieces[0]
        self.grid[4][3] = p2_pieces[1]
        self.grid[4][5] = p2_pieces[2]
        self.grid[6][3] = p2_pieces[3]
        self.grid[6][5] = p2_pieces[4]
        self.grid[2][5] = p2_pieces[5]
        self.grid[2][3] = p2_pieces[6]
        self.grid[2][1] = p2_pieces[7]
        self.grid[1][2] = p2_pieces[8]
        self.grid[8][1] = p2_pieces[9]
        self.grid[8][3] = p2_pieces[10]
        self.grid[8][5] = p2_pieces[11]


        self.grid[9][4] = p1_pieces[0]

        return (p1_pieces, p2_pieces)
    

    def __str__(self):
        """
        Returns a string representation of the board
        """
        raise NotImplementedError


    #is this necessary?
    def _end_game(self):
        """
        Ends the game and exits the programme
        """
        if self.get_winner() == None:
            print("Game ended, no winner")
        else:
            print("Congratulations!", self.get_winner(), "Has Won!")
        
        sys.exit()
    
    #
    #PUBLIC METHODS
    #

    def player_legal_moves(self, color):
        """ 
        Gets all possible legal moves for each piece of the given player color.

        Args:
            color (PieceColor): Color of player (PieceColor.BLACK or 
            PieceColor.RED)

        Raises:
            ValueError: if a valid PieceColor is not inputed

        Returns:
            list[tuple(Piece, list(list(tuple(int, int))))]:a list of tuples. In
            each tuple, the first element is the piece to move, and the second
            element is a list containing the move sequences 
        """
        legal_moves = []
        # can try to use enum here KIV this part
        if color == self.p1_color:
            for piece in self.p1: 
                if piece.get_legal_moves() != []:
                    legal_moves.append((piece, piece.get_legal_moves()))
        elif color == self.p2_color:
            for piece in self.p2:
                if piece.get_legal_moves() != []:
                    legal_moves.append((piece, piece.get_legal_moves()))
        else:
            raise ValueError("Player name invalid!")
        return legal_moves

    # how does TUI and GUI use this? 
    def get_winner(self):
        """ 
        Checks for a winner, and returns the winner name

        Args:
            None

        Raise:
            None

        Returns:
            str: Winner name
        """
        if not self.p1:
            print("Red has won!")
            return self.p2_color
        elif not self.p2:
            print("Black has won!")
            return self.p1_color
        #elif draw:
            #return 'It's a draw!
        else:
            #print("There's no winner yet") No need for this in TUI
            return None

    #again, how is this used without a draw?
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
        if self.get_winner() is None:
            return False
        return True
