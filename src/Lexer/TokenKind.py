from enum import Enum, auto

class TokenKind(Enum):
    #const 
    int_const = auto()
    str_const = auto()
    float_const = auto()
    #instructions or whatever
    loacl_const = auto()

    include_inst = auto()
    def_inst = auto()
    load_inst = auto()
    loadptr_inst = auto()
    ret_inst = auto()

    add_inst = auto()
    sub_inst = auto()
    
    imul_inst = auto()
    mul_inst = auto()
    
    idiv_inst = auto()
    div_inst = auto()
    
    imod_inst = auto()
    mod_inst = auto()
    
    trunc_inst = auto()
    ext_inst = auto()
    iext_inst = auto()
    
    alloc_inst = auto()
    store_inst = auto()
    getptr_inst = auto()
    geteptr_inst = auto()
    getfptr_inst = auto()
    castptr_inst = auto()

    global_inst = auto()
    const_inst = auto()
    private_inst = auto()
    extern_inst = auto()
    call_inst = auto()

    if_inst = auto()

    icmp_inst = auto()
    cmp_inst = auto()
    fcmp_inst = auto()
    
    goto_inst = auto()
    cmp = auto()
    #floats - why do they have a special category  idk 
    fadd_inst = auto()
    fsub_inst = auto()
    fdiv_inst = auto()
    fmul_inst = auto()
    fmod_inst = auto()

    fext_inst = auto()
    ftrunc_inst = auto()

    fti_inst = auto()
    itf_inst = auto()
    
    #other 
    comment = auto()
    type_ = auto()
    meta_info = auto()
    global_ident = auto()
    local_ident = auto()
    label_ident = auto()
    eof = auto()

    #operators
    arrow = auto()
    comma = auto()

    pointer = auto()

    open_paren = auto()
    close_paren = auto()

    open_bracket = auto()
    close_bracket = auto()
    
    open_brace = auto()
    close_brace = auto()
    
    equal = auto()
class Token:
    def __init__(self, Value: str, Kind: TokenKind, Line: int, Start: int, End: int):
        self.Value: str = Value
        self.Kind: TokenKind = Kind
        self.Line: int = Line
        self.Start: int = Start
        self.End: int = End


    def __repr__(self) -> str:
        return "{" + f'"Value" : {self.Value}, "Kind" : {self.Kind}, "Line" : {self.Line}, "Start" : {self.Start}, "End" : {self.End}' + "}"
