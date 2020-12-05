import math
import numpy as np

def solve_part_a(filename):
    seat_rows, seat_cols, seat_ids = zip(*process_boarding_passes(filename))
    return max(seat_ids)

def solve_part_b(filename):
    seat_rows, seat_cols, seat_ids = zip(*process_boarding_passes(filename))
    taken_seats = sorted(seat_ids)
    #We only looking for missing seat ids in the interior of the grid
    #So we can look at the successive seat ids, and there will be exactly 1 where the jump between seat ids is equal to 2
    seat_ids_diff = [x - taken_seats[i - 1] for i, x in enumerate(taken_seats)][1:]
    missing_seat_id = taken_seats[np.argmax(seat_ids_diff)]
    return missing_seat_id + 1

def process_boarding_passes(filename):
    return [convert_binary_code_to_seat_location(bp.strip()) for bp in open(filename, 'r').readlines()]

def convert_binary_code_to_seat_location(binary_code):
    binary_row_code = binary_code[0:7]
    binary_col_code = binary_code[7:(len(binary_code)+1)]
    print(binary_row_code)
    seat_row = process_binary_code_component(binary_row_code, 127)
    seat_col = process_binary_code_component(binary_col_code, 7)
    return seat_row, seat_col, calc_seat_id(seat_row, seat_col)

def process_binary_code_component(binary_code, possible_range_max):
    possible_seat_range = range(0, possible_range_max)
    for i in binary_code:
        midpoint = math.floor((max(possible_seat_range) - min(possible_seat_range)) / 2) + min(possible_seat_range)
        if(i in ['F', 'L']):
            possible_seat_range = range(min(possible_seat_range), midpoint + 1)
        else:
            possible_seat_range = range(midpoint + 1, max(possible_seat_range) + 1)
        print(f"i: {i}, range after change: {possible_seat_range}")

    if(len(possible_seat_range) == 0):
        return midpoint + 1
    else:
        return min(possible_seat_range)

def calc_seat_id(seat_row, seat_col):
    return 8 * seat_row + seat_col

def run_unit_tests():
    assert convert_binary_code_to_seat_location('FBFBBFFRLR')[2] == 357
    assert convert_binary_code_to_seat_location('BFFFBBFRRR')[2] == 567
    assert convert_binary_code_to_seat_location('FFFBBBFRRR')[2] == 119
    assert convert_binary_code_to_seat_location('BBFFBBFRLL')[2] == 820
    assert solve_part_a('Data/input_day5a_test.txt') == 820

run_unit_tests()
answer_part_a = solve_part_a('Data/input_day5a.txt')
answer_part_b = solve_part_b('Data/input_day5a.txt')