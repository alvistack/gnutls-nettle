/* base64.h
 *
 * "ASCII armor" codecs.
 */

/* nettle, low-level cryptographics library
 *
 * Copyright (C) 2002 Niels M�ller, Dan Egnor
 *  
 * The nettle library is free software; you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation; either version 2.1 of the License, or (at your
 * option) any later version.
 * 
 * The nettle library is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 * or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
 * License for more details.
 * 
 * You should have received a copy of the GNU Lesser General Public License
 * along with the nettle library; see the file COPYING.LIB.  If not, write to
 * the Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
 * MA 02111-1307, USA.
 */
 
#ifndef NETTLE_BASE64_H_INCLUDED
#define NETTLE_BASE64_H_INCLUDED

#include <inttypes.h>


#define BASE64_BINARY_BLOCK_SIZE 3
#define BASE64_TEXT_BLOCK_SIZE 4

/* Base64 encoding */

/* Maximum length of output for base64_encode_update. NOTE: Doesn't
 * include any padding that base64_encode_final may add. */
/* We have at most 4 buffered bits, and a total of (4 + length * 8) bits. */
#define BASE64_ENCODE_LENGTH(length) (((length) * 8 + 4)/6)

/* Maximum lengbth of output generated by base64_encode_final. */
#define BASE64_ENCODE_FINAL_LENGTH 3

/* Exact length of output generated by base64_encode_raw, including
 * padding. */
#define BASE64_ENCODE_RAW_LENGTH(length) ((((length) + 2)/3)*4)

struct base64_encode_ctx
{
  unsigned word;   /* Leftover bits */
  unsigned bits;  /* Number of bits, always 0, 2, or 4. */
};

void
base64_encode_init(struct base64_encode_ctx *ctx);

/* Encodes a single byte. Returns amoutn of output (always 1 or 2). */
unsigned
base64_encode_single(struct base64_encode_ctx *ctx,
		     uint8_t *dst,
		     uint8_t src);

/* Returns the number of output characters. DST should point to an
 * area of size at least BASE64_ENCODE_LENGTH(length). */
unsigned
base64_encode_update(struct base64_encode_ctx *ctx,
		     uint8_t *dst,
		     unsigned length,
		     const uint8_t *src);

/* DST should point to an area of size at least
 * BASE64_ENCODE_FINAL_SIZE */
unsigned
base64_encode_final(struct base64_encode_ctx *ctx,
		    uint8_t *dst);

/* Lower level functions */

/* Encodes a string in one go, including any padding at the end.
 * Generates exactly BASE64_ENCODE_RAW_LENGTH(length) bytes of output.
 * Supports overlapped operation, if src <= dst. */
void
base64_encode_raw(uint8_t *dst, unsigned length, const uint8_t *src);

void
base64_encode_group(uint8_t *dst, uint32_t group);


/* Base64 decoding */

/* Maximum length of output for base64_decode_update. */
/* We have at most 6 buffered bits, and a total of (length + 1) * 6 bits. */
#define BASE64_DECODE_LENGTH(length) ((((length) + 1) * 6) / 8)

struct base64_decode_ctx
{
  enum
    {
      BASE64_DECODE_OK,
      BASE64_DECODE_ERROR,
      BASE64_DECODE_END
    } status; 
  unsigned word;   /* Leftover bits */
  unsigned bits;   /* Number buffered bits */
};

void
base64_decode_init(struct base64_decode_ctx *ctx);

/* Returns the number of output characters. DST should point to an
 * area of size at least BASE64_DECODE_LENGTH(length). */
unsigned
base64_decode_update(struct base64_decode_ctx *ctx,
		     uint8_t *dst,
		     unsigned length,
		     const uint8_t *src);

/* Returns 1 on success. */
int
base64_decode_status(struct base64_decode_ctx *ctx);

#endif /* NETTLE_BASE64_H_INCLUDED */
