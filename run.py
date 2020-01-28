#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import glob
import itertools
import multiprocessing
import ntpath
import os
import re
import sys

import editdistance
from colorama import Fore, Style

whitespace_regex = re.compile(r"\s+", re.MULTILINE)
username_regex = re.compile('\((.*?)\)')


def remove_whitespace(str):
    return whitespace_regex.sub("", str)


def check(i):
    [[fn1, fc1], [fn2, fc2]] = i
    if fn1 == fn2:
        return
    str1 = remove_whitespace(fc1)
    str2 = remove_whitespace(fc2)
    ans = editdistance.eval(str1, str2)
    perc = min(ans / len(str1), ans / len(str2))
    return [fn1, fn2, ans, perc]


def readfile(f, max):
    if os.path.getsize(f) > max * 1024:
        print("Skipping {}, over {}kB".format(f, max), file=sys.stderr)
    with open(f, 'r', encoding='utf8') as h:
        return [f, h.read()]


def print_result(path1, path2, ans, perc, loyola_format):
    if not loyola_format:
        path1_string = path1
        path2_string = path2
    else:
        short1 = username_regex.findall(path1)[0]
        short2 = username_regex.findall(path2)[0]
        path1_string = ntpath.basename(path1) + ' | ' + short1
        path2_string = ntpath.basename(path2) + ' | ' + short2
    print(Fore.CYAN, path1_string, Style.RESET_ALL)
    print(Fore.CYAN, path2_string, Style.RESET_ALL)
    print("{0} EditDist={1}, {2:.2f}%{3}\n".format(Fore.RED, ans, perc * 100, Style.RESET_ALL))


def main():
    parser = argparse.ArgumentParser(description='Find edit distance between files')
    parser.add_argument('input', type=str, help='Input dir for files')
    parser.add_argument('-f', '--type', type=str, default='java',
                        help='File type to look for (default: java)')
    parser.add_argument('-t', '--threshold', type=float, default=0.1,
                        help='Threshold under which files should be reported (default: 0.1)')
    parser.add_argument('-p', '--threads', type=int, default=1,
                        help='Number of threads (default: 1)')
    parser.add_argument('-m', '--max', type=int, default=10, help='Max file size in kB (default: 10)')
    parser.add_argument('-nc', '--no-colors', action="store_true", help='Don\'t use colors in output')
    parser.add_argument('-l', '--loyola', action="store_true", help='Loyola sakai directory format')
    args = parser.parse_args()

    if (args.no_colors):
        Fore.YELLOW = Fore.RED = Fore.CYAN = Style.RESET_ALL = ''

    search = os.path.join(args.input, "**",  '*.' + args.type)

    files = list(glob.glob(search, recursive=True))
    files = list(map(lambda x: readfile(x, args.max), files))

    if len(files) > 100:
        print(Fore.YELLOW, "Warning: Calculating edit distance for {} files".format(len(files)), Style.RESET_ALL,
              file=sys.stderr)

    all = list(itertools.combinations(files, 2))
    with multiprocessing.Pool(args.threads) as pool:
        for i, j, ans, perc in pool.imap_unordered(check, all):
            if perc < args.threshold:
                print_result(i, j, ans, perc, args.loyola)
    pool.join()


if __name__ == "__main__":
    main()
