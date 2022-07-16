import literals

label_count = 1

def writeArithmetic(cmd):
    # SP is not affected here.
    global label_count
    output = ""
    if cmd in ["not", "neg"]:
        output = "@SP\n" + "A=M-1\n"
        if cmd == "not":
            output += "D=!M\n"
        elif cmd == "neg":
            output += "D=-M\n"
        output += "M=D\n"
    else:
        # SP must end up lower with one unit
        if cmd in ["add", "sub", "and", "or"]:
            # D is y and M is x
            # Go twice lower than the SP
            output = "@SP\n" + "A=M-1\n" + "D=M\n" + "A=A-1\n"
            if cmd == "add":
                output += "M=M+D\n"
            elif cmd == "sub":
                output += "M=M-D\n"
            elif cmd == "and":
                output += "M=M&D\n"
            elif cmd == "or":
                output += "M=M|D\n"
        elif cmd in ["eq", "lt", "gt"]:
            output = "@SP\n" + "A=M-1\n" + "D=A-1\n" # Go twice lower again
            output += "@R13\n" + "M=D\n" # Store the address in R13 
            output += "@SP\n" + "A=M-1\n" + "D=M\n" + "A=A-1\n" # Get y in D and x in M
            output += "D=M-D\n"
            output += "@LABEL" + str(label_count) + "\n"
            if cmd == "eq":
                output += "D;JEQ\n"
            elif cmd == "lt":
                output += "D;JLT\n"
            else:
                output += "D;JGT\n"
            output += "D=0\n"
            output += "@LABEL" + str(label_count + 1) + "\n"
            output += "0;JMP\n"
            output += "(LABEL" + str(label_count) + ")\n"
            output += "D=-1\n"
            output += "(LABEL" + str(label_count + 1) + ")\n"
            output += "@R13\n" + "A=M\n" + "M=D\n"
            label_count = label_count + 2
            
        # Decrement SP
        output += "@SP\n" + "D=M-1\n" + "M=D\n"
    return output
        
def writePushPop(cmd, segment, index):
    if cmd == literals.C_PUSH:
        output = "@" + str(index) + "\n" + "D=A\n" # Store index in D
        if segment != "constant": # If not constant, then store segment[index] in D
            if segment in ["temp", "static", "pointer"]:
                output += "@" + literals.words[segment] + "\n" + "A=D+A\n" + "D=M\n"
            else:
                output += "@" + literals.words[segment] + "\n" + "A=D+M\n" + "D=M\n"
        output += "@SP\n" + "A=M\n" + "M=D\n" # Change value of stack[SP]
        output += "@SP\n" + "D=M+1\n" + "M=D\n" # Increment SP
    elif cmd == literals.C_POP:
        output = "@" + str(index) + "\n" + "D=A\n" # Get index
        if segment in ["temp", "static", "pointer"]:
            output += "@" + literals.words[segment] + "\n" + "D=D+A\n" # Compute address
        else:
            output += "@" + literals.words[segment] + "\n" + "D=D+M\n" # Compute address
        output += "@R13\n" + "M=D\n" # Store the computed address for later 
        output += "@SP\n" + "A=M-1\n" + "D=M\n" # Get top
        output += "@R13\n" + "A=M\n" + "M=D\n" # Use the computed address
        output += "@SP\n" + "D=M-1\n" + "M=D\n" # Decrement SP
    return output