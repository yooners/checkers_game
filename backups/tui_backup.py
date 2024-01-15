#CHECK self.y is row, self.x is col
#say Borja say in Ed can just show list
"""
TUI for Checkers
"""
import time #representing time in code
from typing import Union, Dict #type hints

import click #create command line interfaces
from colorama import Fore, Style #cross-platform printing of colored text

from checkers import Board, Piece, PieceColor, PieceType
from mocks2 import BoardStub1, PieceStub1, BoardMock1, PieceMock1
from mocks import BoardStub, PieceStub, BoardMock, PieceMock

from bot import RandomBot, SmartBot

#Player 1 is on top
#doing print_board first

class TUIPlayer:
    """
    Simple class to store information about a TUI player

    A TUI player can either a human player using the keyboard,
    or a bot.
    """
#do we need bot implementation for Checkers???

    def __init__(self, n: int, player_type: str, board: Board,
                 color: PieceColor, bot_delay: float):
        """ Constructor

        Args:
            n (int): The player's number (1 or 2)
            player_type (str): "human", "random-bot", or "smart-bot"
            board (Board): The Connect-M board
            color (PieceColor): The player's color
            bot_delay (float): When playing as a bot, an artificial delay
             (in seconds) to wait before making a move.
        """
        self.name = f"Player {n}"
        if player_type == "human":
            self.bot = None
        if player_type == "random-bot":
            self.bot = RandomBot(board, self.name)
            #check if bot needs opponent color attribute 
        elif player_type == "smart-bot":
            self.bot = SmartBot(board, self.name)
            #check if bot needs opponent color attribute 
        self.board = board
        self.next = None
        self.color = color
        self.bot_delay = bot_delay


    def piece_to_move(self):
        '''Returns the piece to be moved given a player input
        '''
        while True:
            row = input(Style.BRIGHT + f"{self.name}> Insert row of piece to move (starting from 0):" + Style.RESET_ALL)
            col = input(Style.BRIGHT + f"{self.name}> Insert column of piece to move (starting from 0):" + Style.RESET_ALL)
            try:
                pos = (int(row), int(col))
            except ValueError:
                print("Please insert valid integers for row/col numbers")
                continue

            try:
                piece = self.board.get_piece(pos)
                if piece is not None and piece.color == self.color:
                    if piece.get_legal_moves() == []:
                    #potentially change this to:
                    #legal_pieces_to_move = [move[0] for move in self.board.player_legal_moves(self.name)]
                    #if piece not in legal_pieces_to_move:
                        print("There are no legal moves for this piece.")
                        continue
                    else:
                        return piece
                else:
                    print("Your piece is not here.")
                    continue
            
            except ValueError:
                print("Your piece is not here.")
                continue

            except IndexError:
                print("That is out of the board.")
                continue


    def all_possible_moves(self):
        """Returns all possible moves after getting a piece position from the
        player 
        
        Returns (lst(tuple)): list of row, column indices that are possible
        moves for the piece
        """
        #what if there are no more checkers for the person??? Then make sure game is over!!!
        piece = self.piece_to_move()
        self.next = piece
        return piece.get_legal_moves()

    
    def get_move(self) -> int:
        """ Gets a move from the player

        If the player is a human player, prompt the player for a column.
        If the player is a bot, ask the bot to suggest a move.

        Returns (tuple): row, column indices to move checker to
        """
        if self.bot is None:
            #legal_moves = self.next.get_legal_moves()
            legal_moves = self.all_possible_moves()
            print("All legal moves:")
            print(legal_moves)
            for i, move in enumerate(legal_moves):
                print(i + 1, move)
            
            print(len(legal_moves) + 1, "Select another piece")
            
            while True:
                #ask to select which move number they want
                try:
                    p_response = int(input(Style.BRIGHT + f"{self.name}> Choose move option number:" + Style.RESET_ALL))
                    if p_response <= 0:
                        raise ValueError
                    if p_response == len(legal_moves) + 1:
                        return self.get_move()
                except ValueError:
                    print("Please insert a valid number")
                    continue

                try:
                    move = legal_moves[p_response - 1]
                    return move
                except IndexError:
                    print("Please insert a valid number")
                    continue
        
        if self.bot is not None:
            time.sleep(self.bot_delay)
            #return tuple with piece and sequence of moves
            next_piece, moves = self.bot.suggest_move()
            self.next = next_piece
            # Print prompt with column already filled in
            print(Style.BRIGHT + f"{self.name}> " + Style.RESET_ALL + str(moves))
            return moves


def print_board(board):
    """ Prints the current checkers board to the screen

    Args:
        board: The board to print

    Returns: None
    """
    grid = board.to_piece_grid()
    nrows = ncols = len(grid)

    # Top row
    display_top = "   0"
    for c in range(1, ncols):
        if c < 10:
            display_top += f" {c}"
    #doesn't show if there are more than 9 rows
    print(display_top)

    print("  ┌" + ("─┬" * (ncols-1)) + "─┐")

    for r in range(nrows):
        if r < 10:
            crow = f"{r} " + Fore.WHITE + "│"
        elif r >= 10:
            crow = f"{r}" + Fore.WHITE + "│"
        for c in range(ncols):
            v = grid[r][c]
            if v is None:
                crow += " "
            elif v.color == PieceColor.BLACK:
                if v.type == PieceType.PIECE:
                    crow += Fore.BLACK + Style.BRIGHT + "●"
                elif v.type == PieceType.KING:
                    crow += Fore.BLACK + Style.BRIGHT + "K"
            elif v.color == PieceColor.RED:
                if v.type == PieceType.PIECE:
                    crow += Fore.RED + Style.BRIGHT + "●"
                elif v.type == PieceType.KING:
                    crow += Fore.RED + Style.BRIGHT + "K"
            crow += Fore.WHITE + "│"
        print(crow)

        if r < nrows - 1:
            print("  ├" + ("─┼" * (ncols-1)) + "─┤")
        else:
            print("  └" + ("─┴" * (ncols-1)) + "─┘" + Style.RESET_ALL)



def play_checkers(board: BoardMock, players: Dict[str, TUIPlayer]) -> None:
    """ Plays a game of Connect Four on the terminal

    Args:
        board (BoardMock): The board to play on
        players (dict): A dictionary mapping each player's color to
          TUIPlayer objects.

    Returns: None
    """
    # The starting player is black
    current = players["black"]

    # Keep playing until there is a winner:
    while not board.is_done():
        # Print the board
        print()
        print_board(board)
        print()

        #all possible legal moves
        #all_moves = current.all_possible_moves()
        #print("Legal moves for piece:")
        #for i, move in enumerate(all_moves):
            #print(i + 1, move)
        #print("Legal moves for piece:", piece.get_legal_moves())
        #must find a way to show/print them
        #print(current.all_possible_moves())

        #Next move
        next_move = current.get_move()

        print("Legal moves for piece", current.next.get_legal_moves())


        # Move the piece
        current.next.move(next_move)

        # Update the player
        if current.color == PieceColor.BLACK:
            current = players["red"]
        elif current.color == PieceColor.RED:
            current = players["black"]
    print()
    print_board(board)

    #Change this based on how actual code is written
    winner = board.get_winner()
    if winner is not None:
        print(winner)
    else:
        print("It's a tie!")


#
# Command-line interface
#

@click.command(name="checkers-tui")
@click.option('--mode',
              type=click.Choice(['real', 'stub', 'mock'], case_sensitive=False),
              default="mock")
#change this when we use the real one
@click.option('--player1',
              type=click.Choice(['human', 'random-bot', 'smart-bot'], case_sensitive=False),
              default="human")
@click.option('--player2',
              type=click.Choice(['human', 'random-bot', 'smart-bot'], case_sensitive=False),
              default="human")
@click.option('--bot-delay', type=click.FLOAT, default=0.5)

def cmd(mode, player1, player2, bot_delay):
    if mode == "real":
        while True:
            try:
                dim = int(input(Style.BRIGHT + f"Desired value of n (board will have n*2 + 2 rows/columns):" + Style.RESET_ALL))
                board = Board(size=dim)
                break
            except ValueError:
                print("Please insert a valid integer.")
                continue
    elif mode == "stub":
        board = BoardStub1(size=9)
    elif mode == "mock":
        board = BoardMock1()

    player1 = TUIPlayer(1, player1, board, PieceColor.BLACK, bot_delay)
    player2 = TUIPlayer(2, player2, board, PieceColor.RED, bot_delay)
    players = {"black": player1, "red": player2}

    play_checkers(board, players)

if __name__ == "__main__":
    cmd()

