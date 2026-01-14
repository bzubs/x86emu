with open("test.bin", "wb") as f:
    f.write(bytes([
        0xB8, 0x05, 0x00,  # MOV AX, 5
        0xB9, 0x06, 0x00,   #MOV BX, 06
        0x8B, 0xD8,        # MOV BX, AX
        0xF4               # HLT (VERY IMPORTANT)
    ]))