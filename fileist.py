#!/usr/bin/env python3
# 2019/07/08: Created & shared.

import os
import os.path
import sys
import datetime as dt

class Fileist:
    '''
    Scan a folder hierarchy, selecting the top 'n' set of
    older / newer files.
    '''
    def __init__(self, root='.', suffix=''):
        ''' The root folder to scan, as well as an ending
        character sequence to match.'''
        self.root = root
        self.results = []
        self.suffix = suffix.lower()

    def _cleanup(self):
        ''' Format the final date and time, and prep for next usage. '''
        results = []
        for result in self.results:
            ztime = dt.datetime.fromtimestamp(result[1])
            results.append([result[0], ztime.strftime("%d %m %Y, %H:%M")])
        self.results.clear()
        return results

    def locate(self, max_=25, newest=True):
        ''' Single interface to file-location & collection activities. '''
        for root, dirs, nodes in os.walk(self.root):
            for node in nodes:
                match = node.lower()
                if not match.endswith(self.suffix):
                    continue;
                file = root + os.path.sep + node
                try:
                    st = os.stat(file, follow_symlinks=False)
                except:
                    print('!', end='')
                    continue
                mtime = st.st_mtime
                if len(self.results) < max_:
                    self.results.append((file, mtime))
                    continue
                for ss, node in enumerate(self.results):
                    should = node[1] < mtime                    
                    if not newest:
                        should = not should
                    if should:
                        self.results.insert(ss, (file, mtime))
                        print('.', end='')
                        break
                if len(self.results) > max_:
                    self.results.pop(max_)
            sys.stdout.flush()
        print()
        return self._cleanup()

if __name__ == '__main__':
    ''' Official command-line interface. '''
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder", help="Folder search (else pwd.)")
    parser.add_argument("-l", "--list", type=int, help="Number to list.")
    parser.add_argument("-o", "--oldest", action='store_true', help="Oldest, not newest.")
    parser.add_argument("-x", "--chop", action='store_true', help="Chop to fit screen.")
    parser.add_argument("-s", "--suffix", help="File suffix (case ignored.)")
    parsed = parser.parse_args()
    if not parsed.folder:
        parsed.folder = '.'
    if not parsed.list:
        parsed.list = 25
    if not parsed.suffix:
        parsed.suffix = ''
    walker = Fileist(parsed.folder, suffix=parsed.suffix)
    for ss, info in enumerate(walker.locate(max_=parsed.list, newest=not parsed.oldest), 1):
        if parsed.chop and len(info[0]) > 50:
            info[0] = '...' + info[0][-50:]
        print(f'{ss}\t{info[1]}: {info[0]}')


