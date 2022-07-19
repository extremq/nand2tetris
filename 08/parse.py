import literals
import os

class Parser:
    def __init__(self, folder_path):
        # Opens the input file/stream and gets ready to parse it.
        self.folder_path = folder_path
        try:
            self.all_files = os.listdir(folder_path)
        except:
            print("Cannot open folder or folder doesn't exist.")
            exit()

        self.raw_files = []
        for file in self.all_files:
            if file.endswith(".vm"):
                # Get the contents of all .vm files
                handle = open(folder_path + file)
                self.raw_files.append(handle.read())
                handle.close()

        # Determine how many statics there are and offset them
        # and prepare for parsing
        self.lines = list()
        self.global_statics = 0
        self.has_init = False
        for file in self.raw_files:
            file = file.splitlines()

            local_statics = 0 
            has_statics = False
            for line in file:
                # Remove empty lines and comments
                if line.startswith("//") or line == "":
                    continue
                
                # Remove line comments after instructions
                for i in range(len(line)):
                    if line[i:].startswith("//"):
                        line = line[:i]

                # Legacy support
                if "function Sys.init" in line:
                    self.has_init = True
                line = line.split()
                if line[0] in ["pop", "push"] and line[1] == "static":
                    has_statics = True
                    local_statics = max(local_statics, int(line[2]))
                    line[2] = str(int(line[2]) + self.global_statics)

                self.lines.append(line)

            if has_statics:
                self.global_statics += local_statics + 1

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

        if command == "push":
            return literals.C_PUSH
        elif command == "pop":
            return literals.C_POP
        elif command in ["add", "sub", "neg", "eq", "lt", "and", "or", "not"]:
            return literals.C_ARITHMETIC
        elif command == "label":
            return literals.C_LABEL
        elif command == "goto":
            return literals.C_GOTO
        elif command == "if-goto":
            return literals.C_IF
        elif command == "function":
            return literals.C_FUNCTION
        elif command == "return":
            return literals.C_RETURN
        elif command == "call":
            return literals.C_CALL
    
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