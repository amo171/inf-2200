	.file	"main.c"
	.text
.Ltext0:
	.globl	c_function
	.type	c_function, @function
c_function:
.LFB2:
	.file 1 "main.c"
	.loc 1 10 0
	.cfi_startproc
	pushl	%ebp
	.cfi_def_cfa_offset 8
	.cfi_offset 5, -8
	movl	%esp, %ebp
	.cfi_def_cfa_register 5
	subl	$16, %esp
1:	call	mcount
	.loc 1 13 0
	movl	$2, -8(%ebp)
	jmp	.L2
.L6:
	.loc 1 14 0
	movl	-8(%ebp), %eax
	leal	0(,%eax,4), %edx
	movl	8(%ebp), %eax
	addl	%edx, %eax
	movl	(%eax), %eax
	testl	%eax, %eax
	je	.L3
	.loc 1 15 0
	movl	-8(%ebp), %eax
	addl	%eax, %eax
	movl	%eax, -4(%ebp)
	jmp	.L4
.L5:
	.loc 1 16 0 discriminator 3
	movl	-4(%ebp), %eax
	leal	0(,%eax,4), %edx
	movl	8(%ebp), %eax
	addl	%edx, %eax
	movl	$0, (%eax)
	.loc 1 15 0 discriminator 3
	movl	-8(%ebp), %eax
	addl	%eax, -4(%ebp)
.L4:
	.loc 1 15 0 is_stmt 0 discriminator 1
	movl	-4(%ebp), %eax
	cmpl	12(%ebp), %eax
	jl	.L5
.L3:
	.loc 1 13 0 is_stmt 1 discriminator 2
	addl	$1, -8(%ebp)
.L2:
	.loc 1 13 0 is_stmt 0 discriminator 1
	movl	-8(%ebp), %eax
	cmpl	12(%ebp), %eax
	jl	.L6
	.loc 1 21 0 is_stmt 1
	nop
	leave
	.cfi_restore 5
	.cfi_def_cfa 4, 4
	ret
	.cfi_endproc
.LFE2:
	.size	c_function, .-c_function
	.globl	fillarray
	.type	fillarray, @function
fillarray:
.LFB3:
	.loc 1 28 0
	.cfi_startproc
	pushl	%ebp
	.cfi_def_cfa_offset 8
	.cfi_offset 5, -8
	movl	%esp, %ebp
	.cfi_def_cfa_register 5
	subl	$16, %esp
1:	call	mcount
	.loc 1 30 0
	movl	$0, -4(%ebp)
	jmp	.L8
.L9:
	.loc 1 31 0 discriminator 3
	movl	-4(%ebp), %eax
	leal	0(,%eax,4), %edx
	movl	8(%ebp), %eax
	addl	%edx, %eax
	movl	$1, (%eax)
	.loc 1 30 0 discriminator 3
	addl	$1, -4(%ebp)
.L8:
	.loc 1 30 0 is_stmt 0 discriminator 1
	movl	-4(%ebp), %eax
	cmpl	12(%ebp), %eax
	jl	.L9
	.loc 1 32 0 is_stmt 1
	nop
	leave
	.cfi_restore 5
	.cfi_def_cfa 4, 4
	ret
	.cfi_endproc
.LFE3:
	.size	fillarray, .-fillarray
	.section	.rodata
.LC0:
	.string	"%d - "
	.text
	.globl	test_print
	.type	test_print, @function
test_print:
.LFB4:
	.loc 1 33 0
	.cfi_startproc
	pushl	%ebp
	.cfi_def_cfa_offset 8
	.cfi_offset 5, -8
	movl	%esp, %ebp
	.cfi_def_cfa_register 5
	subl	$24, %esp
1:	call	mcount
	.loc 1 35 0
	movl	$0, -12(%ebp)
	jmp	.L11
.L13:
	.loc 1 36 0
	movl	-12(%ebp), %eax
	leal	0(,%eax,4), %edx
	movl	8(%ebp), %eax
	addl	%edx, %eax
	movl	(%eax), %eax
	testl	%eax, %eax
	je	.L12
	.loc 1 37 0
	subl	$8, %esp
	pushl	-12(%ebp)
	pushl	$.LC0
	call	printf
	addl	$16, %esp
.L12:
	.loc 1 35 0 discriminator 2
	addl	$1, -12(%ebp)
.L11:
	.loc 1 35 0 is_stmt 0 discriminator 1
	movl	-12(%ebp), %eax
	cmpl	12(%ebp), %eax
	jl	.L13
	.loc 1 39 0 is_stmt 1
	nop
	leave
	.cfi_restore 5
	.cfi_def_cfa 4, 4
	ret
	.cfi_endproc
.LFE4:
	.size	test_print, .-test_print
	.section	.rodata
.LC1:
	.string	"fail"
.LC2:
	.string	"Arrays are equal"
	.text
	.globl	compare_function
	.type	compare_function, @function
compare_function:
.LFB5:
	.loc 1 41 0
	.cfi_startproc
	pushl	%ebp
	.cfi_def_cfa_offset 8
	.cfi_offset 5, -8
	movl	%esp, %ebp
	.cfi_def_cfa_register 5
	subl	$24, %esp
1:	call	mcount
	.loc 1 43 0
	movl	$0, -12(%ebp)
	.loc 1 44 0
	movl	$0, -16(%ebp)
	jmp	.L15
.L19:
	.loc 1 45 0
	movl	-16(%ebp), %eax
	leal	0(,%eax,4), %edx
	movl	8(%ebp), %eax
	addl	%edx, %eax
	movl	(%eax), %edx
	movl	-16(%ebp), %eax
	leal	0(,%eax,4), %ecx
	movl	12(%ebp), %eax
	addl	%ecx, %eax
	movl	(%eax), %eax
	cmpl	%eax, %edx
	je	.L16
	.loc 1 48 0
	movl	$1, -12(%ebp)
.L16:
	.loc 1 49 0
	cmpl	$0, -12(%ebp)
	je	.L17
	.loc 1 50 0
	subl	$12, %esp
	pushl	$.LC1
	call	puts
	addl	$16, %esp
	.loc 1 51 0
	jmp	.L18
.L17:
	.loc 1 44 0 discriminator 2
	addl	$1, -16(%ebp)
.L15:
	.loc 1 44 0 is_stmt 0 discriminator 1
	movl	-16(%ebp), %eax
	cmpl	16(%ebp), %eax
	jl	.L19
.L18:
	.loc 1 54 0 is_stmt 1
	cmpl	$0, -12(%ebp)
	jne	.L21
	.loc 1 55 0
	subl	$12, %esp
	pushl	$.LC2
	call	puts
	addl	$16, %esp
.L21:
	.loc 1 57 0
	nop
	leave
	.cfi_restore 5
	.cfi_def_cfa 4, 4
	ret
	.cfi_endproc
.LFE5:
	.size	compare_function, .-compare_function
	.section	.rodata
.LC3:
	.string	"fillarray"
.LC4:
	.string	"endfill"
	.text
	.globl	main
	.type	main, @function
main:
.LFB6:
	.loc 1 58 0
	.cfi_startproc
	leal	4(%esp), %ecx
	.cfi_def_cfa 1, 0
	andl	$-16, %esp
	pushl	-4(%ecx)
	pushl	%ebp
	.cfi_escape 0x10,0x5,0x2,0x75,0
	movl	%esp, %ebp
	pushl	%ecx
	.cfi_escape 0xf,0x3,0x75,0x7c,0x6
	subl	$20, %esp
1:	call	mcount
	movl	%ecx, %eax
	.loc 1 60 0
	movl	4(%eax), %eax
	addl	$4, %eax
	movl	(%eax), %eax
	subl	$12, %esp
	pushl	%eax
	call	atoi
	addl	$16, %esp
	movl	%eax, -20(%ebp)
	.loc 1 65 0
	movl	-20(%ebp), %eax
	sall	$2, %eax
	subl	$12, %esp
	pushl	%eax
	call	malloc
	addl	$16, %esp
	movl	%eax, -16(%ebp)
	.loc 1 66 0
	movl	-20(%ebp), %eax
	sall	$2, %eax
	subl	$12, %esp
	pushl	%eax
	call	malloc
	addl	$16, %esp
	movl	%eax, -12(%ebp)
	.loc 1 68 0
	subl	$12, %esp
	pushl	$.LC3
	call	puts
	addl	$16, %esp
	.loc 1 69 0
	subl	$8, %esp
	pushl	-20(%ebp)
	pushl	-12(%ebp)
	call	fillarray
	addl	$16, %esp
	.loc 1 70 0
	subl	$8, %esp
	pushl	-20(%ebp)
	pushl	-16(%ebp)
	call	fillarray
	addl	$16, %esp
	.loc 1 71 0
	subl	$12, %esp
	pushl	$.LC4
	call	puts
	addl	$16, %esp
	.loc 1 73 0
	subl	$8, %esp
	pushl	-20(%ebp)
	pushl	-16(%ebp)
	call	c_function
	addl	$16, %esp
	.loc 1 85 0
	nop
	movl	-4(%ebp), %ecx
	.cfi_def_cfa 1, 0
	leave
	.cfi_restore 5
	leal	-4(%ecx), %esp
	.cfi_def_cfa 4, 4
	ret
	.cfi_endproc
.LFE6:
	.size	main, .-main
.Letext0:
	.file 2 "/usr/include/bits/types.h"
	.file 3 "/usr/include/time.h"
	.section	.debug_info,"",@progbits
.Ldebug_info0:
	.long	0x246
	.value	0x4
	.long	.Ldebug_abbrev0
	.byte	0x4
	.uleb128 0x1
	.long	.LASF29
	.byte	0xc
	.long	.LASF30
	.long	.LASF31
	.long	.Ltext0
	.long	.Letext0-.Ltext0
	.long	.Ldebug_line0
	.uleb128 0x2
	.byte	0x4
	.byte	0x7
	.long	.LASF0
	.uleb128 0x2
	.byte	0x1
	.byte	0x8
	.long	.LASF1
	.uleb128 0x2
	.byte	0x2
	.byte	0x7
	.long	.LASF2
	.uleb128 0x2
	.byte	0x4
	.byte	0x7
	.long	.LASF3
	.uleb128 0x2
	.byte	0x1
	.byte	0x6
	.long	.LASF4
	.uleb128 0x2
	.byte	0x2
	.byte	0x5
	.long	.LASF5
	.uleb128 0x3
	.byte	0x4
	.byte	0x5
	.string	"int"
	.uleb128 0x2
	.byte	0x8
	.byte	0x5
	.long	.LASF6
	.uleb128 0x2
	.byte	0x8
	.byte	0x7
	.long	.LASF7
	.uleb128 0x2
	.byte	0x4
	.byte	0x5
	.long	.LASF8
	.uleb128 0x2
	.byte	0x4
	.byte	0x7
	.long	.LASF9
	.uleb128 0x4
	.long	.LASF11
	.byte	0x2
	.byte	0x8b
	.long	0x64
	.uleb128 0x5
	.byte	0x4
	.long	0x83
	.uleb128 0x2
	.byte	0x1
	.byte	0x6
	.long	.LASF10
	.uleb128 0x5
	.byte	0x4
	.long	0x4f
	.uleb128 0x4
	.long	.LASF12
	.byte	0x3
	.byte	0x4b
	.long	0x72
	.uleb128 0x6
	.long	.LASF15
	.byte	0x1
	.byte	0xa
	.long	.LFB2
	.long	.LFE2-.LFB2
	.uleb128 0x1
	.byte	0x9c
	.long	0xe5
	.uleb128 0x7
	.long	.LASF13
	.byte	0x1
	.byte	0xa
	.long	0x8a
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x7
	.long	.LASF14
	.byte	0x1
	.byte	0xa
	.long	0x4f
	.uleb128 0x2
	.byte	0x91
	.sleb128 4
	.uleb128 0x8
	.string	"i"
	.byte	0x1
	.byte	0xb
	.long	0x4f
	.uleb128 0x2
	.byte	0x91
	.sleb128 -16
	.uleb128 0x8
	.string	"j"
	.byte	0x1
	.byte	0xb
	.long	0x4f
	.uleb128 0x2
	.byte	0x91
	.sleb128 -12
	.byte	0
	.uleb128 0x6
	.long	.LASF16
	.byte	0x1
	.byte	0x1c
	.long	.LFB3
	.long	.LFE3-.LFB3
	.uleb128 0x1
	.byte	0x9c
	.long	0x123
	.uleb128 0x7
	.long	.LASF13
	.byte	0x1
	.byte	0x1c
	.long	0x8a
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x7
	.long	.LASF14
	.byte	0x1
	.byte	0x1c
	.long	0x4f
	.uleb128 0x2
	.byte	0x91
	.sleb128 4
	.uleb128 0x8
	.string	"i"
	.byte	0x1
	.byte	0x1d
	.long	0x4f
	.uleb128 0x2
	.byte	0x91
	.sleb128 -12
	.byte	0
	.uleb128 0x9
	.long	.LASF17
	.byte	0x1
	.byte	0x21
	.long	.LFB4
	.long	.LFE4-.LFB4
	.uleb128 0x1
	.byte	0x9c
	.long	0x161
	.uleb128 0x7
	.long	.LASF13
	.byte	0x1
	.byte	0x21
	.long	0x8a
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x7
	.long	.LASF14
	.byte	0x1
	.byte	0x21
	.long	0x4f
	.uleb128 0x2
	.byte	0x91
	.sleb128 4
	.uleb128 0x8
	.string	"i"
	.byte	0x1
	.byte	0x22
	.long	0x4f
	.uleb128 0x2
	.byte	0x91
	.sleb128 -20
	.byte	0
	.uleb128 0x9
	.long	.LASF18
	.byte	0x1
	.byte	0x29
	.long	.LFB5
	.long	.LFE5-.LFB5
	.uleb128 0x1
	.byte	0x9c
	.long	0x1bb
	.uleb128 0x7
	.long	.LASF19
	.byte	0x1
	.byte	0x29
	.long	0x8a
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x7
	.long	.LASF20
	.byte	0x1
	.byte	0x29
	.long	0x8a
	.uleb128 0x2
	.byte	0x91
	.sleb128 4
	.uleb128 0x7
	.long	.LASF14
	.byte	0x1
	.byte	0x29
	.long	0x4f
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0x8
	.string	"i"
	.byte	0x1
	.byte	0x2a
	.long	0x4f
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.uleb128 0xa
	.long	.LASF21
	.byte	0x1
	.byte	0x2b
	.long	0x4f
	.uleb128 0x2
	.byte	0x91
	.sleb128 -20
	.byte	0
	.uleb128 0x9
	.long	.LASF22
	.byte	0x1
	.byte	0x3a
	.long	.LFB6
	.long	.LFE6-.LFB6
	.uleb128 0x1
	.byte	0x9c
	.long	0x243
	.uleb128 0x7
	.long	.LASF23
	.byte	0x1
	.byte	0x3a
	.long	0x4f
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0x7
	.long	.LASF24
	.byte	0x1
	.byte	0x3a
	.long	0x243
	.uleb128 0x2
	.byte	0x91
	.sleb128 4
	.uleb128 0xa
	.long	.LASF14
	.byte	0x1
	.byte	0x3c
	.long	0x4f
	.uleb128 0x2
	.byte	0x75
	.sleb128 -20
	.uleb128 0xa
	.long	.LASF19
	.byte	0x1
	.byte	0x3d
	.long	0x8a
	.uleb128 0x2
	.byte	0x75
	.sleb128 -12
	.uleb128 0xa
	.long	.LASF20
	.byte	0x1
	.byte	0x3e
	.long	0x8a
	.uleb128 0x2
	.byte	0x75
	.sleb128 -16
	.uleb128 0xb
	.long	.LASF25
	.byte	0x1
	.byte	0x3f
	.long	0x90
	.uleb128 0xb
	.long	.LASF26
	.byte	0x1
	.byte	0x3f
	.long	0x90
	.uleb128 0xb
	.long	.LASF27
	.byte	0x1
	.byte	0x40
	.long	0x90
	.uleb128 0xb
	.long	.LASF28
	.byte	0x1
	.byte	0x40
	.long	0x90
	.byte	0
	.uleb128 0x5
	.byte	0x4
	.long	0x7d
	.byte	0
	.section	.debug_abbrev,"",@progbits
.Ldebug_abbrev0:
	.uleb128 0x1
	.uleb128 0x11
	.byte	0x1
	.uleb128 0x25
	.uleb128 0xe
	.uleb128 0x13
	.uleb128 0xb
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x1b
	.uleb128 0xe
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x6
	.uleb128 0x10
	.uleb128 0x17
	.byte	0
	.byte	0
	.uleb128 0x2
	.uleb128 0x24
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x3e
	.uleb128 0xb
	.uleb128 0x3
	.uleb128 0xe
	.byte	0
	.byte	0
	.uleb128 0x3
	.uleb128 0x24
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x3e
	.uleb128 0xb
	.uleb128 0x3
	.uleb128 0x8
	.byte	0
	.byte	0
	.uleb128 0x4
	.uleb128 0x16
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x5
	.uleb128 0xf
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x6
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x27
	.uleb128 0x19
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x6
	.uleb128 0x40
	.uleb128 0x18
	.uleb128 0x2117
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x7
	.uleb128 0x5
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x8
	.uleb128 0x34
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x9
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x27
	.uleb128 0x19
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x6
	.uleb128 0x40
	.uleb128 0x18
	.uleb128 0x2116
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0xa
	.uleb128 0x34
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0xb
	.uleb128 0x34
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.byte	0
	.section	.debug_aranges,"",@progbits
	.long	0x1c
	.value	0x2
	.long	.Ldebug_info0
	.byte	0x4
	.byte	0
	.value	0
	.value	0
	.long	.Ltext0
	.long	.Letext0-.Ltext0
	.long	0
	.long	0
	.section	.debug_line,"",@progbits
.Ldebug_line0:
	.section	.debug_str,"MS",@progbits,1
.LASF25:
	.string	"before_c"
.LASF26:
	.string	"after_c"
.LASF18:
	.string	"compare_function"
.LASF29:
	.string	"GNU C11 5.4.0 20160609 -m32 -masm=att -mtune=generic -march=i686 -g -O0 -p -fstack-protector-strong"
.LASF28:
	.string	"after_asm"
.LASF1:
	.string	"unsigned char"
.LASF3:
	.string	"long unsigned int"
.LASF2:
	.string	"short unsigned int"
.LASF19:
	.string	"asmprimes"
.LASF27:
	.string	"before_asm"
.LASF20:
	.string	"cprimes"
.LASF11:
	.string	"__time_t"
.LASF5:
	.string	"short int"
.LASF22:
	.string	"main"
.LASF16:
	.string	"fillarray"
.LASF0:
	.string	"unsigned int"
.LASF7:
	.string	"long long unsigned int"
.LASF13:
	.string	"primes"
.LASF12:
	.string	"time_t"
.LASF23:
	.string	"argc"
.LASF9:
	.string	"sizetype"
.LASF6:
	.string	"long long int"
.LASF30:
	.string	"main.c"
.LASF10:
	.string	"char"
.LASF14:
	.string	"LIMIT"
.LASF31:
	.string	"/home/andy/Oblig/2200-oblig/assign 1/ahe103-p1/src"
.LASF17:
	.string	"test_print"
.LASF24:
	.string	"argv"
.LASF15:
	.string	"c_function"
.LASF8:
	.string	"long int"
.LASF4:
	.string	"signed char"
.LASF21:
	.string	"fail"
	.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.2) 5.4.0 20160609"
	.section	.note.GNU-stack,"",@progbits
