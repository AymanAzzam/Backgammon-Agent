import numpy as np
import agent

def intialize_board():
    board = np.zeros(29) 
    #positions from 1 to 24: the number of coins in that position (+ for player 1, - for player -1)
    #position 25: number of killed coins for player 1
    #position 26: number of killed coins for player -1
    #position 27: number of coins that have been beared off from the board for player 1
    #position 28: number of coins that have been beared off from the board for player -1
    
    #Player 1 (White)
    board[6] = 5
    board[8] = 3
    board[13] = 5
    board[24] = 2
    
    #Player -1 (Red)
    board[1] = -2
    board[12] = -5
    board[17] = -3
    board[19] = -5
    
    return board

def roll_dice():
    return np.random.randint(1,7,2)

def main():
    max_depth = 2
    board = intialize_board()
    player_num = 1
    i = 0

    while(not agent.game_over(board)):
        dice = roll_dice()
        
        print(str(i))
        print("player " + str(player_num))
        print("dice: " +str(dice[0])+ " and " +str(dice[1]))
        board = agent.agent(board, dice, player_num, max_depth)

        # Play again if the the two dices are equivalent
        if dice[0] == dice[1]:
            print("Second play")
            print("player " + str(player_num))
            print("dice: " +str(dice[0])+ " and " +str(dice[1]))
            board = agent.agent(board, dice, player_num, max_depth)

        player_num = -player_num
        i = i + 1

    if(board[27] >= 15):
        print("The winner is player 1")
    if(board[28] <= -15):
        print("The winner is player -1")
    
if __name__ == '__main__':
    main()
