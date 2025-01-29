import copy
import simplejson as json
from Board import Board


winning_positions = []


def minimax(board, depth, maximiser, alpha, beta):

    evaluation_multiplier = 1 if maximiser else -1

    # check in dict if it is a known position
    dict_check = verify_position_in_dict(board.state)
    if dict_check:
        return dict_check[0], dict_check[1]*evaluation_multiplier

    if depth == 0 or board.validate():
        return None, board.evaluate()*evaluation_multiplier
    
    if maximiser:
        best_move = (None, float('-inf'))

        # play every move and minimax the result
        for move in board.get_all_moves():
            temp_board = copy.deepcopy(board)
            temp_board.pop(move[0], move[1])

            eval = minimax(temp_board, depth - 1, False, alpha, beta)[1]
            # add winning position in game_dict
            if eval == 20:
                add_move_in_game_dict(temp_board.state, move, eval)

            alpha = max(alpha, eval)
            if eval > best_move[1]:
                best_move = move, eval
            if beta <= alpha:
                break
    
    if not maximiser:
        best_move = (None, float('inf'))
        
        for move in board.get_all_moves():
            temp_board = copy.deepcopy(board)
            temp_board.pop(move[0], move[1])

            eval = minimax(temp_board, depth - 1, True, alpha, beta)[1]
            
            beta = min(beta, eval)
            if eval < best_move[1]:
                best_move = move, eval
            if beta <= alpha:
                break
        
    return best_move


def add_move_in_game_dict(board_state, move, eval):
    # we need to unpop the move to get the board position before the move was made
    board_state[move[0]][1] -= move[1]
    
    board_state_str = ""
    
    for row in board_state:
        board_state_str += str(row[1])

    new_data = {
        "position" : board_state_str,
        "best_move": move,
        "eval": eval
    }
    position_found = False

    global winning_positions

    for item in winning_positions:
        if item["position"] == new_data["position"] and item["eval"] == new_data["eval"]:
            position_found = True
    
    if not position_found:
        winning_positions.append(new_data)


def check_mirror_positions(dict_position, board_state_str:str):
    """ Reduce number of branches need to be check in the minimax tree by checking for mirror positions

        We change the move given by the dict to account for mirror row

        I know there must be a better way to do this then by these if statements, but hey do a pull request if you want

        Returns:
            [best_move:[row, pops], eval:int] | None
    
    """

    if (dict_position["position"] == board_state_str):
        return[dict_position["best_move"], dict_position["eval"]]
    
    def swap_positions(s, pos1, pos2):
        s = list(s)
        s[pos1], s[pos2] = s[pos2], s[pos1]
        return ''.join(s)


    def check_swapped_positions(swapped_board_state_str, pos1, pos2):
        if dict_position["position"] == swapped_board_state_str:
            best_move = list(dict_position["best_move"])
            if best_move[0] == pos1:
                best_move[0] = pos2
            elif best_move[0] == pos2:
                best_move[0] = pos1
            return [best_move, dict_position['eval']]
        return None
    
    def check_double_swapped_positions(swapped_board_state_str, pos1, pos2, pos3, pos4):
        if dict_position["position"] == swapped_board_state_str:
            best_move = list(dict_position["best_move"])
            if best_move[0] == pos1:
                best_move[0] = pos2
            elif best_move[0] == pos2:
                best_move[0] = pos1
            elif best_move[0] == pos3:
                best_move[0] = pos4
            elif best_move[0] == pos4:
                best_move[0] = pos3
            return [best_move, dict_position['eval']]
        return None
    

    mirror_positions = [(0, 5), (1, 4), (2, 3)]

    # Check all combinations of single swaps
    for pos1, pos2 in mirror_positions:
        swapped_board_state_str = swap_positions(board_state_str, pos1, pos2)
        result = check_swapped_positions(swapped_board_state_str, pos1, pos2)
        if result:
            test_board = Board()
            test_board.set_state_from_str(board_state_str)
            is_valid, params = validate_input(f"{result[0][0]} {result[0][1]}", test_board)
            if is_valid:
                return result
            else:
                print("Error in check_mirror_positions, single swap", params, board_state_str, result)
                raise Exception("Error in check_mirror_positions", params)
            

    # Check double swaps
    for i in range(len(mirror_positions)):
        for j in range(i + 1, len(mirror_positions)):
            pos1, pos2 = mirror_positions[i]
            pos3, pos4 = mirror_positions[j]
            swapped_board_state_str = swap_positions(board_state_str, pos1, pos2)
            swapped_board_state_str = swap_positions(swapped_board_state_str, pos3, pos4)
            result = check_double_swapped_positions(swapped_board_state_str, pos1, pos2, pos3, pos4)
            if result:
                test_board = Board()
                test_board.set_state_from_str(board_state_str)
                is_valid, params = validate_input(f"{result[0][0]} {result[0][1]}", test_board)
                if is_valid:
                    return result
                else:
                    print("Error in check_mirror_positions, double swap", params, board_state_str, swapped_board_state_str, result, pos1, pos2, pos3, pos4)
                    raise Exception("Error in check_mirror_positions", params)
        

    # swap pos 0-1-2 and 3-4-5
    swapped_board_state_str = board_state_str[::-1]
    if (dict_position["position"] == swapped_board_state_str):
        best_move = list(dict_position["best_move"])
        if best_move:
            best_move[0] = 5 - best_move[0]
            test_board = Board()
            test_board.set_state_from_str(board_state_str)
            is_valid, params = validate_input(f"{best_move[0]} {best_move[1]}", test_board)
            if is_valid:
                return [best_move, dict_position['eval']]
            else:
                print("Error in check_mirror_positions, single swap", params)
                raise Exception("Error in check_mirror_positions", params)




def verify_position_in_dict(board_state):
        
    board_state_str = ""

    for row in board_state:
        board_state_str += str(row[1])

    global winning_positions

    for position in winning_positions:
        pos_found = check_mirror_positions(position, board_state_str)
        if (pos_found):
            return pos_found
        
    return False


def validate_input(input:str, board:Board):
    input_params = input.split(' ')

    validated_params = []

    if len(input_params) != 2:
        return False, "input must be two numbers separated by a space"

    for i, param in enumerate(input_params):
        try:
            pop_quantity = int(param)
            validated_params.append(pop_quantity)
        except:
            return False, "input must be two numbers separated by a space"

        if i > 1:
            return False, "input must be two numbers separated by a space"

    row = validated_params[0]
    pop_quantity = validated_params[1]

    if row < 0:
        return False, "Enter a valid row"
    if row > 5:
        return False, "Enter a valid row"

    if pop_quantity < 1:
        return False, "You must pop at least one bubble"

    if (pop_quantity >= board.state[row][0]):
        return False, "Max pop is row quantity - 1"

    if (pop_quantity + board.state[row][1] > board.state[row][0]):
        return False, "Can't pop more then max row size"

    return True, validated_params


def ask_human_for_move(board):
    valid_move = None

    while not valid_move:
        print("\nIt's your turn " + board.current_player)
        #print(f"\nCurrent board eval = {board.evaluate()}\nAll possible moves : {board.get_all_moves()}")
        #print(f"Best move from minimax : {minimax(board, 5, True, float('-inf'), float('inf'))}")
        print(board)
        move = input("Play next move by entering the row number (starts at 0),\nfollowed by the number of bubble to pop.\ni.e. \"0 1\"\n")
        
        if (move == "exit"):
            board.current_player = 'nobody'
            return False

        valid_move, params = validate_input(move, board)
        if (valid_move):
            board.pop(params[0], params[1])
            board.switch_players()
        else:
            format_print(params)
    
    return valid_move


def ask_bot_for_move(board, bot_difficulty):
    minimax_result = minimax(board, bot_difficulty, True, float('-inf'), float('inf'))
    bot_move = minimax_result[0]
    bot_move_str = f"{bot_move[0]} {bot_move[1]}"
    valid_move, params = validate_input(bot_move_str, board)
    if not valid_move:
        print("Bot made an invalid move", params)
        raise Exception("Bot made an invalid move : " + bot_move_str)
    print(f"\nBot_lvl_{bot_difficulty} plays {bot_move}, with eval {minimax_result[1]}")
    board.pop(bot_move[0], bot_move[1])
    board.switch_players()

    
def load_winning_positions():
    with open("game_dict.json", 'r+') as file:
        game_dict = json.load(file)
        return  game_dict['decisive_positions']


def write_winning_positions(winning_positions):
    with open("game_dict.json", 'r+') as file:
        game_dict = json.load(file)
        game_dict['decisive_positions'] = winning_positions
        file.seek(0)
        json.dump(game_dict, file, ensure_ascii=False, indent=4)


def format_print(message):
    print(f"\n|{len(message) * '-'}|")
    print(f'{message}')
    print(f"|{len(message) * '-'}|\n")


def main():

    # 40 char per line
    game_mode = input("""
                /--------------------------------------\\
                |----------Welcome to Pop it!----------|
                |--------------------------------------|
                |------------The last player-----------|
                |--------------to pop loses------------|
                |--------------------------------------|
                |---------------Game Modes-------------|
                |--------------1: 1 player-------------|
                |--------------2: 2 players------------|
                \\--------------------------------------/\n\n""")

    global winning_positions
    try:
        winning_positions = load_winning_positions()

    except:
        print('Could not open game_dict.json, make sure the file exist')
    
    while game_mode != '1' and game_mode != "2":
        game_mode = input("Enter a valid game mode (1 or 2)\n")


    if game_mode == "1":
        
        input_not_valid = True
        while input_not_valid:
            bot_difficulty = input("Enter bot difficulty (1 to 20)\nMore then 8 will be real slow if the game was not already analysed in the game_dict.\n")
            try:
                bot_difficulty = int(bot_difficulty)
                if bot_difficulty < 21 and bot_difficulty > 0:
                    input_not_valid = False
            except:
                format_print("Bot difficulty must be a number between 1 and 8")

        humain_first_to_play = input('Do you want to play first? [Yes/no]\n')
        if humain_first_to_play == 'Yes':
            player_1_name = 'Humain'
            player_2_name = f'Bot_lvl_{bot_difficulty}'
        else:
            player_1_name = f'Bot_lvl_{bot_difficulty}'
            player_2_name = 'Humain'

    else:
        player_1_name = 'Humain_1'
        player_2_name = 'Humain_2'

    board = Board(player_1_name, player_2_name)
    game_over = False

    while not game_over:

        if game_mode == "1" and player_1_name == "Humain":

            valid_move = ask_human_for_move(board)

            if valid_move == False:
                game_over = True

            if board.validate():
                game_over = True

            
            # One player, play against the computer
            if not game_over and valid_move:
                ask_bot_for_move(board, bot_difficulty)

                if board.validate():
                    game_over = True

        elif game_mode == '1' and player_2_name == 'Humain':
            
            ask_bot_for_move(board, bot_difficulty)

            if board.validate():
                game_over = True

            if not game_over:
                valid_move = ask_human_for_move(board)

                if board.validate():
                    game_over = True


    write_winning_positions(winning_positions)
    format_print("Game over! Congrats " + board.current_player)






if __name__ == "__main__":
    main()

    
        