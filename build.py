import os
import re
import pin
import assembly as ASM

dirname=os.path.dirname(__file__)

inputfile=os.path.join(dirname,'program.asm')
outputfile=os.path.join(dirname,'program.bin')

annotation=re.compile(r"(.*?);.*")

codes=[]

OP2={
    'MOV':ASM.MOV,
}

OP1={}
OP0={
    'NOP':ASM.NOP,
    'HLT':ASM.HLT,
}

OP2SET=set(OP2.values())
OP1SET=set(OP1.values())
OP0SET=set(OP0.values())

REGISTERS={
    'A':pin.A,
    'B':pin.B,
    'C':pin.C,
    'D':pin.D,

}

#print(OP2SET)
#print(OP1SET)
#print(OP0SET)

class Code(object):
    def __init__(self,number,source):
        self.num=number
        self.sou=source.upper()
        self.op=None
        self.dst=None
        self.src=None
        self.prepare()

    def prepare(self):
        command=self.sou.split(',')
        if len(command)>2:
            raise SyntaxError(self)
        elif len(command)==2:
            self.src=command[1].strip()
        
        command=re.split(r" +",command[0])
        if len(command)>2:
            raise SyntaxError(self)
        elif len(command)==2:
            self.dst=command[1].strip()
        
        self.op=command[0].strip()

    def get_op(self):
        if self.op in OP2:
            return OP2[self.op]
        elif self.op in OP1:
            return OP1[self.op]
        elif self.op in OP0:
            return OP0[self.op]
        else:
            raise SyntaxError(self)
    
    def get_am(self,addr):
        if not addr:
            return 0,0
        if addr in REGISTERS:
            return pin.AM_REG,REGISTERS[addr]
        if re.match(r'^[0-9]+$',addr):
            return pin.AM_INS,int(addr)
        if re.match(r'^[0-9A-F]+$',addr):
            return pin.AM_INS,int(addr,16)

        raise SyntaxError
    
    def build_code(self):
        op=self.get_op()
        amd,dst=self.get_am(self.dst)
        ams,src=self.get_am(self.src)
        if op in OP2SET:
            ir=op | (amd<<2) | ams
        elif op in OP1SET:
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
    with open(inputfile,encoding='utf8') as file:
        lines=file.readlines()
    for index,line in enumerate(lines):
        source=line.strip()
        if not source:
            continue
        if ';' in source:
            match=annotation.match(source)
            source=match.group(1)
        else:
            pass

        code=Code(index+1,source)
        codes.append(code)
        #print(codes)

        with open(outputfile,'wb') as file:
            for code in codes:
                values=code.build_code()
                for value in values:
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
