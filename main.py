import copy


class Board:
    def __init__(self, player_1='player_1', player_2='player_2'):
        self.state = [
            [3, 0],
            [5, 0],
            [6, 0],
            [6, 0],
            [5, 0],
            [3, 0],
        ]

        self.player_1:str = player_1
        self.player_2:str = player_2

        self.current_player:str = player_1    
        

    def __str__(self):
        board = "\n  /---------\\\n"

        first_3 = True
        first_5 = True

        for row in self.state:
            start = ""
            end = ""
            match row[0]:
                case 3:
                    if (first_3):
                        start =  " /---"
                        end = "--\\\n"
                        first_3 = False
                    else:
                        start =  " \\---"
                        end = "--/\n"
                case 5:
                    if (first_5):
                        start =  "/--"
                        end = "-\\\n"
                        first_5 = False
                    else:
                        start =  "\\--"
                        end = "-/\n"

                case 6:
                    start = "|-"
                    end = "|\n"
            
            board += start
            for i in range(row[0]):
                if (i < row[1]):
                    board += "X-"
                else:
                    board += "O-"
            board += end


        board += "  \\---------/\n"

        return board


    def pop(self, row, pop_quantity):

        if (pop_quantity >= self.state[row][0]):
            print("Can't pop a full row")
            return

        if pop_quantity > 3:
            print("Can't pop more then 3 at a time")

        if pop_quantity + self.state[row][1] > self.state[row][0]:
            print("Can't pop more then max row size")
            return

        self.state[row][1] += pop_quantity

        return


    def validate(self):

        completed_rows = 0

        for row in self.state:
            if row[0] == row[1]:
                completed_rows += 1
        
        return completed_rows == 6


    def switch_players(self):

        if self.current_player == self.player_1:
            self.current_player = self.player_2
        else:
            self.current_player = self.player_1
    

    def get_all_moves(self):
        """ Get all possible moves on the board
        
            Returns:
                List[Tuple[row:int, number_to_pop:int]]
        """
        all_moves = []
        for i, row in enumerate(self.state):
            for j in range(row[0] - row[1]):
                if (j+1 != row[0] and j+1 <= 3):
                    all_moves.append((i, j+1))
        

        return all_moves


    def evaluate(self):
        """ Evaluate current position on the board

            Returns:
                int > 0 if board is winning
                int < 0 if board is loosing
        
        """
        # all_possible_moves = len(self.get_all_moves())
        min_possible_moves = 0
        for row in self.state:
            if (row[1] == 0 or row[1] + 3 < row[0]):
                min_possible_moves += 2
            elif (row[0] != row[1]):
                min_possible_moves += 1

        if min_possible_moves == 0:
            return 20
        
        if min_possible_moves%2 == 1:
            # game is winning for current player
            return 20 - min_possible_moves

        # game is loosing for current player
        return -1 * (20 - min_possible_moves)
    

    def set_board(self, new_state):
        self.state = new_state

      
                
def minimax(board, depth, maximiser, alpha, beta):
        if depth == 0 or board.validate():
            evaluation_multiplier = 1 if maximiser else -1
            return None, board.evaluate()*evaluation_multiplier
        
        if maximiser:
            best_move = (None, float('-inf'))
            for move in board.get_all_moves():
                temp_board = copy.deepcopy(board)
                temp_board.pop(move[0], move[1])
                eval = minimax(temp_board, depth - 1, False, alpha, beta)[1]
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

    while game_mode != '1' and game_mode != "2":
        game_mode = input("Enter a valid game mode (1 or 2)")


    if game_mode == "1":
        
        input_not_valid = True
        while input_not_valid:
            bot_difficulty = input("\nEnter bot difficulty (1 to 8)\n")
            try:
                bot_difficulty = int(bot_difficulty)
                if bot_difficulty < 9 and bot_difficulty > 0:
                    input_not_valid = False
            except:
                print("Bot difficulty must be a number between 1 and 8")
        player_1_name = 'Humain'
        player_2_name = f'Bot_lvl_{bot_difficulty}'

    else:
        player_1_name = 'Humain_1'
        player_2_name = 'Humain_2'

    board = Board(player_1_name, player_2_name)
    game_over = False

    while not game_over:

        print("\nIt's your turn " + board.current_player)
        #print(f"\nCurrent board eval = {board.evaluate()}\nAll possible moves : {board.get_all_moves()}")
        #print(f"Best move from minimax : {minimax(board, 5, True, float('-inf'), float('inf'))}")
        print(board)
        move = input("Play next move by entering the row number (starts at 0),\nfollowed by the number of bubble to pop.\ni.e. \"0 1\"\n")
        
        if (move == "exit"):
            game_over = True
            board.current_player = 'nobody'
            break

        valid_move, params = validate_input(move, board)
        if (valid_move):
            board.pop(params[0], params[1])
            board.switch_players()
        else:
            print("|---ERROR---|")
            print(params)
            print("|-----------|")


        if board.validate():
            game_over = True

        
        # One player, play against the computer
        if game_mode == "1" and not game_over and valid_move:
            bot_move = minimax(board, bot_difficulty, True, float('-inf'), float('inf'))[0]
            print(f"\n{player_2_name} plays {bot_move}")
            board.pop(bot_move[0], bot_move[1])
            board.switch_players()

            if board.validate():
                game_over = True

    print("Game over! Congrats " + board.current_player)






if __name__ == "__main__":
    main()

    
        