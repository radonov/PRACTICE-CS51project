from connectfour import *





def generate_possible_moves(board):
    #Generator of possible moves
    from connectfour import IllegalMove

    for i in range(0, board.board_width):
        try:
            yield (i, board.do_move(i))
        except IllegalMove:
            pass


#Define what is negative and positive infinity
try:
    positive_infinity = float("inf")
    negative_infinity = float("-inf")
#in case inf does not register, happens on some PCs apparently
except ValueError:                 
    INFINITY = float(2e1000)       
    NEG_INFINITY = float(-2e1000) 

def alpha_beta_pruning(board, depth, eval_fn, playertype, alpha, beta):
    if board.is_game_over() or depth <= 0:
        return eval_fn(board)
    
    if playertype:
        for move, new_board in generate_possible_moves(board):
            alpha = max(alpha, alpha_beta_pruning(new_board, depth-1, eval_fn, False, alpha, beta))
            if beta <= alpha:
                break
        return alpha
    else:
        for move, new_board in generate_possible_moves(board):
            beta = min(beta, alpha_beta_pruning(new_board, depth-1, eval_fn, True, alpha, beta))
            if beta <= alpha:
                break
        return beta

def alpha_beta_search(board, depth, eval_fn):


    best_val = None
    
    for move, new_board in generate_possible_moves(board):
        val = alpha_beta_pruning(new_board, depth-1, eval_fn,False, negative_infinity, positive_infinity)
        if best_val == None or val > best_val[0]:
            best_val = (val, move, new_board)

    return best_val[1]



def get_horizontal_chain_len(board, row, col, player):
    count = 0
    for i in range(3):
        if board.get_cell(row, col+i) == player:
            count += 1
    return count

def get_vertical_chain_len(board, row, col, player):
    count = 0
    for i in range(3):
        if board.get_cell(row+i, col) == player:
            count += 1
    return count

def get_diagonal_chain_len(board, row, col, player):
    count = 0
    for i in range(3):
        if board.get_cell(row+i, col+i) == player:
            count += 1
    return count




def better_evaluate(board):

    score = 0
    '''
    Calculate how many chains you and your opponent has according to the number of
    tokens on the board.
    '''

    if board.longest_chain(board.get_current_player_id()) == 4:
        score = 2000 - board.num_tokens_on_board()
    elif board.longest_chain(board.get_other_player_id()) == 4:
        score = -2000 + board.num_tokens_on_board()

   
    else:
        #calculate own positions
        current_player = board.get_current_player_id() 
        for row in range(3):
            for col in range(4):
                h1 = get_horizontal_chain_len(board, row, col, current_player)
                v1 = get_vertical_chain_len(board, row, col, current_player)
                d1 = get_diagonal_chain_len(board, row, col, current_player)
                m1 = max([h1, v1, d1])
                score += m1*m1

        #calculate other player positions
        other_player = board.get_other_player_id()
        for row in range(3):
            for col in range(4):
                h2 = get_horizontal_chain_len(board, row, col, other_player)
                v2 = get_vertical_chain_len(board, row, col, other_player)
                d2 = get_diagonal_chain_len(board, row, col, other_player)
                print h2, v2, d2
                m2 = max([h2, v2, d2])
                score -= m2*m2
                
        
            

    return score

# Uncomment this line to make your better_evaluate run faster.


the_computer = lambda board: alpha_beta_search(board, depth=4, eval_fn=better_evaluate)
run_game(human_player, the_computer)




