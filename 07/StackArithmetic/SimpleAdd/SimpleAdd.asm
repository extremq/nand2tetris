// push constant 7
@7
D=A
@SP
A=M
M=D
@SP
D=M+1
M=D
// push constant 8
@8
D=A
@SP
A=M
M=D
@SP
D=M+1
M=D
// add
@SP
A=M-1
D=M
A=A-1
M=M+D
@SP
D=M-1
M=D
