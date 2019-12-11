#!/usr/bin/env python3

import semantic_version
import sys

with open('../VERSION', 'r') as f:
    version = f.read()

v = semantic_version.Version(version)

if sys.argv[1] == 'major':
    next_v = v.next_major()
elif sys.argv[1] == 'minor':
    next_v = v.next_minor()
elif sys.argv[1] == 'patch':
    next_v = v.next_patch()

new_version = str(next_v)

with open('../VERSION', 'w') as f:
    f.write(new_version)

print(new_version)
