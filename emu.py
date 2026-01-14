from cpu import CPU
from memory import Memory

cpu = CPU()
mem = Memory()

# Load test binary
with open("test.bin", "rb") as f:
    data = f.read()
mem.mem[0:len(data)] = data

REG16 = [
    "AX",  # 000
    "CX",  # 001
    "DX",  # 010
    "BX",  # 011
    "SP",  # 100
    "BP",  # 101
    "SI",  # 110
    "DI",  # 111
]

def decode_modrm(byte):
    mod = (byte >> 6) & 0b11
    reg = (byte >> 3) & 0b111
    rm  = byte & 0b111
    return mod, reg, rm

cpu.IP = 0
running = True

while running:
    opcode = cpu.fetch8(mem)

    if 0xB8 <= opcode <= 0xBF:  # MOV AX, imm16
        reg = REG16[opcode - 0xB8]
        imm = cpu.fetch16(mem)
        setattr(cpu, reg, imm)

        print(f"MOV {reg}, {hex(imm)}")

    elif opcode == 0x8B:  # MOV r16, r/m16
        modrm = cpu.fetch8(mem)
        mod, reg, rm = decode_modrm(modrm)

        if mod == 0b11:
            dst = REG16[reg]
            src = REG16[rm]
            setattr(cpu, dst, getattr(cpu, src))
            print(f"MOV {dst}, {src}")
        else:
            raise NotImplementedError("Memory addressing not implemented")
        
    elif opcode == 0x89:  # MOV r/m16, r16
        modrm = cpu.fetch8(mem)
        mod, reg, rm = decode_modrm(modrm)

        if mod == 0b11:
            dst = REG16[rm]
            src = REG16[reg]

            setattr(cpu, dst, getattr(cpu, src))
            print(f"MOV {dst}, {src}")
        else:
            raise NotImplementedError("Memory addressing not implemented")


    elif opcode == 0x05:  # ADD AX, imm16
        imm = cpu.fetch16(mem)
        cpu.AX = (cpu.AX + imm) & 0xFFFF
        print(f"ADD AX, {hex(imm)}")

    elif opcode == 0x03:
        modrm = cpu.fetch8(mem)
        mod, reg, rm = decode_modrm(modrm)  

        dest = REG16[rm]
        src = REG16[reg]

        vald = getattr(cpu, dest)
        vals = getattr(cpu, src)

        final = vald + vals

        
        if mod == 0b11:
            setattr(cpu, dest, final)
            cpu.setFlags(final, vald, vals)
        else:
            raise NotImplementedError("Memory addressing not implemented")

    elif opcode == 0xF4:  # HLT
        print("HLT")
        running = False

    else:
        print(f"Unknown opcode: {hex(opcode)}")
        break
