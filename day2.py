from collections import Counter

def count_n_of_char(password, char):
    return Counter(password)[char]

def check_if_password_matches_policy(min_n_char, max_n_char, char, password):
    n_of_char_in_password = count_n_of_char(password, char)
    if( n_of_char_in_password >= min_n_char and n_of_char_in_password <= max_n_char ):
        return True
    return False

def process_input(input_lines):
    counter_correct_passwords = 0
    for l in input_lines:
        policy = l.split(":")[0]
        min_n_char = int(policy.split('-')[0])
        char = policy[-1]
        max_n_char = int(policy.split('-')[1].split(' ')[0])
        password = l.split(":")[1]

        if check_if_password_matches_policy(min_n_char, max_n_char, char, password):
            counter_correct_passwords = counter_correct_passwords + 1

        print( f"policy: {policy}, min: {min_n_char}, max: {max_n_char}, char: {char}, password: {password}, n_correct: {counter_correct_passwords}" )
    return counter_correct_passwords

input = open('Data/input_day2.txt', 'r')
passwords = [l.strip() for l in input.readlines()]
counter_correct_passwords = process_input(passwords)
