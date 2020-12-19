"""
Checking first whether a number already exists in the list by comparing it to the maximum value in the list, speeds up by 23%
But what I learned about this exercise that changing from a list to a set DRAMATICALLY increases performance, and it scales much better too
because using a list makes the algorithm slower as the list gets bigger, but that is much less of an issue (if at all) using a set.
By storing only the unique spoken numbers, and the last 2 indices, we don't use much RAM either
"""
import time
import numpy as np
import ipdb
class MemoryGame():
    def __init__(self, starting_numbers, n_epochs, debug=True):
        self.debug = debug
        self.current_epoch = 0
        self.starting_numbers = starting_numbers
        self.numbers_spoken = set(starting_numbers)
        self.n_epochs = n_epochs + len(starting_numbers)
        self.current_number = starting_numbers[-1]
        self.last_indices = {var: [ix] for ix, var in enumerate(starting_numbers)}
        self.count_zeros = 0
        self.min_number = min(self.starting_numbers)
        self.max_number = max(self.starting_numbers)

    def simulate_memory_game(self):
        [self.simulate_next_epoch() for self.current_epoch in range(len(self.starting_numbers), self.n_epochs)]
        return self.current_number

    def simulate_next_epoch(self):
        if not self.is_last_number_repeat():
            self.add_spoken_number(0)
            self.count_zeros = self.count_zeros + 1
        else:
            self.add_spoken_number(self.return_diff_last_turns_last_number())

        if self.current_epoch % 10000 == 0:
            print(f"Current epoch: {self.current_epoch}, current number: {self.current_number}, "
                  f"count zeros: {self.count_zeros}, min: {self.min_number}, max: {self.max_number},"
                  f"numbers spoken percentage {round(len(self.numbers_spoken) / self.current_epoch, 2)}")

    def is_last_number_repeat(self):
        return self.last_indices[self.current_number][0] != self.current_epoch - 1

    def add_spoken_number(self, number):
        if self.check_if_new_number(number):
            self.numbers_spoken.add(number)
            self.last_indices[number] = [self.current_epoch]
        else:
            self.update_indices(number)
        self.current_number = number
        self.min_number = min(self.min_number, number)
        self.max_number = max(self.max_number, number)

    def check_if_new_number(self, number):
        if self.debug == True:
            return self.check_if_new_number_original(number)
        else:
            return self.check_if_new_number_efficiently(number)

    def check_if_new_number_original(self, number):
        if number not in self.numbers_spoken:
            return True

    def check_if_new_number_efficiently(self, number):
        #We get zeros very quickly, so we check only if the new number is bigger than the max
        #In many cases, we don't have to search the list but simply compare to the largest value
        if number > self.max_number:
            return True

        if number not in self.numbers_spoken:
            return True

    def update_indices(self, number):
        self.last_indices[number] = [self.last_indices[number][-1], self.current_epoch]

    def return_diff_last_turns_last_number(self):
        nr_last_two_turns = self.last_indices[self.current_number]
        if len(nr_last_two_turns) == 1:
            return nr_last_two_turns[0]
        return np.diff(nr_last_two_turns)[0]

def unit_tests():
    part1 = MemoryGame([0,3,6], 2017)
    assert part1.simulate_memory_game() == 436
    part1 = MemoryGame([3,1,2], 2017)
    assert part1.simulate_memory_game() == 1836
    part1 = MemoryGame([3,2,1], 2017)
    assert part1.simulate_memory_game() == 438

#unit_tests()

part1 = MemoryGame([2, 15, 0, 9, 1, 20], 2014, debug=False)
part1.simulate_memory_game()

starttime = time.time()
part2 = MemoryGame([2, 15, 0, 9, 1, 20], 30000000-6)
part2.simulate_memory_game()
part2.current_number
endtime = time.time()
print("Total time:" + str(endtime - starttime))


#unit_tests()