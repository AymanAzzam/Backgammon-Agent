import numpy as np


def update_board(board, move, player):
    
    updated_board = np.copy(board)

    # if there is a move
    if len(move) > 0:
        startPip = move[0]
        endPip = move[1]
        
        # moving the dead coin if the move kills an opponent coin
        if updated_board[endPip] + player == 0:
            updated_board[endPip] = 0
            jail = 25+(player==1)
            updated_board[jail] = updated_board[jail] - player
        
        updated_board[startPip] = updated_board[startPip]- player
        updated_board[endPip] = updated_board[endPip] + player

    return updated_board

def game_over(board):
    return board[27] >= 15 or board[28] <= -15

def legal_move(board,dice,player):
    possible_moves = []

    if player == 1:
        
        # dead coin needs to back to the board
        if board[25] > 0: 
            destination = 25-dice
            if board[destination] >= -1:
                possible_moves.append(np.array([25,destination]))
                
        # no dead coins        
        else:
            # bearing off case
            if sum(board[7:25]>0) == 0: 
                if (board[dice] > 0): # we can bear off a coin
                    possible_moves.append(np.array([dice,27]))
                    
                elif not game_over(board): #play the farthest one in the home board
                    s = np.max(np.where(board[1:7]>0)[0]+1)
                    if s<dice:
                        possible_moves.append(np.array([s,27]))
                    
            possible_start_pips = np.where(board[0:25]>0)[0]

            # finding all other legal options
            for s in possible_start_pips:
                end_pip = s-dice #moving anti-clockwise
                if end_pip > 0 and board[end_pip] > -2:
                    possible_moves.append(np.array([s,end_pip]))
                        
    elif player == -1:
        
        # dead coin needs to back to the board
        if board[26] < 0: 
            start_pip = dice
            if board[start_pip] < 2:
                possible_moves.append(np.array([26,start_pip]))
                
        # no dead coins       
        else:
            # bearing off case
            if sum(board[1:19]<0) == 0: 
                if (board[25-dice] < 0): # we can bear off a coin
                    possible_moves.append(np.array([25-dice,28]))
                elif not game_over(board): #play the farthest one in the home board
                    s = np.min(np.where(board[19:25]<0)[0])
                    if (6-s)<dice:
                        possible_moves.append(np.array([19+s,28]))
                    
            # finding all other legal options
            possible_start_pips = np.where(board[0:25]<0)[0]
            for s in possible_start_pips:
                end_pip = s+dice #Moving Clockwise
                if end_pip < 25 and board[end_pip] < 2:
                    possible_moves.append(np.array([s,end_pip]))
        
    return possible_moves


def legal_moves(board,dice,player):
    
    moves = []
    boards = []

    # try using the first dice, then the second dice
    possible_first_moves = legal_move(board, dice[0], player)
    for move1 in possible_first_moves:
        temp_board = update_board(board,move1,player)
        possible_second_moves = legal_move(temp_board,dice[1], player)
        for move2 in possible_second_moves:
            moves.append(np.array([move1,move2]))
            boards.append(update_board(temp_board,move2,player))

    if dice[0] != dice[1]:
        # try using the second dice, then the first one
        possible_first_moves = legal_move(board, dice[1], player)
        for move1 in possible_first_moves:
            temp_board = update_board(board,move1,player)
            possible_second_moves = legal_move(temp_board,dice[0], player)
            for move2 in possible_second_moves:
                moves.append(np.array([move1,move2]))
                boards.append(update_board(temp_board,move2,player))
            
    # if there's no pair of moves available, Try the maximum dice only:
    if len(moves)==0: 
        # play the largest dice only:
        possible_first_moves = legal_move(board, np.maximum(dice[0],dice[1]), player)
        for move in possible_first_moves:
            moves.append(np.array([move]))
            boards.append(update_board(board,move,player))

    # play the smallest dice only:        
    if(len(moves)==0 and dice[0] != dice[1]):
        possible_first_moves = legal_move(board, np.minimum(dice[0],dice[1]), player)
        for move in possible_first_moves:
            moves.append(np.array([move]))
            boards.append(update_board(board,move,player))
    
    return moves, boards 

# I used the evaluation function mentioned in
#https://bkgm.com/articles/SjoqvistStenlund/report.pdf
def evaluate(board, player):
    n = 0
    m = 0

    if player == 1:
        for i in range(25):
            if(board[i] > 0): #door of max Checkers
                n = n + 2
                if(i < 7):       # in home board for player 1
                    n = n + 1
                if(board[i] > 4): # if number of checkers > 4
                    n = n - 1
            elif(board[i] < 0): #door of min Checkers
                m = m - 2
                if(board[i] < -4): # if number of checkers < 4
                    m = m + 1
        return -0.01 * ( n + m) + 0.029 * ( - board[26] - board[25])

    else:
        for i in range(25):
            if(board[i] < 0): #door of min Checkers
                n = n - 2
                if(i > 18):       # in home board for player 2
                    n = n - 1
                if(board[i] < -4): # if number of checkers < -4
                    n = n + 1
            elif(board[i] > 0): #door of max Checkers
                m = m + 2
                if(board[i] > 4): # if number of checkers < 4
                    m = m - 1
        return -0.01 * ( n + m) + 0.029 * (board[25] + board[26])


def expectminimax(board, dice, player, my_turn,depth,max_depth):
 
    # Condition for Terminal node
    if (game_over(board) or max_depth == depth):
        return evaluate(board, player), [], board
     
    # Maximizer node if player_1
    # Minimizer node if player_2 
    if (my_turn):
        moves, boards = legal_moves(board,dice,player)
        if len(moves) == 0:
            return evaluate(board, player), [], board
        out_value = -100000 * player
        index = 0
        for i in range(len(moves)):
            value, move, edited_board = expectminimax(boards[i], dice , -player, False, depth+1, max_depth)
            if(player == 1 and value > out_value or (player == -1 and value < out_value)):
                out_value = value
                index = i
        return out_value, moves[index], boards[index]
  
    # Chance node. Returns the average of all childreen
    else:
        average = 0
        for d1 in range(7):
            for d2 in range(7):
                value, move, edited_board = expectminimax(board, np.array([d1, d2]), player, True,depth + 1,max_depth)
                average = average + value
        return average/36.0, [], board

def agent(board,dice,player,max_depth):

    my_turn = True
    depth = 0

    value, moves, boards = expectminimax(board, dice, player, my_turn,depth,max_depth)
    
    #print(len(moves))
    if(len(moves) > 0):
        print("1)agent desided to move a coin from " +str(moves[0][0])+ " to " +str(moves[0][1]))
    if(len(moves) > 1):
        print("2)agent desided to move a coin from " +str(moves[1][0])+ " to " +str(moves[1][1]))
    
    if(len(moves) > 0):
        print("New Board : ")
        print(boards[1:25])
        print("#Dead Coins for Player 1 = " + str(boards[25]))
        print("#Dead Coins for Player -1 = " + str(boards[26]))
        print("#Coins that have been beared off from the board for player 1 = " + str(boards[27]))
        print("#Coins that have been beared off from the board for player -1 = " + str(boards[28]))
        print("")
        print("")

    return boards
