// push argument 1
@1
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
// pop pointer 1
@1
D=A
@THIS
D=D+A
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
// push constant 0
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop that 0
@0
D=A
@THAT
D=D+M
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// pop that 1
@1
D=A
@THAT
D=D+M
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
// push argument 0
@0
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 2
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
A=M-1
D=M
A=A-1
M=M-D
@SP
D=M-1
M=D
// pop argument 0
@0
D=A
@ARG
D=D+M
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
// label MAIN_LOOP_START
(MAIN_LOOP_START)
// push argument 0
@0
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
// if-goto COMPUTE_ELEMENT
@SP
A=M-1
D=M
@SP
M=M-1
@COMPUTE_ELEMENT
D;JNE
// goto END_PROGRAM
@END_PROGRAM
0;JMP
// label COMPUTE_ELEMENT
(COMPUTE_ELEMENT)
// push that 0
@0
D=A
@THAT
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
// push that 1
@1
D=A
@THAT
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
A=M-1
D=M
A=A-1
M=M+D
@SP
D=M-1
M=D
// pop that 2
@2
D=A
@THAT
D=D+M
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
// push pointer 1
@1
D=A
@THIS
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
A=M-1
D=M
A=A-1
M=M+D
@SP
D=M-1
M=D
// pop pointer 1
@1
D=A
@THIS
D=D+A
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
// push argument 0
@0
D=A
@ARG
A=D+M
D=M
@SP
A=M
M=D
@SP
M=M+1
// push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
A=M-1
D=M
A=A-1
M=M-D
@SP
D=M-1
M=D
// pop argument 0
@0
D=A
@ARG
D=D+M
@R13
M=D
@SP
A=M-1
D=M
@R13
A=M
M=D
@SP
M=M-1
// goto MAIN_LOOP_START
@MAIN_LOOP_START
0;JMP
// label END_PROGRAM
(END_PROGRAM)
(INFINITE)
@INFINITE
0;JMP
