from solutions.day17 import *

def tests_day17():
    conway_cubes = ConwayCubes()
    conway_cubes.process_input('Data/input_day17_test_parta.txt')
    assert list(map(conway_cubes.is_active_by_position, [(0,0,0),(0,0,1), (100,100,100)])) == [False, True, False]
    assert conway_cubes.count_active_neighbors((0,0,0)) == 1