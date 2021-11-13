MOV C,5;
MOV D,0x1B;
ADD C,D;
MOV SS,1;
MOV SP,0x0F;
;PUSH C;
;PUSH D;
;PUSH 0xff;
;PUSH 5;
;POP T1;
;POP T2;
;POP T3;
CAll addition;
MOV T3,C;
HLT;

addition:
    INC C;
    CMP C,0x22;
    JB addition;
    RET;
HLT;

