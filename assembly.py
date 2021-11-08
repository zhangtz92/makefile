import pin

FETCH=[pin.PC_OUT | pin.MAR_IN ,
        pin.MC_OUT | pin.IR_IN | pin.PC_INC,
        pin.PC_OUT | pin.MAR_IN ,
        pin.MC_OUT | pin.DST_IN | pin.PC_INC,
        pin.PC_OUT | pin.MAR_IN ,
        pin.MC_OUT | pin.SRC_IN | pin.PC_INC,
]

MOV=0|(1<<7)    #10000000
ADD=(1<<4)|(1<<7)       #10010000
SUB=(2<<4)|(1<<7)       #10100000
AND=(3<<4)|(1<<7)       #10110000
OR=(4<<4)|(1<<7)        #11000000
XOR=(5<<4)|(1<<7)       #11010000

INC=0|(1<<6)    #01000000
DEC=(1<<2)|(1<<6)       #01000100
NOT=(2<<2)|(1<<6)       #01001000

HLT=0x3f        #00111111
NOP=1           #00000001

INSTRUCTIONS={
        2:{
                MOV:{
                        #10000100,84
                        #MOV A 5,前面寄存器，后面立即数
                        #需要将原操作数寄存器SRC中值移到目的操作寄存器DST中表示的寄存器里
                        (pin.AM_REG,pin.AM_INS):[
                                pin.DST_W | pin.SRC_OUT
                        ],
                        #10000101,85
                        #MOV D C,前面寄存器，后面寄存器，把寄存器C中值移到寄存器D中
                        #需要将原操作数寄存器SRC中存储的值所表示的寄存器，将该寄存器中值移到目的操作寄存器DST中表示的寄存器里
                        (pin.AM_REG,pin.AM_REG):[
                                pin.SRC_R | pin.DST_W
                        ],
                        #10000110,86
                        #MOV D [0x2000],前面寄存器，后面地址，内存地址2000H中值移到寄存器D中
                        #需要将原操作数寄存器SRC中存储的地址对应的值，移到目的操作寄存器DST中表示的寄存器里
                        (pin.AM_REG,pin.AM_DIR):[
                                pin.SRC_OUT | pin.MAR_IN,
                                pin.DST_W | pin.MC_OUT
                        ],
                        #10000111,87
                        #MOV D [A],前面寄存器，后面存储于寄存器中的内存地址，寄存器A中的内存地址中的值移到寄存器D中
                        #需要将原操作数寄存器SRC中存储的值所表示的寄存器中存储的地址，将其对应的值移到目的操作寄存器DST中表示的寄存器里
                        (pin.AM_REG,pin.AM_RAM):[
                                pin.SRC_R | pin.MAR_IN,
                                pin.DST_W | pin.MC_OUT
                        ],
                        #10001000,88
                        #MOV [0x2000] 4,前面地址，后面立即数，移到内存地址2000H中
                        #需要将原操作数寄存器SRC中的值，移到目的操作寄存器DST中地址表示的内存单元里
                        (pin.AM_DIR,pin.AM_INS):[
                                pin.DST_OUT | pin.MAR_IN,
                                pin.SRC_OUT | pin.MC_IN,

                        ],
                        #10001001,89
                        #MOV [0x2000] D,前面地址，后面寄存器，寄存器D中值移到内存地址2000H中
                        #需要将原操作数寄存器SRC中存储的值所表示的寄存器，将该寄存器中值移到目的操作寄存器DST中地址表示的内存单元里
                        (pin.AM_DIR,pin.AM_REG):[
                                pin.DST_OUT | pin.MAR_IN,
                                pin.SRC_R | pin.MC_IN
                        ],
                        #10001010,8A
                        #MOV [0x2000] [0x1000],前面地址，后面地址，地址1000H中的值移到内存地址2000H中
                        #需要将原操作数寄存器SRC中存储的值所表示的内存单元中的值，移到目的操作寄存器DST中地址表示的内存单元里
                        (pin.AM_DIR,pin.AM_DIR):[
                                pin.SRC_OUT | pin.MAR_IN,
                                pin.T1_IN | pin.MC_OUT,
                                pin.DST_OUT | pin.MAR_IN,
                                pin.T1_OUT | pin.MC_IN 
                        ],
                        #10001011,8B
                        #MOV [0x2000] [A],前面地址，后面存储于寄存器中的内存地址，寄存器A中的内存地址对应的值移到内存地址2000H中
                        #需要将原操作数寄存器SRC中存储的值所表示的寄存器中存储的地址，将其对应的值移到目的操作寄存器DST中地址表示的内存单元里
                        (pin.AM_DIR,pin.AM_RAM):[
                                pin.SRC_R | pin.MAR_IN,
                                pin.T1_IN | pin.MC_OUT,
                                pin.DST_OUT | pin.MAR_IN,
                                pin.T1_OUT | pin.MC_IN 
                        ],
                        #10001100,8C
                        #MOV [B] 5,前面存储于寄存器中的内存地址，后面立即数，移到寄存器B中的内存地址中
                        #需要将原操作数寄存器SRC中存储的值，移到目的操作寄存器DST中值所表示的寄存器中存储的内存单元里
                        (pin.AM_RAM,pin.AM_INS):[
                                pin.DST_R | pin.MAR_IN,
                                pin.SRC_OUT | pin.MC_IN
                        ],
                        #10001101,8D
                        #MOV [B] A,前面存储于寄存器中的内存地址，后面寄存器，寄存器中值移到寄存器B中的内存地址中
                        #需要将原操作数寄存器SRC中存储的值所表示的寄存器，将该寄存器中值移到目的操作寄存器DST中值所表示的寄存器中存储的内存单元里
                        (pin.AM_RAM,pin.AM_REG):[
                                pin.DST_R | pin.MAR_IN,
                                pin.SRC_R | pin.MC_IN
                        ],
                        #10001110,8E
                        #MOV [B] [0x1000],前面存储于寄存器中的内存地址，后面地址，内存地址中的值移到寄存器B中的内存地址中
                        #需要将原操作数寄存器SRC中存储的地址，将该地址中值移到目的操作寄存器DST中值所表示的寄存器中存储的内存单元里
                        (pin.AM_RAM,pin.AM_DIR):[
                                pin.SRC_OUT | pin.MAR_IN,
                                pin.T1_IN | pin.MC_OUT,
                                pin.DST_R | pin.MAR_IN,
                                pin.T1_OUT | pin.MC_IN
                        ],
                        #10001111,8F
                        #MOV [B] [C],前面存储于寄存器中的内存地址，后面存储于寄存器中的内存地址，寄存器C中的内存地址中的值移到寄存器B中的内存地址中
                        #需要将原操作数寄存器SRC中所表示的寄存器中存储的内存单元中的值，移到目的操作寄存器DST中值所表示的寄存器中存储的内存单元里
                        (pin.AM_RAM,pin.AM_RAM):[
                                pin.SRC_R | pin.MAR_IN,
                                pin.T1_IN | pin.MC_OUT,
                                pin.DST_R | pin.MAR_IN,
                                pin.T1_OUT | pin.MC_IN
                        ],
                },
                ADD:{
                        #10010100,94
                        #ADD D 5,前面寄存器，后面立即数
                        #需要将原操作数寄存器SRC中值与目的操作寄存器DST中表示的寄存器中值相加
                        (pin.AM_REG,pin.AM_INS):[
                                pin.DST_R | pin.A_IN,
                                pin.SRC_OUT | pin.B_IN,
                                pin.ALU_ADD | pin.ALU_EN | pin.DST_W
                        ],
                        #10010101,95
                        #ADD D C,前面寄存器，后面寄存器
                        #需要将原操作数寄存器SRC中表示的寄存器中值与目的操作寄存器DST中表示的寄存器中值相加
                        (pin.AM_REG,pin.AM_REG):[
                                pin.DST_R | pin.A_IN,
                                pin.SRC_R | pin.B_IN,
                                pin.ALU_ADD | pin.ALU_EN | pin.DST_W
                        ],
                },
                SUB:{
                        #10100100,A4
                        #SUB D 5,前面寄存器，后面立即数
                        #需要将原操作数寄存器SRC中值与目的操作寄存器DST中表示的寄存器中值相减
                        (pin.AM_REG,pin.AM_INS):[
                                pin.DST_R | pin.A_IN,
                                pin.SRC_OUT | pin.B_IN,
                                pin.ALU_SUB | pin.ALU_EN | pin.DST_W
                        ],
                        #10100101,A5
                        #SUB D C,前面寄存器，后面寄存器
                        #需要将原操作数寄存器SRC中表示的寄存器中值与目的操作寄存器DST中表示的寄存器中值相减
                        (pin.AM_REG,pin.AM_REG):[
                                pin.DST_R | pin.A_IN,
                                pin.SRC_R | pin.B_IN,
                                pin.ALU_SUB | pin.ALU_EN | pin.DST_W
                        ],
                },
                AND:{
                        #10110100,B4
                        #AND B 5,前面寄存器，后面立即数
                        #需要将原操作数寄存器SRC中值与目的操作寄存器DST中表示的寄存器中值位与
                        (pin.AM_REG,pin.AM_INS):[
                                pin.DST_R | pin.A_IN,
                                pin.SRC_OUT | pin.B_IN,
                                pin.ALU_AND | pin.ALU_EN | pin.DST_W
                        ],
                        #10110101,B5
                        #AND D C,前面寄存器，后面寄存器
                        #需要将原操作数寄存器SRC中表示的寄存器中值与目的操作寄存器DST中表示的寄存器中值位与
                        (pin.AM_REG,pin.AM_REG):[
                                pin.DST_R | pin.A_IN,
                                pin.SRC_R | pin.B_IN,
                                pin.ALU_AND | pin.ALU_EN | pin.DST_W
                        ],
                },
                OR:{
                        #11000100,C4
                        #OR B 5,前面寄存器，后面立即数
                        #需要将原操作数寄存器SRC中值与目的操作寄存器DST中表示的寄存器中值位或
                        (pin.AM_REG,pin.AM_INS):[
                                pin.DST_R | pin.A_IN,
                                pin.SRC_OUT | pin.B_IN,
                                pin.ALU_OR | pin.ALU_EN | pin.DST_W
                        ],
                        #11000101,C5
                        #OR D C,前面寄存器，后面寄存器
                        #需要将原操作数寄存器SRC中表示的寄存器中值与目的操作寄存器DST中表示的寄存器中值位或
                        (pin.AM_REG,pin.AM_REG):[
                                pin.DST_R | pin.A_IN,
                                pin.SRC_R | pin.B_IN,
                                pin.ALU_OR | pin.ALU_EN | pin.DST_W
                        ],
                },
                XOR:{
                        #11010100,D4
                        #XOR B 5,前面寄存器，后面立即数
                        #需要将原操作数寄存器SRC中值与目的操作寄存器DST中表示的寄存器中值位异或
                        (pin.AM_REG,pin.AM_INS):[
                                pin.DST_R | pin.A_IN,
                                pin.SRC_OUT | pin.B_IN,
                                pin.ALU_XOR | pin.ALU_EN | pin.DST_W
                        ],
                        #11000101,D5
                        #XOR D C,前面寄存器，后面寄存器
                        #需要将原操作数寄存器SRC中表示的寄存器中值与目的操作寄存器DST中表示的寄存器中值位异或
                        (pin.AM_REG,pin.AM_REG):[
                                pin.DST_R | pin.A_IN,
                                pin.SRC_R | pin.B_IN,
                                pin.ALU_XOR | pin.ALU_EN | pin.DST_W
                        ],
                },

        },
        1:{
                INC:{
                        #01000001,41
                        #INC B,寄存器中值加一
                        pin.AM_REG:[
                             pin.DST_R | pin.A_IN,
                             pin.ALU_INC | pin.ALU_EN | pin.DST_W   
                        ]
                },
                DEC:{
                        #01000101,45
                        #DEC B,寄存器中值减一
                        pin.AM_REG:[
                             pin.DST_R | pin.A_IN,
                             pin.ALU_DEC | pin.ALU_EN | pin.DST_W   
                        ]
                },
                NOT:{
                        #01001000,48
                        #NOT B,寄存器中值位取反
                        pin.AM_REG:[
                             pin.DST_R | pin.A_IN,
                             pin.ALU_NOT | pin.ALU_EN | pin.DST_W   
                        ]
                },

        },
        0:{
                HLT:[
                        pin.HLT
                ],
                NOP:[
                        pin.PCC_RD
                ]

        }
}
#print(MOV)