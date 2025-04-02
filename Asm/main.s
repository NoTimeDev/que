	.file	"main.c"
	.intel_syntax noprefix
 # GNU C17 (GCC) version 14.2.0 (x86_64-w64-mingw32)
 #	compiled by GNU C version 14.2.1 20240910, GMP version 6.3.0, MPFR version 4.2.1, MPC version 1.3.1, isl version isl-0.27-GMP

 # warning: MPFR header version 4.2.1 differs from library version 4.2.2.
 # GGC heuristics: --param ggc-min-expand=100 --param ggc-min-heapsize=131072
 # options passed: -masm=intel -mtune=generic -march=x86-64
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
 # Asm/main.c:4:     int gssg = h + d;
	mov	edx, DWORD PTR 48[rbp]	 # tmp104, h
	mov	eax, DWORD PTR 56[rbp]	 # tmp105, d
	add	eax, edx	 # gssg_3, tmp104
	mov	DWORD PTR -4[rbp], eax	 # gssg, gssg_3
 # Asm/main.c:5:     return gssg;
	mov	eax, DWORD PTR -4[rbp]	 # _4, gssg
 # Asm/main.c:6: }
	add	rsp, 16	 #,
	pop	rbp	 #
	ret	
	.seh_endproc
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
 # Asm/main.c:8: int main(){
	call	__main	 #
 # Asm/main.c:9:     int x = add(1, 2, 3, 4, 5, 6, 7, 8, 9); 
	mov	DWORD PTR 64[rsp], 9	 #,
	mov	DWORD PTR 56[rsp], 8	 #,
	mov	DWORD PTR 48[rsp], 7	 #,
	mov	DWORD PTR 40[rsp], 6	 #,
	mov	DWORD PTR 32[rsp], 5	 #,
	mov	r9d, 4	 #,
	mov	r8d, 3	 #,
	mov	edx, 2	 #,
	mov	ecx, 1	 #,
	call	add	 #
	mov	DWORD PTR -4[rbp], eax	 # x, tmp100
 # Asm/main.c:10:     return x;
	mov	eax, DWORD PTR -4[rbp]	 # _4, x
 # Asm/main.c:11: }
	add	rsp, 96	 #,
	pop	rbp	 #
	ret	
	.seh_endproc
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (GNU) 14.2.0"
