from ast import parse
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
while parser.hasMoreLines():
    line = parser.getLine()
    cmd = parser.commandType()
    output += "// " + " ".join(line) + "\n"
    if cmd in [literals.C_PUSH, literals.C_POP]:
        output += codeWriter.writePushPop(cmd, parser.arg1(), parser.arg2())
    else:
        output += codeWriter.writeArithmetic(parser.arg1())
    parser.advance()

file = open("output.asm", 'w')
file.write(output)
file.close()