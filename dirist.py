#!/usr/bin/env python3
# 2020/05/03: Created & shared on github.com/soft9000/Dirist.
# STATUS: *** Final Test ****

# Note: Our use of f-strings requires Python 3.6, or greater!

''' Dirist: Examine a folder hirearchy, gathering a finite list
of small / large trees that match a set commonly-required,
selection criteria. Includes a Command Line Interface (CLI.)
'''

import os
import os.path
import sys
from collections import OrderedDict
import datetime as dt

class DirEntry:
    ''' Keep track of contained totals for members '''
    MAX = 0xffffffff

    def __init__(self, fq_name):
        self.name  = fq_name
        self.sigma = 0
        self.tally = 0
        self.oldest = DirEntry.MAX
        self.newest = 0

    def is_member(self, fq_name):
        ''' Check to see if the file is part of this entry '''
        if fq_name.find(self.name) == 0:
            return True
        return False

    def collect(self, fq_name):
        ''' 
        Collect file information - returns False if file is
        not a member, else True upon data collection '''
        if not self.is_member(fq_name):
            return False
        try:
            stat_info = os.stat(fq_name, follow_symlinks=False)
            if stat_info.st_mtime < self.oldest:
                self.oldest = stat_info.st_mtime
            if stat_info.st_mtime > self.newest:
                self.newest = stat_info.st_mtime
            self.sigma += stat_info.st_size
            self.tally += 1
            return True
        except:
            return False


class Dirist:
    '''
    Scan a folder hierarchy, selecting the top 'n' set of
    older / newer files.
    '''
    def __init__(self, root='.'):
        ''' The root folder to scan, as well as an ending
        character sequence to match.'''
        if not root.endswith(os.path.sep):
            root += os.path.sep
        self._root = root
        self._depth = root.count(os.path.sep)
        self.results = {}
        self.errors = 0
        self.total = 0
        self.show_errors_ = False
        self.show_verbose_= False

    @staticmethod
    def format(st_time):
        if st_time and st_time != DirEntry.MAX:
            time_ = dt.datetime.fromtimestamp(st_time)
            return time_.strftime("%Y-%m-%d, %H:%M")
        return "(ignored)"

    def _cleanup(self):
        ''' Extract final report, and prep for next usage.
        '''
        results = []
        for key in self.results:
            zrow = OrderedDict()
            node = self.results[key]
            zrow["name"]   = node.name
            zrow["bytes"]  = node.sigma
            zrow["files"]  = node.tally
            zrow["oldest"] = Dirist.format(node.oldest)
            zrow["newest"] = Dirist.format(node.newest)
            results.append(zrow)
        self.results.clear()
        return results

    def show_errors(self, bOn=True):
        self.show_errors_ = bOn

    def show_verbose(self, bOn=True):
        self.show_verbose_ = bOn

    def on_error(self, file):
        self.errors += 1
        if self.show_errors_:
            print(f'\n *** Stat Error {self.errors}: {file}', file=sys.stderr)
            sys.stderr.flush()

    def on_success(self, file):
        if self.show_verbose_:
            print(".", end='')
            sys.stdout.flush()

    def on_define(self, root):
        self.results[root] = DirEntry(root)
        if self.show_verbose_:
            print("+", end='')
            sys.stdout.flush()

    def normalize(self, root):
        nodes = root.split(os.path.sep)
        path = ''
        for node in nodes[0:self._depth]:
            path += node + os.path.sep
        if not path.endswith(os.path.sep):
            path = path + os.path.sep
        return path

    def _setup(self):
        self.results = {}
        self.errors = 0
        self.total  = 0
        for root, dirs, nodes in os.walk(self._root):
            for dir in dirs:
                effective = root + dir
                self.on_define(effective)
            break # first set, only.
        if not self.results:
            self.on_define(self._root)
                            
    def locate(self):
        ''' Single interface to tree-tally & collection activities. '''
        self._setup()
        for root, dirs, nodes in os.walk(self._root):
            for node in nodes:
                self.total += 1
                effective = self.normalize(root)
                file = root + node
                for key in self.results:
                    row = self.results[key]
                    if row.is_member(file):
                        if row.collect(file):
                            self.on_success(file)
                        else:
                            self.on_error(file)
                        break
 
        print()
        return self._cleanup()

if __name__ == '__main__':
    ''' Official C.L.I. '''
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder", help="Folder search (else pwd.)")
    parser.add_argument("-e", "--errors", action='store_true', help="Errors to stderr.")
    parser.add_argument("-v", "--verbose", action='store_true', help="Show standard output.")
    
    parsed = parser.parse_args()
    #parsed = parser.parse_args(["-f", "c:\\d_drive\\USR\\code\Python3"])

    if not parsed.folder:
        parsed.folder = os.getcwd()

    walker = Dirist(parsed.folder)
    walker.show_errors(parsed.errors)
    walker.show_verbose(parsed.verbose)
    bFirst = True
    for row in walker.locate():
        if bFirst:
            print(*row.keys(), sep='|')
            bFirst = False
        print(*row.values(), sep='|')
    print()
    sys.stdout.flush()
    sys.stderr.flush()
    # print(f'Total: {walker.total}, No-Stat: {walker.errors}', file=sys.stderr)
    # print("(done)", file=sys.stderr)
 
