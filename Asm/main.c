#include <stdint.h>
#include <stdio.h> 
struct Example {
    char a;    // 1 byte
    int b;     // 4 bytes
    short c;   // 2 bytes
    int d; 
    int64_t e;
    int64_t f;
    int64_t g;
    int64_t h;
};

struct Example retexmp(){
    struct Example exmaple = {.a = 'h', .b = 90, .c = 10, .d = 90, .e = 190, .f = 180, .g = 901, .h = 20};
    return exmaple;
}

int main(){
    struct Example exmp = retexmp();
    printf("%c", exmp.a);
    printf("%i", exmp.b);
    printf("%i", exmp.c);
    printf("%i", exmp.d);
}
