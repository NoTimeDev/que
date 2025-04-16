from ..Error import Error
from ..Lexer.TokenKind import *
from ..Lexer.Lexer import *
import os 

class Parser:
    def __init__(self, Tokens: list[Token], errcls: Error, plat: str):
        self.Tokens: list[Token] = Tokens
        self.errcls: Error = errcls

        self.plat: str = plat 
        self.include_table: list[str] = []
        
        self.Meta: dict = {
            "Funcs" : {},
            "Structs" : {}
        }
        self.MacTbl: list = []

        self.Ast: dict = {
            "Kind" : "Program",
            "Meta" : {
                "Includes" : self.include_table,
                "Name" : errcls.filename,
                "LinkerFlags" : []
            },
            "Body" : []
        }
        self.Pos: int = 0
        self.isconst: bool = False
        self.isprivate = False
    def Parse(self) -> dict:    
        while self.Pos < len(self.Tokens) and self.CToken().Kind != TokenKind.eof:
            node = self.ParseStmt()
            if node != {"Kind" : "ignore"}:
                self.Ast['Body'].append(node)

        return self.Ast

    def CToken(self):
        return self.Tokens[self.Pos]

    def Advance(self):
        tk = self.CToken()
        if tk.Kind == TokenKind.eof:
            self.errcls.throwerr(tk.Line, tk.Start, tk.End, "unexpected end of file")
            raise EOFError
        self.Pos+=1
        return tk  

    def Expect(self, Kind: TokenKind, val: str):
        tk = self.Advance()
        if tk.Kind != Kind:
            self.errcls.throwerr(tk.Line, tk.Start, tk.End, f"expected '{val}' but recived {tk.Value}")
        
        return tk 


    
    def ParseStmt(self) -> dict:
        if self.CToken().Kind == TokenKind.def_inst:
            return self.ParseFunc()
        elif self.CToken().Kind == TokenKind.getseptr_inst:
            return self.ParseGetSEPtr()
        elif self.CToken().Kind == TokenKind.extern_inst:
            return self.ParseExtern()
        elif self.CToken().Kind == TokenKind.global_inst:
            return self.ParseGlobal()
        elif self.CToken().Kind == TokenKind.getfptr_inst:
            return self.ParseGetFPtr()
        elif self.CToken().Kind == TokenKind.geteptr_inst:
            return self.ParseGetEptr()
        elif self.CToken().Kind == TokenKind.getptr_inst:
            return self.ParseGetPtr()
        elif self.CToken().Kind == TokenKind.cast_inst:
            return self.ParseCast()
        elif self.CToken().Kind == TokenKind.store_inst:
            return self.ParseStore()
        elif self.CToken().Kind == TokenKind.castptr_inst:
            return self.ParseCastPtr()
        elif self.CToken().Kind == TokenKind.alloc_inst:
            return self.ParseAlloc()
        elif self.CToken().Kind == TokenKind.include_inst:
            return self.ParseInc()
        elif self.CToken().Kind in [TokenKind.load_inst, TokenKind.loadptr_inst]:
            return self.ParseLoad()
        elif self.CToken().Kind in [TokenKind.fti_inst, TokenKind.itf_inst]:
            return self.Parsetoint() 
        elif self.CToken().Kind == TokenKind.struct_inst:
            return self.ParseStruct()
        elif self.CToken().Kind == TokenKind.ret_inst:
            return self.ParseRet()
        elif self.CToken().Kind == TokenKind.call_inst:
            return self.ParseCall()
        elif self.CToken().Kind == TokenKind.goto_inst:
            return self.ParseGoto()
        elif self.CToken().Kind == TokenKind.if_inst:
            return self.ParseIf()
        elif self.CToken().Kind == TokenKind.const_inst:
            self.isconst = True
            self.Advance()
            return {"Kind" : "ignore"}
        elif self.CToken().Kind == TokenKind.private_inst:
            self.isprivate = True
            self.Advance()
            return {"Kind" : "ignore"}
        
        else:
            return self.ParseExpr()
    
    def ParseGetSEPtr(self) -> dict:
        tk = self.Advance()
        
        if self.CToken().Kind == TokenKind.pointer:
            self.Advance()
            Point = True 
        else:
            Point = False
        
        Name = self.Expect(TokenKind.local_ident, "a structure variable")
        Struct_Type = self.ParseType()
        self.Expect(TokenKind.comma, ",")
        pos = self.Expect(TokenKind.int_const, "an int")
        Type = self.ParseType()
        self.Expect(TokenKind.arrow, "->")
        ELName = self.Expect(TokenKind.local_ident, "an identifier")

        return {
            "Kind" : "GetSePtr",
            "Point" : Point,
            "Struct_Var" : Name.Value,
            "Pos" : pos.Value,
            "Struct_Type" : Struct_Type,
            "Type" : Type,
            "Name" : ELName.Value,
        }

        self.Advance()
        
    def ParseStruct(self) -> dict:
        self.Advance()
        Name = self.Expect(TokenKind.global_ident, "a global identifier")
        
        self.Expect(TokenKind.open_brace, "{")
        Args = []
        sSize = 0
        while self.CToken().Kind not in [TokenKind.close_brace,TokenKind.eof]:
            #these two cases should not happen but NoTimeDev is a shitty programmer so its 
            #possible it may happen
            if self.CToken().Kind == TokenKind.close_brace: break
            elif self.CToken().Kind == TokenKind.eof: break 
            elif self.CToken().Kind == TokenKind.comma: self.Advance()
            else:   
                Type = self.ParseType()
                self.Expect(TokenKind.arrow, "->")
                Size = self.Expect(TokenKind.int_const, "a int")
                sSize+=int(Size.Value)    
                Args.append({
                    "Type" : Type,
                    "Size" : Size.Value,
                })
        self.Expect(TokenKind.close_brace, '}')

        struct = {
            "Kind" : "Structs",
            "Name" : Name.Value,
            "Elements" : Args,
            "Size" : sSize,
        }
        self.Meta['Structs'].update({Name.Value : struct})
        return struct 

    def ParseGoto(self) -> dict:
        self.Advance()
        if self.CToken().Kind == TokenKind.local_ident:
            Name = self.Advance()
        else:
            Name = self.Expect(TokenKind.global_ident, "a global identifier")

        return {
            "Kind" : "Goto",
            "Name" : Name.Value,
        }
    def ParseIf(self) -> dict:
        self.Advance()
        comp = self.ParseStmt()
        self.Expect(TokenKind.comma, ",")
        if self.CToken().Kind == TokenKind.local_ident:
            Name = self.Advance()
        else:
            Name = self.Expect(TokenKind.global_ident, "a global identifier")
        return {
            "Kind" : "IfStmt",
            "Comp" : comp,
            "Goto" : Name.Value,
        }
    def ParseGetFPtr(self) -> dict:
        self.Advance()

        Name = self.Expect(TokenKind.global_ident, "a func name")
        self.Expect(TokenKind.arrow, "->")
        In = self.Expect(TokenKind.local_ident, "a local identifier")

        return {
            "Kind" : "GetFPtr",
            "Name" : Name.Value,
            "In" : In.Value,
        }  

    def ParseCall(self) -> dict:
        self.Advance()
       
        if self.CToken().Kind == TokenKind.local_ident:
            Name = self.Advance()
        else:
            Name = self.Expect(TokenKind.global_ident, "a global name")
        
        self.Expect(TokenKind.open_paren, "(")
        Args = []
        while self.CToken().Kind not in [TokenKind.close_paren, TokenKind.eof]:
            #these two cases should not happen but NoTimeDev is a shitty programmer so its 
            #possible it may happen
            if self.CToken().Kind == TokenKind.close_paren: break
            elif self.CToken().Kind == TokenKind.eof: break 
            elif self.CToken().Kind == TokenKind.comma: self.Advance()
            else:    
                Args.append({ 
                    "Type" : self.ParseType(),
                    "Value" : self.ParseStmt()
                })

        self.Expect(TokenKind.close_paren, ')')

        self.Expect(TokenKind.comma, ",")
        
        RetType = self.ParseType()
            
        Result = None 
        if self.CToken().Kind == TokenKind.arrow:
            self.Advance()
            Result = self.Expect(TokenKind.local_ident, "a local identifier").Value


        return {
            "Kind" : "Call",
            "Name" : Name.Value, 
            "Args" : Args, 
            "RetType" : RetType,
            "Result" : Result 
        }


    def ParseExtern(self) -> dict:
        self.Advance()
        
        Name = self.Expect(TokenKind.global_ident, "a global name")
        self.Expect(TokenKind.open_paren, "(")
        Types = []
        while self.CToken().Kind not in [TokenKind.close_paren, TokenKind.eof]:
            #these two cases should not happen but NoTimeDev is a shitty programmer so its 
            #possible it may happen
            if self.CToken().Kind == TokenKind.close_paren: break
            elif self.CToken().Kind == TokenKind.eof: break 
            elif self.CToken().Kind == TokenKind.comma: self.Advance()
            else:    
                Types.append(self.ParseType())
        self.Expect(TokenKind.close_paren, ')')

        self.Expect(TokenKind.arrow, "->")
        
        RetType = self.ParseType()
        

        return {
            "Kind" : "Extern",
            "Name" : Name.Value, 
            "Types" : Types, 
            "RetType" : RetType,
        }

    
    def ParseCast(self) -> dict:
        self.Advance()
        Cast = self.Advance() if self.CToken().Kind == TokenKind.global_ident else self.Expect(TokenKind.local_ident, "a local idetifiers name")
        self.Expect(TokenKind.comma, ",")
        Type = self.ParseType()

        return {
            "Kind" : "Cast",
            "Name" : Cast.Value,
            "To" : Type,
        }
    def ParseCastPtr(self) -> dict:
        tk = self.Advance()
        casting = self.Expect(TokenKind.local_ident, "a local identifier")
        self.Expect(TokenKind.comma, ",")
        Type = self.ParseType()

        self.Expect(TokenKind.arrow, "->")
        name  = self.Expect(TokenKind.local_ident, "a local identifier")


        return {
            "Kind" : "PtrCast",
            "To" : Type,
            "Casting" : casting.Value,
            "Name" : name.Value,
        }
    def ParseGlobal(self) -> dict:
        tk = self.Advance()

        Type = self.ParseType()
        self.Expect(TokenKind.comma, ",")
        Size = self.Expect(TokenKind.int_const, "an int")
        self.Expect(TokenKind.arrow, "->")
        Name = self.Expect(TokenKind.global_ident, "a global identifier")

        if self.CToken().Kind == TokenKind.equal:
            self.Advance()
            Val = self.ParseStmt()
        else:
            Val = None 

        cs = self.isconst 
        pr = self.isprivate
        self.isconst = False
        self.isprivate = False
        return {
            "Kind" : "GlobalVar",
            "Type" : Type,
            "Size" : Size.Value,
            "Name" : Name.Value,
            "Value" : Val,
            "Const" : cs,
            "Private" : pr,
        }
    def ParseGetEptr(self) -> dict:
        tk = self.Advance()
        
        if self.CToken().Kind == TokenKind.pointer:
            self.Advance()
            Point = True 
        else:
            Point = False
        
        if self.CToken().Kind == TokenKind.global_ident:
            fr = self.Advance() 
        else:     
            fr = self.Expect(TokenKind.local_ident, "a local or global identifier")
            
    
        ListType = self.ParseType()
        self.Expect(TokenKind.comma, ",")
        pos = self.ParseStmt()
        Type = self.ParseType()
        self.Expect(TokenKind.arrow, "->")
        Name = self.Expect(TokenKind.local_ident, "an identifier")

        return {
            "Kind" : "GetEPtr",
            "Point" : Point,
            "From" : fr.Value,
            "Pos" : pos,
            "ListType" : ListType,
            "Type" : Type,
            "Name" : Name.Value,
        }
    def ParseGetPtr(self) -> dict:
        tk = self.Advance()
        
        if self.CToken().Kind == TokenKind.global_ident:
            to = self.Advance() 
        else:     
            to = self.Expect(TokenKind.local_ident, "a local or global identifier")
            
        self.Expect(TokenKind.comma, ",")
        Type = self.ParseType()
        self.Expect(TokenKind.arrow, "->")

        Name = self.Expect(TokenKind.local_ident, "a local identifier")
        
        return {
            "Kind" : "GetPtrNode",
            "To" : to.Value,
            "Type" : Type,
            "Name" : Name.Value, 
        }

    def ParseAlloc(self) -> dict:
        tk = self.Advance()

        Type = self.ParseType()
        self.Expect(TokenKind.comma, ",")
        Size = self.Expect(TokenKind.int_const, "an int")
        self.Expect(TokenKind.arrow, "->")
        Name = self.Expect(TokenKind.local_ident, "a local identifier")
        
        return {
            "Kind" : "AllocNode",
            "Type" : Type,
            "Size" : str(int(Type['Size']) // 8),
            "Name" : Name.Value,
        }

    def ParseStore(self) -> dict: 
        tk = self.Advance() 
        Type = self.ParseType()
        Val = self.ParseStmt()
        self.Expect(TokenKind.comma, ",")
        if self.CToken().Kind == TokenKind.pointer:
            self.Advance()
            Point = True 
        else:
            Point = False
        
        if self.CToken().Kind == TokenKind.global_ident:
            Name = self.Advance()
        else:
            Name = self.Expect(TokenKind.local_ident, "a local identifier")
        
        return {
            "Kind" : "StoreNode",
            "Type" : Type,
            "Val" : Val,
            "Point" : Point,
            "Name" : Name.Value
        }

    def Parsetoint(self) -> dict:
        tk = self.Advance()
        Loading = self.ParseStmt()
        self.Expect(TokenKind.comma, ",")
        Type_ = self.ParseType()
        self.Expect(TokenKind.arrow, "->")
        Name = self.Expect(TokenKind.local_ident, "an identifier")

        return {
            "Kind" : "IntToFloat",
            "inst" : tk.Value,
            "Loading" : Loading,
            "Type" : Type_,
            "Into" : Name.Value,
            "Loc" : {
                "Start" : Name.Start,
                "End" : Name.End
            }
        } 
    
    def ParseLocalConst(self) -> dict:
        self.Advance()
        ident = self.Expect(TokenKind.local_ident, "local identifier")
        self.Expect(TokenKind.comma, ",")
        stmt = self.ParseStmt()

        return {
            "Kind" : "LConstNode",
            "Value" : stmt
        }

    def ParseRet(self) -> dict:
        tk = self.Advance()
        if self.CToken().Kind == TokenKind.type_ and self.CToken().Value == "void":
            return {
                "Kind" : "RetNode",
                "Type" : self.ParseType(),
                "Value" : "None",
                "Loc" : {
                    "Start" : tk.Start,
                    "End" : tk.End
                }
            }
        Val = self.ParseExpr()
    
        self.Expect(TokenKind.comma, ",")
        Type_ = self.ParseType()
        return {
            "Kind" : "RetNode",
            "Value" : Val,
            "Type" : Type_,
            "Loc" : {
                "Start" : tk.Start,
                "End" : tk.End 
            }
        }
    def ParseLoad(self) -> dict:
        
        tk = self.Advance()
        if self.CToken().Kind == TokenKind.pointer:
            self.Advance()
            Point = True 
        else:
            Point = False

        if self.CToken().Kind == TokenKind.global_ident:
            Loading = self.Advance()
        else:
            Loading = self.Expect(TokenKind.local_ident, "local identifier")
       
        self.Expect(TokenKind.comma, ",")
        Type_ = self.ParseType()
        self.Expect(TokenKind.arrow, "->")
        Name = self.Expect(TokenKind.local_ident, "an identifier")
        
        return {
            "Kind" : "LoadNode" if tk.Value == "load" else "LoadPtrNode",
            "Loading" : Loading.Value,
            "Type" : Type_,
            "Into" : Name.Value,
            "Pointer" : Point,
            "Loc" : {
                "Start" : Name.Start,
                "End" : Name.End
            }
        } 
    def ParseInc(self) -> dict:
        tk = self.Advance()
        Name = self.Expect(TokenKind.str_const, "a string")
    
        try:
            open(Name.Value, "r")
        except FileNotFoundError:
            self.errcls.throwerr(Name.Line, tk.Start, Name.End, f"no such file or directory '{Name.Value}'")
        else:
            inc_abs_path = os.path.abspath(Name.Value)
            if inc_abs_path not in self.Ast['Meta']['Includes']:
                pre = os.getcwd()
                os.chdir(os.path.dirname(inc_abs_path))
                self.Ast['Meta']['Includes'].append(inc_abs_path)
                with open(inc_abs_path, "r") as File:
                    SourceCode: str = File.read()
                    SourceCode+='\n'

                errcls: Error = Error(SourceCode, inc_abs_path)
                Lexed_inc_cls: Lexer = Lexer(SourceCode, errcls)
                LexedTokens: list[Token] = Lexed_inc_cls.Lex()
                if(Lexed_inc_cls.errcls.meterr):
                    self.errcls.meterr = True
                    self.errcls.err+="\n"+Lexed_inc_cls.errcls.err

                self.Tokens[self.Pos:self.Pos] = LexedTokens[:-1]
                os.chdir(pre)
                return {"Kind" : "SwitchFile", "Name" : inc_abs_path}
   
        return {
            "Kind" : "ignore"
        }       

    def ParseFunc(self) -> dict:
        self.Advance()
        Name = self.Expect(TokenKind.global_ident, "function name")
        
        self.Meta['Funcs'].update({Name.Value : True})

        Args = []
        self.Expect(TokenKind.open_paren, '(') 
        while self.CToken().Kind not in [TokenKind.close_paren, TokenKind.eof]:
            #these two cases should not happen but NoTimeDev is a shitty programmer so its 
            #possible it may happen
            if self.CToken().Kind == TokenKind.comma: self.Advance()
            elif self.CToken().Kind == TokenKind.close_paren: break
            elif self.CToken().Kind == TokenKind.eof: break
            else:
                Args.append({
                    "Type" : self.ParseType(),
                    "Name" : self.Expect(TokenKind.local_ident, "a local identifier").Value,
                })
        self.Expect(TokenKind.close_paren,  ')')
        self.Expect(TokenKind.arrow, '->')
        
        Type_ = self.ParseType()
        
        Body: list[dict] = []
        self.Expect(TokenKind.open_brace, '{')
        while self.CToken().Kind not in [TokenKind.close_brace, TokenKind.eof]:
            #these two cases should not happen but NoTimeDev is a shitty programmer so its 
            #possible it may happen
            if self.CToken().Kind == TokenKind.close_brace: break
            if self.CToken().Kind == TokenKind.eof: break
            
            Body.append(self.ParseStmt())
        self.Expect(TokenKind.close_brace, '}')
        
        ip = self.isprivate
        self.isprivate = False
        return {
            "Kind" : "FunctionNode",
            "Name" : Name.Value,
            "Type" : Type_,
            "Private" : ip, 
            "Args" : Args,
            "Body" : Body,
            "Loc" : {
                "Start" : Name.Start,
                "End" : Name.End 
            }
        }
            
    def ParseType(self) -> dict:
        tk = self.Advance()
        if tk.Kind == TokenKind.open_bracket:
            size = self.Expect(TokenKind.int_const, "a size")

            self.Expect(TokenKind.close_bracket, "]")

            Type = self.ParseType()

            return {
                "Kind" : "List",
                "Of" : Type,
                "Size" : int(size.Value) * int(Type['Size']),
            }
        if tk.Kind == TokenKind.pointer:
            pointingto = self.ParseType()
            return {
                "Kind" : "Pointer",
                "To" : pointingto,
                "Size" : "64",
            }
        if tk.Kind == TokenKind.type_ and tk.Value == "pad":
            return {
                "Kind" : "Pad"
            }
        if tk.Kind == TokenKind.type_ and tk.Value != "ptr":
            return {
                "Kind" : "Primitive",
                "Val" : tk.Value,
                "Size" : "0" if tk.Value == "void" else tk.Value[1:],
                "Loc" : {
                    "Start" : tk.Start,
                    "End" : tk.End
                }
            }
        if tk.Kind == TokenKind.type_ and tk.Value == "ptr":
            return {
                "Kind" : "Pointer",
                "To" : { 
                    "Kind" : "Primitive",
                    "Val" : "i64",
                    "Size" : "64",
                },
                "Size" : "64",
            } 
        if tk.Kind == TokenKind.global_ident:
            return {
                "Kind" : "Struct",
                "Name" : tk.Value,
                "Size" : "1"
            }
        else:
            self.errcls.throwerr(tk.Line, tk.Start, tk.End, f"expected a type but recived '{tk.Value}'")
        
        return {}
    
    def Handlemetaif(self, Tree: dict):
        if Tree['Kind'] == "If_Defined":
            if Tree['Condition'] in self.MacTbl:
                return {
                        "Kind" : "Block",
                        "Body" : Tree['Body']
                } 
            else:
                if Tree['Alternate'] != None:
                    return self.Handlemetaif(Tree['Alternate'])
        elif Tree['Kind'] == "Else_if_defined":
            if Tree['Condition'] in self.MacTbl:
                return {
                        "Kind" : "Block",
                        "Body" : Tree['Body']
                }
            else:
                if Tree['Alternate'] != None:
                   return self.Handlemetaif(Tree['Alternate'])
        elif Tree['Kind'] == "Else_Meta":
            return {
                "Kind" : "Block",
                "Body" : Tree['Body']
            }

        return {"Kind" : "ignore"}
    def ParseMeta(self) -> dict:
        tk = self.Advance()
        
        if tk.Value == "!file":
            name = self.Expect(TokenKind.str_const, 'a string')
            return {
                "Kind" : "File",
                "FileName" : name.Value
            }
        elif tk.Value == "!marklast":
            name = self.Expect(TokenKind.local_ident, "a local identifier")
            return {
                "Kind" : "MLast",
                "Name" : name.Value
            }
        elif tk.Value == "!define":
            name = self.Expect(TokenKind.meta_info, "meta name")
            self.MacTbl.append(name.Value)

            return {"Kind" : "OumOum"}
        elif tk.Value == "!if":
            tk = self.Expect(TokenKind.meta_info, "meta info")
            if tk.Value == "!os":
                os = self.Expect(TokenKind.str_const, "a string")
                self.Expect(TokenKind.open_brace, "{")
                bdy: list = []
                linkflgs = self.Ast['Meta']['LinkerFlags'].copy()
                incs = self.Ast['Meta']['Includes'].copy()
                while self.CToken().Kind != TokenKind.eof and self.CToken().Kind != TokenKind.close_brace:
                    if self.CToken().Kind == TokenKind.close_brace:
                        break 
                    if self.CToken().Kind == TokenKind.eof:
                        break

                    bdy.append(self.ParseStmt())
                self.Expect(TokenKind.close_brace, "}")
                if os.Value == self.plat:
                    return {
                        "Kind" : "Block",
                        "Body" : bdy
                    } 
                else:
                    self.Ast['Meta']['LinkerFlags'] = linkflgs
                    self.Ast['Meta']['Includes'] = incs 
                return {"Kind" : "ignore"}
        elif tk.Value == "!ldflags":
            self.Expect(TokenKind.open_bracket, "[")
            flgs = []
            while self.CToken().Kind != TokenKind.close_bracket and self.CToken().Kind != TokenKind.eof:
                self.Ast['Meta']['LinkerFlags'].append(self.Expect(TokenKind.str_const, "a string").Value)
                if self.CToken().Kind == TokenKind.comma:
                    self.Advance()
            self.Expect(TokenKind.close_bracket, "]")
            return {"Kind" : "ignore"}
        elif tk.Value == "!asmtext":
            code = self.Expect(TokenKind.str_const, "a string")
            return {
                "Kind" : "AsmText",
                "Code" : code.Value
            }
        elif tk.Value == "!ifdef":
            Defined = self.Expect(TokenKind.meta_info, "meta info")
            self.Expect(TokenKind.open_brace, "{")
            bdy: list = []
            while self.CToken().Kind != TokenKind.eof and self.CToken().Kind != TokenKind.close_brace:
                if self.CToken().Kind == TokenKind.close_brace:
                    break 
                if self.CToken().Kind == TokenKind.eof:
                    break

                bdy.append(self.ParseStmt())
            self.Expect(TokenKind.close_brace, "}")
            
            if self.CToken().Kind == TokenKind.meta_info and self.CToken().Value in ["!eifdef", "!else"]:
                Alternate = self.ParseMeta()
            else:
                Alternate = None

            return self.Handlemetaif({ #type: ignore
                "Kind" : "If_Defined",
                "Condition" : Defined.Value,
                "Body" : bdy,
                "Alternate" : Alternate
            })
            
        elif tk.Value == "!eifdef":
            Defined = self.Expect(TokenKind.meta_info, "meta info")
            self.Expect(TokenKind.open_brace, "{")
            bdy: list = []
            while self.CToken().Kind != TokenKind.eof and self.CToken().Kind != TokenKind.close_brace:
                if self.CToken().Kind == TokenKind.close_brace:
                    break 
                if self.CToken().Kind == TokenKind.eof:
                    break

                bdy.append(self.ParseStmt())
            self.Expect(TokenKind.close_brace, "}")
            
            if self.CToken().Kind == TokenKind.meta_info and self.CToken().Value in ["!eifdef", "!else"]:
                Alternate = self.ParseMeta()
            else:
                Alternate = None
            return {
                    "Kind" : "Else_if_defined",
                    "Condition" : Defined.Value,
                    "Body" : bdy,
                    "Alternate" : Alternate,
            }
        elif tk.Value == "!else":
            self.Expect(TokenKind.open_brace, "{")
            bdy: list = []
            while self.CToken().Kind != TokenKind.eof and self.CToken().Kind != TokenKind.close_brace:
                if self.CToken().Kind == TokenKind.close_brace:
                    break 
                if self.CToken().Kind == TokenKind.eof:
                    break

                bdy.append(self.ParseStmt())
            self.Expect(TokenKind.close_brace, "}")
            
            return {
                "Kind" : "Else_Meta",
                "Body" : bdy 
            }

                        
        return {"Kind" : "ignore"}
    def ParseBin(self) -> dict:
        inst = self.Advance()
        Type_ = self.ParseType()

        left = self.ParseExpr()
        self.Expect(TokenKind.comma, ",")
        right = self.ParseExpr()

        self.Expect(TokenKind.arrow, '->')
        Name = self.Expect(TokenKind.local_ident, "a local identifier")
        return {
            "Kind" : "BinNode",
            "Left" : left,
            "Right" : right,
            "Type" : Type_,
            "Name" : Name.Value,
            "inst" : inst.Value,

            "Loc" : {
                'Start' : Name.Start,
                "End" : Name.End
            }
        }
    def ParsefBin(self) -> dict:
        inst = self.Advance()
        Type_ = self.ParseType()

        left = self.ParseExpr()
        self.Expect(TokenKind.comma, ",")
        right = self.ParseExpr()

        self.Expect(TokenKind.arrow, '->')
        Name = self.Expect(TokenKind.local_ident, "a local identifier")
        return {
            "Kind" : "FloatBinNode",
            "Left" : left,
            "Right" : right,
            "Type" : Type_,
            "Name" : Name.Value,
            "inst" : inst.Value,

            "Loc" : {
                'Start' : Name.Start,
                "End" : Name.End
            }
        }

   
    def ParseIdent(self) -> dict:
        Name = self.Advance()

        if Name.Value[0] == "@":
            Kind = "GIdent"
        else:
            Kind = "LIdent"
        
        return {
            "Kind" : Kind,
            "Name" : Name.Value,
            "Loc" : {
                "Start" :Name.Start,
                "End" : Name.End
            }
        }

    def ParseInt(self) -> dict:
        num = self.Advance()
        return {
            "Kind" : "Integer",
            "Value" : num.Value,
            "Loc" : {
                "Start" : num.Start,
                "End" : num.End
            }
        }
    def ParseFloat(self) -> dict:
        num = self.Advance()
        return {
            "Kind" : "Float",
            "Value" : num.Value,
            "Loc" : {
                "Start" : num.Start,
                "End" : num.End
            }
        }

    def ParseSizech(self) -> dict:
        tk = self.Advance()
        Loading = self.ParseStmt()
        self.Expect(TokenKind.comma, ",")
        Type_ = self.ParseType()
        self.Expect(TokenKind.arrow, "->")
        Name = self.Expect(TokenKind.local_ident, "an identifier")

        return {
            "Kind" : "SizeNode",
            "Inst" : tk.Value,
            "Old" : Loading,
            "Type" : Type_,
            "New" : Name.Value,
            "Loc" : {
                "Start" : Name.Start,
                "End" : Name.End
            }
        } 
   
    def Parsecomment(self) -> dict:
        comm = self.Advance().Value
        if comm[0:12] == "#asmcomment:":
            return {"Kind" : "comment",
                    "Value" : comm[12:]
                    }
    
        return {"Kind" : "ignore"}

    def ParseFSizech(self) -> dict:
        tk = self.Advance()

        fr = self.ParseStmt()
        self.Expect(TokenKind.arrow, "->")
        to = self.Expect(TokenKind.local_ident, "local identifier")
        
        return {
            "Kind" : "FloatSizeCh",
            "Inst" : tk.Value,
            "From" : fr,
            "To" : to.Value,
        }

    def ParseDeref(self) -> dict:
        tk = self.Advance()
        Type = self.ParseType()
        Name = self.Expect(TokenKind.local_ident, "a local identifier")

        return {
            "Kind" : "Dereference",
            "Type" : Type,
            "Name" : Name.Value,
        }
    def ParseList(self) -> dict:
        self.Advance()

        List = []
        while self.CToken().Kind not in [TokenKind.eof, TokenKind.close_bracket]:
            if self.CToken().Kind == TokenKind.comma:
                self.Advance()
            elif self.CToken().Kind == TokenKind.close_bracket:
                break 
            else:
                if self.CToken().Kind == TokenKind.meta_info and self.CToken().Value == "!str":
                    self.Advance()
                    string: str = self.Expect(TokenKind.str_const, "a string").Value
                    string = string.encode().decode("unicode_escape")

                    for c in string:
                        List.append({
                            "Kind" : "Integer",
                            "Value" : ord(c),
                        })
                else:
                    List.append(self.ParseStmt())
        self.Expect(TokenKind.close_bracket, ")")

        return {
            "Kind" : "List",
            "Size" : len(List),
            "List" : List,
        }
    def ParseconstStruct(self) -> dict:
        self.Advance()

        List = []
        while self.CToken().Kind not in [TokenKind.eof, TokenKind.close_brace]:
            if self.CToken().Kind == TokenKind.comma:
                self.Advance()
            elif self.CToken().Kind == TokenKind.close_brace:
                break 
            else:
                Type = self.ParseType()
                List.append({
                        "Type" : Type, 
                        "Value" : self.ParseStmt()
                })
        self.Expect(TokenKind.close_brace, "}")

        return {
            "Kind" : "Struct_c",
            "Size" : len(List),
            "List" : List,
        }
    

    def ParseCmp(self) -> dict:
        tk = self.Advance()

        Type = self.ParseType()
        cmpinst = self.Expect(TokenKind.cmp, "a compare inst")
        Op1 = self.ParseStmt()
        self.Expect(TokenKind.comma, ",")
        Op2 = self.ParseStmt()
        self.Expect(TokenKind.arrow, "->")
        Name = self.Expect(TokenKind.local_ident, "a local identifier")

        return {
            "Kind" : "cmp", 
            "inst" : tk.Value,
            "Type" : Type, 
            "cmpinst" : cmpinst.Value,
            "Op1" : Op1,
            "Op2" : Op2, 
            "Name" : Name.Value,
        }
    
    def ParseShifts(self) -> dict:
        inst = self.Advance().Value
        Type = self.ParseType()
        Val = self.ParseStmt()
        self.Expect(TokenKind.comma, ",")
        Num = self.ParseStmt() 
        self.Expect(TokenKind.arrow, "->")
        Name  = self.Expect(TokenKind.local_ident, "a local ident")

        return {
            "Kind" : "Shift",
            "Inst" : inst,
            "Type" : Type,
            "Val" : Val,
            "Num" : Num,
            "Name" : Name.Value,
        }

    def ParseExpr(self) -> dict:
        tk = self.CToken() 
        if tk.Kind == TokenKind.meta_info:
            return self.ParseMeta()
        elif tk.Kind == TokenKind.open_bracket:
            return self.ParseList()
        elif tk.Kind == TokenKind.open_brace:
            return self.ParseconstStruct()
        elif tk.Kind == TokenKind.pointer:
            return self.ParseDeref()
        elif tk.Kind in [TokenKind.add_inst, TokenKind.sub_inst, 
                        TokenKind.idiv_inst, TokenKind.div_inst,
                        TokenKind.imul_inst, TokenKind.mul_inst,
                        TokenKind.imod_inst, TokenKind.mod_inst,
                         TokenKind.xor_inst, 
                         TokenKind.or_inst, TokenKind.and_inst,
            ]:
            return self.ParseBin()
        elif tk.Kind in [TokenKind.shl_inst, TokenKind.shr_inst, TokenKind.ashr_inst]:
            return self.ParseShifts()
        elif tk.Kind in [TokenKind.fadd_inst, TokenKind.fsub_inst,
                         TokenKind.fmod_inst, TokenKind.fmul_inst,
                         TokenKind.fdiv_inst]:
            return self.ParsefBin()
        elif tk.Kind in [TokenKind.fext_inst, TokenKind.ftrunc_inst]:
            return self.ParseFSizech()
        elif tk.Kind in [
                TokenKind.ext_inst, TokenKind.iext_inst,
                TokenKind.trunc_inst
            ]:
            return self.ParseSizech()
        elif tk.Kind in [TokenKind.local_ident, TokenKind.global_ident, TokenKind.label_ident]:
            return self.ParseIdent()
        elif tk.Kind == TokenKind.int_const:
            return self.ParseInt()
        elif tk.Kind == TokenKind.float_const:
            return self.ParseFloat() 
        elif tk.Kind == TokenKind.comment:
            return self.Parsecomment() 
        elif tk.Kind in [TokenKind.cmp_inst, TokenKind.icmp_inst, TokenKind.fcmp_inst]:
            return self.ParseCmp()
        else:
            self.errcls.throwerr(tk.Line, tk.Start, tk.End, "expected an expression")
            self.Advance()

        return {"Kind" : "ignore"}

