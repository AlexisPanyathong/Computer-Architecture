"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Add a list property to the `CPU` class to hold 256 bytes of memory(ram).
        self.ram = [0] * 256
        
        # Add 8 general-purpose registers.
        self.reg = [0] * 8
        
        # Also add properties for any internal registers you need, e.g. `PC`.
        self.pc = 0 
        

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0
            
            with open(filename) as f:
                
                for line in f:
                    comment_split = line.strip().split('#')
                    
                    value = comment_split[0].strip()
                    
                    if value == '':
                        continue
                    
                    num = int(value)
                    
        except FileNotFoundError:
                print('File not found')
                sys.exit(2)

        # For now, we've just hardcoded a program:

        # filename = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        for instruction in filename:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    
    # Inside the CPU, there are two internal registers used for memory operations:
    # the _Memory Address Register_ (MAR) and the _Memory Data Register_ (MDR). The
    #  MAR contains the address that is being read or written to. The MDR contains
    # the data that was read or the data to write. You don't need to add the MAR or
    # MDR to your `CPU` class, but they would make handy paramter names for
    # `ram_read()` and `ram_write()`, if you wanted.
    
    # `ram_read()` should accept the address to read and return the value stored there.
    def ram_read(self, mar):
        return self.ram[mar]
    
    # `raw_write()` should accept a value to write, and the address to write it to.
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr
    

    def run(self):
        """Run the CPU."""
        # Took these from lines 29, 32, & 34
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001 
        
        running = True
        # While running:
        while running:
            
            # Read the memory address that's stored in the PC and store that results in the IR.
            ir = self.ram_read(self.pc)
            
            # Using `ram_read()`,read the bytes at `PC+1` and `PC+2` from RAM into variables `operand_a` and `operand_b` in case the instruction needs them.
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            
            # If ir is equal to LDI
            if ir == LDI:
                print('Operands a: ', operand_a, self.ram[operand_a])
                print('Operands b: ', operand_b, self.ram[operand_b])
                
                self.reg[operand_a] = operand_b
                self.pc += 3
            
            elif ir == PRN:
                reg = self.ram_read(self.pc + 1)
                self.reg[reg]
                print(f'Printing: {self.reg[reg]}')
                self.pc += 2
            
            elif ir == HLT:
               # HALT
               print('Halt') 
               running = False
               self.pc += 1
               
            else:
                print(f'Error, unknown command {ir}')
                sys.exit(1)
            
