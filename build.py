import os
import re
import pin
import assembly as ASM

dirname=os.path.dirname(__file__)

inputfile=os.path.join(dirname,'program.asm')
outputfile=os.path.join(dirname,'program.bin')

annotation=re.compile(r"(.*?);.*")  #正则：‘.’表示单字符，‘*’表示任意次，‘？’表示非贪婪，只匹配第一个分号

codes=[]    #存放编译后的机器码，格式为Code对象
marks={}

OP2={
    'MOV':ASM.MOV,  #10000000
    'ADD':ASM.ADD,  #10010000
    'SUB':ASM.SUB,  #10100000
    'AND':ASM.AND,  #10110000
    'OR':ASM.OR,    #11000000
    'XOR':ASM.XOR,  #11010000
    'CMP':ASM.CMP,  #11100000
}

OP1={
    'INC':ASM.INC,  #01000000
    'DEC':ASM.DEC,  #01000100
    'NOT':ASM.NOT,  #01001000
    'JMP':ASM.JMP,  #01001100
    'JZ':ASM.JZ,    #01010000 零跳转
    'JNZ':ASM.JNZ,  #01010100 非零跳转
    'JC':ASM.JC,    #01011000 溢出跳转
    'JNC':ASM.JNC,  #01011100 非溢出跳转
    'JB':ASM.JB,    #01100000 负数跳转
    'JNB':ASM.JNB,  #01100100 非负数跳转
    'JP':ASM.JP,    #01101000 奇数跳转
    'JNP':ASM.JNP,  #01101100 偶数跳转
    'PUSH':ASM.PUSH,    #01110000 入栈
    'POP':ASM.POP,      #01110100 出栈
    'CALL':ASM.CALL,    #01111000 函数调用

}
OP0={
    'NOP':ASM.NOP,  #00000001
    'HLT':ASM.HLT,  #00111111
    'RET':ASM.RET,  #00000010 函数返回
}

OP2SET=set(OP2.values())    #OP2中各元素值组成的集合{ASM.MOV,ASM.ADD...}
OP1SET=set(OP1.values())    #OP1中各元素值组成的集合
OP0SET=set(OP0.values())    #OP0中各元素值组成的集合{ASM.NOP,ASM.HLT...}

REGISTERS={
    'A':pin.A,
    'B':pin.B,
    'C':pin.C,
    'D':pin.D,
    'CS':pin.CS,
    'BP':pin.BP,
    'SS':pin.SS,
    'SP':pin.SP,
    'T1':pin.T1,
    'T2':pin.T2,
    'T3':pin.T3,

}   #寄存器编号集合，这些值将会被写入DST与SRC中，通过DW,SW,DR,SR控制对应寄存器


#print(OP2SET)
#print(OP1SET)
#print(OP0SET)

class Code(object):
    def __init__(self,number,source):
        self.num=number #行号
        self.sou=source.upper() #分号之前的代码内容
        self.op=None    #操作符
        self.dst=None   #目的操作数寄存器对应值
        self.src=None   #原操作数寄存器对应值
        self.lable=None #转移指令标识符
        self.byte=0     #指令占用的字节数
        self.prepare()  #内建函数，代码处理，将self.sou分为op,dst,src

    def prepare(self):  #内建函数，代码处理，将self.sou分为op,dst,src
        if self.sou.endswith(':'):  #判断是否为转移指令标识
            self.lable=self.sou.strip(':')
            return
            
        command=self.sou.split(',') #通过‘，’进行分隔
        if len(command)>2:  #出现两个以上逗号，代码错误
            raise SyntaxError(self)
        elif len(command)==2:   #一个逗号，为二地址指令
            self.src=command[1].strip() #逗号后的值，去掉多余空格后，为原操作数寄存器对应值
            self.byte=3
        
        command=re.split(r" +",command[0])  #以空格对逗号前的值进行分割
        if len(command)>2:
            raise SyntaxError(self)
        elif len(command)==2:
            self.dst=command[1].strip()
            if(self.byte!=3):
               self.byte=2
        else:
            self.byte=1
        
        self.op=command[0].strip()

    def get_op(self):   #将MOV、ADD等操作符转为对应机器码
        if self.op in OP2:
            return OP2[self.op]
        elif self.op in OP1:
            return OP1[self.op]
        elif self.op in OP0:
            return OP0[self.op]
        else:
            raise SyntaxError(self)
    
    def get_am(self,addr):  #获得操作数
        global marks
        if not addr:
            return None,None
        if addr in marks:
            return pin.AM_INS,marks[addr]
        if addr in REGISTERS:
            return pin.AM_REG,REGISTERS[addr]   #寄存器寻址AM_REG=1
        if re.match(r'^[0-9]+$',addr):
            return pin.AM_INS,int(addr) #立即数寻址AM_INS=0
        if re.match(r'^0X[0-9A-F]+$',addr):
            return pin.AM_INS,int(addr,16)  #立即数寻址AM_INS=0
        mat=re.match(r'^\[([0-9]+)\]$',addr)
        if mat:
            return pin.AM_DIR,int(mat.group(1)) #直接寻址AM_DIR=2,通过mat.group(1)刷选[]内的内容
        mat=re.match(r'^\[(0X[0-9A-F]+)\]$',addr)
        if mat:
            return pin.AM_DIR,int(mat.group(1),16) #直接寻址AM_DIR=2,通过mat.group(1)刷选[]内的内容,并转化为16进制
        mat=re.match(r'^\[(.+)\]$',addr)    #直接寻址AM_RAM=3,通过mat.group(1)刷选[]内的内容
        if mat and mat.group(1) in REGISTERS:
            #print(mat)
            #print(mat.group(1))
            return pin.AM_RAM,REGISTERS[mat.group(1)]

        raise SyntaxError(self)
    
    def build_code(self):
        op=self.get_op()
        amd,dst=self.get_am(self.dst)
        ams,src=self.get_am(self.src)
        #print(amd,dst)
        #print(ams,src)
        #if src and (amd,ams) not in ASM.INSTRUCTIONS[2][op]:
        #    raise SyntaxError(self)

        if op in OP2SET:
            if amd is None or ams is None:
                #print('err0')
                raise SyntaxError(self)
            else:
                ir=op | (amd<<2) | ams
        elif op in OP1SET:
            if amd is None:
                #print('err1')
                raise SyntaxError(self)
            else:
                ir=op | amd
        else:
            ir=op

        return[ir,dst,src]

    def __repr__(self):
        return f'[{self.num}] {self.sou}'

class SyntaxError(Exception):
    def __init__(self,code:Code,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.code=code



def compile_program():
    global marks
    with open(inputfile,encoding='utf8') as file:
        lines=file.readlines()
    for index,line in enumerate(lines):
        source=line.strip()
        if not source:
            continue
        if ';' in source:
            match=annotation.match(source)
            source=match.group(1)
            if not source:
                continue
        else:
            pass

        code=Code(index+1,source)
        print(code)
        codes.append(code)

    #print(codes)

    for var in range(len(codes)-1,-1,-1):
        code_temp=codes[var]
        #print(code_temp.byte)
        if code_temp.lable:
            jump_byte=0
            for i in range(var):
                jump_byte=jump_byte+codes[i].byte
            marks[code_temp.lable]=jump_byte
            del codes[var]
    
    #print(codes)
    #print(marks)
    #print(marks['INCEASE'])
    
    with open(outputfile,'wb') as file:
        for code in codes:
            values=code.build_code()
            for value in values:
                if value is None:
                    continue
                result= value.to_bytes(1,byteorder='little')
                file.write(result)
                

def main():
    try:
        compile_program()
    except SyntaxError as e:
        print(f'Syntax Error in {e.code}')
        return
    print("Finish Build")


if __name__ == '__main__':
    main()
