import ipdb
import itertools

"""What I like in this code is my use of Composition over Inheritance, delegating the task of decoding the instructions."""

class BitMaskSystem():
    def __init__(self, decoder):
        self.decoder = decoder

    def process_initialization_program(self, filename):
        initialization_steps = [line.strip() for line in open(filename).readlines()]
        [self.take_appropriate_action_initalization_step(step) for step in initialization_steps]

    def take_appropriate_action_initalization_step(self, step):
        if step[0:4] == 'mask':
            self.decoder.update_mask(step)
        else:
            self.decoder.write_to_memory(step)

    def sum_all_values_in_memory(self):
        return sum([val for i, val in self.decoder.memory.items()])

class Decoder():
    def __init__(self):
        self.memory = {}
        self.bitmask = ''

    def update_mask(self, mask_string):
        mask = list(mask_string.split( ' = ' )[1])
        mask = [int(mask_val) if mask_val != 'X' else 'X' for mask_val in mask]
        print(f"Updating mask... to {mask}")
        self.bitmask = mask

    def process_memory_step(self, step):
        address_string, value_string = step.split(' = ')
        address = address_string.replace('mem[', '').replace(']', '')
        return int(address), int(value_string)

    def convert_decimal_to_36bit_binarystring(self, dec_number):
        binary_string = bin(dec_number)[2:]
        return [int(x) for x in binary_string.zfill(36)]

class DecoderPartA(Decoder):
    def __init__(self):
        super().__init__()

    def write_to_memory(self, step):
        address, decimal_write_value = self.process_memory_step(step)
        print(f"Writing to memory address {address}, with value: {decimal_write_value}")
        self.memory[address] = self.apply_bitmask_to_binary_write_value(self.convert_decimal_to_36bit_binarystring(decimal_write_value))

    def apply_bitmask_to_binary_write_value(self, decimal_write_value):
        for i in [i for i in range(0, len(decimal_write_value)) if self.bitmask[i] != 'X']:
            if self.bitmask[i] != decimal_write_value[i]:
                decimal_write_value[i] = max(decimal_write_value[i], self.bitmask[i]) - decimal_write_value[i]
        return int(''.join([str(x) for x in decimal_write_value]),2)

class DecoderPartB(Decoder):
    def __init__(self):
        super().__init__()

    def write_to_memory(self, step):
        encoded_address, decimal_write_value = self.process_memory_step(step)
        decoded_address = self.apply_bitmask_to_address(self.convert_decimal_to_36bit_binarystring(encoded_address))

        print(f'decoded address: {decoded_address}')
        memory_addresses = self.get_memory_addresses_from_decoded_address(decoded_address)
        for a in memory_addresses:
            self.memory[a] = decimal_write_value
        print(f'{len(memory_addresses)} addresses updated with value {decimal_write_value}')

    def apply_bitmask_to_address(self, address):
        for i in range(0, len(self.bitmask)):
            if self.bitmask[i] in ['X', 1]:
                address[i] = self.bitmask[i]
        return [[str(a)] if a != 'X' else ['0','1'] for a in address]

    def get_memory_addresses_from_decoded_address(self, decoded_address):
        return [int('0b' + ''.join(a), 2) for a in itertools.product(*decoded_address)]

def unit_tests():
    system = BitMaskSystem(DecoderPartA())
    system.process_initialization_program('Data/input_day14_testa.txt')
    assert system.sum_all_values_in_memory() == 165
    system.decoder = DecoderPartB()
    system.process_initialization_program('Data/input_day14_testb.txt')
    assert system.sum_all_values_in_memory() == 208

unit_tests()

system = BitMaskSystem(DecoderPartA())
system.process_initialization_program('Data/input_day14.txt')
answer_part_a = system.sum_all_values_in_memory()
system.decoder = DecoderPartB()
system.process_initialization_program('Data/input_day14.txt')
answer_part_b = system.sum_all_values_in_memory()