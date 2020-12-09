"""Idea: save instruction lines that have been executed, and before execution each line,
check if it is not already contained in the list. If it is, quit the main loop and return the current value of acc"""
import ipdb

class gameConsole():
    def __init__(self, filename):
        self.filename = filename
        self.processed_lines = []
        self.current_line = 0
        self.accumulator = 0
        self.processed_last_instruction = 0
        self.instruction_dict = {'acc': self.acc, 'jmp': self.jmp, 'nop': self.nop}
        self.console_buffer = [line.strip() for line in open(filename).readlines()]
        self.n_tries_brute_force_nop = 0
        self.n_tries_brute_force_jmp = 0
        self.global_change_allowed = 1

    def solve_part_a(self):
        self.main_loop(change_allowed = False)
        return self.accumulator

    def solve_part_b(self):
        self.main_loop(change_allowed = True)
        return self.accumulator

    def main_loop(self, change_allowed = True):
        while(self.current_line not in self.processed_lines and self.processed_last_instruction == 0):
            if self.check_terminination_condition():
                self.terminate()
            else:
                if change_allowed and self.global_change_allowed:
                    print("accumulator value: " + str(self.accumulator))
                    self.process_current_line_with_fix()
                else:
                    self.process_current_line()

    def check_terminination_condition(self):
        return self.current_line == (len(self.console_buffer) - 1)

    def terminate(self):
        print("Now terminating")
        self.process_current_line()
        self.current_line = len(self.console_buffer) - 1
        self.processed_last_instruction = 1

    def process_current_line(self):
        instruction, arg = self.read_current_instruction()
        self.instruction_dict[instruction](arg)

    def read_current_instruction(self):
        #print(f"Reading current instruction {self.current_line}")
        self.processed_lines.append(self.current_line)
        instruction, arg = self.console_buffer[self.current_line].split(" ")
        arg = arg.replace("+", "" )
        return instruction, arg

    def process_current_line_with_fix(self):
        instruction, arg = self.read_current_instruction()
        if instruction == "nop":
            instruction = self.change_nop_to_jmp_if_leads_to_termination(arg)
        elif instruction == "jmp":
            instruction = self.change_jmp_to_nop_if_leads_to_termination(arg)
        self.instruction_dict[instruction](arg)

    def change_nop_to_jmp_if_leads_to_termination(self, instr_value):
        """Or if it leads to a line after which all subsequent line numbers contain no jmp instructions"""
        if self.check_change_nop_to_jmp_leads_directly_to_termination(instr_value) or self.change_nop_to_jmp_leads_eventually_to_last_instruction(instr_value):
            #print( f"Changing nop to jmp at line {self.current_line} leads to a direct termination.")
            self.console_buffer[self.current_line] = 'jmp ' + instr_value
            return 'jmp'
        else:
            #print(f"Changing nop to jmp at line {self.current_line} does not lead to a termination.")
            return 'nop'

    def check_change_nop_to_jmp_leads_directly_to_termination(self, instr_value):
        return self.current_line + int(instr_value) == (len(self.console_buffer)-1)

    def change_nop_to_jmp_leads_eventually_to_last_instruction(self, instr_value):
        if self.check_is_last_backward_jmp_instruction_in_subsequent_lines(self.current_line + int(instr_value) ):
            return True
        else:
            return self.check_brute_force_change_nop_to_jmp_leads_to_termination('nop', instr_value)

    def check_brute_force_change_nop_to_jmp_leads_to_termination(self, instr, instr_value):
        if instr == 'nop':
            self.n_tries_brute_force_nop = self.n_tries_brute_force_nop + 1
            print(f"This is the {self.n_tries_brute_force_nop}th brute force try for {instr}")
            changed_instr = 'jmp'
        else:
            self.n_tries_brute_force_jmp = self.n_tries_brute_force_jmp + 1
            print(f"This is the {self.n_tries_brute_force_jmp}th brute force try for {instr}")
            changed_instr = 'nop'

        temp_game_console = gameConsole(self.filename)
        temp_game_console.current_line = self.current_line
        console_buffer_to_check = self.console_buffer.copy()
        console_buffer_to_check[self.current_line] = changed_instr + ' ' + instr_value
        temp_game_console.console_buffer = console_buffer_to_check
        temp_game_console.processed_lines = list(set(self.processed_lines) - set([self.current_line]))
        temp_game_console.solve_part_a()

        print(str(max(self.processed_lines)) + " - " + str(max(temp_game_console.processed_lines)))

        if temp_game_console.check_terminination_condition():
            print(f"The following line is changed: {self.current_line}")
            self.global_change_allowed = 0
            return True
        return False

    def change_jmp_to_nop_if_leads_to_termination(self, instr_value):
        if self.check_is_last_backward_jmp_instruction_in_subsequent_lines(self.current_line) or self.check_brute_force_change_nop_to_jmp_leads_to_termination('jmp', instr_value):
            #print( f"Changing jmp to nop at line {self.current_line} leads to an eventual termination.")
            self.console_buffer[self.current_line] = 'nop ' + instr_value
            return 'nop'
        else:
            #print(f"Changing jmp to nop at line {self.current_line} does not necessarily lead to an eventual termination.")
            return 'jmp'

    def check_is_last_backward_jmp_instruction_in_subsequent_lines(self, current_line):
        remaining_lines = self.console_buffer[(current_line + 1):]
        return sum(["jmp -" in line for line in remaining_lines]) == 0

    def acc(self, *args):
        acc_value = int(args[0])
        #print( f"Current line {self.current_line}: Instruction: acc, arg: {acc_value}")
        self.accumulator = self.accumulator + acc_value
        self.current_line = self.current_line + 1

    def jmp(self, *args):
        n_lines = int(args[0])
        #print( f"Current line {self.current_line}: Instruction: jmp, arg: {n_lines}")
        self.current_line = self.current_line + n_lines

    def nop(self, *args):
        #print( f"Current line {self.current_line}: Instruction: nop, arg: {args[0]}")
        self.current_line = self.current_line + 1

    def reset_state(self):
        self = self.__init__(self.filename)

def unit_tests():
    game_console = gameConsole('Data/input_day8a_test.txt')
    assert game_console.solve_part_a() == 5
    game_console.reset_state()
    assert game_console.solve_part_b() == 8

unit_tests()
game_console = gameConsole('Data/input_day8.txt')
answer_part_a = game_console.solve_part_a()
game_console = gameConsole('Data/input_day8.txt')
answer_part_b = game_console.solve_part_b()