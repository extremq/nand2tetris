// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.
    @2
    M=0
(REPEAT)
    @0
    D=M // Store R0 in D
    
    @END
    D;JEQ // If R0 = 0 jump to END

    @0
    M=M-1 // Subtract 1 from R0
    
    @1
    D = M // Store R1 in D
    @2
    M = M + D // Add R1 to R2

    @REPEAT
    0;JMP
(END)