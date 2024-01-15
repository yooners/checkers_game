# project-shikai-sycalvind-ianhuzhang-smayan
Names and component:
- Shi Kai Chow: Game Logic
- Siyang Calvin Dai: TUI
- Smayan Khanna: GUI
- Ian Zhang: Bot

*Note: We use the code in mocks.py for our mocks.

Running the code in this repository requires using a number of Python libraries. Please create a virtual environment before installing these libraries. Then, install the modules listed in each section below to run the code succesfully.

# TUI

**Running the TUI:**
All code here should be run from the root project repository.

You will need to download **time**, **click** and **colorama** in your local environment to run the TUI.

- To run the TUI on a standard 8 x 8 Checkers game with 2 human players:
```
    python3 src/tui.py
```

The TUI displays the checkers board in its initial state. Pieces are displayed as red/black dots (signifying which player it belongs to). The white 'X's signify white grids on the checkers board, where pieces cannot go on.

The TUI will ask a player to select a piece. You must specify the row index (starting from 0) and the column index (starting from 0) of the piece you would like to select. You can refer to the coordinate labels at the top and left sides of the board. If your piece is not on the tile that you selected, you will be prompted to select again.

Once you have selected a piece, the TUI highlights a list of options of all possible legal moves (including intermediate tile coordinates reached) for that piece. If there are no legal moves for the piece you selected, the TUI will inform you that there are no legal moves and prompt you to select another piece. This method of highlighting the legal moves follows Professor Borja's suggestion (Ed post #1308). The numbers in each bracket represent the row index, and column index respectively of each tile reached by the piece, in order. For example, if the move includes 2 jumps, the move option will be displayed as "(2, 3), (4, 6)". There is also an option for you to select another piece to move instead.

Once you have chosen your move, select the option number (the integer to the left of the move) of your desired move. If you insert a number that is not valid, the TUI will prompt you to select again. The TUI will carry out your move and display the final state of the board after your move. If a piece has Kinged during the game, it will be displayed as a "K" of your respective color on the board. 

- The TUI supports board sizes from 6x6 to 20x20. You can play on boards of different sizes by running: 
```
    python3 src/tui.py --size <n>
```

Where ``<n>`` should be replaced with a number between 2-9 inclusive. The number of rows and columns on the board will be n * 2 + 2. For example, to play on a 20x20 board, you would run:
```
    python3 src/tui.py --size 9
```

- You can also play against a bot by setting either red or black to be a bot:
```
    python3 src/tui.py --black <bot>

    python3 src/tui.py --red <bot>
```

Where ``<bot>`` should be replaced with either ``smart-bot`` or ``random-bot``.

- You can even have 2 bots play against one another like this:
```
    python3 src/tui.py --black <bot> --red <bot>
```

The TUI inserts an artificial delay of half a second between each bot's move, so that you can more easily observe the progress of the game. You can modify this delay using the ``--bot-delay <seconds>`` parameter.

- In the unlikely event that actual game logic fails or crashes, you can still experience the TUI's features by 
running it with mock game logic. You can adjust the board size on mocks in the same way as you would with the real game logic:
```
    python3 src/tui.py --mode mock --size <n>
```


# GUI

**Running the GUI:**

You will need to download **pygame**, **click** and **itertools** in your local environment to run the GUI.

To run the GUI, run the following from the root of the repository (standard 8 x 8 Checkers game with 2 human players):

    python3 src/gui.py

To change the mode of GUI, run the following from the root of the repository. Preferably, run ```real``` as it uses game logic.

    python3 src/gui.py --mode <mode>

To change the board size of the GUI, run the following from the root of the repository (Default 3, must be > 0)
The number of rows and columns on the board will be n * 2 + 2 so n = 3 is 8x8, n = 9 is 20x20

    python3 src/gui.py --mode real --board-size <n>

To change the players to a bot, run this command. Default is two human players (Remember, Player 1 is always black and Player 2 is always red)
You can set either player1 or player2 to be a bot:

    python3 src/gui.py --mode real --board-size 3 --player2 <bot>
    
    python3 src/gui.py --mode real --board-size 3 --player1 <bot>
    
**OR** like the TUI, you can have two bots play
against each other like this:

    python3 src/gui.py --player1 <bot> --player2 <bot>

There are two bots, ``smart-bot`` and ``random-bot``

The ``--bot-delay <seconds>`` parameter is also supported. I reccomend 0.5
for player bot games.

The GUI displays the state of the board. If it is your piece, select a piece on your team. If it has legal moves, it will display it. Now click the move you want to make. Once you do this, your turn will end. If you select a piece on your team with no legal moves, no moves will be drawn. If piece(s) can jump, you **can only** select the jump move(s) -this is a fundamental rule of checkers. In that scenario, you will not be able to select other pieces which can't jump even if their moves **are legal!**. 

**Important Note!** 
If there is a fork in the path like shown below you will only be allowed to select the tile which doesn't have a shared tile with another move. I.e. clicking the center green dot won't move the piece (the GUI wont allow you to) - you will have to click either the right or left green dot to specify your path. This is to avoid confusion.

**Also note pygame takes a few seconds to render the board so you might see a black screen for 5-6 seconds. **

<img width="365" alt="Screenshot 2023-03-03 at 6 54 29 PM" src="https://user-images.githubusercontent.com/88395390/222868649-97b6237c-6731-4015-adda-b9d4e4ea4abe.png">

With all that done, here are the commands I reccomend for the best playing/viewing experience. Enjoy!
    
Bot v Bot

    python3 src/gui.py --player1 smart-bot --player2 smart-bot --bot-delay 0.4
    
Player v Bot

    python3 src/gui.py --player2 smart-bot --bot-delay 0.5
    
Player v Player - Try a bigger board!

    python3 src/gui.py --board-size 6
    

# Bots

The ``bots.py`` file includes two classes:

- ``RandomBot``: A bot that will just choose a move at random
- ``SmartBot``: A bot that will make moves according to https://www.wikihow.com/Win-at-Checkers, with modifications by me. Will play with the following logic:

    1. In early game stages, try to take control of the center "safely" (#9)
    2. King as many pieces as possible
    3. If forced to take, takes as many pieces as possible
    4. Blocks opponent from taking the bot's pieces
    5. Tries to run from Opponent captures
    6. If winning, attacks opponent pieces
    7. Consolidates pieces "safely" (#9)
    8. Advances non-king pieces "safely" (#9)
    9. Plays any "safe move" that does not result in an opponent capture
    10. Randomly moves

Smart bot also talks! Keep an eye out for what it 
says in the Terminal.


These two classes are used in the TUI and GUI, but you can also run
``bot.py`` to run 100 simulated games where two bots face each other,
and see the percentage of wins and ties. For example:
    
    $ python3 src/bot.py -n 1000 --black random-bot --red random-bot
    Bot 1: Black (random-bot) wins: 48.40%
    Bot 2: Red (random-bot) wins: 50.40%
    Ties: 1.20%

    $ python3 src/bot.py -n 1000 --black random-bot --red smart-bot
    Bot 1: Black (random-bot) wins: 0.20%
    Bot 2: Red (smart-bot) wins: 98.90%
    Ties: 0.90%

You can control the number of simulated games using the ``-n <number of games>`` parameter to ``bots.py``, and the color of each bot by using the ``--black <bot>`` and ``--red <bot>`` parameters, where ``<bot>`` is either ``smart-bot`` or ``random-bot``. The default number of games simulated is 100, and the default bot for both colors is ``random-bot``.

You can also control the board size by using ``--size <board_size>``. The default board size is 3.



# Design Changes since Milestone 1
**- Grading comment:
"There is a class representing a board, but it includes Checkers-specific game logic. It would be better to implement a Board class that is completely game-agnostic, allowing Checkers logic to appear only in a main Checkers class (and/or a Piece class)"**

**- Grading comment:
"The board class uses the "n" in "C_n", which constrains the type of board we would create. For example, there is a variant of Chess that is played on a 16x12 board. We may want to be able to support boards of that size in the future. It would be better to be able to specify an arbitrary number of rows and columns."**

We did the following to address both comments:

We changed the Board Class such that board dimensions are not restricted to checkers logic anymore, and one can input the number of rows/cols separately. The Board Class only holds board information, not checkers logic

We created a new Checkers Class that specifically handles Checkers game logic.


**- Grading comment:
"There is no way for the GUI/TUI to access the state of the board so it can display it."**

We created a getter method "to_piece_grid(self)" in the Board Class to allow GUI/TUI to access board without calling on attribute.

**- Grading comment:
"The game logic implementation has minor differences with the design in design/checkers.py. Make sure to keep that file updated as you change the design."**

Design file is now aligned with src/checkers.py

**- Other changes:**

Public attributes changed to private

Unnecessary methods removed




# Component Changes Since Milestone 2

**Game Logic**

Checkers Class:

Created new 'Checkers' class

- Majority of old 'board' class moved here, board now only to represent a board

Added functionality within player_legal_moves to only include pieces with jumps
- created helper functions for clarity

Completed get_winner(), is_done()

Piece Class:

Fully implemented DFS in get_legal_moves
- Split into initialiser and helper function for clarity, general debugging

Overall:

Added functionality for GUI, TUI and bot
- incorporated methods (eg: is_done(), temporary_step()) for GUI, TUI and bot.py

**TUI**

- Grading comment: "Does not provide a means to select a piece, and highlight all possible moves for that piece."

I integrated with the game logic to allow the player to select a piece by inputing its row and column coordinates in the TUI. The TUI will then display a list of all legal moves for the piece, if any. If there are no possible moves for that piece, the TUI would say that "There are no legal moves for this piece."

- Grading comment: "Does not support board sizes from 6x6 to 20x20"

I added @click.option to allow players to alter the Checkers board size, while setting the default board size to 8x8.

- Grading comment: "Correctness can be improved by addressing the issues with trying to have a bot play as either player1 or player2"

I added code to integrate the TUI with bots to play as either "black" or "red", or both.

- Grading comment: "Quality could be improved by adhering to 80 characters per line, and splitting up arithmetic looks like a good way to go about that here."

I improved code quality by adhering to 80 characters per line.

- Grading comment: "I think it'd also be cool if you figured out a way to make the board appear checkered, but that's just a cosmetic thing that you would want to work on last."

I tried making the board checkered by adding a white "X" on white tiles where pieces cannot go onto.

- Others changes:

Integrated TUI with new Checkers Class.

Changed "player 1" and "player 2" names to "black" and "red" to minimize confusion.

Added code to integrate with game logic, to prevent users from not jumping when jumps are possible.

Added and refined detailed docstrings for functions.

**GUI**

- Grading commment - Does not support board sizes from 6x6 to 20x20

Added a click option to support any board size 6x6 to 20x20 or even larger if needed. 

Configured GUI to work with new 'Checkers' class and PieceColor attributes

Added piece movement

Implemented turns

Implemented displaying a pieces legal moves

Integrated the GUI with the new Checkers Class

Added a gold "K" to the king piece to make it easier to differentiate (also a gold outline)

Created a GameInterface class to clean the code.

Added code to check and deal with forked paths and intersecting moves - see description above

Fixed bugs such as rendering issues when two bots played

Overall:
Added functionality for bots including bot delays and bot-bot games. Integrated GUI with real gameplay (checkers.py)

**Bot**


Milestone 1:

Configured bot to work with new 'Checkers' class and PieceColor attributes

Changed each logical step in suggest_move() to an individual Bot method

Implemented new logic:
  - Maintaining Back Row
  - Consolidating Pieces

Milestone 2:

Implemented remaining Logical steps
  - Attacking
  - Running
  - Blocking
  - Playing safe moves

Fixed bugs

Optimized parameters in bot logic

Added functionality to test the bot through the command line independently of GUI and TUI

