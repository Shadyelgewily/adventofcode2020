import math
import numpy as np
from mip import Model, minimize, INTEGER
import ipdb
"""For Part B we can use a MIP (Mixted Integer Program) solver, because the problem can be defined as a linear program
This way we can efficiently solve the problem in a few minutes. Using a commercial solver,  much faster.
It will take a while for the actual puzzle input, but for the examples (except the last one) it is quite fast (<2 minutes).

And then I realized the trick is to impose a lower bound on the solution, because that is given in the puzzle. Then it becomes much much faster.

It's probably possible to make the solving time even shorter by imposing additional constraints on the multipliers. We know that 
the multipliers are related. We know that every multiplier has a dependence relation with the multiplier of the first bus (the one that arrives exactly at the timestamp).
They are related to the ratio of the bus speeds. I expected that incorporating this information would speed up the algorithm tremendously, but it didn't make THAT much of a difference.

Any extra constraints that I added only increased the solving time.

Another strategy is to find the first feasible solution that satisfies the constraints, whereby we apply the strict constraints on the multipliers. Because we know there are only very few solutions, so once we found one, we are most likely done

It is not a coincidence that all the bus speeds are prime numbers. We probably need to apply an appropriate prime number theorem.
We can probably use the modular multiplicative inverse theorem to find integers that multiply with the busspeeds such the answers are successive (i.e., mod 1).

Notice that:

61 * 30 - 1 = 1829 and 1829 divides nicely by 59
4*59*31- 1 = 7315 and that divides nicely by 7
28*1045*7 - 1 = 204819 and divides nicely by 63
then if you multiply 204819 * 7315 * 1829 you get a number for which the bus timing property holds. But it is not the first instance, so we can find a smaller case.
And maybe it will only work if we know all the x'es
What's also interesting is that if you know that ax mod b = 1, then k*ax mod b = k (not 1)

we know that 1830 mod 59 = 1 (so 1829/59 = constant) and that any constant times 1829 is thus also a multiple of 59
we also know that 1829*4 mod 7 = 1 (so that 7315/7 = constant) and that any constant times 7315 is thus also a multiple of 7
For example if you then multiply 7315 and 1829, 
then you know that the product satisfies both the original multiples; but is probably not the smallest of such numbers.
"""


def calc_part_a(filename):
    timestamp, available_buses = read_notes_part_a(filename)
    waiting_times = calc_waiting_times(available_buses, timestamp)
    return min(waiting_times) * available_buses[np.argmin(waiting_times)]

def read_notes_part_a(filename):
    timestamp, available_buses = [line.strip() for line in open(filename, "r").readlines()]
    timestamp = int(timestamp)
    available_buses = [int(bus) for bus in available_buses.split(',') if bus != 'x']
    return timestamp, available_buses

def calc_waiting_times(available_buses, timestamp):
    return [math.ceil(timestamp / bus_speed) * bus_speed - timestamp for bus_speed in available_buses]

def calc_part_b(filename, lower_bound_timestamp):
    bus_speeds, bus_minutes = read_notes_part_b(filename)
    return solve_bus_minute_MIP_faster(bus_speeds, bus_minutes, lower_bound_timestamp)

def read_notes_part_b(filename):
    all_buses = [line.strip() for line in open(filename, "r").readlines()][1].split(',')
    bus_minutes = [ix for ix, val in enumerate(all_buses) if val != 'x'][1:]
    bus_speeds = [int(bus) for bus in all_buses if bus != 'x']
    return bus_speeds, bus_minutes

def solve_bus_minute_MIP(bus_speeds, bus_minutes, lower_bound_timestamp):
    I = range(0, len(bus_speeds))
    m = Model("bus_times")

    bus_times = [m.add_var(var_type=INTEGER) for i in I]
    multipliers = [m.add_var(var_type=INTEGER) for i in I]
    m.objective = minimize(bus_times[0])

    for i in I:
        #Bus times must be positive, at least one trip must be made (hence multiplier >= 1)
        m += bus_times[i] >= 0
        m += multipliers[i] >= 1
        # Constraints on the bus departure times because they can only be multiples of the bus speeds
        m += bus_times[i] - multipliers[i]*bus_speeds[i] == 0

    #Constraints on the bus departure times because of the order of departures
    for i in range(0, len(bus_minutes)):
        m += bus_times[i+1] == bus_times[0] + bus_minutes[i]

    m += bus_times[0] >= lower_bound_timestamp

    m.optimize()
    return m.objective_value

def solve_bus_minute_MIP_faster(bus_speeds,bus_minutes, lower_bound_timestamp):
    I = range(0, len(bus_speeds))
    m = Model("bus_times")

    bus_minutes = [0] + bus_minutes
    bus_times = m.add_var(var_type=INTEGER)
    multipliers = [m.add_var(var_type=INTEGER) for i in I]
    m.objective = minimize(bus_times)
    m += bus_times >= lower_bound_timestamp

    #The multipliers are related to the multipliers of the first bus speed in the following way:
    #If the first bus speed is 17, and another bus speed is 607 for example.
    #Then we know that the multiplier of the bus speed with 607 is smaller, with the property that multiplier[bus with speed 607] >= floor(17/607) * multiplier[bus with speed 17]
    #So we have a constraint: m2 - (607/17)*m1 >= 0

    #for i in range(1, len(multipliers)):
        #min_multiplier_ratio = np.floor(bus_speeds[0]/bus_speeds[i])
        #m += multipliers[i] - min_multiplier_ratio * multipliers[0] >= 0
        #m += multipliers[i]*bus_speeds[i] - bus_times - max(bus_minutes) <= 0

    for i in I:
        #Bus times must be positive, at least one trip must be made (hence multiplier >= 1)
        # Constraints on the bus departure times because they can only be multipless of the bus speeds
        m += multipliers[i] >= 1
        m += bus_times + bus_minutes[i] - multipliers[i]*bus_speeds[i] == 0

    m.threads = 3
    m.emphasis = 1

    m.optimize(max_solutions=1)
    for var in m.vars:
        print(var.x)
    return  m.objective_value

def unit_tests():
    assert calc_part_a('Data/input_day13_testa.txt') == 295
    assert calc_part_b('Data/input_day13_testa.txt', lower_bound_timestamp= 1000000) == 1068781
    assert solve_bus_minute_MIP_faster([7, 13, 59, 31, 19], [1, 4, 6, 7], 1000000) == 1068781
    assert solve_bus_minute_MIP_faster([17, 13, 19], [2, 3], 1) == 3417
    assert solve_bus_minute_MIP_faster([67, 7, 59, 61], [1, 2, 3], 1) == 754018
    assert solve_bus_minute_MIP_faster([67, 7, 59, 61], [2, 3, 4], 1) == 779210
    #assert solve_bus_minute_MIP_faster([67, 7, 59,  61], [1, 3, 4], 1) == 1261476
    #assert solve_bus_minute_MIP_faster([1789, 37, 47, 1889], [1, 2, 3], 1000000000) == 1202161486

#unit_tests()
calc_part_a('Data/input_day13.txt')
calc_part_b('Data/input_day13.txt', lower_bound_timestamp=100000000000000)