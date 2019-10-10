#!/usr/bin/env python3
'''
Program to continuously copy a tree of arbitrary
information over to another location. Designed to
work with several others, so as to increase the
completion rate, on a mountable volume.
'''

import os, time, random
import shutil
from io import BytesIO as BytesIO

source = "/tmp/dumb"
dest = "/media/profnagy/bashme"

def doJunker(times, source):
    _bytes = bytes([0xfe, 0xff])
    for time in range(0, times):
        with open(f"{source}/{os.getpid()}-junker-{time}", 'wb') as fh:
            for i in range(204800):
               fh.write(_bytes)


def doCopy(source, dest):
    print(time.asctime(time.localtime(time.time())), "Copying", source, end='')
    tree = dest + '/' + str(time.time())
    while os.path.exists(tree):
        time.sleep(random.randrange(1, 8))
        tree = dest + '/' + str(time.time())
    print(" to", tree)
    shutil.copytree(source, tree)


def doMain():
    try:
        doJunker(10, source)

        while True:
            doCopy(source, dest)
    except Exception as reason:
        print(reason)
    finally:
        pass

if __name__ == "__main__":
    doMain()
    
