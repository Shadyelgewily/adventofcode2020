import numpy as np
import re

def count_n_valid_passports_part1(filename):
    list_of_clean_passports = process_passports(filename)
    valid_passport_checks = [check_if_passport_contains_all_fields(p) for p in list_of_clean_passports]
    return sum(valid_passport_checks)

def count_n_valid_passports_part2(filename):
    list_of_clean_passports = process_passports(filename)
    passports_with_all_fields = [p for p in list_of_clean_passports if check_if_passport_contains_all_fields(p)]
    valid_passport_checks = [check_if_all_fields_are_valid(p) for p in passports_with_all_fields]
    return sum(valid_passport_checks)

def check_if_all_fields_are_valid(passport):
    obligatory_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
    byr, iyr, eyr, hgt, hcl, ecl, pid = [extract_passport_info_by_keyword(passport, f) for f in obligatory_fields]
    t1 = check_valid_birth_year(byr)
    t2 = check_valid_issue_year(iyr)
    t3 = check_valid_expiration_year(eyr)
    t4 = check_valid_height(hgt)
    t5 = check_valid_haircolor(hcl)
    t6 = check_valid_eye_color(ecl)
    t7 = check_valid_passportid(pid)
    return t1 and t2 and t3 and t4 and t5 and t6 and t7

def extract_passport_info_by_keyword(passport, keyword):
    return passport.split(keyword+':')[1].split(' ')[0]

def process_passports(filename):
    raw_passports = open(filename, 'r').read()
    list_of_raw_passports = raw_passports.split('\n\n')
    return [clean_passport(p) for p in list_of_raw_passports]

def clean_passport(p):
    return p.replace('\n', ' ')

def check_if_passport_contains_all_fields(passport, obligatory_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']):
    optional_fields = ['cid']
    return np.all([f + ":" in passport for f in obligatory_fields])

def four_digits_and_min_max_valid_year(test_string, min_year, max_year):
    return bool(re.search('^[\d]{4,4}$', test_string)) and int(test_string) >= min_year and int(test_string) <= max_year

def check_valid_birth_year(byr):
    return four_digits_and_min_max_valid_year(byr, 1920, 2002)

def check_valid_issue_year(iyr):
    return four_digits_and_min_max_valid_year(iyr, 2010, 2020)

def check_valid_expiration_year(eyr):
    return four_digits_and_min_max_valid_year(eyr, 2020, 2030)

def check_valid_height(hgt):
    scale = hgt[-2:]
    if scale not in ['cm', 'in']:
        return False
    hgt = hgt.replace(scale, '')
    if scale == 'cm':
        return check_valid_height_in_cm(hgt)
    else:
        return check_valid_height_in_inch(hgt)

def check_valid_height_in_cm(hgt):
    return (int(hgt) > 150 and int(hgt) <= 193)

def check_valid_height_in_inch(hgt):
    return (int(hgt) > 59 and int(hgt) <= 76)

def check_valid_haircolor(hcl):
    return bool(re.search('^#[0-9a-f]{6,6}$', hcl))

def check_valid_eye_color(ecl):
    return ecl in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

def check_valid_passportid(pid):
    return bool(re.search('^[0-9]{9,9}$', pid))

def run_unit_tests():
    answer_test_part1 = count_n_valid_passports_part1('Data/input_day4a_test.txt')
    assert answer_test_part1 == 2

    assert check_valid_birth_year('1991') == True
    assert check_valid_birth_year('1919') == False
    assert check_valid_birth_year('199') == False
    assert check_valid_birth_year('19945') == False
    assert check_valid_birth_year('a1991') == False

    assert check_valid_haircolor('#000000') == True
    assert check_valid_haircolor('#aaaaaa') == True
    assert check_valid_haircolor('#a0f2c3') == True
    assert check_valid_haircolor('#AAAAAA') == False
    assert check_valid_haircolor('#gggggg') == False

    assert check_valid_eye_color('hzl') == True
    assert check_valid_eye_color('bla') == False

    assert check_valid_passportid('012345678') == True
    assert check_valid_passportid('00000000000') == False

    test_passport = 'hcl:78cda6 pid:36823553 iyr:2021 cid:235 byr:2028 eyr:2011 hgt:113 ecl:#02ce86'
    assert extract_passport_info_by_keyword(test_passport, 'hcl') == '78cda6'
    assert extract_passport_info_by_keyword(test_passport, 'pid') == '36823553'
    assert extract_passport_info_by_keyword(test_passport, 'iyr') == '2021'
    assert extract_passport_info_by_keyword(test_passport, 'cid') == '235'
    assert extract_passport_info_by_keyword(test_passport, 'byr') == '2028'
    assert extract_passport_info_by_keyword(test_passport, 'eyr') == '2011'
    assert extract_passport_info_by_keyword(test_passport, 'hgt') == '113'
    assert extract_passport_info_by_keyword(test_passport, 'ecl') == '#02ce86'

    assert count_n_valid_passports_part2('Data/input_day4b_test_invalid.txt') == 0
    assert count_n_valid_passports_part2('Data/input_day4b_test_valid.txt') == 4
run_unit_tests()

answer_part1 = count_n_valid_passports_part1('Data/input_day4.txt')
answer_part2 = count_n_valid_passports_part2('Data/input_day4.txt')