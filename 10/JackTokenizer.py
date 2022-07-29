import os

class Tokenizer:
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
            if file.endswith(".jack"):
                # Get the contents of all .jack files
                handle = open(folder_path + file)
                self.raw_files.append(handle.read())
                handle.close()

        # Keywords
        self.keywords = [
            'class',
            'constructor',
            'function',
            'method',
            'field',
            'static',
            'var',
            'int',
            'char',
            'boolean',
            'void',
            'true',
            'false',
            'null',
            'this',
            'let',
            'do',
            'if',
            'else',
            'while',
            'return'
        ]

        # Symbols
        self.symbols = [
            '{',
            '}',
            '(',
            ')',
            '[',
            ']',
            '.',
            ',',
            ';',
            '+',
            '-',
            '*',
            '/',
            '&',
            '|',
            '<',
            '>',
            '=',
            '~'
        ]

        self.file_tokens = {}

    def process_files(self):
        # Take each file in order and generate an xml file for it
        file_index = 0
        for file in self.raw_files:
            in_comment = False
            in_multi_comment = False
            in_string = False
            token = "" # Current token

            file_index = file_index + 1
            self.file_tokens[file_index] = [] # Current list of tokens

            for i in range(len(file)):
                # Check for comments
                if file[i] == '/' and file[i + 1] == '/':
                    in_comment = True
                    continue

                if file[i] == '/' and file[i + 1] == '*':
                    in_multi_comment = True
                    continue
                
                if in_comment:
                    if file[i] == '\n':
                        in_comment = False
                    
                    continue

                if in_multi_comment:
                    if file[i - 1] == '*' and file[i] == '/':
                        in_multi_comment = False
                    
                    continue

                # This may start or end a string
                if file[i] == '"':
                    in_string = not in_string

                    # Separate the tokens
                    # Signal that it's a string by adding a "
                    if not in_string:
                        self.process_token('"' + token, file_index)
                    else:
                        self.process_token(token, file_index)
                    token = ""

                    continue

                # Go through the file, character by character
                if not in_string and (file[i] == ' ' or file[i] == '\n' or file[i] == '\t'):
                    self.process_token(token, file_index)
                    token = ""
                else:
                    token += file[i]

            self.generate_xml(file_index)

    def process_token(self, token, file_index):
        if token == "":
            return

        # Check if string
        if token[0] == '"':
            self.add_token(token[1:], file_index, "stringConstant")
            token = token[1:]
            return
        
        while token != '':
            # Always check the first character
            if token[0] in self.symbols:
                temp_token = token[0]

                # Replace special XML chars
                if temp_token == '<':
                    temp_token = '&lt;'
                elif temp_token == '>':
                    temp_token = '&gt;'
                elif temp_token == '"':
                    temp_token = '&quot;'
                elif temp_token == '&':
                    temp_token = '&amp;'

                self.add_token(temp_token, file_index, "symbol")
                token = token[1:]
                continue
            # Check if this is a integer constant
            elif token[0].isdigit():
                end = 1
                encountered = False

                # Two cases:
                # 12345
                # 12345somethingelse
                # I check where the digits end in order to pass the token
                for i in range(1, len(token)):
                    if not token[i].isdigit():
                        end = i
                        encountered = True
                        break

                if not encountered:
                    end = len(token)

                self.add_token(token[:end], file_index, "integerConstant")
                token = token[end:]
                continue
            else: 
                end = 1
                encountered = False

                # Same as above
                for i in range(1, len(token)):
                    if token[i] in self.symbols:
                        end = i
                        encountered = True
                        break
                
                if not encountered:
                    end = len(token)

                if token[:end] in self.keywords:
                    self.add_token(token[:end], file_index, "keyword")
                else:
                    self.add_token(token[:end], file_index, "identifier")
                token = token[end:]

    def add_token(self, token, file_index, type):
        self.file_tokens[file_index].append((type, token))

    def generate_xml(self, file_index):
        xml = "<tokens>\n"

        for type, token in self.file_tokens[file_index]:
            xml += f"<{type}> {token} </{type}>\n"

        xml += "</tokens>\n"

        file_name = self.file_tokens[file_index][1][1] # Second pair is always class name
        with open(f"{file_name}T.xml", "w") as handle:
            handle.write(xml)





