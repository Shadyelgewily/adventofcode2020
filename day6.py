from collections import Counter

def solve_part_a(filename):
    customs_forms_per_group, group_sizes = process_customs_forms(filename)
    n_questions_answered_yes_by_at_least_1 = [check_n_questions_answered_yes_at_least_once(form) for form in customs_forms_per_group]
    return(sum(n_questions_answered_yes_by_at_least_1))

def solve_part_b(filename):
    customs_forms_per_group, group_sizes = process_customs_forms(filename)
    n_questions_answered_yes_by_all = [check_n_questions_answered_yes_by_everyone(form, group_size) for form, group_size in zip(customs_forms_per_group, group_sizes)]
    return(sum(n_questions_answered_yes_by_all))

def process_customs_forms(filename):
    customs_forms_data = open(filename).read()
    group_forms = customs_forms_data.strip('\n').split('\n\n')
    group_sizes = [len(gf.split('\n')) for gf in group_forms]
    list_of_customs_forms = [gf.replace('\n', '') for gf in group_forms]
    return list_of_customs_forms, group_sizes

def check_n_questions_answered_yes_at_least_once(customs_form):
    return len(set(customs_form))

def check_n_questions_answered_yes_by_everyone(customs_form, group_size):
    return len([q for q, cnt in Counter(customs_form).items() if cnt == group_size])

def unit_tests():
    assert solve_part_a('Data/input_day6a_test.txt') == 11
    assert solve_part_b('Data/input_day6a_test.txt') == 6

unit_tests()
solve_part_a('Data/input_day6.txt')
solve_part_b('Data/input_day6.txt')