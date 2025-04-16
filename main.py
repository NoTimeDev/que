import os
from src.Utils.Utils import * 
from src.Lexer.Lexer import *
from src.Parser.Parser import * 
from src.CodeGen.CodeGen import *
from src.Error import *

import subprocess
import platform     
import json
import sys 
import colorama
colorama.init(autoreset=True)

def main(argv: list[str] = sys.argv, argc: list[str] = len(sys.argv)):
    if(argc == 1):
        printr(f"{BWhite}que:{BRed} fatal error:{Reset} no input files")
        exit(1)

    if not os.path.exists(argv[1]):
        printr(f"{BWhite}que:{BRed} fatal error:{Reset} no such file or directory '{argv[1]}'")
        exit(1)
    else:
        with open(argv[1], 'r') as File: SourceCode: str = File.read()
        SourceCode+='\n'

        ErrorClass: Error = Error(SourceCode, argv[1])
        Lexer_Class: Lexer = Lexer(SourceCode, ErrorClass)   
        LexedTokens: list[Token] = Lexer_Class.Lex()

        if ErrorClass.meterr == True:
            printr(ErrorClass.err)
            exit(1)

        
        if "-plat=win" in argv:
            platform_ = "Windows"
        elif "-plat=linux" in argv:
            platform_ = "Linux"
        else:
            platform_ = platform.system()

        Parser_Class: Parser = Parser(LexedTokens, ErrorClass, platform_)

        try:
            Ast: dict = Parser_Class.Parse()
        except EOFError:
            printr(ErrorClass.err)
            exit(1)
        else:
            if ErrorClass.meterr == True:
                printr(ErrorClass.err)
                exit(1)
        if("-dump" in argv):
            print(json.dumps(Ast, indent=4))

        if "-smac" in argv:
            smac = argv[argv.index('-smac') + 1]
        else:
            smac = ""
        CodeGenClass: CodeGen = CodeGen(Ast, Parser_Class.Meta, platform_, smac)
        Cont = CodeGenClass.Gen()
        
        Name = "out"
        if "-name" in argv:
            Name = argv[argv.index('-name') + 1]
        
        with open(Name + ".asm", "w") as File:
            File.write(Cont)


        if "-plat=win" in argv:
            subprocess.run(["wine", "nasm", Name + ".asm", "-o", Name + ".o","-f", "win64"])      
            subprocess.run(["x86_64-w64-mingw32-ld", Name + ".o", "-o", Name +".exe", '-I"/home/devvy/.wine/drive_c/windows/system32"', "-lkernel32"] + Ast["Meta"]["LinkerFlags"]) 
        else:
            subprocess.run(["nasm", Name + ".asm", "-o", Name + ".o","-f", "elf64"])      
            subprocess.run(["ld", Name + ".o", "-o", Name + ".exe" if platform_ == "Windows" else Name] + Ast["Meta"]["LinkerFlags"])
           
        if "-clean" in argv:
            os.remove(os.path.abspath(f"./{Name}.asm"))
            os.remove(os.path.abspath(f"./{Name}.o"))
if __name__ == '__main__':
    main()
