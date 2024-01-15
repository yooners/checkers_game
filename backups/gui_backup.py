"""
GUI for Connect Four

Sources used -
Credit to TechWithTim, Helped understanding Pygame logic and how game interfaces
work.
Link: https://www.youtube.com/watch?v=_kOXGzkbnps&t=551s (Part 3)

Credit - TechwithTim to figure out how to draw checkboard
https://www.youtube.com/watch?v=vnd3RfeG3NM&t=1704s (Part 1)
"""

import os
import sys
from typing import Union, Dict

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import click

# from mocks import BoardMock, BoardStub, PieceMock, PieceStub
from bot import RandomBot, SmartBot
from mocks2 import PieceColor, PieceType, BoardMock1, BoardStub1, PieceMock1, \
    PieceStub1
from checkers import Board, Piece

# BoardType = Union[Board, BoardStub,
#                   BoardMock, BoardBotMock]

#
#CONSTANTS
#

#Window size 
WIDTH = 720
HEIGHT = 720

#Colors
WHITE = (255,255,255) 
BLUE = (0,0,255)
GREEN = (1,200,32)
GOLD = (225,223,0)
BLACK = (0,0,0)
RED = (255, 0, 0)

class GUIPlayer:
    """
    Simple class to store information about a GUI player

    A TUI player can either a human player using the keyboard,
    or a bot.
    """

    name: str
    bot: Union[None, RandomBot, SmartBot]
    # board: BoardType
    color: tuple

    def __init__(self, n: int, player_type: str, board,
                 color: PieceColor):
        """ Constructor

        Args:
            n: The player's number (1 or 2)
            player_type: "human", "random-bot", or "smart-bot"
            board: The Checkers board
            color: The player's color
        """

        if player_type == "human":
            self.name = f"Player {n}"
            self.bot = None
        if player_type == "random-bot":
            self.name = f"Random Bot {n}"
            self.bot = RandomBot(board, f"Player {n}")
        elif player_type == "smart-bot":
            self.name = f"Smart Bot {n}"
            self.bot = SmartBot(board, f"Player {n}")
        self.board = board
        self.color = color

class GameInterface:
    """
    Simple class to store information about player moves and make moves.
    """
    def __init__(self, board, surface: pygame.surface.Surface) -> None:
        """ Constructor

        Args:
            board: The Checkers board
            surface: Pygame surface to draw the board on
        """
        self.selected_piece = None
        self.move_made = False
        self.board = board
        self.surface = surface
        self.is_bot_player = False

    def select_move(self, position: tuple, current: GUIPlayer) -> bool:
        """ Checks if a poisition which the player selected with the mouse
        is a piece on the correct team during the correct turn. If the piece is
        valid, it will display its legal moves on the board. The function then
        checks whether the player selects one of the legal moves it can make and
        makes the move if the player clicks a valid move on the screen.

        If the player wishes to deselect a piece, he or she can simply select
        another piece on the right team or click on a position of the board
        which is not a legal move. 

        Args:
            position: The position clicked on the board
            current: The player whos turn it is currently

        Returns: None
        """
        try:
            piece = self.board.get_piece(position)
        except ValueError:
            piece = None

        #Checks whether the current player is a bot or not 
        self.is_bot_player = True if current.bot is not None else False

        if piece is not None:
            if current.color == piece.color:
                self.selected_piece = piece
        elif self.selected_piece is not None:
            for move in self.selected_piece.get_legal_moves():
                if position == move[0]:
                    self.move_made = True
                    self.selected_piece.move(move)

    def draw_legal_moves(self) -> None:
        """ If the player has selected a valid piece, this will draw the board
        including the legal moves (if any) of said selected piece. If the player
        is a bot, there is no need to display its legal moves as it has already
        made its choice. The display of moves is only needed for the user 
        to see where he or she should play next. 
        
        If no piece is selected, it will simply draw the board. 

        Args: None beyond self

        Returns: None
        """
        if self.selected_piece is not None and self.is_bot_player is False:
            legal_moves = self.selected_piece.get_legal_moves() 
        else:
            legal_moves = []
        
        draw_board(self.surface, self.board, legal_moves)
    
    def update(self) -> None:
        """ Updates the game by drawing the board and checking whether a move
        has been made. If a move has been made, that means the players current
        turn is over and the turn will be reset.

        Args: None beyond self

        Returns: Boolean: 
        True if the turn has ended or False if the turn is still going on.
        """
        self.draw_legal_moves()
        
        if self.move_made is True:
            self.selected_piece = None 
            self.move_made = False
            return True

        pygame.display.update()
        return False

def draw_board(surface: pygame.surface.Surface, board, moves: list) -> None:
    """ Draws the current state of the board in the window including whether
        any legal moves should be displayed. 

    Args:
        surface: Pygame surface to draw the board on
        board: The board to draw
        moves: List of legal moves to draw 

    Returns: None

    """
    #Computing the row height. Since all tiles are squares this is equal
    #to the column width. 
    rh = HEIGHT // len(board._board) + 1
    surface.fill(BLACK)
    font = pygame.font.SysFont('times new roman', rh//3)
    text = font.render('K', 3, GOLD)

    #Draws the board
    for i, row in enumerate(board._board):
        for j in range(i%2, len(row), 2):
            rect = (i * rh, j * rh, rh, rh)
            pygame.draw.rect(surface, color=RED, rect=rect)

    #Draws the pieces
    for i, row in enumerate(board._board):
        for j, piece in enumerate(row):
            #calculates the pieces position and the position of the text if king
            center = (j * rh + rh // 2, i * rh + rh // 2)
            center_text = (j * rh + rh/2.6, i * rh + rh/3)
            #The piece has an outline. Outer_radius is the width of it. 
            inner_radius = (rh / 2.5) 
            outer_radius = (rh / 2.2)

            if piece is not None:
                if piece.color == PieceColor.BLACK:
                    if piece.type == PieceType.KING:
                        pygame.draw.circle(surface, color=GOLD,\
                                    center=center, radius=outer_radius)
                        pygame.draw.circle(surface, color=BLACK,\
                                    center=center, radius=inner_radius)
                        surface.blit(text, center_text)
                    elif piece.type == PieceType.PIECE:
                        pygame.draw.circle(surface, color=WHITE,\
                                    center=center, radius=outer_radius)
                        pygame.draw.circle(surface, color=BLACK,\
                                    center=center, radius=inner_radius)
                else:
                    if piece.type == PieceType.KING:
                        pygame.draw.circle(surface, color=GOLD,\
                                    center=center, radius=outer_radius)
                        pygame.draw.circle(surface, color=RED,\
                                    center=center, radius=inner_radius)
                        surface.blit(text, center_text)
                    elif piece.type == PieceType.PIECE:
                        pygame.draw.circle(surface, color=WHITE,\
                                    center=center, radius=outer_radius)
                        pygame.draw.circle(surface, color=RED,\
                                    center=center, radius=inner_radius)

    #Draws legal moves for a piece, if there are any to be drawn.
    for move in moves:
        center = (move[0][1] * rh + rh // 2, move[0][0] * rh + rh // 2)
        radius = (rh / 4) 
        pygame.draw.circle(surface, color=GREEN, center=center, radius=radius)   
    
def checkers(board, players: Dict[tuple, GUIPlayer],
                   bot_delay: float) -> None:
    """ Plays a game of Checkers on a Pygame window

    Args:
        board: The board to play on
        players: A dictionary mapping piece colors to
          TUIPlayer objects.
        bot_delay: When playing as a bot, an artificial delay
          (in seconds) to wait before making a move.

    Returns: None

    """
    # Initialize Pygame, clock and surface
    pygame.init()
    pygame.display.set_caption("Checkers")
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # The starting player is always BLACK by convention
    current = players[PieceColor.BLACK]

    #Initializes the game interface
    Game = GameInterface(board, surface)

    while board.get_winner() is None:
        # Process Pygame events
        # If the mouse is pressed over a valid piece, the player can choose to
        # make a move. If the user closes the window, quit the game.
        move_made = False
        events = pygame.event.get()
        rh = HEIGHT // len(board._board) + 1
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Check for mouse events and makes moves based on position on board
            if current.bot is None and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                board_x, board_y = mouse_y // rh, mouse_x // rh
                position = (board_x, board_y)
                Game.select_move(position, current)

        # CODE FOR THE PLAYER IF IT IS A BOT
        if current.bot is not None:
            piece, moves = current.bot.suggest_move()
            Game.select_move((pieces, piece.y), current)
            piece = Game.selected_piece
            pygame.time.wait(int(bot_delay * 1000))
            Game.select_move(moves[0], current)

        move_made = Game.update()

        # UPDATING PLAYER AND TURN
        if move_made is True:
            if current.color == PieceColor.BLACK:
                current = players[PieceColor.RED]
            elif current.color == PieceColor.RED:
                current = players[PieceColor.BLACK]

        clock.tick(24)

    # Print the winner (on the terminal)
    winner = board.get_winner()
    if winner is not None:
        print(winner)
    else:
        print("It's a tie!")

#
# Command-line interface
#

@click.command(name="checkers-gui")
@click.option('--mode', type=click.Choice(['real', 'stub', 'mock'], \
                case_sensitive=False), default="real")

#Board size for the board - Can be any integer > 0
@click.option('--board-size', type = click.INT, default=2)

@click.option('--player1',
                type=click.Choice(['human', 'random-bot', 'smart-bot'], \
                case_sensitive=False), default="human")

@click.option('--player2',
                type=click.Choice(['human', 'random-bot', 'smart-bot'], \
                case_sensitive=False), default="human")

@click.option('--bot-delay', type=click.FLOAT, default=0.5)

def cmd(mode, board_size, player1, player2, bot_delay):
    if mode == "real": 
        board = Board(board_size)
    elif mode == "stub":
        board = BoardStub1(board_size)
    elif mode == "mock":
        board = BoardMock1(board_size)

    player1 = GUIPlayer(1, player1, board, PieceColor.BLACK)
    player2 = GUIPlayer(2, player2, board, PieceColor.RED)

    players = {PieceColor.BLACK: player1, PieceColor.RED: player2}

    checkers(board, players, bot_delay)

if __name__ == "__main__":
    cmd()
    