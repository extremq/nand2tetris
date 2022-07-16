import literals

class Parser:
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

            # Remove line comments after instructions
            for i in range(len(line)):
                if line[i:].startswith("//"):
                    line = line[:i]

            line = line.split()
            temp.append(line)

        # Cleaned instructions remain.
        self.lines = temp

        # Instruction counter
        self.counter = 0;

    def hasMoreLines(self):
        # Returns true if there are remaining lines
        return self.counter + 1 <= len(self.lines)

    def advance(self):
        # Reads the next line and sets it as the current command
        if self.hasMoreLines():
            self.counter = self.counter + 1

    def getLine(self):
        return self.lines[self.counter]

    def commandType(self):
        # Returns a constant representing the type of the
        # current command.
        currentLine = self.getLine()
        command = currentLine[0]

        # TO DO OTHER COMMANDS
        if command == "push":
            return literals.C_PUSH
        elif command == "pop":
            return literals.C_POP
        else:
            return literals.C_ARITHMETIC
    
    def arg1(self):
        # Returns a constant representing the type of the
        # current command.
        currentLine = self.getLine()
        type = self.commandType()

        if type == literals.C_RETURN:
            print("Error, return has no arguments.")
            exit()
        elif type == literals.C_ARITHMETIC:
            return currentLine[0]
        else:
            return currentLine[1]

    def arg2(self):
        # Returns a constant representing the type of the
        # current command.
        currentLine = self.getLine()
        type = self.commandType()

        if type not in [literals.C_PUSH, literals.C_POP, literals.C_FUNCTION, literals.C_CALL]:
            print("Error, command has no second argument.")
            exit()
        else:
            return currentLine[2]