## How To Run
to run a que program in your terminal run the following commands   
`python main.py <file> -name <exename>`  
currently que does not clean up .asm and .o files  
  
Note: que syntax may be changed after an update 

## Basic arithmetic 
```llvm
#the structure for arithmetic intructions in zed look like this

include "std.que"

def @main() -> i32{
    add i32 4, 5 -> $Add1
    load $Add1, i32 -> $LoadedVreg
    ret $LoadedVreg, i32
}
```
lets look at this code `include "std.que"` includes some code so that the main function will be called across different oses. 

`def @main() -> i32{` defines the main function and set the return type to a 32 bit integer   

> **Note:** you will handle if i32 is signed or unsigned with instructions prefixed with `i` for signed and ones without for usinged 

`add i32 4, 5 -> $Add1` adds 4 + 5 and stores the value in a virtual register callled `$Add1` 

`load $Add1, i32 -> $LoadedVreg` this code loads the virtual register $Add1 into another virtual register called $LoadedVreg

> **Note:** you dont need to load a virtual register but loading ensures that if in assembly the variable is not loaded into a valid register it will be and you can use this virtual register anywhere and it will always be loaded 

`ret $LoadedVreg, i32` and lastly this code returns the virtual register with the value 9 

![Alt Text](/Docs/2025-03-23-212603_hyprshot.png)

as you can see we got the expected out put code

> **Note:** vreg refers to virtual register


|Synatx|use|
|-------|-------|
|`add <size> <op1>, <op2> -> <vregname>`|adds <op1> and <op2> and store it in vreg name(unsigned, signed)|
|`sub <size> <op1>, <op2> -> <vregname>`|subtracts <op2> from <op1> and store it in vreg name(unsigned, singed)|
|`mul <size> <op1>, <op2> -> <vregname>`|multiplies <op1> by <op2> and stores it in the vreg name(unsigned)|
|`imul <size> <op1>, <op2> -> <vregname>`|multiplies <op1> by <op2> and stores it in the vreg name(signed)|
|`div <size> <op1>, <op2> -> <vregname>`|divides <op1> by <op2> and stores it in the vreg name(unsigned)|
|`idiv <size> <op1>, <op2> -> <vregname>`|divides <op1> by <op2> and stores it in the vreg name(signed)|
|`mod <size> <op1>, <op2> -> <vregname>`|gets the remiander of <op1> / <op2> and stores it in the vreg name(unsigned)|
|`imod <size> <op1>, <op2> -> <vregname>`|gets the remaineder of <op1> / <op2> and stores it in the vreg name(signed)|
|`load <vregtoload>, <type> -> <vregname>`|loads a vitural register and stores it in the vreg name(unsigned, signed)|
|`ext <vregtoextend>, <type> -> <vregname>`|extends a vreg to the type provided and stores it in the vreg name(unsigned)|
|`iext <vregtoextend>, <type> -> <vregname>`|extends a vreg to the type provided and stores it in the vreg name(signed)|

