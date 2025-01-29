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
            if (row[0] == 3):
                if (first_3):
                    start =  " /---"
                    end = "--\\\n"
                    first_3 = False
                else:
                    start =  " \\---"
                    end = "--/\n"
            elif (row[0] == 5):
                if (first_5):
                    start =  "/--"
                    end = "-\\\n"
                    first_5 = False
                else:
                    start =  "\\--"
                    end = "-/\n"
            elif (row[0] == 6):
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

        if self.current_player == 'nobody':
            return True

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

        # no move can be played when the player received the board
        # the game is over and the player current player wins
        if min_possible_moves == 0:
            return 20
        
        # the number of possible moves in the position is even
        # game is winning for current player
        if min_possible_moves%2 == 0:
            return 20 - min_possible_moves
        
        # the number of possible moves in the position is odd
        # game is loosing for current player
        return -1 * (20 - min_possible_moves)
    

    def set_board(self, new_state):
        self.state = new_state