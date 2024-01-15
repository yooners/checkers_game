from checkers import Piece, Checkers, PieceType, PieceColor
import random
import click


class RandomBot:
    """
    Simple Bot that just picks a move at random
    """

    _game: Checkers
    _color: str

    def __init__(self, game: Checkers, color: PieceColor):
        """ 
        Constructor

        Args:
            game: (Checkers): Game that the bot will play on
            color: Color that the bot will play as
        """
        assert type(color) == PieceColor

        self._game = game
        self._color = color


    def suggest_move(self, botvbot=False) -> tuple((Piece, list((int, int)))):
        """ 
        Suggests a move

        Returns: (Piece, list((int, int))): The Piece moved, and the sequence
        of moves suggested by bot
        """
        possible_moves = self._game.player_legal_moves(self._color)
        random_moves = []
        for piece, moves in possible_moves:
            for move in moves:
                random_moves.append((piece, move))
        return random.choice(random_moves)


class SmartBot:
    """
    "Smart" bot.
    
    Basic Strategy taken from https://www.wikihow.com/Win-at-Checkers, plus
    some of my own additions. Plays with the following priorities:

    1. In early game stages, try to take control of the center "safely" (#6)
    2. King as many pieces as possible
    3. If forced to take, takes as many pieces as possible
    4. Blocks opponent from taking the bot's pieces
    5. Tries to run from Opponent captures
    6. If winning, attacks opponent pieces
    7. Consolidates pieces "safely" (#6)
    8. Advances non-king pieces "safely"
    9. Plays any "safe move" that does not result in an opponent capture
    10. Randomly moves
    """

    _game: Checkers
    _color: str

    def __init__(self, game: Checkers, color: PieceColor):
        """
        Constructor

        Args:
            game: (Checkers) Game the bot will play on
            color: Color that the bot will play as
        """
        assert type(color) == PieceColor
        
        self._game = game
        self._color = color


    def suggest_move(self, botvbot=False) -> tuple((Piece, list((int, int)))):
        """
        Suggests a move according to the priorities above.
        
        Outputs:
            tuple(Piece, list((tuple(int, int)))
             - Suggested move by the bot
        """
        all_possible_moves = []
        all_moves = self._game.player_legal_moves(self._color)
        for piece, moves in all_moves:
            if len(moves) > 0:
                all_possible_moves.append((piece, moves))
        possible_moves = all_possible_moves

        # Priority 1
        move = self._suggest_center(possible_moves)
        if move is not None:
        #    print("SAFE CENTER")
            return move
        
        # Priority 2
        move = self._suggest_king(possible_moves)
        if move is not None:
        #    print("KING")
            if not botvbot:
                text = ['One more king for me!', "I'm going to win now!", \
                        'I am so smart!']
                print(random.choice(text))
            return move
        
        # Priority 3
        move = self._suggest_capture(possible_moves)
        if move is not None:
        #    print("CAPTURE")
            if not botvbot:
                if len(move[1]) > 1:
                    text = ['WOMBO COMBOOO!!!', "You didn't see that coming!",\
                            'YESSSSS!!']
                else:
                    text = ['I took your piece!!', 'Hahaha', 'Wow you stink!']
                print(random.choice(text))
            return move
        
        # Priority 4
        move = self._suggest_block(possible_moves)
        if move is not None:
        #    print("BLOCK")
            if not botvbot:
                text = ["I see what you're trying to do...", "Not this time!",\
                'Haha you thought :)']
                print(random.choice(text))
            return move
        
        # Priority 5
        move = self._suggest_run()
        if move is not None:
        #    print("RUN")
            if not botvbot:
                text = ["I see what you're trying to do...", "Not this time!",\
                'Haha you thought :)']
                print(random.choice(text))
            return move
            
        # Priority 6
        move = self._suggest_attack(possible_moves)
        if move is not None:
        #    print("ATTACK")
            if random.random() > 0.75:
                if not botvbot:
                    text = ['Come here!!!', "I'm coming!!!", "You can't run..."]
                    print(random.choice(text))
            return move
        
        # Priority 7
        move = self._suggest_consolidate(possible_moves)
        if move is not None:
        #    print("SAFE CONSOLIDATE")
            return move

        # Priority 8
        move = self._suggest_advance(possible_moves)
        if move is not None:
        #    print("ADVANCE")
            return move
        
        # Priority 9
        moves = self._suggest_safe_move(possible_moves)
        if moves is not None:
        #    print("SAFE")
            return random.choice(moves)
        
        #print("RANDOM")
        if not botvbot:
            text = ["Sigh...", "I don't have any good moves :(", \
            "Wow you're good!"]
            print(random.choice(text))
        random_moves = []
        for piece, moves in possible_moves:
            for move in moves:
                random_moves.append((piece, move))
        return random.choice(random_moves)
        

    def _suggest_center(self, possible_moves):
        """
        Suggests a random move that safelyoccupies a center tile, in early game.
        If game is more developed, or no center moves are legal, returns None.

        Inputs:
            possible_moves: list[tuple(Piece, list(tuple(int, int)))]
             - List of legal moves for the bot
        
        Outputs:
            Optional[tuple(Piece, list(tuple(int, int)))]
             - Suggested move by the bot
        """
        b_dims = self._game.dims

        # In early game, try to control the center on your side
        if self._game.move_counter < b_dims - 2:
            ### REMOVE math.inf IN REAL TESTING ###
            possible_center_moves = []
            safe_moves = self._suggest_safe_move(possible_moves)
            if safe_moves is None:
                return
            for piece, moves in safe_moves:
                if self._color == PieceColor.BLACK:

                    # If move ends in center, then add to possible moves
                    if moves[-1][0] == b_dims / 2 and moves[-1][1] > 0 \
                        and moves[-1][1] < b_dims - 1:
                        possible_center_moves.append((piece, moves))

                elif self._color == PieceColor.RED:
                    if moves[-1][0] == b_dims / 2 - 1 and moves[-1][1] > 0 \
                        and moves[-1][1] < b_dims - 1:
                        possible_center_moves.append((piece, moves))

            if len(possible_center_moves) > 0:
                return random.choice(possible_center_moves)
    

    def _suggest_king(self, possible_moves):
        """
        Suggests a random move that makes a king, if possible. Otherwise, 
        returns None.

        Inputs:
            possible_moves: list[tuple(Piece, list(list(tuple(int, int))))]
             - List of legal moves for the bot
        
        Outputs:
            Optional[tuple(Piece, list(tuple(int, int)))]
             - Suggested move by the bot
        """
        # If I can make a king, then I make a random king.
        possible_king_moves = []
        for piece, all_moves in possible_moves:
            for moves in all_moves:
                if self._color == PieceColor.BLACK:
                    # If final move makes a king, then add to possible moves
                    if moves[-1][0] == 0 and piece.type == PieceType.PIECE:
                        possible_king_moves.append((piece, moves))
                elif self._color == PieceColor.RED:
                    # If final move makes a king, then add to possible moves
                    if moves[-1][0] == self._game.dims - 1 and \
                        piece.type == PieceType.PIECE:
                        
                        possible_king_moves.append((piece, moves))
        if len(possible_king_moves) > 0:
            return random.choice(possible_king_moves)


    def _suggest_advance(self, possible_moves):
        """
        Suggests a random safe move that advances bot's pieces. Otherwise, 
        returns None.

        Inputs:
            possible_moves: list[tuple(Piece, list(list(tuple(int, int))))]
             - List of legal moves for the bot
        
        Outputs:
            Optional[tuple(Piece, list(tuple(int, int)))]
             - Suggested move by the bot
        """
        advances = []
        safe_moves = self._suggest_safe_move(possible_moves)
        if safe_moves is None:
            return
        for piece, move in safe_moves:
            if piece.type == PieceType.PIECE:
                advances.append((piece, move))
        if len(advances) > 0:
            return random.choice(advances)


    def _suggest_capture(self, possible_moves):
        """
        Suggests a capture move that results in the highest total score.
        Taking a king adds 5 score, taking a normal piece adds 3 score.
        Scoring taken from http://www.cs.columbia.edu/~devans/TIC/AB.html

        Returns None if no capture moves are possible.

        Inputs:
            possible_moves: list[tuple(Piece, list(list(tuple(int, int))))]
             - List of legal moves for the bot
        
        Outputs:
            Optional[tuple(Piece, list(tuple(int, int)))]
             - Suggested move by the bot
        """
        if abs(possible_moves[0][0].row - possible_moves[0][1][0][0][0]) > 1:
            # If my first possible move is a capture move (means all legal
            # moves must be captures)
            max = 0
            take_moves = []
            for piece, moves in possible_moves:
                moves2 = []
                for move in moves:
                    moves2.append([(piece.row, piece.col)] + move)

                score = 0
                for i in range(0, len(moves2) - 1):
                    jumped_r = int((moves2[i][0][0] + moves2[i+1][0][0])/2)
                    jumped_c = int((moves2[i][0][1] + moves2[i+1][0][1])/2)

                    if self._game.board.board[jumped_r][jumped_c].type == \
                        PieceType.PIECE:
                        score += 3
                    elif self._game.board.board[jumped_r][jumped_c].type == \
                        PieceType.KING:
                        score += 5

                if score > max:
                    max = score
                    take_moves = [(piece, move)]
                elif score == max:
                    take_moves.append((piece, move))

            if len(take_moves) > 0:
                return random.choice(take_moves)
            
    
    def _suggest_block(self, possible_moves):
        """
        Suggests a move that blocks an opponent's move that captures the most
        pieces. 

        Returns None if no such blocking moves are possible.

        Inputs:
            possible_moves: list[tuple(Piece, list(list(tuple(int, int))))]
             - List of legal moves for the bot
        
        Outputs:
            Optional[tuple(Piece, list(tuple(int, int)))]
             - Suggested move by the bot
        """
        safe_moves = self._suggest_safe_move(possible_moves)
        if safe_moves is None:
            return
        
        opp_moves = []
        if self._color == PieceColor.BLACK:
            all_opp_moves = self._game.player_legal_moves(PieceColor.RED)
        if self._color == PieceColor.RED:
            all_opp_moves = self._game.player_legal_moves(PieceColor.BLACK)
        
        # Try to stop the opponent's move that takes most of the bot's pieces.
        for piece, moves in all_opp_moves:
            for move in moves:
                if len(move) > 0:
                    opp_moves.append((piece, move))
        if len(opp_moves) == 0:
            return
        opp_move_1 = opp_moves[0]

        if abs(opp_move_1[1][0][0] - opp_move_1[0].row) > 1:
            max = 0
            move_most_takes = None
            for piece, moves in opp_moves:
                if len(moves) > max:
                    max = len(moves)
                    move_most_takes = (piece, moves)
            
            if move_most_takes is not None:
                blocks = []
                for piece, move in safe_moves:
                    if move[-1] == move_most_takes[1][0]:  # If can block
                        blocks.append((piece, move))
                if len(blocks) > 0:
                    return random.choice(blocks)    # Then it randomly blocks


    def _suggest_consolidate(self, possible_moves):
        """
        Attempts to consolidate pieces without allowing a capture.

        Returns None if no such moves are possible.

        Inputs:
            possible_moves: list[tuple(Piece, list(list(tuple(int, int))))]
             - List of legal moves for the bot
        
        Outputs:
            Optional[tuple(Piece, list(tuple(int, int)))]
             - Suggested move by the bot
        """
        safe_moves = self._suggest_safe_move(possible_moves)
        if safe_moves is None:
            return

        if self._color == PieceColor.BLACK:
            pieces = self._game.p1
        if self._color == PieceColor.RED:
            pieces = self._game.p2
        
        max = self._calculate_consolid(pieces)

        possible_congl_moves = []
        piece, move = safe_moves[0]
        for piece, move in safe_moves:
            orig_loc = (piece.row, piece.col)
            move_loc = move[-1]
            piece._temporary_step(move_loc)
            
            congl = self._calculate_consolid(pieces)
            piece._temporary_step(orig_loc)

            if congl > max:
                max = congl
                possible_congl_moves = [(piece, move)]
            if congl == max:
                possible_congl_moves.append((piece, move))

        if len(possible_congl_moves) > 0:
            return random.choice(possible_congl_moves)


    def _calculate_consolid(self, pieces):
        """
        Calculates the maximum of number of connected pieces.

        Inputs:
            piece: (Piece)
             - Starting piece for calculating consolidation factor
        
        Outputs: (int)
             - Number of pieces connected to the given piece
        """   
        visited = set()
        max = 0
        for piece in pieces:
            if piece in visited:
                continue
            
            visited, curr = self._consolid_dft(set(), piece)
            if curr > max:
                max = curr
        return max
            

    def _consolid_dft(self, visited, piece):
        """
        Helper DFT function for _calculate_consolid()

        Inputs:
            visited: (set)
             - Set of visited pieces
            piece: (Piece)
             - Current piece in DFT
        
        Outputs: (int)
             - Number of non-visited pieces connected to the given piece
        """   
        dirs = [(1, -1), (-1, -1), (-1, 1), (1, 1)]
        color = piece.color
        visited.add(piece)
        consolid = 1
        for dir in dirs:
            try:
                new_r = piece.row + dir[0]
                new_c = piece.col + dir[1]
                if new_r < 0 or new_c < 0:
                    continue
                p = self._game.board.board[new_r][new_c]
                if p is not None and p.color == color and p not in visited:
                    consolid += self._consolid_dft(visited, p)[1]
            except IndexError:
                continue
        
        return visited, consolid


    def _suggest_safe_move(self, possible_moves):
        """
        Suggests "safe" moves that don't let opponent capture on the next turn.

        Returns None if no such moves are possible.

        Inputs:
            possible_moves: list[tuple(Piece, list(list(tuple(int, int))))]
             - List of legal moves for the bot
        
        Outputs:
            Optional[list(tuple(Piece, list(tuple(int, int))))]
             - Suggested safe moves by the bot
        """
        safe_moves = []
        for piece, moves in possible_moves:
            for move in moves:
                orig_loc = (piece.row, piece.col)
                move_loc = move[-1]
                piece._temporary_step(move_loc)
                    
                if self._color == PieceColor.BLACK:
                    all_opp_moves = self._game.player_legal_moves(PieceColor.RED)
                if self._color == PieceColor.RED:
                    all_opp_moves = self._game.player_legal_moves(PieceColor.BLACK)
                
                new_opp_moves = []
                for opp_piece, opp_moves in all_opp_moves:
                    for opp_move in opp_moves:
                        if len(opp_move) > 0:
                            new_opp_moves.append((opp_piece, opp_move))
                piece._temporary_step(orig_loc)
                if len(new_opp_moves) == 0:
                    return [(piece, move)]

                opp_piece_1, opp_move_1 = new_opp_moves[0]
                if abs(opp_piece_1.row - opp_move_1[0][0]) <= 1:
                    if abs(orig_loc[0] - move_loc[0]) < 2:
                        safe_moves.append((piece, move))
            
        if len(safe_moves) > 0:
            return safe_moves
    
    
    def _suggest_run(self):
        """
        Suggests a move that runs away from an opponent's capture move.

        Returns None if no such escape moves are possible.

        Inputs:
            possible_moves: list[tuple(Piece, list(list(tuple(int, int))))]
             - List of legal moves for the bot
        
        Outputs:
            Optional[tuple(Piece, list(tuple(int, int)))]
             - Suggested move by the bot
        """
        opp_moves = []
        if self._color == PieceColor.BLACK:
            all_opp_moves = self._game.player_legal_moves(PieceColor.RED)
        if self._color == PieceColor.RED:
            all_opp_moves = self._game.player_legal_moves(PieceColor.BLACK)
        
        for piece, moves in all_opp_moves:
            for move in moves:
                if len(move) > 0:
                    opp_moves.append((piece, move))

        if len(opp_moves) == 0:
            return 
        
        opp_move_1 = opp_moves[0]

        # If Opponent can take...
        if abs(opp_move_1[1][0][0] - opp_move_1[0].row) > 1:
            possible_runs = []

            # Try and move the piece being taken.
            take_r = int((opp_move_1[1][0][0] + opp_move_1[0].row)/2)
            take_c = int((opp_move_1[1][0][1] + opp_move_1[0].col)/2)
            run_piece = self._game.board.board[take_r][take_c]
            run_moves = run_piece.get_legal_moves()
            start_loc = (run_piece.row, run_piece.col)
            for move in run_moves:
                end_loc = move[-1]
                run_piece._temporary_step(end_loc)
                if self._color == PieceColor.BLACK:
                    new_opp_moves = self._game.player_legal_moves(PieceColor.RED)
                if self._color == PieceColor.RED:
                    new_opp_moves = self._game.player_legal_moves(PieceColor.BLACK)
                
                run_piece._temporary_step(start_loc)
                for piece, opp_moves in new_opp_moves:
                    for opp_move in opp_moves:
                        if abs(opp_move[0][0] - piece.row) < 2:
                            possible_runs.append((run_piece, move))

            if len(possible_runs) > 0:
                return random.choice(possible_runs)
        

    def _suggest_attack(self, possible_moves):
        """
        Suggests a move that safely attacks opponent's pieces, when the bot is
        winning on pieces.

        Returns None if no such safe attack moves are possible.

        Inputs:
            possible_moves: list[tuple(Piece, list(list(tuple(int, int))))]
             - List of legal moves for the bot
        
        Outputs:
            Optional[tuple(Piece, list(tuple(int, int)))]
             - Suggested move by the bot
        """
        avg_row = 0
        avg_col = 0
        if self._color == PieceColor.BLACK:
            for piece in self._game.p2:
                avg_row += piece.row
                avg_col += piece.col
            avg_row /= len(self._game.p2)
            avg_col /= len(self._game.p2)

            bot_pieces = len(self._game.p1)
            opp_pieces = len(self._game.p2)
        if self._color == PieceColor.RED:
            for piece in self._game.p1:
                avg_row += piece.row
                avg_col += piece.col
            avg_row /= len(self._game.p2)
            avg_col /= len(self._game.p2)

            bot_pieces = len(self._game.p2)
            opp_pieces = len(self._game.p1)

        if bot_pieces > opp_pieces:
            safe_moves = self._suggest_safe_move(possible_moves)
            if safe_moves is None:
                return
            if avg_row > 0 and avg_col > 0:
                attack_moves = []
                for piece, move in safe_moves:
                    if abs(move[-1][0] - avg_row) < abs(piece.row - \
                        avg_row) and abs(move[-1][1] - avg_col) < \
                        abs(piece.col - avg_col):
                        # ^^^ If a move gets closer in terms of row and col
                        attack_moves.append((piece, move))
                    elif abs(move[-1][0] - avg_row) < abs(piece.row - \
                        avg_row) or abs(move[-1][1] - avg_col) < \
                        abs(piece.col - avg_col):
                        # ^^^ If a move gets closer in terms of row or col
                        attack_moves.append((piece, move))
                
                if len(attack_moves) > 0:
                    return random.choice(attack_moves)


def _simulate(black, red, scores, size, n=100) -> None:
    """
    Simulates n games between two bots

    Args:
        black: (str) Type of bot that will play with black pieces
        red: (str) Type of bot that will play with red pieces
        scores: (dict) Dictionary mapping colors to wins
        size: (int) Size of board for bots to play on
        n (int): Number of games to simulate, default is 100

    Returns: None
    """
    for _ in range(n):
        game = Checkers(size)
        if black == 'random-bot':
            bot1 = RandomBot(game, PieceColor.BLACK)
        elif black == 'smart-bot':
            bot1 = SmartBot(game, PieceColor.BLACK)
        if red == 'random-bot':
            bot2 = RandomBot(game, PieceColor.RED)
        elif red == 'smart-bot':
            bot2 = SmartBot(game, PieceColor.RED)

        current = bot1

        # While the game isn't over, make a move
        while not game.is_done(): 
            Piece, moves = current.suggest_move(True)
            Piece.move(moves)

            # Update the player
            if current._color == PieceColor.BLACK:
                current = bot2
            elif current._color == PieceColor.RED:
                current = bot1

        # If there is a winner, add one to that
        # bot's tally
        winner = game.get_winner()
        if winner is not None and winner != "It's a draw!":
            scores[winner] += 1
        
    return scores["Black has won!"], scores["Red has won!"]


@click.command(name="checkers-bot")
@click.option('-n', '--num-games',  type=click.INT, default=100)
@click.option('--black', type=click.Choice(['random-bot', 'smart-bot'], \
                case_sensitive=False),default="random-bot")
@click.option('--red', type=click.Choice(['random-bot', 'smart-bot'], \
                case_sensitive=False), default="random-bot")
@click.option('--size', type=click.INT, default=3)


def cmd(num_games, black, red, size):
    scores = {"Black has won!": 0, "Red has won!": 0}
    black_wins, red_wins = _simulate(black, red, scores, size, num_games)

    assert black == 'random-bot' or black == 'smart-bot'
    assert red == 'random-bot' or red == 'smart-bot'

    ties = num_games - (black_wins + red_wins)

    print(f"Bot 1: Black ({black}) wins: {100 * black_wins / num_games:.2f}%")
    print(f"Bot 2: Red ({red}) wins: {100 * red_wins / num_games:.2f}%")
    print(f"Ties: {100 * ties / num_games:.2f}%")


if __name__ == "__main__":
    cmd()
