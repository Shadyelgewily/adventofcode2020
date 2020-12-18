import ipdb

class BitMaskSystem():
    def __init__(self):
        self.bitmask = ''
        self.memory = {}

    def process_initialization_program(self, filename):
        initialization_steps = [line.strip() for line in open(filename).readlines()]
        [self.take_appropriate_action_initalization_step(step) for step in initialization_steps]

    def take_appropriate_action_initalization_step(self, step):
        if step[0:4] == 'mask':
            self.update_mask(step)
        else:
            self.write_to_memory(step)

    def update_mask(self, mask_string):
        mask = list(mask_string.split( ' = ' )[1])
        mask = [int(mask_val) if mask_val != 'X' else 'X' for mask_val in mask]
        print(f"Updating mask... to {mask}")
        self.bitmask = mask

    def write_to_memory(self, step):
        position, binary_write_value = self.process_memory_step(step)
        print(f"Writing to memory position {position}, with value: {binary_write_value}")
        self.memory[position] = self.apply_bitmask_to_binary_write_value(self.convert_decimal_to_36bit_binarystring(binary_write_value))

    def process_memory_step(self, step):
        position_string, value_string = step.split(' = ')
        position = position_string.replace('mem[', '').replace(']', '')
        return int(position), int(value_string)

    def apply_bitmask_to_binary_write_value(self, binary_write_value):
        for i in [i for i in range(0, len(binary_write_value)) if self.bitmask[i] != 'X']:
            if self.bitmask[i] != binary_write_value[i]:
                binary_write_value[i] = max(binary_write_value[i], self.bitmask[i]) - binary_write_value[i]
        return int(''.join([str(x) for x in binary_write_value]),2)

    def convert_decimal_to_36bit_binarystring(self, dec_number):
        binary_string = bin(dec_number)[2:]
        return [int(x) for x in binary_string.zfill(36)]

    def sum_all_values_in_memory(self):
        return sum([val for i, val in self.memory.items()])

def unit_tests():
    system = BitMaskSystem()
    system.process_initialization_program('Data/input_day14_testa.txt')
    assert system.sum_all_values_in_memory() == 165

unit_tests()

system = BitMaskSystem()
system.process_initialization_program('Data/input_day14.txt')
system.sum_all_values_in_memory()
