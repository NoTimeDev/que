%macro .l_saveregs 0  ;save calle reg 
    mov qword [rbp-8], rbx
    mov qword [rbp-16], r12
    mov qword [rbp-24], r13
    mov qword [rbp-32], r14
    mov qword [rbp-40], r15
%endmacro 

%macro .l_dropregs 0 ;save calle reg 
    mov rbx, qword [rbp-8]
    mov r12, qword [rbp-16]
    mov r13, qword [rbp-24]
    mov r14, qword [rbp-32]
    mov r15, qword [rbp-40]
%endmacro

%macro .w_saveregs 0 ;save calle reg 
    mov qword [rbp-8], rbx
    mov qword [rbp-16], rdi
    mov qword [rbp-24], r12
    mov qword [rbp-32], r13
    mov qword [rbp-40], r14
    mov qword [rbp-48], r15
    movsd qword [rbp-56], xmm6
    movsd qword [rbp-64], xmm7
    movsd qword [rbp-72], xmm8
    movsd qword [rbp-80], xmm9
    movsd qword [rbp-88], xmm10
    movsd qword [rbp-96], xmm11
    movsd qword [rbp-104], xmm12
    movsd qword [rbp-112], xmm13
    movsd qword [rbp-120], xmm14
    movsd qword [rbp-128], xmm15
%endmacro

%macro .w_dropregs 0 ;save calle reg 
     mov rbx, qword [rbp-8]
    mov rdi, qword [rbp-16]
    mov r12, qword [rbp-24]
    mov r13, qword [rbp-32]
    mov r14, qword [rbp-40]
    mov r15, qword [rbp-48]
    movsd xmm6, qword [rbp-56]
    movsd xmm7, qword [rbp-64]
    movsd xmm8, qword [rbp-72]
    movsd xmm9, qword [rbp-80]
    movsd xmm10, qword [rbp-88]
    movsd xmm11, qword [rbp-96]
    movsd xmm12, qword [rbp-104]
    movsd xmm13, qword [rbp-112]
    movsd xmm14, qword [rbp-120]
    movsd xmm15, qword [rbp-128]
%endmacro 
%macro .l_startcall 1
    mov qword rax, [rbp - %1]
    mov qword rcx, [rbp - %1 + 8]
    mov qword rdx, [rbp - %1 + 16]
    mov qword rsi, [rbp - %1 + 24]
    mov qword rdi, [rbp - %1 + 32]
    mov qword r10, [rbp - %1 + 40]
    mov qword r11, [rbp - %1 + 48]

    movsd xmm8, [rbp - %1 + 56]  
    movsd xmm9, [rbp - %1 + 64]
    movsd xmm10, [rbp - %1 + 72]
    movsd xmm11, [rbp - %1 + 80]
    movsd xmm12, [rbp - %1 + 88]
    movsd xmm13, [rbp - %1 + 96]
    movsd xmm14, [rbp - %1 + 104]
    movsd xmm15, [rbp - %1 + 112]
%endmacro 

%macro .l_endcall 1 
    mov qword [rbp - %1], rax
    mov qword [rbp - %1 + 8], rcx
    mov qword [rbp - %1 + 16], rdx
    mov qword [rbp - %1 + 24], rsi
    mov qword [rbp - %1 + 32], rdi
    mov qword [rbp - %1 + 40], r10
    mov qword [rbp - %1 + 48], r11 

    movsd [rbp - %1 + 56], xmm8  
    movsd [rbp - %1 + 64], xmm9
    movsd [rbp - %1 + 72], xmm10
    movsd [rbp - %1 + 80], xmm11
    movsd [rbp - %1 + 88], xmm12
    movsd [rbp - %1 + 96], xmm13
    movsd [rbp - %1 + 104], xmm14
    movsd [rbp - %1 + 112], xmm15
%endmacro  

%macro .w_startcall 1
    mov qword [rbp - %1 + 8], r10
    mov qword [rbp - %1 + 16], r11

    movsd [rbp - %1 + 24], xmm4
    movsd [rbp - %1 + 32], xmm5 
%endmacro
 
%macro .w_endcall 1
    mov qword r10, [rbp - %1 + 8] 
    mov qword r11, [rbp - %1 + 16]  
    
    movsd xmm4, [rbp - %1 + 24]
    movsd xmm5, [rbp - %1 + 32] 

%endmacro

