# Backgammon
The game rules and the intial state are explained in https://www.bkgm.com/rules.html

### Board Representation
The two players are defined as player 1 and player -1.
The board has 29 positions:
- position 0 isn't used.
- positions 1-24 Contain the number of checkers in that position as exaplined in https://www.bkgm.com/rules.html
- positions 25 contains the number of killed checkers for player 1
- positions 26 contains the number of killed checkers for player -1
- positions 27 contains the number of checkers have been beard off for player 1
- positions 28 contains the number of checkers have been beard off for player -1

Positions for player 1 are positive values while positions for player -1 are negative values

few examples:
- `board[23] = 3` means that player 1 has 3 checkers on the 23rd position of the board.
- `board[21] = -10` means that player -1 has 10 checkers on the 21st position of the board.
- `board[25] = 1` means that player 1 has 1 killed checker.
- `board[28] = -2` means that player -1 has beared off two checkers.

### Agent
The Agent uses the expectminimax algorithm to represent the possible moves then it choses the best moves based on the evaluatuion function, you can control the depth of tree using max_depth parameter in **backgammon.py**. The evaluation function is explained in https://bkgm.com/articles/SjoqvistStenlund/report.pdf

### Run
The code is implemented using python so you should have python and numpy library installed the run the following command:
```bash
python backgammon.py
```