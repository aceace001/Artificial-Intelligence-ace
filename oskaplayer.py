# initialize board, global variable
START_BOARD = ['wwwww', '----', '---', '--', '---', '----', 'bbbbb']

'''
a more convenient way to make pieces on the board move, since the lists are not 2D, and each row is actually a string,
so it's easier to convert strings into list and change their content; then return the changed string. Argument 1 is
the string that needs to be changed, 2 is the content that is used to replace, 3 is the index position
'''

def replace_char(string, char, index):
    string = list(string)  # convert string to list
    string[index] = char  # change content of the list with corresponding index position
    return ''.join(string)  # return by changing the list back to string

'''
MOVE Function, the function to make pieces actually move, argument 1 is the board given, argument 2 is the coordinate of
the piece, argument 3 is the direction that the piece will move(for calculation purposes, -1 is move left, 0 is move 
right); if the piece in that coordinate can move, then function return the board after the movement, 
else return false(piece cannot move)
'''
def move(board, pos, direction):
    board_2 = board.copy()  # copy the board to make pieces move
    mid = len(board_2) // 2  # find middle point of the board
    x = pos[0]  # X is the position in the row (x coordinate)
    y = pos[1]  # Y is which row is at (y coordinate)
    y1 = y + 1  # next objective
    if y1 > mid:  # if y1 is below mid, then add 1 to original direction in order to match the correct index
        x1 = x + direction + 1
    else:
        x1 = x + direction
    if y1 >= len(board_2):  # reaches the bottom of the board, cannot move anymore
        return False
    if x1 < 0 or x1 >= len(board_2[y + 1]):  # pieces cannot reach outside of left and right boundary
        return False
    piece = board_2[y][x]  # record the piece in the original coordinate
    if board_2[y1][x1] == '-':  # the objective coordinate is empty, can move
        board_2[y] = replace_char(board_2[y], '-', x)  # original coordinate of the piece becomes empty
        board_2[y1] = replace_char(board_2[y1], piece, x1)  # the piece move to the objective coordinate
        return board_2  # return the board after this movement
    else:  # the objective coordinate has already been occupied by some pieces, means it's not empty
        if board_2[y1][x1] == piece:  # if the piece on that objective coordinate is on the same side,
            return False              # then cannot jump over it
        else:  # if the piece on that objective coordinate is on the opponent side
            y2 = y1 + 1  # then move forward based on direction
            if y2 > mid:  # if y2 is below mid, then add 1 to original direction in order to match the correct index
                x2 = x1 + direction + 1
            else:
                x2 = x1 + direction
            if y2 >= len(board_2):  # reaches the bottom of board, cannot move any further
                return False
            elif x2 < 0 or x2 >= len(board_2[y2]):  # pieces cannot reach outside of left and right boundary
                return False
            else:
                if board_2[y2][x2] == '-':  # the objective coordinate is empty, can jump onto it
                    board_2[y] = replace_char(board_2[y], '-', x)  # original coordinate of the piece becomes empty
                    board_2[y1] = replace_char(board_2[y1], '-', x1)  # the coordinate of opponent's piece becomes empty
                    board_2[y2] = replace_char(board_2[y2], piece, x2)  # the piece jump to that objective coordinate
                    return board_2  # return the board after this movement
                else:  # the objective coordinate is not empty, piece cannot jump
                    return False

'''
movegen function, to return all new boards that can be generated in one move, argument 1 is the board given,
argument 2 is an indication as to whose turn it is next ('b' or 'w'); function returns a list of all new boards that can
be generated in one move by the indicated player, if cannot generate moves, return empty list "[]".
Note: This function always make pieces move from the top to bottom, so "w" can move downwards; but in order to make "b"
move upwards and since the board is symmetrical, we can reverse the board before any movement then reverse it again 
after the movement.
'''
def movegen(board, piece):
    global START_BOARD # load initialized board, purpose is to check which side is at the top; if the side is at the bottom, reverse the board to do any operations
    flag = False    # check whether need to reverse.
    board_list = [] # record a list of all new boards that can be generated in one move by the indicated player
    board_2 = board.copy()
    if START_BOARD[0][0] == piece:
        flag = False
    elif START_BOARD[-1][0] == piece:  # if argument 2 is "b", then need reverse the board
        flag = True
    else:   # argument 2 is something other than "w" or "b", then cannot do any further operations
        return False
    # reverse the board if argument is "b"
    if flag:
        board_2.reverse()
    # go through every grid on the board, find all the pieces that need to move
    for y in range(len(board_2)):
        for x in range(len(board_2[y])):
            if board_2[y][x] == piece:    # find the pieces that can be operated
                temp = move(board_2, (x, y), -1)      # direction: left downwards
                if temp:    # if pieces can be generated in move function
                    if flag:    # reverse the board again after the movement if argument is "b"
                        temp.reverse()
                    board_list.append(temp) # then add the next move generated to board_list
                temp = move(board_2, (x, y), 0)    # direction: right downwards
                if temp:    # if pieces can be generated in move function
                    if flag:    # reverse the board again after the movement if argument is "b"
                        temp.reverse()
                    board_list.append(temp) # then add the next move generated to board_list
    # return list of all possible next move
    return board_list


'''
END function to check whether "game over", or check whether the player meet the two requirements for winning;
argument is the current board information; if the game has ended, function returns the pieces of winning side, else return false
'''
def end(board):
    global START_BOARD  # load global variable
    top_piece = START_BOARD[0][0]  # record whether the pieces on the top is b or w
    buttom_piece = START_BOARD[-1][0]  # record the pieces on the buttom
    board_2 = board.copy()
    win_piece = ''  # record the pieces of winner's side
    win_count = 0  # record the number of pieces of winner's side
    # identify whether pieces on top meet the requirements for winning
    flag = True  # a flag for winning
    for i in range(len(board_2) - 1):  # go through every row of the board except the bottom row, if find any pieces of own side, then this is not a win
        if top_piece in board_2[i]:  # find the first piece that does not meet the requirement, make the flag false
            flag = False
            break   # and exit for loop
    if flag:  # after the for loop, if flag is still true, then it meet the requirement for winning, return winner's piece
        # if one side has all their pieces removed from the board, then that player loses
        if top_piece not in board_2[-1]:
            return buttom_piece
        win_piece = top_piece
        win_count = board_2[-1].count(top_piece)
    # reverse the board and repeat the same thing for pieces at the buttom, check whether the buttom wins
    board_2.reverse()
    flag = True
    for i in range(len(board_2) - 1):
        if buttom_piece in board_2[i]:
            flag = False
            break
    if flag:
        # if one side has all their pieces removed from the board, then that player loses
        if buttom_piece not in board_2[-1]:
            board_2.reverse()  # reverse the board before returning
            return top_piece
        temp_count = board_2[-1].count(buttom_piece)  # record number of temporary pieces
        board_2.reverse()  # reverse the board before returning
        if win_piece:  # if both side wins, count the number of each side's pieces
            if win_count == temp_count: # draw if both side have same number of pieces
                return 'equal'
            # else the side with more pieces wins
            elif win_count < temp_count:
                win_piece = buttom_piece
        else:
            win_piece = buttom_piece
    if win_piece:
        return win_piece
    return False


'''
Static board evaluation function in order to identify the optimal solution.We also need the function to see whether the move is 
worth taking and use the score into the MiniMax algorithm function. Argument 1 is the current board information and 
argument 2 is the current indicated player. The function returns the score calculated based on my own evaluation algorithm.
    The basic idea about this algorithm is subtraction:
1. calculate current score for each side, and the final score evaluated for current player is the difference between two players' score
2. when calculating current score, their initialized score = the number of pieces * vertical distance to reach the end of other side (# of rows)
3. evaluation is divided into two parts: "distance score" and "position score"; "distance score" is the vertical distance 
for each piece of current side to reach the end of opposite side, the closer it gets the less score will be subtracted;
"position socre" is when piece is positioned at the rightmost or leftmost side of the board, then it will have less options 
to move, so only add 1 to their score, otherwise add 2 to score.
4. special case 1: if the piece cannot move, then this is a big disadvantage for our side because it means opponent will
have one more move than us(since we cannot move). In order to avoid this, subtract 100 to score so the piece will choose 
other moves instead
5. special case 2: if the piece can meet requirement for winning, then this move is the best next move, so let initialzied 
score times 4 first. Therefore, it will always have the highest score no matter how the evaluation goes afterwards. 
'''
def score(board, piece):
    global START_BOARD  # load global variable
    top_piece = START_BOARD[0][0]  # record whether the pieces on the top is b or w
    buttom_piece = START_BOARD[-1][0]  # record the pieces on the buttom
    score1 = score2 = len(START_BOARD) * len(START_BOARD[0])  # allocate initialized score
    board_2 = board.copy()
    # check whether meet requirement for winning in end function
    temp = end(board_2)
    if temp:  # meet requirement, score for winner times 4
        if temp == top_piece:
            score1 = score1 * 4
        elif temp == buttom_piece:
            score2 = score2 * 4
        else:  # draw
            score1 = score1 * 2
            score2 = score2 * 2
    else:  # does not meet requirement, starts to evaluate
        temp_move = movegen(board_2, top_piece)  # if the piece can move in movegen function
        if temp_move:  # if the piece can move in movegen function
            for y in range(len(board_2)):  # go through the board
                for x in range(len(board_2[y])):
                    if board_2[y][x] == top_piece:  # finds the top piece, start to count the score
                        score1 -= len(board_2) - 1 - y  # "distance score", the closer the piece to the opposite end, the less score it will be subtracted
                        if x == 0 or x == len(board_2[y]) - 1:  # "position score", if the piece is positioned at the rightmost or leftmost of the board, then socre + 1
                            score1 += 1
                        else:   # if the piece is positioned other than leftmost or rightmost, then score + 2
                            score1 += 2
        else:  # if the piece cannot move, score - 100
            score1 = -100
        # do the same evaluation for the other side, but need to reverse the board first then reverse it again in the end
        board_2.reverse()
        temp_move = movegen(board_2, top_piece)
        if temp_move:
            for y in range(len(board_2)):
                for x in range(len(board_2[y])):
                    if board_2[y][x] == buttom_piece:
                        score2 -= len(board_2) - 1 - y
                        if x == 0 or x == len(board_2[y]) - 1:
                            score2 += 1
                        else:
                            score2 += 2
        else:
            score2 = -100
        board_2.reverse()
    # count the score, return resulting score; calculated by subtracting the score the oppponent's score from argument 2 player's score
    if piece == top_piece:
        return score1 - score2
    else:
        return score2 - score1


'''
Oskaplayer top level function, contains MiniMax algorithm; argument 1 is the board given, argument 2 is an indication as
to whose turn it is next ('b' or 'w'), argument 3 is the moves to look ahead. The function uses Minimax algorithm based 
on the score evaluated in SCORE function to find the next best move. It returns the board for the next best move.
One of the basic principles about MiniMax is that the opponent will always take the best strategy against you no matter
how you play the next move. Therefore, the basic idea in this game and this function is that we can find all the moves 
generated from movegen, then the opponent find all the move generated for themselves and assume they will take the best 
move; then we find the most optimal solution among those moves, then that move will be our best move.
Moves to look ahead means the depth we will let MiniMax algorithm search, then we find the best move only within this depth.
'''
def oskaplayer(board, piece, step):
    global START_BOARD  # load global variable
    board_2 = board.copy()  # copy the board to make pieces move
    open_list = []  # store the information for doing further operations in MiniMax search
    if START_BOARD[0][0] == piece:  # check whether need to reverse board
        flag = False
        opp_piece = START_BOARD[-1][0]  # set opponent's piece
    else:
        flag = True
        opp_piece = START_BOARD[0][0]
    # starts the algorithm
    board_list = movegen(board_2, piece)  # find all the possible moves generated from movegen function
    if not board_list:  # if cannot move, then return back to the original board given
        return board_2
    for i in board_list:
        open_list.append([i.copy(), i.copy()])  # find the first level that need to do any operations

    while open_list:
        for i in range(len(open_list)):
            temp_list = movegen(open_list[i][1], opp_piece)  # all the possible moves generated by opponent
            temp_list = sorted(temp_list, key=lambda x: score(x, opp_piece), reverse=True)  # sort score in descending order, then the first value will be the best strategy
            if temp_list:  # exclude the situation where the opponent cannot make further moves
                open_list[i][1] = temp_list[0].copy()
        step -= 1  # this depth of moves has already been searched
        if step == 0:  # if all depth has been searched, then exit loop
            break
        open_list = sorted(open_list, key=lambda x: score(x[1], piece),
                           reverse=True)  # sort score in descending order in order to clear any repetitive situation where operations have same score in the end
        # if the element has the same score as the previous element, then pop that element until loop ends.
        con = 1
        while con < len(open_list):
            flag = False
            for i2 in range(0, con):
                if open_list[i2][1] == open_list[con][1]:
                    flag = True
                    open_list.pop(con)
                    break
            if not flag:
                con += 1
        # expand the next move over and over again
        temp_open_list = []
        for i2 in open_list:
            temp_list = movegen(i2[1], piece)
            if temp_list:  # expand all the possible moves for next step
                for i3 in temp_list:
                    temp_open_list.append([i2[0].copy(), i3.copy()])
            else:
                temp_open_list.append([i2[0].copy(), i2[1].copy()])
        open_list = temp_open_list
    # if open_list is not empty, means we can find our best move, sort the list in descending order; return the first one which is our best move
    if open_list:
        open_list = sorted(open_list, key=lambda x: score(x[1], piece), reverse=True)
        return open_list[0][0]
    # no other strategies left, then just return the current board
    return board

