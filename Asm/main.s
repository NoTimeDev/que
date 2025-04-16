	.file	"main.c"
	.intel_syntax noprefix
# GNU C17 (GCC) version 14.2.1 20250207 (x86_64-pc-linux-gnu)
#	compiled by GNU C version 14.2.1 20250207, GMP version 6.3.0, MPFR version 4.2.1, MPC version 1.3.1, isl version isl-0.27-GMP

# warning: MPFR header version 4.2.1 differs from library version 4.2.2.
# GGC heuristics: --param ggc-min-expand=100 --param ggc-min-heapsize=131072
# options passed: -masm=intel -mtune=generic -march=x86-64 -O0
	.text
	.globl	retexmp
	.type	retexmp, @function
retexmp:
.LFB0:
	.cfi_startproc
	push	rbp	#
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp	#,
	.cfi_def_cfa_register 6
	push	rbx	#
	.cfi_offset 3, -24
	mov	QWORD PTR -72[rbp], rdi	# .result_ptr, .result_ptr
# Asm/main.c:15:     struct Example exmaple = {.a = 'h', .b = 90, .c = 10, .d = 90, .e = 190, .f = 180, .g = 901, .h = 20};
	mov	BYTE PTR -64[rbp], 104	# exmaple.a,
	mov	DWORD PTR -60[rbp], 90	# exmaple.b,
	mov	WORD PTR -56[rbp], 10	# exmaple.c,
	mov	DWORD PTR -52[rbp], 90	# exmaple.d,
	mov	QWORD PTR -48[rbp], 190	# exmaple.e,
	mov	QWORD PTR -40[rbp], 180	# exmaple.f,
	mov	QWORD PTR -32[rbp], 901	# exmaple.g,
	mov	QWORD PTR -24[rbp], 20	# exmaple.h,
# Asm/main.c:16:     return exmaple;
	mov	rax, QWORD PTR -72[rbp]	# tmp98, .result_ptr
	mov	rcx, QWORD PTR -64[rbp]	# tmp99, exmaple
	mov	rbx, QWORD PTR -56[rbp]	#, exmaple
	mov	QWORD PTR [rax], rcx	# <retval>, tmp99
	mov	QWORD PTR 8[rax], rbx	# <retval>,
	mov	rcx, QWORD PTR -48[rbp]	# tmp100, exmaple
	mov	rbx, QWORD PTR -40[rbp]	#, exmaple
	mov	QWORD PTR 16[rax], rcx	# <retval>, tmp100
	mov	QWORD PTR 24[rax], rbx	# <retval>,
	mov	rcx, QWORD PTR -32[rbp]	# tmp101, exmaple
	mov	rbx, QWORD PTR -24[rbp]	#, exmaple
	mov	QWORD PTR 32[rax], rcx	# <retval>, tmp101
	mov	QWORD PTR 40[rax], rbx	# <retval>,
# Asm/main.c:17: }
	mov	rax, QWORD PTR -72[rbp]	#, .result_ptr
	mov	rbx, QWORD PTR -8[rbp]	#,
	leave	
	.cfi_def_cfa 7, 8
	ret	
	.cfi_endproc
.LFE0:
	.size	retexmp, .-retexmp
	.section	.rodata
.LC0:
	.string	"%i"
	.text
	.globl	main
	.type	main, @function
main:
.LFB1:
	.cfi_startproc
	push	rbp	#
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp	#,
	.cfi_def_cfa_register 6
	sub	rsp, 64	#,
# Asm/main.c:19: int main(){
	mov	rax, QWORD PTR fs:40	# tmp106, MEM[(<address-space-1> long unsigned int *)40B]
	mov	QWORD PTR -8[rbp], rax	# D.3258, tmp106
	xor	eax, eax	# tmp106
# Asm/main.c:20:     struct Example exmp = retexmp();
	lea	rax, -64[rbp]	# tmp107,
	mov	rdi, rax	#, tmp107
	mov	eax, 0	#,
	call	retexmp	#
# Asm/main.c:21:     printf("%c", exmp.a);
	movzx	eax, BYTE PTR -64[rbp]	# _1, exmp.a
# Asm/main.c:21:     printf("%c", exmp.a);
	movsx	eax, al	# _2, _1
	mov	edi, eax	#, _2
	call	putchar@PLT	#
# Asm/main.c:22:     printf("%i", exmp.b);
	mov	eax, DWORD PTR -60[rbp]	# _3, exmp.b
	mov	esi, eax	#, _3
	lea	rax, .LC0[rip]	# tmp108,
	mov	rdi, rax	#, tmp108
	mov	eax, 0	#,
	call	printf@PLT	#
# Asm/main.c:23:     printf("%i", exmp.c);
	movzx	eax, WORD PTR -56[rbp]	# _4, exmp.c
# Asm/main.c:23:     printf("%i", exmp.c);
	cwde
	mov	esi, eax	#, _5
	lea	rax, .LC0[rip]	# tmp109,
	mov	rdi, rax	#, tmp109
	mov	eax, 0	#,
	call	printf@PLT	#
# Asm/main.c:24:     printf("%i", exmp.d);
	mov	eax, DWORD PTR -52[rbp]	# _6, exmp.d
	mov	esi, eax	#, _6
	lea	rax, .LC0[rip]	# tmp110,
	mov	rdi, rax	#, tmp110
	mov	eax, 0	#,
	call	printf@PLT	#
	mov	eax, 0	# _14,
# Asm/main.c:25: }
	mov	rdx, QWORD PTR -8[rbp]	# tmp112, D.3258
	sub	rdx, QWORD PTR fs:40	# tmp112, MEM[(<address-space-1> long unsigned int *)40B]
	je	.L5	#,
	call	__stack_chk_fail@PLT	#
.L5:
	leave	
	.cfi_def_cfa 7, 8
	ret	
	.cfi_endproc
.LFE1:
	.size	main, .-main
	.ident	"GCC: (GNU) 14.2.1 20250207"
	.section	.note.GNU-stack,"",@progbits
