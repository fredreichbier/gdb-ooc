import gdb

from .mangle import mangle_path

class BreakOOC(gdb.Command):
    """
        Works like the ordinary `b`/`breakpoint` command, but provides
        name mangling!
    """
    def __init__(self):
        gdb.Command.__init__(self, 'booc', gdb.COMMAND_BREAKPOINTS)

    def invoke(self, argument, from_tty):
        gdb.execute('b %s' % mangle_path(argument), from_tty)

BreakOOC()
