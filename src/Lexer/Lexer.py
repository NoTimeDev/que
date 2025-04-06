from re import S
from .TokenKind import *
from ..Error import *

class Lexer:
    def __init__(self, Sourecode: str, errcls: Error):
        self.Sourecode = Sourecode
        self.errcls: Error = errcls

    def Lex(self) -> list[Token]:
        Tokens: list[Token] = []

        def Add(Val: str, Kind: TokenKind, line: int, start: int, end: int):
            Tokens.append(Token(Val, Kind, line, start, end))

        pos: int = 0
        line: int = 1
        col: int = 1
        
        while pos < len(self.Sourecode):
            c_char = self.Sourecode[pos]
            if c_char in ["\t", ' ']:
                pos+=1
                col+=1
            elif c_char == '\n':
                line+=1
                pos+=1
                col = 1
            elif c_char == '[':
                Add('[', TokenKind.open_bracket, line, col, col)
                pos+=1; col+=1
            elif c_char == ']':
                Add(']', TokenKind.close_bracket, line, col, col)
                pos+=1; col+=1
            elif c_char == '(':
                Add('(', TokenKind.open_paren, line, col, col)
                pos+=1; col+=1
            elif c_char == ')':
                Add(')', TokenKind.close_paren, line, col, col)
                pos+=1; col+=1
            elif c_char == '{':
                Add('{', TokenKind.open_brace, line, col, col)
                pos+=1; col+=1
            elif c_char == '}':
                Add('}', TokenKind.close_brace, line, col, col)
                pos+=1; col+=1
            elif c_char == ',': 
                Add(',', TokenKind.comma, line, col, col)
                pos+=1; col+=1
            elif c_char == '*': 
                Add('*', TokenKind.pointer, line, col, col)
                pos+=1; col+=1
            elif c_char == '=': 
                Add('=', TokenKind.equal, line, col, col)
                pos+=1; col+=1
           
            elif c_char == '#':
                com: str = ""
                while pos < len(self.Sourecode) and self.Sourecode[pos] != '\n':
                    com+=self.Sourecode[pos]
                    pos+=1 
                    col+=1 

                Add(com, TokenKind.comment, line, col, col)
            elif c_char == '-':
                if self.Sourecode[pos + 1].isdigit():
                    number: str = "-"
                    start: int = col
                    pos+=1
                    col+=1

                    dotcount: int = 0
                    while pos < len(self.Sourecode) and self.Sourecode[pos].isdigit() or self.Sourecode[pos] == '.':
                        if dotcount > 1:
                            self.errcls.throwerr(line, col, col, "float contains multiple decimal points")
                            break
                        if self.Sourecode[pos] == ".":
                            dotcount+=1
                        number+=self.Sourecode[pos]
                        pos+=1
                        col+=1

                    if dotcount == 0:
                        Add(number, TokenKind.int_const, line, start, col)
                    else:
                        Add(number, TokenKind.float_const, line, start, col)
                elif self.Sourecode[pos + 1] == '>':
                    Add('->', TokenKind.arrow, line, col, col+1)
                    pos+=2; col+=2
                else:
                    self.errcls.throwerr(line, col, col, f"expected a number or '>'")
                    pos+=1; col+=1
            elif c_char == '"':
                start: int = col

                pos+=1
                col+=1

                string: str = ""
                
                while pos < len(self.Sourecode) and self.Sourecode[pos] != '"':
                    if self.Sourecode[pos] == '\n':
                        self.errcls.throwerr(line, col, col, "unterminated string (\")")  
                        break
                    string+=self.Sourecode[pos]
                    col+=1
                    pos+=1


                pos+=1
                col+=1
                
                Add(string, TokenKind.str_const, line, start, col)
            elif c_char.isdigit():
                number: str = ""
                start: int = col

                dotcount: int = 0
                while pos < len(self.Sourecode) and self.Sourecode[pos].isdigit() or self.Sourecode[pos] == '.':
                    if dotcount > 1:
                        self.errcls.throwerr(line, col, col, "float contains multiple decimal points")
                        break
                    if self.Sourecode[pos] == ".":
                        dotcount+=1
                    number+=self.Sourecode[pos]
                    pos+=1  
                    col+=1

                if dotcount == 0:
                    Add(number, TokenKind.int_const, line, start, col)
                else:
                    Add(number, TokenKind.float_const, line, start, col)
            elif c_char == '!':
                start: int = col 
                meta: str = "!"

                pos+=1
                col+=1

                while pos < len(self.Sourecode) and self.Sourecode[pos].isalnum() or self.Sourecode[pos] in ['.', '_', '-']:
                    meta+=self.Sourecode[pos]
                    pos+=1
                    col+=1

                Add(meta, TokenKind.meta_info, line, start, col)
            elif c_char.isalpha() or c_char == "_":
                alphas: dict[str, TokenKind] = {
                    "def" : TokenKind.def_inst,
                    "include" : TokenKind.include_inst,
                    "localconst" : TokenKind.loacl_const,
                    "load" : TokenKind.load_inst,
                    "loadptr" : TokenKind.loadptr_inst,
                    "ret" : TokenKind.ret_inst,
                     
                    "add" : TokenKind.add_inst, 
                    "sub" : TokenKind.sub_inst,

                    "idiv" : TokenKind.idiv_inst,
                    "div" : TokenKind.div_inst,

                    "imul" : TokenKind.imul_inst,
                    "mul" : TokenKind.mul_inst,
                    
                    "imod" : TokenKind.imod_inst,
                    "mod" : TokenKind.mod_inst,
                    
                    "trunc" : TokenKind.trunc_inst, 
                    
                    "iext" : TokenKind.iext_inst, 
                    "ext" : TokenKind.ext_inst,
                    
                    "fadd" : TokenKind.fadd_inst,
                    "fsub" : TokenKind.fsub_inst,
                    "fdiv" : TokenKind.fdiv_inst,
                    "fmul" : TokenKind.fmul_inst,
                    
                    "fext" : TokenKind.fext_inst,
                    "ftrunc" : TokenKind.ftrunc_inst,

                    "fti" : TokenKind.fti_inst,
                    "itf" : TokenKind.itf_inst,
                    
                    "alloc" : TokenKind.alloc_inst,
                    "store" : TokenKind.store_inst,
                    
                    "getptr" : TokenKind.getptr_inst,
                    "geteptr" : TokenKind.geteptr_inst,
                    "getfptr" : TokenKind.getfptr_inst,
                    
                    "global" : TokenKind.global_inst,
                    "const" : TokenKind.const_inst,
                    "castptr" : TokenKind.castptr_inst,
                    "private" : TokenKind.private_inst,
                    "extern" : TokenKind.extern_inst,
                    "call" : TokenKind.call_inst,

                    "if" : TokenKind.if_inst,
                    "cmp" : TokenKind.cmp_inst,
                    "icmp" : TokenKind.icmp_inst,
                    "fcmp" : TokenKind.fcmp_inst,

                    "goto" : TokenKind.goto_inst,
                    "le" : TokenKind.cmp,
                    "leoe" : TokenKind.cmp,
                    "gt" : TokenKind.cmp,
                    "gtoe" : TokenKind.cmp,
                    "eq" : TokenKind.cmp,
                    "ne" : TokenKind.cmp,


                    "ptr" : TokenKind.type_,
                    "f64" : TokenKind.type_,
                    "f32" : TokenKind.type_,
                    "i64" : TokenKind.type_,
                    "i32" : TokenKind.type_,
                    "i16" : TokenKind.type_,
                    "i8" : TokenKind.type_,
                    "void" : TokenKind.type_,
                }

                start: int = col
                alpha: str = ""
                
                while pos < len(self.Sourecode) and self.Sourecode[pos].isalnum() or self.Sourecode[pos] in ['_', '.']:
                    alpha+=self.Sourecode[pos]
                    pos+=1 
                    col+=1 
                   
                if self.Sourecode[pos] == ":":
                    pos+=1; col+=1 
                    Add(alpha, TokenKind.label_ident, line, start, col) 
                elif alpha not in list(alphas.keys()):
                    self.errcls.throwerr(line, start, col, f"no such instruction {alpha}")
                else:
                    Add(alpha, alphas[alpha], line, start, col)
            elif c_char in '$':
                start: int = col 
                treg: str = "$"

                pos+=1
                col+=1

                while pos < len(self.Sourecode) and self.Sourecode[pos].isalnum() or self.Sourecode[pos] in ['.', '_', '-', ":"]:
                    treg+=self.Sourecode[pos]
                    pos+=1
                    col+=1

                Add(treg, TokenKind.local_ident, line, start, col)
            elif c_char in '@':
                start: int = col 
                treg: str = "@"

                pos+=1
                col+=1

                while pos < len(self.Sourecode) and self.Sourecode[pos].isalnum() or self.Sourecode[pos] in ['.', '_', ':']:
                    treg+=self.Sourecode[pos]
                    pos+=1
                    col+=1

                Add(treg, TokenKind.global_ident, line, start, col)
            else:   
                self.errcls.throwerr(line, col, col, f"unrecogonised token '{c_char}'")
                pos+=1; col+=1

        if len(Tokens) != 0:
            Add("eof", TokenKind.eof, Tokens[-1].Line, Tokens[-1].Start + 1, Tokens[-1].End + 1)                                                                            
        return Tokens
