from Board import Board
from main import validate_input
import simplejson as json

with open("game_dict.json", 'r+') as file:
    game_dict = json.load(file)
    all_test_passed = True
    position_counter = 0
    for position in game_dict['decisive_positions']:
        position_counter += 1
        board = Board()
        board.set_state_from_str(position['position'])
        move_str = f"{position['best_move'][0]} {position['best_move'][1]}"
        valid_move, params = validate_input(move_str, board)

        if not valid_move:
            print(f"Error in position: {position['position']}")
            print(f"Move: {move_str}")
            print(f"Error: {params}")
            all_test_passed = False

    print(f"Tested {position_counter} positions")
    if all_test_passed:
        print("All tests passed")
    else:
        print("Some tests failed, check the output above")
