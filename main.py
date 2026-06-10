import sys
from lexer import Lexer
from parser import Parser

def run_parser(file_path):
    try:
        with open(file_path, 'r') as f:
            code = f.read()
        
        print(f"\n--- Processing File: {file_path} ---")
        lexer = Lexer(code)
        tokens = lexer.tokens
        
        parser = Parser(tokens)
        parser.parse_program()
        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except SyntaxError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_parser(sys.argv[1])
    else:
        # If no arguments, run all tests
        test_files = [
            'test1_valid.txt',
            'test2_error_decl.txt',
            'test3_error_brace.txt',
            'test4_error_assign.txt',
            'test5_error_func.txt'
        ]
        for tf in test_files:
            run_parser(tf)
