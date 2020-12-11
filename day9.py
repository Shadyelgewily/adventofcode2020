import random
import numpy as np
from operator import itemgetter
from bisect import bisect_left
import ipdb

"""Method A: Using Binary search, I expect this to be fast for sum of n = 2 numbers, but more difficult to scale"""
def binary_search(values, match_value):
    i = bisect_left(values, match_value)
    if i != len(values) and values[i] == match_value:
        return i
    else:
        return -1

def check_if_elem_satisfies_policy_method_A(values, match_value):
    values = np.sort(values)
    for i in range(0, len(values)):
        sum_found = binary_search([v for ix, v in enumerate(values) if ix != i], match_value - values[i])
        if sum_found != -1:
            return True
    return False

"""Method B: quite fast, but not as fast as binary search (probably). But more scalable perhaps."""
def check_if_elem_satisfies_policy_method_B(values, match_value):
    values = np.sort(values)
    counter = 1
    for i in get_range_in_reverse_order(values):
        k = 0
        sum_of_values = get_new_sum_of_values(values, [k, i])
        while( (sum_of_values <= match_value) and (k < i) ):
            log_msg(counter, sum_of_values, **{'i': i, 'k': k})

            if( sum_of_values == match_value):
                return True

            k = k + 1
            sum_of_values = get_new_sum_of_values(values, [k, i])
            counter = counter + 1

    return False

def get_range_in_reverse_order(values):
    return range(len(values) - 1, -1, -1)

def get_new_sum_of_values(values, indices):
    return np.sum(itemgetter(*indices)(values))

def log_msg(counter, sum_of_values, **kwargs):
    print(f"Current iteration {counter} with (i={kwargs['i']}, k={kwargs['k']}), sum: {sum_of_values}")

def find_first_elem_that_violates_policy(puzzle_input, n_preamble = 25):
    puzzle_input = puzzle_input.copy()
    preamble = puzzle_input[0:n_preamble]
    match_value = puzzle_input[n_preamble]

    while(check_if_elem_satisfies_policy_method_A(preamble, match_value) and len(preamble) == n_preamble):
        print( f"Binary search for matchvalue = {match_value}" )
        del puzzle_input[0]
        preamble = puzzle_input[0:n_preamble]
        match_value = puzzle_input[n_preamble]
    print(f"Violation found. BEEP BEEP BEEP.")
    return match_value

def solve_part_b(complete_list, match_value):
    n_contiguous = 1
    process_completed = False
    while(process_completed is False):
        n_contiguous = n_contiguous + 1
        process_completed, min_value, max_value = check_if_sum_of_any_contiguous_set_equals_match_value(complete_list, n_contiguous, match_value)
    return min_value + max_value

def check_if_sum_of_any_contiguous_set_equals_match_value(complete_list, n_contiguous, match_value):
    contiguous_combis = find_contiguous_sets_of_size_n(complete_list, n_contiguous)
    sums_contiguous_combis = np.array([np.sum(c) for c in contiguous_combis])
    sum_equals_match_value_ix = np.where(sums_contiguous_combis == match_value)[0]
    print(f"Checking {len(contiguous_combis)} contiguous combis of length {n_contiguous}")

    if len(sum_equals_match_value_ix) > 0:
        first_match_ix = min(sum_equals_match_value_ix)
        return True, min(contiguous_combis[first_match_ix]), max(contiguous_combis[first_match_ix])
    else:
        return False, -1, -1

def find_contiguous_sets_of_size_n(complete_list, n):
    return [itemgetter(*tuple(range(i, i + n)))(complete_list) for i in range(0, len(complete_list) - n + 1)]

def unit_tests():
    random.seed(53498)
    test_part_a1 = list(range(1, 26))
    random.shuffle(test_part_a1)
    assert check_if_elem_satisfies_policy_method_A(test_part_a1[0:24], 45) == True
    assert check_if_elem_satisfies_policy_method_B(test_part_a1[0:24], 45) == True
    test_part_a2 = [35, 20, 15, 25, 47]
    assert check_if_elem_satisfies_policy_method_A(test_part_a2[0:4], 40) == True
    assert check_if_elem_satisfies_policy_method_B(test_part_a2[0:4], 40) == True

    puzzle_input_part_b = [int(v.strip("\n")) for v in open("Data/input_day9a_test.txt").readlines()]
    assert find_first_elem_that_violates_policy(puzzle_input_part_b, 5) == 127
    assert solve_part_b(puzzle_input_part_b, 127) == 62

unit_tests()

input_part_a = [int(v.strip("\n")) for v in open("Data/input_day9.txt").readlines()]
find_first_elem_that_violates_policy(input_part_a, 25)
solve_part_b(input_part_a, 27911108)