%macro .saveregs 0  ;save calle reg 
    mov [reg_storage + 0],  rax
    mov [reg_storage + 8],  rbx
    mov [reg_storage + 16], rcx
    mov [reg_storage + 24], rdx
    mov [reg_storage + 32], rsi
    mov [reg_storage + 40], rdi
    mov [reg_storage + 48], rbp
    mov [reg_storage + 56], rsp
    mov [reg_storage + 64], r8
    mov [reg_storage + 72], r9
    mov [reg_storage + 80], r10
    mov [reg_storage + 88], r11
    mov [reg_storage + 96], r12
    mov [reg_storage + 104], r13
    mov [reg_storage + 112], r14
    mov [reg_storage + 120], r15

    movsd [xmm_storage + 0],   xmm0
    movsd [xmm_storage + 8],   xmm1
    movsd [xmm_storage + 16],  xmm2
    movsd [xmm_storage + 24],  xmm3
    movsd [xmm_storage + 32],  xmm4
    movsd [xmm_storage + 40],  xmm5
    movsd [xmm_storage + 48],  xmm6
    movsd [xmm_storage + 56],  xmm7
    movsd [xmm_storage + 64],  xmm8
    movsd [xmm_storage + 72],  xmm9
    movsd [xmm_storage + 80],  xmm10
    movsd [xmm_storage + 88],  xmm11
    movsd [xmm_storage + 96],  xmm12
    movsd [xmm_storage + 104], xmm13
    movsd [xmm_storage + 112], xmm14
    movsd [xmm_storage + 120], xmm15
%endmacro 

%macro .dropregs 0 ;save calle reg 
    movsd xmm0,  [xmm_storage + 0]
    movsd xmm1,  [xmm_storage + 8]
    movsd xmm2,  [xmm_storage + 16]
    movsd xmm3,  [xmm_storage + 24]
    movsd xmm4,  [xmm_storage + 32]
    movsd xmm5,  [xmm_storage + 40]
    movsd xmm6,  [xmm_storage + 48]
    movsd xmm7,  [xmm_storage + 56]
    movsd xmm8,  [xmm_storage + 64]
    movsd xmm9,  [xmm_storage + 72]
    movsd xmm10, [xmm_storage + 80]
    movsd xmm11, [xmm_storage + 88]
    movsd xmm12, [xmm_storage + 96]
    movsd xmm13, [xmm_storage + 104]
    movsd xmm14, [xmm_storage + 112]
    movsd xmm15, [xmm_storage + 120]

    ; --- Restore GPRs ---
    mov rax, [reg_storage + 0]
    mov rbx, [reg_storage + 8]
    mov rcx, [reg_storage + 16]
    mov rdx, [reg_storage + 24]
    mov rsi, [reg_storage + 32]
    mov rdi, [reg_storage + 40]
    mov rbp, [reg_storage + 48]
    mov rsp, [reg_storage + 56]
    mov r8,  [reg_storage + 64]
    mov r9,  [reg_storage + 72]
    mov r10, [reg_storage + 80]
    mov r11, [reg_storage + 88]
    mov r12, [reg_storage + 96]
    mov r13, [reg_storage + 104]
    mov r14, [reg_storage + 112]
    mov r15, [reg_storage + 120]
%endmacro

