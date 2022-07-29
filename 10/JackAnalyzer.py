import sys
from JackTokenizer import Tokenizer


if len(sys.argv) == 1:
    print("Specify a folder path: python JackAnalyzer.py PATH")
    exit()

folder_path = sys.argv[1]

# Create the tokenizer and generate the XML file.
tokenizer = Tokenizer(folder_path)
tokenizer.process_files()