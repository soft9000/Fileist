#!/usr/bin/env python3
# 2019/07/08: Created & shared on github.com/soft9000/Fileist.
# 2019/07/09: Updated to report (MS Windows Test) stat() errors.

# Note: Our use of f-strings requires Python 3.6, or greater!

''' Fileist: Examine a file hirearchy, gathering a finite list
of newest / oldest files that match a set commonly-required,
selection criteria. Includes a Command Line Interface (CLI.)
'''

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
        self.errors = 0
        self.total = 0
        self.show_errors_ = False

    def _cleanup(self):
        ''' Format the final date and time, and prep for next usage. '''
        results = []
        for result in self.results:
            ztime = dt.datetime.fromtimestamp(result[1])
            results.append([result[0], ztime.strftime("%Y-%m-%d, %H:%M")])
        self.results.clear()
        return results

    def _prime(self, file, mtime, newest):
        ''' Build the initial list, in the sorted order. '''
        if not self._prospect(file, mtime, newest):
            self.results.append((file, mtime))

    def _prospect(self, file, mtime, newest):
        ''' Add a file if it belongs in the sorted list.
        No list-size management takes place. False if
        the file is not added, else True.'''
        for ss, node in enumerate(self.results):
            should = node[1] < mtime                    
            if not newest:
                should = not should
            if should:
                self.results.insert(ss, (file, mtime))
                return True
        return False

    def show_errors(self, bOn=True):
        self.show_errors_ = bOn
                            
    def locate(self, max_=25, newest=True):
        ''' Single interface to file-location & collection activities. '''
        self.errors = 0
        self.total  = 0
        for root, dirs, nodes in os.walk(self.root):
            for node in nodes:
                self.total += 1
                match = node.lower()
                if not match.endswith(self.suffix):
                    continue
                file = root + os.path.sep + node
                try:
                    st = os.stat(file, follow_symlinks=False)
                except:
                    self.errors += 1
                    if self.show_errors_:
                        print(f'\n *** Stat Error {self.errors}: {file}', file=sys.stderr)
                        sys.stderr.flush()
                    else:
                        print('!', end='')
                    continue
                mtime = st.st_mtime
                if len(self.results) < max_:
                    self._prime(file, mtime, newest)
                    print('+', end='')
                elif self._prospect(file, mtime, newest):
                    print('.', end='')
                    if len(self.results) > max_:
                        self.results.pop(max_)
            sys.stdout.flush()
        print()
        return self._cleanup()

if __name__ == '__main__':
    ''' Official C.L.I. '''
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder", help="Folder search (else pwd.)")
    parser.add_argument("-l", "--list", type=int, help="Number to list.")
    parser.add_argument("-o", "--oldest", action='store_true', help="Oldest, not newest.")
    parser.add_argument("-e", "--errors", action='store_true', help="Errors to stderr.")
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
    walker.show_errors(parsed.errors)
    for ss, info in enumerate(walker.locate(max_=parsed.list, newest=not parsed.oldest), 1):
        if parsed.chop and len(info[0]) > 50:
            info[0] = '...' + info[0][-50:]
        print(f'{ss}\t{info[1]} - {info[0]}')
    print(f'Total: {walker.total}, No-Stat: {walker.errors}')


