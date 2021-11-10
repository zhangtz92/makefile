;MOV A,3;

;MOV B,A;

;MOV C,[0x00];

;MOV D,[A];

;MOV [0x1C],0xfc;

;MOV A,3;

;MOV [0x1D],A;

;MOV [0x1E],[A];

;MOV [0x1F],[0x06];
;MOV A,0x1d;

;MOV B,0x1e;

;MOV C,0x1f;

;MOV D,0x2f;

;MOV [A],0xfc;

;MOV [B],C;

;MOV [C],[0x03];

;MOV [D],[A];

;MOV C,3;
;ADD C,5;
;NOP;
;MOV D,15;
;SUB D,C;
;INC D;
;DEC C;
;MOV C,0xa0;
;MOV D,0xaf;
;AND C,D;
;NOT C;
MOV C,5;
MOV D,3;
ADD C,D;

INCEASE:
    INC C;
    JMP INCEASE

HLT;