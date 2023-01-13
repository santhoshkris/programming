#!/usr/bin/env python3
"""A Simple sed attempt."""

import fileinput

filename = "test.txt"

with fileinput.FileInput(filename, inplace=True, backup='.bak') as f:
    for line in f:
        print(line.replace("hello", "hello world"), end='')
