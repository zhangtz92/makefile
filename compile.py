import os
import pin
import assembly as ASM

dirname=os.path.dirname(__file__)
filename=os.path.join(dirname,'cpu.bin')

micro=[pin.HLT for _ in range(0x10000)]

for addr in range(0x10000):
    ir=addr>>8
    psw=(addr>>8) & 0x0f
    cyc=addr & 0x0f

    if cyc < len(ASM.FETCH):
        micro[addr]=ASM.FETCH[cyc]
        #micro[addr]=0

with open(filename,'wb') as file:
    for value in micro:
        result= value.to_bytes(4,byteorder='little')
        file.write(result)
        #print(value,result)

print("COMPLIE Finish")