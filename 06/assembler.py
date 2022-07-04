from parse import Parser
import sys

if len(sys.argv) == 1:
    print("Specify a file path: python assembler.py PATH")
    exit()
else:
    file_path = sys.argv[1]
    parser = Parser(file_path)

# Determine labels
while parser.hasMoreCommands():
    line = parser.getLine()
    if parser.commandType() == parser.L_COMMAND and not line[1].isdigit():
        # (name)
        symbol = line[1:-1]
        value = parser.addSymbol(symbol, parser.counter)
        parser.deleteLine()
    else:
        parser.advance()

parser.counter = 0 # Start from line 0 

output = "" # Binary output

while parser.hasMoreCommands():
    line = parser.getLine()
    # Replace last symbols
    if parser.commandType() == parser.A_COMMAND and not line[1].isdigit():
        # @name
        symbol = line[1:]
        value = parser.addSymbol(symbol)
        line = "@" + str(value)
        parser.replaceLine(line)

    if parser.commandType() == parser.A_COMMAND:
        binary = format(int(line[1:]), "016b")
    else:
        # Compute the three tags
        jmp = None
        comp = None
        dest = None

        a = "0"

        if line.find(';') != -1:
            # Jump
            # Separate the line and the jump
            jmp = line[line.find(';') + 1:]
            line = line[:line.find(';')]
        else:
            jmp = "000"
        if line.find('=') != -1:
            # Dest
            dest = line[:line.find('=')]
            line = line[line.find('=') + 1:]
        else:
            dest = "000"

        comp = line
        if 'M' in comp: 
            # Check if A is used as an address
            a = "1"

        # Finish it up
        binary = "111" + a + parser.comp(comp) + parser.dest(dest) + parser.jump(jmp)

    parser.advance()
    output = output + binary + '\n'


final = open('output.txt', 'w')
final.write(output)