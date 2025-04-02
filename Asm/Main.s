	.file	"main.c"
	.text
	.globl	main
	.def	main;	.scl	2;	.type	32;	.endef
main:
	pushq	%rbp
	movq	%rsp, %rbp
	subq	$48, %rsp
	call	__main
	movl	$90, -4(%rbp)
	movl	$80, -8(%rbp)
	movl	-4(%rbp), %eax
	leave
	ret
	.def	__main;	.scl	2;	.type	32;	.endef
	.ident	"GCC: (GNU) 14.2.0"
