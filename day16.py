import numpy as np
from operator import itemgetter
import ipdb

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

    def get_scanning_error_rate(self):
        return sum(self.invalid_values)

def unit_tests():
    ticket_translation = TicketTranslation()
    ticket_translation.read_notes('Data/input_day16_testa.txt')
    ticket_translation.scan_invalid_tickets()
    assert ticket_translation.get_scanning_error_rate() == 71

#unit_tests()

ticket_translation = TicketTranslation()
ticket_translation.read_notes('Data/input_day16.txt')
ticket_translation.scan_invalid_tickets()
answer_part_a = ticket_translation.get_scanning_error_rate()

