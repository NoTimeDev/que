	.file	"main.c"
	.intel_syntax noprefix
 # GNU C17 (GCC) version 14.2.0 (x86_64-w64-mingw32)
 #	compiled by GNU C version 14.2.1 20240910, GMP version 6.3.0, MPFR version 4.2.1, MPC version 1.3.1, isl version isl-0.27-GMP

 # warning: MPFR header version 4.2.1 differs from library version 4.2.2.
 # GGC heuristics: --param ggc-min-expand=100 --param ggc-min-heapsize=131072
 # options passed: -masm=intel -mtune=generic -march=x86-64 -fno-omit-frame-pointer
	.text
	.globl	add
	.def	add;	.scl	2;	.type	32;	.endef
	.seh_proc	add
add:
	push	rbp	 #
	.seh_pushreg	rbp
	mov	rbp, rsp	 #,
	.seh_setframe	rbp, 0
	sub	rsp, 16	 #,
	.seh_stackalloc	16
	.seh_endprologue
	mov	DWORD PTR 16[rbp], ecx	 # i, i
	mov	DWORD PTR 24[rbp], edx	 # y, y
	mov	DWORD PTR 32[rbp], r8d	 # p, p
	mov	DWORD PTR 40[rbp], r9d	 # f, f
 # Asm/main.c:4:     float x1 =9.2;
	movss	xmm0, DWORD PTR .LC0[rip]	 # tmp100,
	movss	DWORD PTR -4[rbp], xmm0	 # x1, tmp100
 # Asm/main.c:5:     int gssg = h + d;
	mov	edx, DWORD PTR 48[rbp]	 # tmp105, h
	mov	eax, DWORD PTR 56[rbp]	 # tmp106, d
	add	eax, edx	 # gssg_4, tmp105
	mov	DWORD PTR -8[rbp], eax	 # gssg, gssg_4
 # Asm/main.c:6:     return x1;
	movss	xmm0, DWORD PTR -4[rbp]	 # _5, x1
 # Asm/main.c:7: }
	add	rsp, 16	 #,
	pop	rbp	 #
	ret	
	.seh_endproc
	.section .rdata,"dr"
.LC1:
	.ascii "%f\0"
	.text
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
	.seh_proc	main
main:
	push	rbp	 #
	.seh_pushreg	rbp
	mov	rbp, rsp	 #,
	.seh_setframe	rbp, 0
	sub	rsp, 96	 #,
	.seh_stackalloc	96
	.seh_endprologue
 # Asm/main.c:9: int main(){
	call	__main	 #
 # Asm/main.c:10:     float x = add(1, 4, 3, 4, 5, 6, 6,5, 6); 
	mov	DWORD PTR 64[rsp], 6	 #,
	mov	DWORD PTR 56[rsp], 5	 #,
	mov	DWORD PTR 48[rsp], 6	 #,
	mov	DWORD PTR 40[rsp], 6	 #,
	mov	DWORD PTR 32[rsp], 5	 #,
	mov	r9d, 4	 #,
	mov	r8d, 3	 #,
	mov	edx, 4	 #,
	mov	ecx, 1	 #,
	call	add	 #
	movd	eax, xmm0	 # tmp101,
	mov	DWORD PTR -4[rbp], eax	 # x, tmp101
 # Asm/main.c:11:     float x2 = add(1, 4, 3, 4, 5, 6, 6,5, 6); 
	mov	DWORD PTR 64[rsp], 6	 #,
	mov	DWORD PTR 56[rsp], 5	 #,
	mov	DWORD PTR 48[rsp], 6	 #,
	mov	DWORD PTR 40[rsp], 6	 #,
	mov	DWORD PTR 32[rsp], 5	 #,
	mov	r9d, 4	 #,
	mov	r8d, 3	 #,
	mov	edx, 4	 #,
	mov	ecx, 1	 #,
	call	add	 #
	movd	eax, xmm0	 # tmp102,
	mov	DWORD PTR -8[rbp], eax	 # x2, tmp102
 # Asm/main.c:12:     printf("%f", x);
	pxor	xmm0, xmm0	 # _1
	cvtss2sd	xmm0, DWORD PTR -4[rbp]	 # _1, x
	movapd	xmm1, xmm0	 # tmp103, _1
	movapd	xmm0, xmm1	 # tmp104, tmp103
	movq	rax, xmm1	 # tmp105, tmp103
	movapd	xmm1, xmm0	 #, tmp104
	mov	rdx, rax	 #, tmp105
	lea	rax, .LC1[rip]	 # tmp106,
	mov	rcx, rax	 #, tmp106
	call	printf	 #
	mov	eax, 0	 # _8,
 # Asm/main.c:13: }
	add	rsp, 96	 #,
	pop	rbp	 #
	ret	
	.seh_endproc
	.section .rdata,"dr"
	.align 4
.LC0:
	.long	1091777331
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (GNU) 14.2.0"
	.def	printf;	.scl	2;	.type	32;	.endef
