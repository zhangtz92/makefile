;MOV A,3;

;MOV B,A;

;MOV C,[0x00];

;MOV D,[A];

;MOV [0x1C],0xfc;

;MOV A,3;

;MOV [0x1D],A;

;MOV [0x1E],[A];

;MOV [0x1F],[0x06];
MOV A,0x1d;

MOV B,0x1e;

MOV C,0x1f;

MOV D,0x2f;

MOV [A],0xfc;

MOV [B],C;

MOV [C],[0x03];

MOV [D],[A];

HLT;

