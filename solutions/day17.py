import pandas as pd
import ipdb
import itertools
import numpy as np

class ConwayCubes():
    def __init__(self, active_neighbors_to_stay_active = [2,3], active_neighbors_to_become_active = [3]):
        self.world_state = {}
        self.new_world_state = {}
        self.simulation_history = []
        self.active_neighbors_to_stay_active = active_neighbors_to_stay_active
        self.active_neighbors_to_become_active = active_neighbors_to_become_active

    def process_input(self, filename):
        map_rows = [e.strip() for e in open(filename, 'r').readlines()]
        map_characters = np.array([self.split_map_line_into_chars(r) for r in map_rows])
        self.world_state = {self.translate_position_to_dict_key((0, row, col)):
                                map_characters[row, col]
                            for row in range(0, map_characters.shape[0])
                            for col in range(0, map_characters.shape[1])}
        self.simulation_history.append(self.world_state)

    def update_world(self):
        self.new_world_state = self.world_state.copy()
        #Expand slices
        coordinates = itertools.product(range(0, self.new_world_state.shape[0]), range(0, self.new_world_state.shape[1]),
                                        range(0, self.new_world_state.shape[2]))
        for z, y, x in coordinates:
            cube_state = self.world_state[z,y,x]
            print(cube_state)
            if self.is_active(cube_state) and self.count_active_neighbors((z,y,x)) in self.active_neighbors_to_stay_active:
                self.update_active_to_inactive((z,y,x))
            elif self.is_inactive(cube_state) and self.count_active_neighbors((z,y,x)) in self.active_neighbors_to_become_active:
                self.update_inactive_to_active((z,y,x))
        self.world_state = self.new_world_state.copy()

    def translate_position_to_dict_key(self, position):
        return str(position[0]) + str(position[1]) + str(position[2])

    def expand_world_with_new_neighbors(self, neighbors):
        #new_neighbors = simply measure at the boundaries and add those
        #for each new neighbor, add to
        pass

    def count_active_neighbors(self, position):
        neighbors = self.get_neighbors(position)
        return sum([self.is_active_by_position(n) for n in neighbors])

    def get_neighbors(self, position):
        neighbors =  set(itertools.product(range(position[0]-1, position[0]+2),
                                      range(position[1]-1, position[1]+2),
                                      range(position[2]-1, position[2]+2)
                                      )) - set(position)
        return list(map(self.translate_position_to_dict_key, neighbors))

    def update_inactive_to_active(self, position):
        self.new_world_state[position] = '#'

    def update_active_to_inactive(self, position):
        self.new_world_state[position] = '.'

    def split_map_line_into_chars(self, line):
        return [char for char in line]

    def get_n_active_cubes(self):
        pass

    def is_inactive(self, seat_type):
        return seat_type == '.'

    def is_inactive_by_position(self, position):
        try:
            return self.world_state[self.translate_position_to_dict_key(position)] == '.'
        except:
            return True

    def is_active(self, seat_type):
        return seat_type == '#'

    def is_active_by_position(self, position):
        try:
            return self.world_state[self.translate_position_to_dict_key(position)] == '#'
        except:
            return False

conway_cubes = ConwayCubes()
conway_cubes.process_input('Data/input_day17_test_parta.txt')
#conway_cubes.update_world()
list(map(conway_cubes.is_active_by_position, [(0,0,0),(0,0,1), (100,100,100)]))
conway_cubes.count_active_neighbors((0,0,0))