import operator
import ipdb

class Ferry():
    def __init__(self, filename):
        self.filename = filename
        self.position_history = [(0, 0)]
        self.directional_angle = 90
        self.actions = {'N': self.action_N, 'S': self.action_S, 'E': self.action_E, 'W': self.action_W,
                        'L': self.action_L, 'R': self.action_R, 'F': self.action_F}

    def follow_instructions(self):
        instructions = [(instr[0], instr[1:].strip()) for instr in open(self.filename, "r").readlines()]
        [self.actions[action](int(value)) for action, value in instructions]

    def action_N(self, distance):
        self.position_history.append(tuple(map(operator.add, self.position_history[-1], (distance, 0))))

    def action_S(self, distance):
        self.position_history.append(tuple(map(operator.add, self.position_history[-1], (-distance, 0))))

    def action_E(self, distance):
        self.position_history.append(tuple(map(operator.add, self.position_history[-1], (0, distance))))

    def action_W(self, distance):
        self.position_history.append(tuple(map(operator.add, self.position_history[-1], (0, -distance))))

    def action_L(self, degrees):
        self.directional_angle = (self.directional_angle - degrees ) % 360

    def action_R(self, degrees):
        self.directional_angle = (self.directional_angle + degrees ) % 360

    def action_F(self, distance):
        if self.directional_angle == 0:
            self.action_N(distance)
        elif self.directional_angle == 90:
            self.action_E(distance)
        elif self.directional_angle == 180:
            self.action_S(distance)
        elif self.directional_angle == 270:
            self.action_W(distance)

    def get_manhattan_distance(self):
        return abs(self.position_history[-1][0]) + abs(self.position_history[-1][1])

def unit_tests():
    ferry = Ferry('Data/input_day12a_test.txt')
    ferry.follow_instructions()
    assert ferry.get_manhattan_distance() == 25

unit_tests()
ferry = Ferry('Data/input_day12.txt')
ferry.follow_instructions()
ferry.get_manhattan_distance()