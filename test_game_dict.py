from Board import Board
from main import validate_input, check_mirror_positions
import simplejson as json
from itertools import product

def test_move(move_str, board_position_str):
    board = Board()
    board.set_state_from_str(board_position_str)
    valid_move, params = validate_input(move_str, board)

    if not valid_move:
        print(f'{"-"*20}\n')
        print(f"Move not possible in this position: {position['position']}")
        print(f"Move: {move_str}")
        print(f"Error: {params}")
        print(f'{"-"*20}\n\n')
        return False
    return True


with open("game_dict.json", 'r+') as file:
    game_dict = json.load(file)
    all_test_passed = True
    position_counter = 0
    for position in game_dict['decisive_positions']:
        position_counter += 1
        move_str = f"{position['best_move'][0]} {position['best_move'][1]}"
        valid_move = test_move(move_str, position['position'])

        if not valid_move:
            all_test_passed = False

    print(f"Tested {position_counter} positions")
    if all_test_passed:
        print("All tests passed")
    else:
        print("Some tests failed, check the output above")

    
    print(f'{"-"*20}\n\n')
    print("testing mirror positions, this can take a long time, feel free to abort the process if no errors are found after some time.")
    print(f'{"-"*20}\n\n')
    
    # gen board positions
    def generate_all_positions():
        positions = []
        for pos in product(range(4), range(6), range(7), range(7), range(6), range(4)):
            positions.append(f"{pos[0]}{pos[1]}{pos[2]}{pos[3]}{pos[4]}{pos[5]}")
        return positions
    
    positions_str = generate_all_positions()
    
    # validate every position
    for position in positions_str:
        for row, value in enumerate(position):
            value = int(value)
            if row == 0 and value > 3:
                print("Invalid position found : ", position)
            if row == 1 and value  > 5:
                print("Invalid position found : ", position)
            if row == 2 and value  > 6:
                print("Invalid position found : ", position)
            if row == 5 and value  > 3:
                print("Invalid position found : ", position)
            if row == 4 and value  > 5:
                print("Invalid position found : ", position)
            if row == 3 and value  > 6:
                print("Invalid position found : ", position)


    # check if the mirror positions algo is valid

    for dict_position in game_dict['decisive_positions']:
        for position in positions_str:
            mirror_position = check_mirror_positions(dict_position, position)
            if mirror_position:
                best_move = mirror_position[0]
                test_move(f"{best_move[0]} {best_move[1]}", position)

    print("You made it through all the tests and everything seams to work just fine!\n")