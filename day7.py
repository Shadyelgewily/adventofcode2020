import networkx as nx
import matplotlib
import ipdb
from itertools import product

class BagRules():
    def __init__(self, filename):
        self.rules = None
        self.nodes = None
        self.graph = None
        self.process_rules(filename)

    def solve_part_a(self):
        return len(nx.ancestors(self.graph, 'shiny gold'))

    def process_rules(self, filename):
        self.read_rules(filename)
        self.create_graph_of_bag_rules()

    def read_rules(self, filename):
        self.rules = [l.strip('\n\.') for l in open(filename).readlines()]

    def create_graph_of_bag_rules(self):
        self.graph = nx.DiGraph()
        self.create_nodes_from_input()
        self.create_graph_edges_per_rule()

    def create_nodes_from_input(self):
        self.nodes = [rule.split('bags')[0].strip(' ') for rule in self.rules]

    def create_graph_edges_per_rule(self):
        for rule in self.rules:
            for edge in self.process_rule(rule):
                print(edge)
                weight = edge[1][0]
                if weight > 0:
                    self.graph.add_weighted_edges_from([(edge[0], edge[1][1], weight)])

    def process_rule(self, rule):
        rule_components = [rcomp.strip(' ') for rcomp in rule.split('contain')]
        outer_bag = rule_components[0].replace( " bags", "")
        inner_bags = rule_components[1].split(', ')
        inner_bags_amounts = [self.get_bag_amount(bag) for bag in inner_bags]
        inner_bags_types = [self.get_bag_type(bag) for bag in inner_bags]
        inner_bag_edges = zip(inner_bags_amounts, inner_bags_types)

        return list(product([outer_bag], inner_bag_edges))

    def get_bag_amount(self, bag_type_string):
        amount = bag_type_string.split(' ')[0]
        if amount == 'no':
            amount = 0
        return int(amount)

    def get_bag_type(self, bag_type_string):
        return " ".join(bag_type_string.split(' ')[1:3])

def run_unit_tests():
    bag_rules = BagRules('Data/input_day7a_test.txt')
    assert bag_rules.solve_part_a() == 4

run_unit_tests()
bag_rules = BagRules('Data/input_day7.txt')
bag_rules.solve_part_a()