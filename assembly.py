import pin

FETCH=[pin.PC_OUT | pin.MAR_IN ,
        pin.MC_OUT | pin.IR_IN | pin.PC_INC,
        pin.PC_OUT | pin.MAR_IN ,
        pin.MC_OUT | pin.DST_IN | pin.PC_INC,
        pin.PC_OUT | pin.MAR_IN ,
        pin.MC_OUT | pin.SRC_IN | pin.PC_INC,
]

MOV=0|(1<<7)
ADD=(1<<4)|(1<<7)
HLT=0x3f
NOP=0

INSTRUCTIONS={
        2:{
                MOV:{
                        #MOV A 5,前面寄存器，后面立即数
                        #需要将原操作数寄存器SRC中值移到目的操作寄存器DST中表示的寄存器里
                        (pin.AM_REG,pin.AM_INS):[
                                pin.DST_W | pin.SRC_OUT
                        ]
                }
        },
        1:{},
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