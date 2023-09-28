#!/usr/bin/env python3

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from . import args_mod
from doc_mod import Doc

def main():

    if not getattr(args_mod.iargs, 'command', None):
        print("See adocs --help")
        exit()
    
    if args_mod.iargs.command == "create":
        doc = Doc()
        doc.create()
    elif args_mod.iargs.command == "xref":
        doc = Doc()
        doc.xref()
    elif args_mod.iargs.command == "rename":
        doc = Doc()
        doc.rename()
    elif args_mod.iargs.command == "delete":
        doc = Doc()    
        doc.delete()
    else:
        exit()

if __name__ == "__main__":
    main()
