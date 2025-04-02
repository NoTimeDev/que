import sys

Red: str = "\033[31m"
Green: str = "\033[32m"
Yellow: str = "\033[33m"
Blue: str = "\033[34m"
Magenta: str = "\033[35m"
Cyan: str = "\033[36m"
White: str = "\033[37m"
Grey: str = "\033[90m"

BrightRed: str = "\033[91m"
BrightGreen: str = "\033[92m"
BrightYellow: str = "\033[93m"
BrightBlue: str = "\033[94m"
BrightMagenta: str = "\033[95m"
BrightCyan: str = "\033[96m"
BrightWhite: str = "\033[97m"

UBrightRed: str = "\033[4;91m"
UBrightGreen: str = "\033[4;92m"
UBrightYellow: str = "\033[4;93m"
UBrightBlue: str = "\033[4;94m"
UBrightMagenta: str = "\033[4;95m"
UBrightCyan: str = "\033[4;96m"
UBrightWhite: str = "\033[4;97m"

BRed: str = "\033[1;31m"
BGreen: str = "\033[1;32m"
BYellow: str = "\033[1;33m"
BBlue: str = "\033[1;34m"
BMagenta: str = "\033[1;35m"
BCyan: str = "\033[1;36m"
BWhite: str = "\033[1;1m"

UBRed: str = "\033[1;4;31m"
UBGreen: str = "\033[1;4;32m"
UBYellow: str = "\033[1;4;33m"
UBBlue: str = "\033[1;4;34m"
UBMagenta: str = "\033[1;4;35m"
UBCyan: str = "\033[1;4;36m"
UBWhite: str = "\033[1;4;1m"



Reset: str = "\033[0m"

def printr(Kwargs, end="\n"):
    print(Kwargs, end=end, file=sys.stderr)
