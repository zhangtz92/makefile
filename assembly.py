import pin

FETCH=[pin.PC_OUT | pin.MAR_IN ,
        pin.MC_OUT | pin.IR_IN | pin.PC_INC,
        pin.PC_OUT | pin.MAR_IN ,
        pin.MC_OUT | pin.DST_IN | pin.PC_INC,
        pin.PC_OUT | pin.MAR_IN ,
        pin.MC_OUT | pin.SRC_IN | pin.PC_INC,
]