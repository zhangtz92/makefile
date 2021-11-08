import os
import pin
import assembly as ASM

dirname=os.path.dirname(__file__)
filename=os.path.join(dirname,'cpu.bin')

micro=[pin.HLT for _ in range(0x10000)]

def compile_addr2(addr,ir,psw,index):
    global micro
    op = ir & 0xf0
    amd = (ir & 0x0c)>>2 #二地址指令中1xxx[aa][bb]中的[aa]
    ams = ir & 0x03 #二地址指令中1xxx[aa][bb]中的[bb]
    INST=ASM.INSTRUCTIONS[2]
    if op not in INST:
        micro[addr]=pin.PCC_RD  #如果找不到操作符，则程序计数器清零
        return
    am=(amd,ams)#寻址方式
    #print(am)
    if am not in INST[op]:
        micro[addr]=pin.PCC_RD  #如果找不到对于寻址方式，则程序计数器清零
        return
    #print('ok3')
    EXE=INST[op][am]
    if index < len(EXE):
        micro[addr]=EXE[index]
        #print('ok')
    else:
        micro[addr]=pin.PCC_RD  #程序计数器清零，重新开始

def compile_addr1(addr,ir,psw,index):
    global micro
    op = ir & 0xfc  #一地址指令格式为01xxxx[aa]
    amd = ir & 0x03 #一地址指令中01xxxx[aa]中的[aa]
    INST=ASM.INSTRUCTIONS[1]
    if op not in INST:
        micro[addr]=pin.PCC_RD  #如果找不到操作符，则程序计数器清零
        return
    #print(ams)
    if amd not in INST[op]:
        micro[addr]=pin.PCC_RD  #如果找不到对于寻址方式，则程序计数器清零
        return
    #print('ok3')
    EXE=INST[op][amd]
    if index < len(EXE):
        micro[addr-2]=EXE[index]
        #print('ok')
    else:
        micro[addr-2]=pin.PCC_RD  #程序计数器清零，重新开始

def compile_addr0(addr,ir,psw,index):
    global micro
    op = ir
    INST=ASM.INSTRUCTIONS[0]
    if op not in INST:
        micro[addr]=pin.PCC_RD  #如果找不到操作符，则程序计数器清零
        return
    EXE=INST[op]
    if index < len(EXE):
        micro[addr-4]=EXE[index]
    else:
        micro[addr-4]=pin.PCC_RD  #程序计数器清零，重新开始

for addr in range(0x10000):
    ir=addr>>8
    psw=(addr>>8) & 0x0f
    cyc=addr & 0x0f

    if cyc < len(ASM.FETCH):
        micro[addr]=ASM.FETCH[cyc]
        #micro[addr]=0
        continue

    addr2=ir & (1 << 7)
    addr1=ir & (1 << 6)

    index=cyc-len(ASM.FETCH)
    if addr > 0:
        if addr2:
            compile_addr2(addr,ir,psw,index)
        elif addr1:
            compile_addr1(addr,ir,psw,index)
        else:
            compile_addr0(addr,ir,psw,index)

with open(filename,'wb') as file:
    for value in micro:
        result= value.to_bytes(4,byteorder='little')
        file.write(result)
        #print(value,result)

print("COMPLIE Finish")