#!/usr/bin/env python3
'''
Program to continuously copy a tree of arbitrary
information over to another location.
'''

import os, time, random
import shutil

source = "/tmp/dumb"
dest = "/media/profnagy/bashme"

def doJunker(times, source):
    _bytes = bytes(b'\0x00ff' * 512)
    print(type(_bytes))
    for time in range(0, times):
        with open(f"{source}/{os.getpid()}-junker-{time}", "w") as fh:
            for i in range(8):
                print(*_bytes, file=fh, sep='', end='')


def doCopy(count, source, dest):
    print(time.asctime(time.localtime(time.time())), "Copying", source, end='')
    count += 1
    tree = dest + '/' + str(time.time())
    while os.path.exists(tree):
        time.sleep(random.randrange(1, 8))
        tree = dest + '/' + str(time.time())
    print(" to", tree)
    shutil.copytree(source, tree)
    return count


def doMain():
    try:
        doJunker(10, source)
        copy = 0
        while True:
            copy = doCopy(copy, source, dest)
    except Exception as reason:
        print(reason)
    finally:
        pass

if __name__ == "__main__":
    doMain()
    
