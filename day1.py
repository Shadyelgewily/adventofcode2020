import numpy as np
from operator import itemgetter

input = open('Data/input_day1a.txt', 'r')
expenses = [int(e.strip()) for e in input.readlines()]
def get_range_in_reverse_order(expenses):
    return range(len(expenses) - 1, -1, -1)

def log_msg(counter, sum_of_values, **kwargs):
    print(f"Current iteration {counter} with (i={kwargs['i']}, k={kwargs['k']}), sum: {sum_of_values}")

def get_new_sum_of_expenses(expenses, indices):
    return np.sum(itemgetter(*indices)(expenses))

"""The goal for me was to circumvent O(n^2) and O(n^3) complexity when permuting over all combinations.
The algorithms sort the expenses, start with indices i and k the sum of the highest and lowest expense and
 move i and k closer together whenever the sum is larger than 2020. That means we can omit a large number of combinations,
 because we can easily infer that they are infeasible.
When summing 3 values, the same principle is used but then with a third index."""

def find_elem_with_sum2_eqto(expenses, match_value = 2020):
    expenses = np.sort(expenses)
    counter = 1
    for i in get_range_in_reverse_order(expenses):
        k = 0
        sum_of_values = get_new_sum_of_expenses(expenses, [k, i])
        while( (sum_of_values <= match_value) and (k < i) ):
            log_msg(counter, sum_of_values, **{'i': i, 'k': k})

            if( sum_of_values == match_value):
                return([expenses[i], expenses[k], expenses[k] * expenses[i]] )

            k = k + 1
            sum_of_values = get_new_sum_of_expenses(expenses, [k, i])
            counter = counter + 1


def find_elem_with_sum3_eqto(expenses, match_value = 2020):
    expenses = np.sort(expenses)
    counter = 0
    for i in get_range_in_reverse_order(expenses):
        k = 1; j = 0
        sum_of_values = expenses[k] + expenses[i] + expenses[j]
        while( (sum_of_values <= match_value) and (k < i) ):
            counter = counter + 1
            print(f"Current iteration {counter} with (i={i}, k={k}, j={j}), sum: {sum_of_values}")
            while((sum_of_values <= match_value) and (j < k)):
                if (sum_of_values == match_value):
                    return ([expenses[i], expenses[k], expenses[j], expenses[k] * expenses[i] * expenses[j]])
                j = j + 1
                sum_of_values = expenses[k] + expenses[i] + expenses[j]
            k = k + 1
            sum_of_values = expenses[k] + expenses[i] + expenses[j]

which_elems_part1 = find_elem_with_sum2_eqto(expenses, 2020)
which_elems_part2 = find_elem_with_sum3_eqto(expenses, 2020)