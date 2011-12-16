import sys
sys.path.append('.') # TODO: nicer nicer!

import gdbooc

gdbooc.register_printers(gdb.current_objfile())
