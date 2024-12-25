#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template --host network-task.ctf74.ru --port 30255
from pwn import *

port = int(args.PORT or 30255)

def start_remote(argv=[], *a, **kw):
    '''Connect to the process on the remote host'''
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)


#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
import random
io = start()


io.readuntilS('\n')
io.readuntilS('\n')
k = 10**31
io.sendline(str(k).encode())
numbers = [int(num) for num in io.readuntilS('\n').split() if num.isdigit()]
maxBulls = numbers[0]

for place in range(32):
    for digit in range(1, 10):
        v = k + digit * 10 ** place
        io.sendline(str(v).encode())
        mbull = [int(num) for num in io.readuntilS('\n').split() if num.isdigit()]
        if mbull and mbull[0] > maxBulls:
            k = v
            digit = 0
            maxBulls = mbull[0]
            break
    if digit > 0:
        print('SS', place)
io.interactive()