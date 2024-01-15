"""
GUI for Checkers!

Bibliography

Credit to TechWithTim, Helped understanding Pygame logic and how Game interfaces
work. 
Link: https://www.youtube.com/watch?v=_kOXGzkbnps&t=551s (Part 3)

Credit - TechwithTim to figure out how to draw checkboard. 
https://www.youtube.com/watch?v=vnd3RfeG3NM&t=1704s (Part 1)

https://java2blog.com/find-common-elements-in-two-lists-python/
"""

import os
import sys
import itertools
from typing import Union, Dict

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import click

from bot import RandomBot, SmartBot
from mocks import PieceColor, PieceType, CheckersMock, CheckersStub
from checkers import Checkers

CheckersType = Union[Checkers, CheckersMock, CheckersStub]

#
#CONSTANTS
#

#Window size 
WIDTH = 720
HEIGHT = 720

#Universal Colors
WHITE = (255,255,255) 
GREEN = (1,200,32)
GOLD = (225,223,0)
BLACK = (0,0,0)
RED = (255, 0, 0)

class GUIPlayer:
    """
    Simple class to store information about a GUI player

    A GUI player can either be a human player or a bot.
    """

    name: str
    bot: Union[None, RandomBot, SmartBot]
    board: CheckersType
    color: PieceColor

    def __init__(self, n: int, player_type: str, board: CheckersType,
                 color: PieceColor) -> None:
        """ Constructor

        Args:
            n: int: The player's number (1 or 2)
            player_type: str: "human", "random-bot", or "smart-bot"
            board: CheckersType: The Checkers board
            color: PieceColor: The player's color
        """
        player_color = {1: PieceColor.BLACK, 2: PieceColor.RED}

        if player_type == "human":
            self.name = f"Player {n}"
            self.bot = None
        if player_type == "random-bot":
            self.name = f"Random Bot {n}"
            self.bot = RandomBot(board, player_color[n])
        elif player_type == "smart-bot":
            self.name = f"Smart Bot {n}"
            self.bot = SmartBot(board, player_color[n])
        self.board = board
        self.color = color


class GameInterface:
    """
    Class to store information about player moves and make moves. Handles most
    of the GUI logic is used to make the main game loop cleaner.
    """

    board: CheckersType
    surface: pygame.surface.Surface
    bot_delay: float

    def __init__(self, Checkers_board: CheckersType, 
                surface: pygame.surface.Surface, bot_delay: float) -> None:
        """ Constructor

        Args:
            Checkers_board: CheckersType: The Checkers board
            surface: pygame.surface.Surface: Pygame surface to draw the board on
            bot_delay: float: The bot-delay
        """
        self.Checkers_board = Checkers_board
        self.surface = surface
        self.bot_delay = bot_delay

        self.current_color = PieceColor.BLACK
        self.selected_piece = None
        self.move_made = False
        self.can_move = False
        self.movable_pieces = [move[0] for move in self.Checkers_board.\
                player_legal_moves(self.current_color)]


    def select_move(self, position: tuple, current: GUIPlayer, 
                    bot_move = None) -> None:
        """ Checks if a poisition which the player selected with the mouse is a 
        piece on the correct team during the correct turn. If the piece is
        valid, it will display its legal moves on the board. The function then
        checks whether the player selects one of the legal moves it can make and
        makes the move if the player clicks a valid move on the screen.

        If the player wishes to deselect a piece, he or she can simply select
        another piece on the right team or click on a position of the board
        which is not a legal move. 

        If the player is a bot, it simply moves as the bot suggests. 

        Args:
            position: tuple(int, int): The position clicked on the board
            bot_move: list[tuple(int, int)]: The move the bot wants to make - 
            Default is none
            current: GUIPlayer: The player whos turn it is currently

        Returns: None
        """
        try:
            piece = self.Checkers_board.board.get_piece(position)
        except ValueError:
            piece = None

        #Checking if the player is a bot
        self.is_bot_player = True if current.bot is not None else False

        #LOGIC IF BOT
        if self.is_bot_player:
            self.move_made = True
            piece.move(bot_move)

        #LOGIC IF THE PLAYER IS HUMAN
        if piece is not None and self.current_color == piece.color:
            self.selected_piece = piece
            if piece in self.movable_pieces:
                self.can_move = True
            else:
                self.can_move = False
    
        elif self.selected_piece is not None:
            common_mvs = self.same_paths(self.selected_piece.get_legal_moves())
            for move in self.selected_piece.get_legal_moves():
                if len(move) == 1:
                    if self.can_move and position == move[0]:
                        self.move_made = True
                        self.selected_piece.move(move)
                #checks for multiple moves which share the same tile
                elif position in move and position not in common_mvs:
                    self.move_made = True
                    self.selected_piece.move(move)


    def same_paths(self, legal_moves) -> list:
        """ Checks if any of the legal moves share a tile. If for example,
        a piece can take two different paths to the same tile this function will
        check for that. This is important to avoid confusion, as it should be
        clear which exact sequence of moves the user intends to make. If this
        situation originates, the user should select a step which isn't common 
        between two different moves. Note that this always occurs with 
        multi-jump moves and is an edge case. 

        Args: legal_moves: list[tuples]: The legal moves of the piece

        Returns: common_moves: list[tuples(int,int)]
        The common move(s) or destination 
        """
        #Citation: https://java2blog.com/find-common-elements-in-two-
        #lists-python/

        common_moves = []
        for a, b in itertools.combinations(legal_moves, 2):
            common_move = set(a).intersection(b)
            if common_move != set():
                common_moves += list(common_move)

        return list(set(common_moves))


    def draw_legal_moves(self) -> None:
        """ If the player has selected a valid piece, this will draw the board
        including the legal moves (if any) of said selected piece. If the player
        is a bot, there is no need to display its legal moves as it has already
        made its choice. The display of moves is only needed for the user 
        to see where he or she should play next. 

        Once a move is made, there is no need to draw legal moves as the turn 
        ends.

        If no piece is selected, it will simply draw the board. 

        Args: None beyond self

        Returns: None
        """
        if self.selected_piece is not None and self.is_bot_player is False \
            and self.move_made is False:
            legal_moves = self.selected_piece.get_legal_moves() \
                if self.selected_piece in self.movable_pieces else []
        else:
            #No valid piece has been selected or the player is a bot
            legal_moves = []
        
        draw_board(self.surface, self.Checkers_board, legal_moves)
    

    def update(self) -> None:
        """ Updates the game by drawing the board and checking whether a move
        has been made. If a move has been made, that means the players current
        turn is over and the turn will be reset. Also adds bot_delays if needed

        Args: None beyond self

        Returns: Boolean: 
        True if the turn has ended or False if the turn is still going on.
        """
        self.draw_legal_moves()

        if self.move_made is True:
            #Resets move and colors to keep track of turns
            self.selected_piece = None 
            self.move_made = False
            self.can_move = False
            self.current_color = PieceColor.RED if self.current_color == \
                PieceColor.BLACK else PieceColor.BLACK

            #Updates the movable pieces to the next player's color
            self.movable_pieces = [move[0] for move in self.Checkers_board.\
                player_legal_moves(self.current_color)]

            #Adds Bot Delay
            if self.is_bot_player:
                pygame.time.wait(int(self.bot_delay * 1000))

            pygame.display.update()
            return True

        pygame.display.update()
        return False


def draw_board(surface: pygame.surface.Surface, Checkers_board: CheckersType,
             moves: list) -> None:
    """ Draws the current state of the board in the window including whether
        any legal moves should be displayed. 

    Args:
        surface: pygame.surface.Surface: Pygame surface to draw the board on
        Checkers_board: CheckersType: The Checker board to draw
        moves: list[list(tuple(int, int)))]: List of legal moves of a piece to
        draw 

    Returns: None

    """
    #Computing the row height. Since all tiles are squares this is equal
    #to the column width. 
    rh = HEIGHT // len(Checkers_board.grid) + 1
    surface.fill(BLACK)
    font = pygame.font.SysFont('times new roman', rh//3)
    text = font.render('K', 3, GOLD)

    #Draws the board - works with any size
    for i, row in enumerate(Checkers_board.grid):
        #Credit - TechwithTim (see bibliography above)
        #to figure out how to draw checkboard. 
        for j in range(i%2, len(row), 2):
            rect = (i * rh, j * rh, rh, rh)
            pygame.draw.rect(surface, color=RED, rect=rect)

    #Draws the pieces
    for i, row in enumerate(Checkers_board.grid):
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
        for step in move:
            center = (step[1] * rh + rh // 2, step[0] * rh + rh // 2)
            radius = (rh / 4) 
            pygame.draw.circle(surface, color=GREEN, center=center, \
                radius=radius)   
        

def checkers(Checkers_board: CheckersType, players: Dict[tuple, GUIPlayer],
            bot_delay: float) -> None:
    """ Plays a game of Checkers on a Pygame window

    Args:
        Checkers: CheckersType: The checkers board to play on
        players: Dict[tuple, GUIPlayer]: A dictionary mapping piece colors to
          TUIPlayer objects.
        bot_delay: float: When playing as a bot, an artificial delay
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

    #Initializes the game interface which handles the GUI
    Game = GameInterface(Checkers_board, surface, bot_delay)

    while not Checkers_board.is_done():
        # Process Pygame events
        # If the mouse is pressed over a valid piece, the player can choose to
        # make a move. If the user closes the window, quit the game.
        clock.tick(24)
        move_made = False
        events = pygame.event.get()
        rh = HEIGHT // len(Checkers_board.grid) + 1

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Check for mouse events and makes moves based on position on board
            if current.bot is None and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                board_row, board_col = mouse_y // rh, mouse_x // rh
                position = (board_row, board_col)
                Game.select_move(position, current)

        # CODE FOR THE PLAYER IF IT IS A BOT
        if current.bot is not None:
            piece, moves = current.bot.suggest_move()
            Game.select_move((piece.row, piece.col), current, moves)
        
        move_made = Game.update()

        #UPDATING PLAYER AND TURN
        if move_made is True:
            if current.color == PieceColor.BLACK:
                current = players[PieceColor.RED]
            elif current.color == PieceColor.RED:
                current = players[PieceColor.BLACK]
    
    # Print the winner (on the terminal)
    winner = Checkers_board.get_winner()
    print(winner)

#
# Command-line interface
#

@click.command(name="checkers-gui")
@click.option('--mode', type=click.Choice(['real', 'stub', 'mock'], \
                case_sensitive=False), default="real")

#Board size for the board - Can be any integer > 0
@click.option('--board-size', type = click.INT, default=3)

@click.option('--player1',
                type=click.Choice(['human', 'random-bot', 'smart-bot'], \
                case_sensitive=False), default="human")

@click.option('--player2',
                type=click.Choice(['human', 'random-bot', 'smart-bot'], \
                case_sensitive=False), default="human")

@click.option('--bot-delay', type=click.FLOAT, default=0.5)


def cmd(mode, board_size, player1, player2, bot_delay):
    if mode == "real": 
        Checkers_board = Checkers(board_size)
    elif mode == "stub":
        Checkers_board = CheckersStub(board_size)
    elif mode == "mock":
        Checkers_board = CheckersMock(board_size)

    player1 = GUIPlayer(1, player1, Checkers_board, PieceColor.BLACK)
    player2 = GUIPlayer(2, player2, Checkers_board, PieceColor.RED)

    players = {PieceColor.BLACK: player1, PieceColor.RED: player2}

    checkers(Checkers_board, players, bot_delay)


if __name__ == "__main__":
    cmd()
    