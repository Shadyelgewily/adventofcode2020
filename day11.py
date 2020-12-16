import pandas as pd
import numpy as np
import ipdb
from operator import itemgetter
import operator
import re

"""The code works and I like the readability of the code (but becomes quite long and tedious for part b), but the double for loop is time consuming. This approach 
wouldn't work if thousands of epoch would be needed (in reasonable time). So I can learn a thing or two about program efficiency.
Especially the get_first_seat_in_ix_range() function is slow, so it is probably better to use a list comprehension. But even that was slow.
So a deep-dive is necessary to make the algorithm faster, probably changing the double for loop into a double list comprehension
"""

class seatingMap():
    def __init__(self, filename):
        self.map_state = self.read_seating_map(filename)
        self.simulation_history = []
        self.n_epochs = 0

    def read_seating_map(self, filename):
        map_rows = [e.strip() for e in open(filename, 'r').readlines()]
        map_characters = [self.split_map_line_into_chars(r) for r in map_rows]
        map = pd.DataFrame.from_records(map_characters)
        return map

    def split_map_line_into_chars(self, line):
        return [char for char in line]

    def simulate_epochs(self, max_epochs = 500):
        while self.is_equilibrium_reached() == False and self.n_epochs < max_epochs:
            self.n_epochs = self.n_epochs + 1
            print(f"Simulation epoch {self.n_epochs}, occupied seats: {self.get_n_occupied_seats()}")
            self.simulation_history.append(self.map_state.copy())
            self.update_map()

    def update_map(self):
        self.new_map_state = self.map_state.copy()
        for i in range(0, self.map_state.shape[0]):
            for j in range(0, self.map_state.shape[1]):
                seat_type = self.map_state.iloc[i, j]
                if self.is_empty(seat_type) and self.count_adjacent_occupied((i,j)) == 0:
                    self.update_empty_to_occupied((i,j))
                elif self.is_occupied(seat_type) and self.count_adjacent_occupied((i,j)) >= self.min_visible_seats_change_occupied_to_empty:
                    self.update_occupied_to_empty((i,j))
        self.map_state = self.new_map_state.copy()

    def update_empty_to_occupied(self, position):
        self.new_map_state.iloc[tuple(position)] = '#'

    def update_occupied_to_empty(self, position):
        self.new_map_state.iloc[tuple(position)] = 'L'

    def count_adjacent_occupied(self, position):
        return np.sum([self.is_adjacent_left_occupied(position),
                       self.is_adjacent_right_occupied(position),
                       self.is_adjacent_up_occupied(position),
                       self.is_adjacent_down_occupied(position),
                       self.is_adjacent_diag_ne_occupied(position),
                       self.is_adjacent_diag_se_occupied(position),
                       self.is_adjacent_diag_sw_occupied(position),
                       self.is_adjacent_diag_nw_occupied(position)]
                      )

    def is_adjacent_left_occupied(self, position):
        if position[1] == 0:
            return False
        seat_type = self.get_adjacent_seat_type_in_direction(position, (0, -1))
        return self.is_occupied(seat_type)

    def is_adjacent_right_occupied(self, position):
        if position[1] == self.map_state.shape[1] -1:
            return False
        seat_type = self.get_adjacent_seat_type_in_direction(position, (0, 1))
        return self.is_occupied(seat_type)

    def is_adjacent_up_occupied(self, position):
        if position[0] == 0:
            return False
        seat_type = self.get_adjacent_seat_type_in_direction(position, (-1, 0))
        return self.is_occupied(seat_type)

    def is_adjacent_down_occupied(self, position):
        if position[0] == self.map_state.shape[0] - 1:
            return False
        seat_type = self.get_adjacent_seat_type_in_direction(position, (1, 0))
        return self.is_occupied(seat_type)

    def is_adjacent_diag_ne_occupied(self, position):
        if position[0] == 0 or position[1] == self.map_state.shape[1] - 1:
            return False
        seat_type = self.get_adjacent_seat_type_in_direction(position, (-1, 1))
        return self.is_occupied(seat_type)

    def is_adjacent_diag_se_occupied(self, position):
        if position[0] == self.map_state.shape[0] - 1 or position[1] == self.map_state.shape[1] - 1:
            return False
        seat_type = self.get_adjacent_seat_type_in_direction(position, (1, 1))
        return self.is_occupied(seat_type)

    def is_adjacent_diag_sw_occupied(self, position):
        if position[0] == self.map_state.shape[0] - 1 or position[1] == 0:
            return False
        seat_type = self.get_adjacent_seat_type_in_direction(position, (1, -1))
        return self.is_occupied(seat_type)

    def is_adjacent_diag_nw_occupied(self, position):
        if position[0] == 0 or position[1] == 0:
            return False
        seat_type = self.get_adjacent_seat_type_in_direction(position, (-1, -1))
        return self.is_occupied(seat_type)

    def is_floor(self, seat_type):
        return seat_type == '.'

    def is_empty(self, seat_type):
        return seat_type == 'L'

    def is_occupied(self, seat_type):
        return seat_type == '#'

    def get_n_occupied_seats(self):
        return sum(np.sum(self.map_state == '#'))

    def is_equilibrium_reached(self):
        if len(self.simulation_history) == 0:
            return False
        return np.all(self.map_state == self.simulation_history[-1])

    def set_policy(self, policy):
        self.policy = policy
        if self.policy == 'A':
            self.min_visible_seats_change_occupied_to_empty = 4
        else:
            self.min_visible_seats_change_occupied_to_empty = 5

    def get_adjacent_seat_type_in_direction(self, position, direction):
        if self.policy == 'A':
            return self.map_state.iloc[tuple(map(operator.add, position, direction))]
        if self.policy == 'B':
            return self.get_first_seat_type_in_direction(position, direction)

    def get_first_seat_type_in_direction(self, position, direction, debug=False):
        if direction == (1, 0):
            directional_ix_range = [tuple(map(operator.add, position, (next_y, 0))) for next_y in range(1, self.map_state.shape[0] - position[0])]
        elif direction == (0, 1):
            directional_ix_range = [tuple(map(operator.add, position, (0, next_x))) for next_x in range(1, self.map_state.shape[1] - position[1])]
        elif direction == (-1, 0):
            directional_ix_range = [tuple(map(operator.add, position, (-next_y, 0))) for next_y in range(1, position[0] - 0 + 1)]
        elif direction == (0, -1):
            directional_ix_range = [tuple(map(operator.add, position, (0, -next_x))) for next_x in range(1, position[1] - 0 + 1)]
        elif direction == (1, 1):
            first_edge_distance = min(tuple(map(operator.add, (self.map_state.shape[0]-1, self.map_state.shape[1]-1), (-position[0], -position[1]))))
            directional_ix_range = [tuple(map(operator.add, position, (next_yx, next_yx))) for next_yx in range(1, first_edge_distance + 1)]
        elif direction == (-1, -1):
            first_edge_distance = min(tuple(map(operator.add, position, (0,0))))
            directional_ix_range = [tuple(map(operator.add, position, (-next_yx, -next_yx))) for next_yx in range(1, first_edge_distance +1)]
        elif direction == (-1, 1):
            first_edge_distance = min(position[0] - 0, self.map_state.shape[1] - position[1] -1)
            directional_ix_range = [tuple(map(operator.add, position, (-next_yx, next_yx))) for next_yx in range(1, first_edge_distance +1)]
        elif direction == (1, -1):
            first_edge_distance = min(self.map_state.shape[0] - position[0] - 1, position[1] - 0)
            directional_ix_range = [tuple(map(operator.add, position, (next_yx, -next_yx))) for next_yx in range(1, first_edge_distance + 1)]
        else:
            return 'L'

        return self.get_first_seat_in_ix_range(directional_ix_range)

    """This method is more clear and is more true to the method name, but slow for many iterations"""
    def get_first_seat_in_ix_range_slow(self, directional_ix_range):
        if len(directional_ix_range) == 0:
            return 'L'
        line_of_sight = ''.join(itemgetter(*directional_ix_range)(self.map_state.iloc))
        ix_first_chair_in_sight = re.search(r'[^.]', line_of_sight)
        if ix_first_chair_in_sight is None:
            return 'L' #if empty line consists only of floor, then it can be considered as an empty chair next to it
        return line_of_sight[ix_first_chair_in_sight.start()]

    """I expect this method to be faster: it simply iterates only until the first match of a chair, and then returns the appropriate match"""
    def get_first_seat_in_ix_range(self, directional_ix_range):
        if len(directional_ix_range) == 0:
            return 'L'
        first_nonfloor_in_line_of_sight = next((pos for pos in itemgetter(*directional_ix_range)(self.map_state.iloc) if pos in ['L', '#']), None)
        if first_nonfloor_in_line_of_sight is None:
            return 'L' #if empty line consists only of floor, then it can be considered as an empty chair next to it
        return first_nonfloor_in_line_of_sight

def unit_tests():
    part1_test = seatingMap('Data/input_day11_testa.txt')
    part1_test.set_policy('A')
    part1_test.simulate_epochs()
    assert part1_test.get_n_occupied_seats() == 37
    assert part1_test.n_epochs == 6

    part2_test = seatingMap('Data/input_day11_testb1.txt')
    part2_test.set_policy('B')
    assert part2_test.get_first_seat_type_in_direction((0,0), (1,0)) == '#'
    assert part2_test.get_first_seat_type_in_direction((4,3), (0,-1)) == '#'
    assert part2_test.get_first_seat_type_in_direction((4,4), (0,-1)) == 'L'
    assert part2_test.get_first_seat_type_in_direction((7,8), (0,1)) == 'L'
    assert part2_test.get_first_seat_type_in_direction((100,100), (0,1)) == 'L'
    assert part2_test.get_first_seat_type_in_direction((2,2), (-1,1)) == '#'
    assert part2_test.get_first_seat_type_in_direction((8,1), (-1,-1)) == '#'
    assert part2_test.count_adjacent_occupied((4,3)) == 8

    part2_test2 = seatingMap('Data/input_day11_testb2.txt')
    part2_test2.set_policy('B')
    assert part2_test2.count_adjacent_occupied((1,1)) == 0
    assert part2_test2.count_adjacent_occupied((1,3)) == 1

    part2_test3 = seatingMap('Data/input_day11_testb3.txt')
    part2_test3.set_policy('B')
    assert part2_test3.count_adjacent_occupied((3,3)) == 0

    part2_example = seatingMap('Data/input_day11_testa.txt')
    part2_example.set_policy('B')
    part2_example.simulate_epochs()
    assert part2_example.get_n_occupied_seats() == 26

unit_tests()

part1 = seatingMap('Data/input_day11.txt')
part1.set_policy('A')
part1.simulate_epochs()
part1.get_n_occupied_seats()
ipdb.set_trace()
part2 = seatingMap('Data/input_day11.txt')
part2.set_policy('B')
part2.simulate_epochs()
part2.get_n_occupied_seats()