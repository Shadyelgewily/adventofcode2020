import pandas as pd
import numpy as np
import ipdb
import operator

"""The code works and I like the readability of the code, but the double for loop is time consuming. This approach 
wouldn't work if thousands of epoch would be needed (in reasonable time). So I can learn a thing or two about program efficiency."""

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
        while self.is_equilibrium_reached() == False and self.n_epochs <= max_epochs:
            self.n_epochs = self.n_epochs + 1
            print(f"Simulation epoch {self.n_epochs}, occupied seats: {self.get_n_occupied_seats()}")
            self.simulation_history.append(self.map_state.copy())
            self.update_map()

    def update_map(self):
        self.new_map_state = self.map_state.copy()
        for i in range(0, self.map_state.shape[0]):
            for j in range(0, self.map_state.shape[1]):
                if self.is_empty((i,j)) and self.count_adjacent_occupied((i,j)) == 0:
                    self.update_empty_to_occupied((i,j))
                elif self.is_occupied((i,j)) and self.count_adjacent_occupied((i,j)) >= 4:
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
        adj_position = tuple(map(operator.add, position, (0,-1)))
        return self.is_occupied(adj_position)

    def is_adjacent_right_occupied(self, position):
        if position[1] == self.map_state.shape[1] -1:
            return False
        adj_position = tuple(map(operator.add, position, (0,1)))
        return self.is_occupied(adj_position)

    def is_adjacent_up_occupied(self, position):
        if position[0] == 0:
            return False
        adj_position = tuple(map(operator.add, position, (-1,0)))
        return self.is_occupied(adj_position)

    def is_adjacent_down_occupied(self, position):
        if position[0] == self.map_state.shape[0] - 1:
            return False
        adj_position = tuple(map(operator.add, position, (1,0)))
        return self.is_occupied(adj_position)

    def is_adjacent_diag_ne_occupied(self, position):
        if position[0] == 0 or position[1] == self.map_state.shape[1] - 1:
            return False
        adj_position = tuple(map(operator.add, position, (-1, 1)))
        return self.is_occupied(adj_position)

    def is_adjacent_diag_se_occupied(self, position):
        if position[0] == self.map_state.shape[0] - 1 or position[1] == self.map_state.shape[1] - 1:
            return False
        adj_position = tuple(map(operator.add, position, (1, 1)))
        return self.is_occupied(adj_position)

    def is_adjacent_diag_sw_occupied(self, position):
        if position[0] == self.map_state.shape[0] - 1 or position[1] == 0:
            return False
        adj_position = tuple(map(operator.add, position, (1, -1)))
        return self.is_occupied(adj_position)

    def is_adjacent_diag_nw_occupied(self, position):
        if position[0] == 0 or position[1] == 0:
            return False
        adj_position = tuple(map(operator.add, position, (-1, -1)))
        return self.is_occupied(adj_position)

    def is_floor(self, position):
        return self.map_state.iloc[position] == '.'

    def is_empty(self, position):
        return self.map_state.iloc[position] == 'L'

    def is_occupied(self, position):
        return self.map_state.iloc[position] == '#'

    def get_n_occupied_seats(self):
        return sum(np.sum(self.map_state == '#'))

    def is_equilibrium_reached(self):
        if len(self.simulation_history) == 0:
            return False
        return np.all(self.map_state == self.simulation_history[-1])

def unit_tests():
    part1_test = seatingMap('Data/input_day11_testa.txt')
    part1_test.simulate_epochs()
    assert part1_test.get_n_occupied_seats() == 37
    assert part1_test.n_epochs == 6

unit_tests()
part1 = seatingMap('Data/input_day11.txt')
part1.simulate_epochs()
part1.get_n_occupied_seats()