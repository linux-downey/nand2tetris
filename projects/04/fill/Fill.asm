// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(KLOOP)
@24576
D=M
@UNPRESS
D,JEQ
@PRESS
D,JGT


(PRESS)
@2
M=-1
@SCREEN
0,JEQ

(UNPRESS)
@2
M=0
@SCREEN
0,JEQ


(SCREEN)
@16384
D=A
@0
M=D

@24576
D=A
@1
M=D

(SLOOP)
@2
D=M
@0
A=M
M=D

@0
D=M
D=D+1
M=D

@1
D=D-M

@SLOOP
D;JLT

@KLOOP
0;JEQ





