C x86_64/gcm-hash.asm

ifelse(`
   Copyright (C) 2022 Niels Möller

   This file is part of GNU Nettle.

   GNU Nettle is free software: you can redistribute it and/or
   modify it under the terms of either:

     * the GNU Lesser General Public License as published by the Free
       Software Foundation; either version 3 of the License, or (at your
       option) any later version.

   or

     * the GNU General Public License as published by the Free
       Software Foundation; either version 2 of the License, or (at your
       option) any later version.

   or both in parallel, as here.

   GNU Nettle is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   General Public License for more details.

   You should have received copies of the GNU General Public License and
   the GNU Lesser General Public License along with this program.  If
   not, see http://www.gnu.org/licenses/.
')

C Common registers

define(`KEY', `%rdi')
define(`P', `%xmm0')
define(`BSWAP', `%xmm1')
define(`H', `%xmm2')
define(`D', `%xmm3')
define(`T', `%xmm4')

    C void gcm_init_key (union gcm_block *table)

PROLOGUE(_nettle_gcm_init_key)
define(`MASK', `%xmm5')
	W64_ENTRY(1, 6)
	movdqa	.Lpolynomial(%rip), P
	movdqa	.Lbswap(%rip), BSWAP
	movups	2048(KEY), H	C Middle element
	pshufb	BSWAP, H
	C Multiply by x mod P, which is a left shift.
	movdqa	H, T
	psllq	$1, T
	psrlq	$63, H		C 127 --> 64, 63 --> 0
	pshufd	$0xaa, H, MASK	C 64 --> (96, 64, 32, 0)
	pslldq	$8, H		C 0 --> 64
	por	T, H
	pxor	T, T
	psubd	MASK, T		C All-ones if bit 127 was set
	pand	P, T
	pxor	T, H
	movups	H, (KEY)

	C Set D = x^{-64} H = {H0, H1} + P1 H0
	pshufd	$0x4e, H, D	C Swap H0, H1
	pclmullqhqdq P, H
	pxor	H, D
	movups	D, 16(KEY)
	W64_EXIT(1, 6)
	ret
undefine(`MASK')
EPILOGUE(_nettle_gcm_init_key)

C Use pclmulqdq, doing one 64x64 --> 127 bit carry-less multiplication,
C with source operands being selected from the halves of two 128-bit registers.
C Variants:
C  pclmullqlqdq low half of both src and destination
C  pclmulhqlqdq low half of src register, high half of dst register
C  pclmullqhqdq high half of src register, low half of dst register
C  pclmulhqhqdq high half of both src and destination

C To do a single block, M0, M1, we need to compute
C
C R = M0 D1 + M1 H1
C F = M0 D0 + M1 H0
C
C Corresponding to x^{-127} M H = R + x^{-64} F
C
C Split F as F = F1 + x^64 F0, then the final reduction is
C
C R + x^{-64} F = R + P1 F0 + x^{64} F0 + F1
C
C In all, 5 pclmulqdq. If we we have enough registers to interleave two blocks,
C final reduction is needed only once, so 9 pclmulqdq for two blocks, etc.
C
C We need one register each for D and H, one for P1, one each for accumulating F
C and R. That uses 5 out of the 16 available xmm registers. If we interleave
C blocks, we need additionan D ang H registers (for powers of the key) and the
C additional message word, but we could perhaps interlave as many as 4, with two
C registers left for temporaries.

define(`X', `%rsi')
define(`LENGTH', `%rdx')
define(`DATA', `%rcx')

define(`R', `%xmm5')
define(`M', `%xmm6')
define(`F', `%xmm7')

    C void gcm_hash (const struct gcm_key *key, union gcm_block *x,
    C                size_t length, const uint8_t *data)

PROLOGUE(_nettle_gcm_hash)
	W64_ENTRY(4, 8)
	movdqa		.Lpolynomial(%rip), P
	movdqa		.Lbswap(%rip), BSWAP
	movups		(KEY), H
	movups		16(KEY), D
	movups		(X), R
	pshufb		BSWAP, R

	sub		$16, LENGTH
	jc		.Lfinal

.Loop:
	movups		(DATA), M
	pshufb		BSWAP, M
.Lblock:
	pxor		M, R
	movdqa		R, M
	movdqa		R, F
	movdqa		R, T
	pclmullqlqdq	D, F 	C D0 * M0
	pclmullqhqdq	D, R	C D1 * M0
	pclmulhqlqdq	H, T	C H0 * M1
	pclmulhqhqdq	H, M	C H1 * M1
	pxor		T, F
	pxor		M, R

	pshufd		$0x4e, F, T		C Swap halves of F
	pxor		T, R
	pclmullqhqdq	P, F
	pxor		F, R

	add		$16, DATA
	sub		$16, LENGTH
	jnc		.Loop
.Lfinal:
	add		$16, LENGTH
	jnz		.Lpartial

	pshufb		BSWAP, R
	movups		R, (X)
	W64_EXIT(4, 8)
	ret

.Lpartial:
	C Copy zero padded to stack
	mov		%rsp, %r8
	sub		$16, %rsp
	pxor		M, M
	movups		M, (%rsp)
.Lread_loop:
	movb		(DATA), %al
	sub		$1, %r8
	movb		%al, (%r8)
	add		$1, DATA
	sub		$1, LENGTH
	jnz		.Lread_loop

	C Move into M register, jump into loop with LENGTH = 0
	movups		(%rsp), M
	add		$16, %rsp
	jmp		.Lblock

EPILOGUE(_nettle_gcm_hash)

	RODATA
	C The GCM polynomial is x^{128} + x^7 + x^2 + x + 1,
	C but in bit-reversed representation, that is
	C P = x^{128}+ x^{127} + x^{126} + x^{121} + 1
	C We will mainly use the middle part,
	C P1 = (P + a + x^{128}) / x^64 = x^{563} + x^{62} + x^{57}
	ALIGN(16)
.Lpolynomial:
	.byte 1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0xC2
.Lbswap:
	.byte 15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0
