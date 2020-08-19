"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,  # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111,  # PRN R0
            0b00000000,
            0b00000001,  # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        print(op)

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while True:
            # ir set to ram address stored in register
            ir = self.ram[self.pc]

            if ir == LDI:
                # set operand_a and use ram read with addy at self.pc + 1
                operand_a = self.ram_read(self.pc + 1)
                # set operand_b and use ram read with addy at self.pc + 2
                operand_b = self.ram_read(self.pc + 2)
                # set value of a register
                self.reg[operand_a] = operand_b

                self.pc += 2
            elif ir == PRN:
                current_value = self.ram_read(self.pc + 1)

                print(self.reg[current_value])

                self.pc += 1
            elif ir == HLT:
                break
            else:
                break

            self.pc += 1

            self.trace()

    def ram_read(self, addy):
        return self.ram[addy]

    def ram_write(self, addy, value):
        if addy not in self.ram or self.ram[addy]:
            self.ram[addy] = value
        else:
            print('Hey item something went wrong, check ram_write function')
