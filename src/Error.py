from .Utils.Utils import *


class Error:
    def __init__(self, SourceCode: str, filename: str):
        self.SourceCode: list[str] = SourceCode.split('\n')
        self.filename: str = filename
        self.err: str = ""
        self.meterr: bool = False

    def highlight(self, linestr: str, poses: list, col: str):
        string: str = ""
        pos: int = 0
        
        indx: int = 0
        while pos < len(linestr):
            if(indx < len(poses) and poses[indx] == pos and indx % 2 == 0):
                string+=col
                indx+=1
                if(poses[indx] == pos):
                    string+=linestr[pos]+Reset 
                    pos+=1 
                else:
                    while pos != poses[indx]:
                        string+=linestr[pos] 
                        pos+=1

                    string+=f"{Reset}"
            else:
                string+=linestr[pos]
                pos+=1 

        return string
    def throwerr(self, line, start, end, msg, noh = False):
        self.meterr = True

        self.err += f"{self.filename}:[{line}:{start}-{end}]:[{UBRed}error{Reset}] {msg}{Reset}\n"
        if(line != 1):
            self.err += f"{Grey}{line - 1}|{self.SourceCode[line - 2]}{Reset}\n"
        if noh == False:
            self.err += f"{line}|{self.highlight(self.SourceCode[line - 1], [start - 1, end - 1], Red)}\n"
        else:
            self.err += f"{line}|{self.SourceCode[line - 1]}\n"
        if(line != len(self.SourceCode) - 1):
            self.err += f"{Grey}{line + 1}|{self.SourceCode[line]}{Reset}\n" 

    def throwwarning(self, line, start, end, msg):
        pass 
