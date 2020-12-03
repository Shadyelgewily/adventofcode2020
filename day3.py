import pandas as pd
import numpy as np
import ipdb
from operator import mul
from functools import reduce

def read_map_as_df(filename, slope):
    map_rows = [e.strip() for e in open(filename, 'r').readlines()]
    map_characters = [split_map_line_into_chars(r) for r in map_rows]
    map = pd.DataFrame.from_records(map_characters)
    extended_map = copy_map_horizontally(map, slope)
    return extended_map

def split_map_line_into_chars(line):
    return [char for char in line]

def calc_needed_horizontal_copies(map, slope):
    n_steps_needed_vertical = np.ceil(map.shape[0]/slope[0])
    n_steps_needed_horizontal = n_steps_needed_vertical * slope[1]
    n_copies_of_map_needed = int(np.ceil(n_steps_needed_horizontal / map.shape[1]))
    return n_copies_of_map_needed

def copy_map_horizontally(map, slope):
    return pd.concat([map] * calc_needed_horizontal_copies(map, slope), axis=1)

def check_tree_on_position(map, position):
    return map.iloc[tuple(position)] == '#'

def traverse_map(map, slope):
    position = np.array([0,0])
    needed_steps = int(np.ceil(map.shape[0]/slope[0]))
    n_trees = 0
    for step in range(0, needed_steps):
        if check_tree_on_position(map, position):
            tree_msg = 'tree found'
            n_trees = n_trees + 1
        else:
            tree_msg = 'tree_not_found'
        print(f"Step: {step+1}/{needed_steps}, position: ({position[0]},{position[1]}), {tree_msg}")
        position = position + slope

    return n_trees

def solve_part_b_per_slope(filename_map, slope):
    print(f"\n\nNew slope")
    map = read_map_as_df(filename_map, slope)
    n_trees_for_this_slope = traverse_map(map, slope)
    return n_trees_for_this_slope


slope = np.array([1, 3])
map = read_map_as_df('Data/input_day3a_test.txt', slope)
n_trees_part1_test = traverse_map(map, slope)

slope = np.array([1, 3])
map = read_map_as_df('Data/input_day3a.txt', slope)
n_trees_part1 = traverse_map(map, slope)



list_of_slopes = [np.array([1,1]),
                  np.array([1,3]),
                  np.array([1,5]),
                  np.array([1,7]),
                  np.array([2,1])]

filename_map_part_b_test = 'Data/input_day3a_test.txt'
test_answer_part_b_components = [solve_part_b_per_slope(filename_map_part_b_test, slope) for slope in list_of_slopes]
test_answer_part_b = np.prod(np.array(test_answer_part_b_components))

filename_map_part_b = 'Data/input_day3a.txt'
answer_part_b_components = [solve_part_b_per_slope(filename_map_part_b, slope) for slope in list_of_slopes]

#Interesting finding: for such a large number, np.prod fails because of an overflow
wrong_answer_part_b = np.prod(answer_part_b_components)
answer_part_b = reduce(mul, answer_part_b_components, 1)

