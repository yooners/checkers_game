"""
TUI for Checkers
"""
import time

import click
from colorama import Fore, Style

from checkers import Board, Checkers, Piece, PieceColor, PieceType
from mocks import BoardMock, CheckersMock, PieceMock

from bot import RandomBot, SmartBot


class TUIPlayer:
    """
    Simple class to store information about a TUI player

    A TUI player can either be a human player using the keyboard, or a bot.
    """


    def __init__(self, player_type, game, color, bot_delay):
        """ Constructor

        Args:
            player_type (str): "human", "random-bot", or "smart-bot"
            game (Checkers): The Checkers game
            color (PieceColor): The player's color
            bot_delay (float): When playing as a bot, an artificial delay
             (in seconds) to wait before making a move.
        """
        self.color = color
        if self.color == PieceColor.BLACK:
            self.name = "Player 1: Black"
        if self.color == PieceColor.RED:
            self.name = "Player 2: Red"
        if player_type == "human":
            self.bot = None
        if player_type == "random-bot":
            self.bot = RandomBot(game, self.color)
        if player_type == "smart-bot":
            self.bot = SmartBot(game, self.color)
        self.game = game
        self.next = None
        self.bot_delay = bot_delay


    def piece_to_move(self):
        """Returns the piece to be moved given a human player input
        
            Args:
                (None)
        
            Returns: 
                Piece: a piece object in the Checkers game
        """
        while True:
            row = input(Style.BRIGHT +
            f"{self.name}> Insert row of piece to move (starting from 0):" +
            Style.RESET_ALL)
            col = input(Style.BRIGHT +
            f"{self.name}> Insert column of piece to move (starting from 0):" +
            Style.RESET_ALL)

            try:
                pos = (int(row), int(col))
            except ValueError:
                print("Please insert valid integers for row/col numbers")
                continue

            try:
                piece = self.game.board.get_piece(pos)
                if piece.color == self.color:
                    legal_pieces_to_move = [move[0] for move in
                    self.game.player_legal_moves(self.color)]
                    if piece not in legal_pieces_to_move:
                        print("There are no legal moves for this piece." +
                        " Remember: you need to jump if it is possible!")
                        continue
                    else:
                        return piece
                else:
                    print("Your piece is not here.")
                    continue

            except ValueError:
                print("Your piece is not here.")
                continue


    def all_possible_moves(self):
        """Returns all possible moves for the piece after getting a piece
        chosen by a human player.

            Args:
                (None) 

            Returns: 
                lst(lst(tuple)): list of moves including intermediate
                coordinates reached by the piece
        """
        piece = self.piece_to_move()
        self.next = piece
        return piece.get_legal_moves()


    def get_move(self):
        """ Gets the next move from the player.

        If the player is a human player, prompt the player to choose a move out
        of all the possible legal moves for chosen piece.
        If the player is a bot, ask the bot to suggest a move.

            Args:
                (None)

            Returns:
                lst(tuple): a move including intermediate coordinates reached
                by the piece
        """
        if self.bot is None:
            legal_moves = self.all_possible_moves()
            print("All legal moves:")
            for i, move in enumerate(legal_moves):
                print(i + 1, str(move)[1:-1])
            #Option for the player to select a different piece instead
            print(len(legal_moves) + 1, "Select another piece")

            while True:
                #ask the player to select which move option they want
                try:
                    p_response = int(input(Style.BRIGHT +
                    f"{self.name}> Choose move option number:" +
                    Style.RESET_ALL))
                    if p_response <= 0:
                        raise ValueError
                    if p_response == len(legal_moves) + 1:
                        #allows the player to select another piece
                        return self.get_move()
                except ValueError:
                    print("Please insert a valid option number")
                    continue

                try:
                    move = legal_moves[p_response - 1]
                    return move
                except IndexError:
                    print("Please insert a valid option number")
                    continue

        else:
            time.sleep(self.bot_delay)
            next_piece, move = self.bot.suggest_move()
            self.next = next_piece
            # displays the coordinates of the piece chosen by bot, and the move
            print(Style.BRIGHT + f"{self.name}> " + Style.RESET_ALL + 
            f"({next_piece.row}, {next_piece.col}) -> ", str(move)[1:-1])
            return move


def print_board(board):
    """ Prints the current checkers board to the screen

        Args:
            board: The board to print

        Returns: None
    """
    grid = board.to_piece_grid()
    nrows = ncols = len(grid)

    # Col coordinate labels
    cols_digit_1 = '    '
    for c in range(1, ncols):
        if c < 10:
            cols_digit_1 += "  "
        else:
            cols_digit_1 = cols_digit_1 + " " + str(c)[0]
    print(cols_digit_1)

    cols_digit_2 = "   0"
    for c in range(1, ncols):
        if c < 10:
            cols_digit_2 += f" {c}"
        else:
            cols_digit_2 = cols_digit_2 + " " + str(c)[1]
    print(cols_digit_2)

    # Top row    
    print("  ┌" + ("─┬" * (ncols-1)) + "─┐")

    for r in range(nrows):
        #print the row coordinates
        if r < 10:
            crow = f"{r} " + Fore.WHITE + "│"
        elif r >= 10:
            crow = f"{r}" + Fore.WHITE + "│"
        for c in range(ncols):
            v = grid[r][c]
            if v is None:
                #make the board checkered
                if (r % 2 == 0 and c % 2 == 0) or (r % 2 != 0 and c % 2 != 0):
                    crow += Fore.WHITE + "X"
                else:
                    crow += Fore.WHITE + " " 
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


def play_checkers(game, players):
    """ Plays a game of Checkers on the terminal

    Args:
        game (Checkers): The checkers game
        players (dict): A dictionary mapping each player's color to
          TUIPlayer objects.

    Returns: None
    """
    # the starting player is black
    current = players[PieceColor.BLACK]

    # keep playing until there is a winner:
    while not game.is_done():
        # print the board
        print()
        print_board(game.board)
        print()

        #get next move
        next_move = current.get_move()

        #move the piece
        current.next.move(next_move)

        #update the player
        if current.color == PieceColor.BLACK:
            current = players[PieceColor.RED]
        elif current.color == PieceColor.RED:
            current = players[PieceColor.BLACK]
    print()
    print_board(game.board)

    print(game.get_winner())


#
# Command-line interface
#

@click.command(name="checkers-tui")
@click.option('--mode',
              type=click.Choice(['real', 'mock'], case_sensitive=False),
              default="real")
#to change the board size
@click.option('--size',
              type=click.INT,
              default=3)
@click.option('--black',
              type=click.Choice(['human', 'random-bot', 'smart-bot'], 
              case_sensitive=False),
              default="human")
@click.option('--red',
              type=click.Choice(['human', 'random-bot', 'smart-bot'], 
              case_sensitive=False),
              default="human")
@click.option('--bot-delay', type=click.FLOAT, default=0.5)

def cmd(mode, size, black, red, bot_delay):
    if mode == "real":
        game = Checkers(size = size)
    elif mode == "mock":
        game = CheckersMock(size = size)

    player1 = TUIPlayer(black, game, PieceColor.BLACK, bot_delay)
    player2 = TUIPlayer(red, game, PieceColor.RED, bot_delay)
    players = {PieceColor.BLACK: player1, PieceColor.RED: player2}

    play_checkers(game, players)

if __name__ == "__main__":
    cmd()
