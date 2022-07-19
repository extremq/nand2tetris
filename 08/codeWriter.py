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
        output += "@SP\n" + "M=M+1\n" # Increment SP
    elif cmd == literals.C_POP:
        output = "@" + str(index) + "\n" + "D=A\n" # Get index
        if segment in ["temp", "static", "pointer"]:
            output += "@" + literals.words[segment] + "\n" + "D=D+A\n" # Compute address
        else:
            output += "@" + literals.words[segment] + "\n" + "D=D+M\n" # Compute address
        output += "@R13\n" + "M=D\n" # Store the computed address for later 
        output += "@SP\n" + "A=M-1\n" + "D=M\n" # Get top
        output += "@R13\n" + "A=M\n" + "M=D\n" # Use the computed address
        output += "@SP\n" + "M=M-1\n" # Decrement SP
    return output

def writeLabel(label):
    # Writes assembly code that affects the label command
    return "(" + label + ")\n"

def writeGoto(label):
    # Writes assembly code that affects the goto command
    return "@" + label + "\n" + "0;JMP\n"

def writeIf(label):
    # Writes assembly code that affects the if-goto command
    output = "@SP\n" + "A=M-1\n" + "D=M\n" # Get the top of the stack and place it in D
    output += "@SP\n" + "M=M-1\n" # Pop the stack
    output += "@" + label + "\n" # Set the label
    output += "D;JNE\n" # Check if expression is not equal to 0
    return output

def writeFunction(name, vars):
    # Writes assembly code that generates a function
    output = "(" + name + ")\n"
    for i in range(int(vars)):
        # Initialize the locals to 0
        output += writePushPop(literals.C_PUSH, "constant", "0")
    return output

def writeCall(name, args):
    # Writes assembly code that generates a call to a function
    global label_count
    label = name + "$" + str(label_count)
    label_count += 1
    # Save the return address too
    output = "@" + label + "\n"
    output += "D=A\n" + "@SP\n" + "A=M\n" + "M=D\n" + "@SP\n" + "M=M+1\n"
    # Push LCL, ARG, THIS, THAT onto the stack
    output += "@LCL\n" + "D=M\n" + "@SP\n" + "A=M\n" + "M=D\n" + "@SP\n" + "M=M+1\n" 
    output += "@ARG\n" + "D=M\n" + "@SP\n" + "A=M\n" + "M=D\n" + "@SP\n" + "M=M+1\n" 
    output += "@THIS\n" + "D=M\n" + "@SP\n" + "A=M\n" + "M=D\n" + "@SP\n" + "M=M+1\n" 
    output += "@THAT\n" + "D=M\n" + "@SP\n" + "A=M\n" + "M=D\n" + "@SP\n" + "M=M+1\n"
    output += "@SP\n" + "D=M\n" # Get stack pos  (D = SP)
    output += "@LCL\n" + "M=D\n" # LCL = SP
    output += "@" + str(5 + int(args)) + "\n" + "D=D-A\n" # SP - (5 + nArgs)
    output += "@ARG\n" + "M=D\n" # ARG = SP - 5 - nArgs
    output += "@" + name + "\n" + "0;JMP\n"
    output += "(" + label + ")\n"
    return output

def writeReturn():
    # Writes assembly code that generates a return
    output = "@LCL\n" + "D=M\n" + "@R13\n" + "M=D\n" # Store LCL
    output += "A=D-1\n" + "A=A-1\n" + "A=A-1\n" + "A=A-1\n" + "A=A-1\n" + "D=M\n" # Return address
    output += "@R14\n" + "M=D\n" # Store it
    # Reposition the return value (Reusing memory, popping)
    output += "@SP\n" + "A=M-1\n" + "D=M\n"
    output += "@ARG\n" + "A=M\n" + "M=D\n" # Place it on *ARG
    # Reposition SP
    output += "D=A+1\n" + "@SP\n" + "M=D\n"
    # Restore other labels
    output += "@R13\n" + "D=M\n" # D = old LCL
    output += "A=D-1\n" + "D=M\n"
    output += "@THAT\n" + "M=D\n" # THAT = *(LCL - 1)
    output += "@R13\n" + "D=M\n" # D = old LCL
    output += "A=D-1\n" + "A=A-1\n" + "D=M\n"
    output += "@THIS\n" + "M=D\n" # THIS = *(LCL - 2)
    output += "@R13\n" + "D=M\n" # D = old LCL
    output += "A=D-1\n" + "A=A-1\n" + "A=A-1\n" + "D=M\n"
    output += "@ARG\n" + "M=D\n" # ARG = *(LCL - 3)
    output += "@R13\n" + "D=M\n" # D = old LCL
    output += "A=D-1\n" + "A=A-1\n" + "A=A-1\n" + "A=A-1\n" + "D=M\n"
    output += "@LCL\n" + "M=D\n" # LCL = *(LCL - 4)
    output += "@R14\n" + "A=M\n" # Get the return address back
    output += "0;JMP\n" # And jump
    return output

def writeEnd():
    # Writes infinite loop
    return "(INFINITE)\n" + "@INFINITE\n" + "0;JMP\n"

def writeInit():
    # Writes the jump necessary for Sys.init
    return "@256\n" + "D=A\n" + "@SP\n" + "M=D\n" + writeCall("Sys.init", "0")
