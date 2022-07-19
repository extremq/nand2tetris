from ast import parse
import code
from parse import Parser
import sys
import literals
import codeWriter

if len(sys.argv) == 1:
    print("Specify a file path: python VM.py PATH")
    exit()
else:
    file_path = sys.argv[1]
    parser = Parser(file_path)

output = ""
if parser.has_init:
    output += codeWriter.writeInit()

while parser.hasMoreLines():
    line = parser.getLine()
    cmd = parser.commandType()
    output += "// " + " ".join(line) + "\n" # Put a comment with the vm line

    # Choose which kind of command this is
    if cmd in [literals.C_PUSH, literals.C_POP]:
        output += codeWriter.writePushPop(cmd, parser.arg1(), parser.arg2())
    elif cmd == literals.C_ARITHMETIC:
        output += codeWriter.writeArithmetic(parser.arg1())
    elif cmd == literals.C_LABEL:
        output += codeWriter.writeLabel(parser.arg1())
    elif cmd == literals.C_GOTO:
        output += codeWriter.writeGoto(parser.arg1())
    elif cmd == literals.C_IF:
        output += codeWriter.writeIf(parser.arg1())
    elif cmd == literals.C_FUNCTION:
        output += codeWriter.writeFunction(parser.arg1(), parser.arg2())
    elif cmd == literals.C_CALL:
        output += codeWriter.writeCall(parser.arg1(), parser.arg2())
    elif cmd == literals.C_RETURN:
        output += codeWriter.writeReturn()
    parser.advance()

output += codeWriter.writeEnd()

file = open(file_path + "/output.asm", 'w')
file.write(output)
file.close()