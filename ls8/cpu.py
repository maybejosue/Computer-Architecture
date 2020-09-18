"""CPU functionality."""

import sys

# LDI = 0b10000010
# PRN = 0b01000111
# HLT = 0b00000001
# MUL = 0b10100010


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.cycle = True
        self.flag = {
            'L': None,
            'G': None,
            'E': None
        }

        self.machine_code = {
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b00000001: self.HLT,
            0b10100010: self.MUL,
            0b10100111: self.CMP,
            0b01010101: self.JEQ,
            0b01010110: self.JNE,
            0b01010100: self.JMP
        }

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        print(sys.argv)

        # open program
        program = open(sys.argv[1], 'r')
        # read program
        r = program.read()
        # split everything after the #
        s = r.split("\n")
        for i in s:
            if len(i) > 0:
                if i[0] in '10':
                    num = int(i[:8], 2)
                    self.ram[address] = num
                    address += 1

        # join program

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == 'MUL':
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
        elif op == 'CMP':
            self.flag['E'] = 1 if self.reg[reg_a] == self.reg[reg_b] else 0
            self.flag['L'] = 1 if self.reg[reg_a] < self.reg[reg_b] else 0
            self.flag['G'] = 1 if self.reg[reg_a] > self.reg[reg_b] else 0

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

    def CMP(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)

        self.alu('CMP', operand_a, operand_b)
        self.pc += 3

    def JEQ(self):
        if self.flag['E'] == True:
            return self.JMP()
        self.pc += 2

    def JNE(self):
        if self.flag['E'] == False:
            return self.JMP()
        self.pc += 2

    def JMP(self):
        operand_a = self.ram_read(self.pc+1)
        self.pc = self.reg[operand_a]

    def LDI(self):
        # set operand_a and use ram read with addy at self.pc + 1
        operand_a = self.ram_read(self.pc + 1)
        # set operand_b and use ram read with addy at self.pc + 2
        operand_b = self.ram_read(self.pc + 2)
        # set value of a register
        self.reg[operand_a] = operand_b

        self.pc += 3

    def PRN(self):
        current_value = self.ram_read(self.pc + 1)

        print(self.reg[current_value])

        self.pc += 2

    def HLT(self):
        self.cycle = False

    def MUL(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)

        self.alu('MUL', operand_a, operand_b)
        self.pc += 3

    def run(self):
        """Run the CPU."""
        while self.cycle:
            ir = self.ram[self.pc]

            self.machine_code[ir]()

    def ram_read(self, addy):
        return self.ram[addy]

    def ram_write(self, addy, value):
        self.ram[addy] = value
