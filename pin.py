MSR=1
MAR=2
MDR=3
MC=4
IR=5
DST=6
SRC=7
A=8
B=9
C=10
D=11
DI=12
SI=13
SP=14
BP=15
CS=16
DS=17
SS=18
ES=19
VEC=20
T1=21
T2=22
T3=23

#读出
MSR_OUT=MSR
MAR_OUT=MAR
MDR_OUT=MDR
MC_OUT=MC
IR_OUT=IR
DST_OUT=DST
SRC_OUT=SRC
A_OUT=A
B_OUT=B
C_OUT=C
D_OUT=D
DI_OUT=DI
SI_OUT=SI
SP_OUT=SP
BP_OUT=BP
CS_OUT=CS
DS_OUT=DS
SS_OUT=SS
ES_OUT=ES
VEC_OUT=VEC
T1_OUT=T1
T2_OUT=T2
T3_OUT=T3

write_shift=5
#写入
MSR_IN=MSR << write_shift
MAR_IN=MAR << write_shift
MDR_IN=MDR << write_shift
MC_IN=MC << write_shift
IR_IN=IR << write_shift
DST_IN=DST << write_shift
SRC_IN=SRC << write_shift
A_IN=A << write_shift
B_IN=B << write_shift
C_IN=C << write_shift
D_IN=D << write_shift
DI_IN=DI << write_shift
SI_IN=SI << write_shift
SP_IN=SP << write_shift
BP_IN=BP << write_shift
CS_IN=CS << write_shift
DS_IN=DS << write_shift
SS_IN=SS << write_shift
ES_IN=ES << write_shift
VEC_IN=VEC << write_shift
T1_IN=T1 << write_shift
T2_IN=T2 << write_shift
T3_IN=T3 << write_shift

DST_W =2 ** 10
DST_R =2 ** 11
SRC_W =2 ** 12
SRC_R =2 ** 13

#PC_CS=2 ** 14
#PC_WE=2 ** 15
#PC_EN=2 ** 16

#PC_OUT=PC_CS
#PC_RD=PC_CS | PC_WE
#PC_INC=PC_CS | PC_WE | PC_EN

PC_RD=2 ** 14
PC_EN=2 ** 15
PC_OUT=2 ** 16
PC_INC=PC_EN


ALU_OP0=2 ** 17
ALU_OP1=2 ** 18
ALU_OP2=2 ** 19

ALU_ADD=0
ALU_SUB=ALU_OP0
ALU_AND=ALU_OP1
ALU_OR=ALU_OP0 | ALU_OP1
ALU_NOT=ALU_OP2
ALU_XOR=ALU_OP2 | ALU_OP0

ALU_ADD_EN=2 ** 20

PCC_RD=2 ** 30

HLT=2 ** 31


