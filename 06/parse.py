# Encapsulates access to the input code. Reads an assembly language command,
# parses it, and provides convenient access to the command’s components
# (fields and symbols). In addition, removes all white space and comments.

class Parser():
    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2

    def __init__(self, file_path):
        # Opens the input file/stream and gets ready to parse it.
        self.file_path = file_path

        try:
            file = open(file_path)
        except:
            print("Cannot open the file.")

        # Get the whole content of the file
        self.raw_content = file.read()
        file.close()

        # Prepare for parsing
        self.lines = self.raw_content.splitlines()

        temp = list()
        for line in self.lines:
            # Remove empty lines and comments
            if line.startswith("//") or line == "":
                continue

            # Take out the spaces
            line = line.replace(" ", "")

            # Remove line comments after instructions
            for i in range(len(line)):
                if line[i:].startswith("//"):
                    line = line[:i]

            temp.append(line)

        # Cleaned instructions remain.
        self.lines = temp

        # Instruction counter
        self.counter = 0

        # Dictionary of symbols
        self.symbols = {
            "SP": 0x0,
            "LCL": 0x1,
            "ARG": 0x2,
            "THIS": 0x3,
            "THAT": 0x4,
            "SCREEN": 0x4000,
            "KBD": 0x6000,
            "R0": 0x0,
            "R1": 0x1,
            "R2": 0x2,
            "R3": 0x3,
            "R4": 0x4,
            "R5": 0x5,
            "R6": 0x6,
            "R7": 0x7,
            "R8": 0x8,
            "R9": 0x9,
            "R10": 0xa,
            "R11": 0xb,
            "R12": 0xc,
            "R13": 0xd,
            "R14": 0xe,
            "R15": 0xf
        }

        self.jump_dict = {
            "000": "000",
            "JGT": "001",
            "JEQ": "010",
            "JGE": "011",
            "JLT": "100",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111"
        }
    
        self.dest_dict = {
            "000": "000",
            "M": "001",
            "D": "010",
            "MD": "011",
            "A": "100",
            "AM": "101",
            "AD": "110",
            "AMD": "111",
        }

        self.comp_dict = {
            "0"  : "101010",
            "1"  : "111111",
            "-1" : "111010",
            "D"  : "001100",
            "A"  : "110000",
            "!D" : "001101",
            "!A" : "110001",
            "-D" : "001111",
            "-A" : "110011",
            "D+1": "011111",
            "A+1": "110111",
            "D-1": "001110",
            "A-1": "110010",
            "D+A": "000010",
            "A+D": "000010",
            "D-A": "010011",
            "A-D": "000111",
            "D&A": "000000",
            "A&D": "000000",
            "D|A": "010101",
            "A|D": "010101",
            "M"  : "110000",
            "!M" : "110001",
            "-M" : "110011",
            "M+1": "110111",
            "1+M": "110111",
            "M-1": "110010",
            "D+M": "000010",
            "M+D": "000010",
            "D-M": "010011",
            "M-D": "000111",
            "D&M": "000000",
            "M&D": "000000",
            "D|M": "010101",
            "M|D": "010101"
        }

        # Max symbol value
        self.max_symbol = 16

    def addSymbol(self, alias, value=None):
        # Symbols are read only
        if value is not None:
            # Only for labels
            self.symbols.update({alias: value})

        elif alias not in self.symbols:
            # Only for A-commands
            self.symbols[alias] = self.max_symbol
            self.max_symbol = self.max_symbol + 1

        return self.symbols[alias]

    def hasMoreCommands(self):
        # Returns true if there are more commands in the input?
        return self.counter + 1 <= len(self.lines)

    def replaceLine(self, string):
        self.lines[self.counter] = string

    def getLine(self):
        return self.lines[self.counter]

    def deleteLine(self):
        self.lines.pop(self.counter)

    def advance(self):
        # Reads the next command from the input and makes it the current command.
        # Should be called only if hasMoreCommands() is true.
        # Initially there is no current command.
        if self.hasMoreCommands():
            self.counter = self.counter + 1

    def commandType(self):
        # Returns the type of the current command.
        first_char = self.lines[self.counter][0]

        if first_char == "@":
            return self.A_COMMAND
        elif first_char == "(":
            return self.L_COMMAND
        else:
            return self.C_COMMAND
            
    def dest(self, value):
        # Returns the dest mnemonic.
        return self.dest_dict[value]


    def comp(self, value):
        # Returns the comp mnemonic.
        if value not in self.comp_dict:
            print("Invalid line %d" % (self.counter))
        else:
            return self.comp_dict[value]

    def jump(self, value):
        # Returns the jump mnemonic.
        return self.jump_dict[value]
