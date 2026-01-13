class Memory:
    def __init__(self, size=1024 * 1024):
        self.size = size
        self.mem = bytearray(size)
        #each memory address stores 1 byte i.e. 8 bits

    def write8(self, addr, val):
        self.mem[addr] = val & 0xFF

    def write16(self, addr, val):
        #little endian so LSB at lower address
        self.mem[addr] = val & 0xFF              # low byte
        self.mem[addr + 1] = (val >> 8) & 0xFF 


    

    def read8(self, addr):
        return self.mem[addr] 
    

    def read16(self, addr):
        vall = self.mem[addr] 
        valh = self.mem[addr + 1]

        

        val = vall | (valh << 0xFF)
        return val



def main():
    memory = Memory()
    memory.write8(88, 90)
    val = memory.read8(1024)

    print(val)   


if __name__ == "__main__":
    main()
