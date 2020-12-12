import numpy as np
from collections import Counter
from itertools import combinations
import ipdb

def solve_part_a(filename):
    list_of_joltages = prepare_list_of_joltages(filename)
    joltage_differences = [list_of_joltages[ix] - list_of_joltages[ix-1] for ix in range(1, len(list_of_joltages))]
    joltage_differences_distribution = Counter(joltage_differences)
    return joltage_differences_distribution[1] * joltage_differences_distribution[3]

def prepare_list_of_joltages(filename):
    list_of_joltages = [int(j.strip('\n')) for j in ['0'] + open(filename).readlines()]
    list_of_joltages.append(max(list_of_joltages) + 3)
    return np.sort(list_of_joltages)

#Part B involves finding out at each index how many valid combinations of indices there are in the next few indices
#(of arbitrary length <= 3)
# To be valid, we must ensure that it connects from the left side to the chain as well as the right side
# that means that on both sides the combinations must include joltages that are within 3 joltage differences from the next
# value in the chain. When you've checked all those combinations, you must jump over to the next joltage in the list
# that was NOT part of the combinations at the current step, because that is the next index that has not yet been considered.
# So travel to that next index and repeat until you traversed the entire list.
# When you multiply the number of valid combinations at each index and iterate to the end of the list,
# you know the number of total combinations.
def solve_part_b(filename):
    list_of_joltages = prepare_list_of_joltages(filename)
    ix = 0
    total_combis = 1
    while ix <= (len(list_of_joltages)-1):
        print(f"Current index {ix}, value {list_of_joltages[ix]}, total_combis {total_combis}")
        split_multiplier, ix = process_next_split(list_of_joltages, ix)
        total_combis = total_combis * split_multiplier
    return total_combis

def process_next_split(list_of_joltages, current_ix):
    considered_joltages = list_of_joltages[current_ix+1:]
    current_joltage = list_of_joltages[current_ix]
    considered_joltages = considered_joltages[considered_joltages - current_joltage <= 3]
    allowed_from_left_side = list(considered_joltages[(considered_joltages <= calc_max_left_joltage_next_split(list_of_joltages, current_ix))])
    allowed_from_right_side = list(considered_joltages[(considered_joltages >= calc_min_right_joltage_next_split(list_of_joltages, current_ix))])
    valid_combis = construct_valid_combis_for_current_split(allowed_from_left_side, allowed_from_right_side)
    print(f"valid combis: {repr(valid_combis)}, for this split {len(valid_combis)} valid combis")
    if(len(valid_combis) > 0):
        return len(valid_combis),find_next_split(list_of_joltages, max(allowed_from_right_side))
    else:
        return 1, len(list_of_joltages)

def calc_max_left_joltage_next_split(list_of_joltages, current_ix):
    considered_joltages = list_of_joltages[current_ix+1:]
    current_joltage = list_of_joltages[current_ix]
    return max(considered_joltages[considered_joltages - current_joltage <= 3])

def calc_min_right_joltage_next_split(list_of_joltages, current_ix):
    considered_joltages = list_of_joltages[current_ix+1:]
    current_joltage = list_of_joltages[current_ix]
    remaining_items = considered_joltages[considered_joltages - current_joltage > 3]
    if len(remaining_items) == 0:
        return float("inf")
    else:
        return min(remaining_items) - 3

def find_next_split(list_of_joltages, max_allowed_from_right_side):
    return np.min(np.where(list_of_joltages >= max_allowed_from_right_side))

def construct_valid_combis_for_current_split(allowed_from_left_side, allowed_from_right_side):
    combis_size_1 = list(combinations(set(allowed_from_left_side + allowed_from_right_side), 1))
    combis_size_2 = list(combinations(set(allowed_from_left_side + allowed_from_right_side), 2))
    combis_size_3 = list(combinations(set(allowed_from_left_side + allowed_from_right_side), 3))
    all_combis = combis_size_1 + combis_size_2 + combis_size_3
    valid_combis_from_left_side = [any(item in combi for item in allowed_from_left_side) for combi in all_combis]
    valid_combis_from_right_side =  [any(item in combi for item in allowed_from_right_side) for combi in all_combis]
    valid_combis_from_both_sides = [bool(valid_combis_from_left_side[ix] * valid_combis_from_right_side[ix]) for ix in range(0, len(all_combis))]
    return np.array([sorted(combi) for combi in all_combis], dtype='object')[valid_combis_from_both_sides]

def run_unit_tests():
    assert solve_part_a('Data/input_day10_testa1.txt') == 35
    assert solve_part_a('Data/input_day10_testa2.txt') == 220
    assert solve_part_b('Data/input_day10_testa1.txt') == 8
    assert solve_part_b('Data/input_day10_testa2.txt') == 19208
run_unit_tests()
solve_part_a('Data/input_day10.txt')
solve_part_b('Data/input_day10.txt')