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
            print("Max pop is row quantity - 1")
            return

        if (pop_quantity + self.state[row][1] > self.state[row][0]):
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
                if (j != 0):
                    all_moves.append((i, j))
        

        for move in all_moves:
            print(move)

        return all_moves


    def evaluate(self):
        """ Evaluate current position on the board

            Returns:
                int : 1 if the board is winning for the current_player, -1 otherwise
        
        """
        min_possible_moves = 0
        for row in self.state:
            if (row[1] == 0):
                min_possible_moves += 2
            elif (row[0] != row[1]):
                min_possible_moves += 1

        print(f"\nIn evaluate, min_possible_moves = {min_possible_moves}\n")
        if (min_possible_moves%2):
            return -1

        return 1
    
    
    def set_board(self, new_state):
        pass


def validate_input(input:str, board:Board):
    input_params = input.split(' ')

    validated_params = []

    for i, param in enumerate(input_params):
        try:
            pop_quantity = int(param)
            validated_params.append(pop_quantity)
        except:
            return False, "input must be two numbers separated by a space\n"

        if i > 1:
            return False, "input must be two numbers separated by a space\n"

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

    board = Board()

    # 40 char per line
    print("""
        /--------------------------------------\\
        |----------Welcome to Pop it!----------|
        |--------------------------------------|
        |------------Last player to------------|
        |--------------pop looses--------------|
        \\--------------------------------------/
    """)

    game_over = False

    while not game_over:

        print("\nIt's your turn " + board.current_player)
        print(f"\nCurrent board eval = {board.evaluate()}\nAll possible moves :")
        board.get_all_moves()
        move = input(
        """
    Play next move by entering the row number (starts at 0), 
    followed by the number of bubble to pop.
    i.e "0 1"
    """)
        
        if (move == "exit"):
            game_over = True
            board.current_player = 'nobody'
            break

        isValid, params = validate_input(move, board)
        if (isValid):
            board.pop(params[0], params[1])
            board.switch_players()
            print(board)
        else:
            print("|---ERROR---|")
            print(params)
            print("|-----------|")

        if board.validate():
            game_over = True

    print("Game over! Congrats " + board.current_player)






if __name__ == "__main__":
    main()

    
        