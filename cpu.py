class CPU:
    def __init__(self):
        self.AX = 0
        self.BX = 0
        self.CX = 0
        self.DX = 0
        self.SP = 0xFFFE
        self.BP = 0
        self.SI = 0
        self.DI = 0

        self.IP = 0
        self.FLAGS = [0, 0, 0, 0]
        #flags include ZF, SF, CF, OF 

    def fetch8(self, mem):
        value = mem.read8(self.IP)
        self.IP += 1
        return value

    def fetch16(self, mem):
        value = mem.read16(self.IP)
        self.IP += 2
        return value
    
    def setFlags(self, result, op1=None, op2=None):
        """Set ZF, SF, CF, OF for 16-bit arithmetic.
        result: the full integer result (can be > 16 bits)
        op1, op2: optional operands for OF calculation
        """
        result16 = result & 0xFFFF

        # Zero Flag
        self.FLAGS[0] = int(result16 == 0)

        # Sign Flag (bit 15)
        self.FLAGS[1] = int((result16 & 0x8000) != 0)

        # Carry Flag (if result > 16-bit)
        self.FLAGS[2] = int(result > 0xFFFF)

        # Overflow Flag (for signed 16-bit arithmetic)
        if op1 is not None and op2 is not None:
            # OF is set if signs of operands same but sign of result differs
            self.FLAGS[3] = int(((op1 ^ result16) & (op2 ^ result16) & 0x8000) != 0)
        else:
            self.FLAGS[3] = 0

            
        

