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

    """Consider only the subtree from shiny gold downwards. Each node occurs only once in the network, i.e. the network is not circular
       So the idea is for each node in the subtree, to:
    - find all possible paths to shiny gold
    - traverse each of the paths in turn until you reach shiny gold
    - multiply the weights along the way
    - add those numbers to a total sum before going to the next path
    - When all paths are traversed for a particular node, go to the next node and repeat
    """
    def solve_part_b(self):
        relevant_subtree = nx.dfs_tree(self.graph, 'shiny gold')
        relevant_nodes = relevant_subtree.nodes - ['shiny gold']
        total_sum = 0
        for n in relevant_nodes:
            total_sum = total_sum + self.calc_contribution_to_sum_of_node(n)
        return total_sum

    def calc_contribution_to_sum_of_node(self, node):
        possible_paths = list(nx.all_simple_paths(self.graph, 'shiny gold', node))
        total_sum = 0
        for path in possible_paths:
            total_sum = total_sum + self.calc_contribution_to_sum_of_path(path)
        return total_sum

    def calc_contribution_to_sum_of_path(self, path):
        path_steps = [(path[i], path[i + 1]) for i in range(0, len(path) - 1)]
        contribution_to_sum = 1
        for source, dest in path_steps:
            contribution_to_sum = contribution_to_sum * self.graph.get_edge_data(source, dest)['weight']
        return contribution_to_sum

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
    assert bag_rules.solve_part_b() == 32

    bag_rules = BagRules('Data/input_day7b_test.txt')
    assert bag_rules.solve_part_b() == 126


run_unit_tests()
bag_rules = BagRules('Data/input_day7.txt')
bag_rules.solve_part_a()
bag_rules.solve_part_b()
