C s390x/fat/gcm-hash.asm

ifelse(`
   Copyright (C) 2020 Mamone Tarsha

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

dnl picked up by configure
dnl PROLOGUE(_nettle_fat_gcm_init_key)
dnl PROLOGUE(_nettle_fat_gcm_hash)

define(`fat_transform', `$1_s390x')
include_src(`s390x/msa_x4/gcm-hash.asm')
