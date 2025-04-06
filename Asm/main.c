#include <stdint.h>
#include <stdio.h> 

int main(){
    float x = 9.3;
    float y = 9.8;
    uint8_t ext = x == y;
    if(ext){
        return 3;
    }
    return 0;
}
