// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

//set r3 = r1,use r3 as a temperaty counter.
@1
D=M
@2
M=0
@3
M=D

(LOOP)
	@3
	D=M
	@END
	D,JEQ   

	@0
	D=M     //put r0 -> D
	@2
	M=M+D   //r2 = r2 + r0
	@3
	M=M-1   //r3(count) = r3 -1
	
	@LOOP
	0,JEQ
(END)


