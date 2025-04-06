	.file	"main.c"
	.intel_syntax noprefix
# GNU C17 (GCC) version 14.2.1 20250207 (x86_64-pc-linux-gnu)
#	compiled by GNU C version 14.2.1 20250207, GMP version 6.3.0, MPFR version 4.2.1, MPC version 1.3.1, isl version isl-0.27-GMP

# warning: MPFR header version 4.2.1 differs from library version 4.2.2.
# GGC heuristics: --param ggc-min-expand=100 --param ggc-min-heapsize=131072
# options passed: -masm=intel -mtune=generic -march=x86-64
	.text
	.globl	main
	.type	main, @function
main:
.LFB0:
	.cfi_startproc
	push	rbp	#
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp	#,
	.cfi_def_cfa_register 6
# ./Asm/main.c:5:     float x = 9.3;
	movss	xmm0, DWORD PTR .LC0[rip]	# tmp101,
	movss	DWORD PTR -8[rbp], xmm0	# x, tmp101
# ./Asm/main.c:6:     float y = 9.8;
	movss	xmm0, DWORD PTR .LC1[rip]	# tmp102,
	movss	DWORD PTR -4[rbp], xmm0	# y, tmp102
# ./Asm/main.c:7:     uint8_t ext = x == y;
	movss	xmm0, DWORD PTR -8[rbp]	# tmp104, x
	ucomiss	xmm0, DWORD PTR -4[rbp]	# tmp104, y
	setnp	al	#, tmp103
	mov	edx, 0	# tmp106,
	movss	xmm0, DWORD PTR -8[rbp]	# tmp105, x
	ucomiss	xmm0, DWORD PTR -4[rbp]	# tmp105, y
	cmovne	eax, edx	# tmp103,, _1, tmp106
# ./Asm/main.c:7:     uint8_t ext = x == y;
	mov	BYTE PTR -9[rbp], al	# ext, _1
# ./Asm/main.c:8:     if(ext){
	cmp	BYTE PTR -9[rbp], 0	# ext,
	je	.L2	#,
# ./Asm/main.c:9:         return 3;
	mov	eax, 3	# _2,
	jmp	.L3	#
.L2:
# ./Asm/main.c:11:     return 0;
	mov	eax, 0	# _2,
.L3:
# ./Asm/main.c:12: }
	pop	rbp	#
	.cfi_def_cfa 7, 8
	ret	
	.cfi_endproc
.LFE0:
	.size	main, .-main
	.section	.rodata
	.align 4
.LC0:
	.long	1091882189
	.align 4
.LC1:
	.long	1092406477
	.ident	"GCC: (GNU) 14.2.1 20250207"
	.section	.note.GNU-stack,"",@progbits
