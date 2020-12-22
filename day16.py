import numpy as np
from operator import itemgetter
import itertools
import ipdb
from operator import mul
from functools import reduce
class TicketTranslation():
    def __init__(self):
        self.rules = {}
        self.my_ticket = []
        self.nearby_tickets = []
        self.invalid_tickets = []
        self.invalid_values = []

    def read_notes(self, filename):
        file = open(filename, "r")
        self.process_notes(file)

    def process_notes(self, file):
        rules, my_ticket, nearby_tickets = file.read().split('\n\n')
        self.process_rules(rules)
        self.process_my_ticket(my_ticket)
        self.process_nearby_tickets(nearby_tickets)

    def process_rules(self, rules):
        names, ranges = list(zip(*[r.split(': ') for r in rules.split('\n')]))
        self.rules = {name: self.translate_range(range) for (name, range) in zip(names, ranges)}
        self.all_allowed_values = {val for rule in self.rules.values() for val in rule}

    def translate_range(self, valid_range):
        ranges = valid_range.split(' or ')
        bounds = [r.split('-') for r in ranges]
        valid_ranges = [list(range(int(b[0]),int(b[1])+1)) for b in bounds]
        valid_numbers = [item for sublist in valid_ranges for item in sublist]
        return valid_numbers

    def process_my_ticket(self, my_ticket):
        self.my_ticket = [int(val) for val in my_ticket.replace('your ticket:\n','').split(',')]

    def process_nearby_tickets(self, nearby_tickets):
        tickets =  nearby_tickets.replace('nearby tickets:\n','').strip('\n').split('\n')
        tickets = [ticket.split(',') for ticket in tickets]
        self.nearby_tickets = [list(map(int, ticket)) for ticket in tickets]

    def scan_invalid_tickets(self):
        for ix, ticket in enumerate(self.nearby_tickets):
            ix_invalid = np.where(np.array([v not in self.all_allowed_values for v in ticket]))[0]
            if(len(ix_invalid) > 0):
                self.invalid_tickets.append(ix)
                self.invalid_values.append(itemgetter(*np.array(ix_invalid))(ticket))
        self.valid_tickets = [t for ix, t in enumerate(self.nearby_tickets) if ix not in self.invalid_tickets]

    def set_correct_ordering_of_rules(self):
        valid_rules_per_field = self.calc_valid_rules_per_field()
        self.ordered_rules = self.calc_correct_ordering_of_rules(valid_rules_per_field)

    def calc_valid_rules_per_field(self):
        considered_tickets = [self.my_ticket] + self.valid_tickets
        values_per_field = list(zip(*considered_tickets))
        field_values_rules_combis = list(itertools.product(values_per_field, self.rules.values()))
        result_field_values_rules_combis = np.array([set(field_vals).issubset(set(rule)) for field_vals, rule in field_values_rules_combis])
        result_matrix = result_field_values_rules_combis.reshape(len(values_per_field), len(self.rules))
        valid_rules_per_field = np.apply_along_axis(lambda x: set(np.where(x == True)[0]), 1, result_matrix)
        return valid_rules_per_field

    def calc_correct_ordering_of_rules(self, valid_rules_per_field):
        ordered_rules = dict()
        known_rules = set()
        while len(known_rules) < len(self.rules):
            ordered_rules.update({key: val - known_rules for key, val in enumerate(valid_rules_per_field) if len(set(val - known_rules)) == 1})
            known_rules = {next(iter(rule)) for rule in ordered_rules.values()}
        return {key: list(self.rules.keys())[next(iter(val))] for key, val in ordered_rules.items()}

    def get_scanning_error_rate(self):
        return sum(self.invalid_values)

    def get_prod_of_departure_fields(self):
        departure_fields = [field_ix for field_ix, rule in self.ordered_rules.items() if 'departure' in rule]
        return reduce(mul, itemgetter(*departure_fields)(self.my_ticket))

def unit_tests():
    ticket_translation = TicketTranslation()
    ticket_translation.read_notes('Data/input_day16_testa.txt')
    ticket_translation.scan_invalid_tickets()
    ticket_translation.set_correct_ordering_of_rules()
    assert ticket_translation.get_scanning_error_rate() == 71

    ticket_translation = TicketTranslation()
    ticket_translation.read_notes('Data/input_day16_testb.txt')
    ticket_translation.scan_invalid_tickets()
    ticket_translation.set_correct_ordering_of_rules()

#unit_tests()

ticket_translation = TicketTranslation()
ticket_translation.read_notes('Data/input_day16.txt')
ticket_translation.scan_invalid_tickets()
answer_part_a = ticket_translation.get_scanning_error_rate()
ticket_translation.set_correct_ordering_of_rules()
answer_part_b = ticket_translation.get_prod_of_departure_fields()