import gdb

import re

# This regex is used to parse ooc symbol names with modules and classes.
# There will be mixups with namespace0/namespace1, but that doesn't matter
# since they are mangled in the same way.
PATTERN = """
    (?P<module>[a-zA-Z0-9/_]+) # Our first namespace, a module
    \s+
    (
        (?P<cls>[a-zA-Z0-9_]+) # Our second namespace, might be a class
        \s+
    )?
    (?P<function>[a-zA-Z0-9_!?]+) # our actual function!
    \s*
    (?P<suffix>~[a-zA-Z0-9_]+)? # dat suffix
    \s*
    (?P<parens>\(\s*\))? # my parens are deaaaaaaaaaaaaaaaaaaad
"""
MATCH = re.compile(PATTERN, re.VERBOSE)

REPLACE_CHARS = re.compile('[/ ]')

def mangle(module, cls, function, suffix=''):
    """
        Create the C name from these. `cls` and `suffix` can be ''.
    """
    mangled = []
    # Module!
    mangled.append(REPLACE_CHARS.sub('_', module))
    # Double-Underscore!
    mangled.append('')
    # Class?
    if cls:
        mangled.append(cls)
    # Function name!
    function = function.replace('!', '__bang').replace('?', '__quest')
    mangled.append(function)
    # Suffix!
    if suffix:
        mangled.append(suffix)
    return '_'.join(mangled)

def mangle_path(path):
    m = MATCH.match(path)
    if m is None:
        raise OOCException('Malformed symbol path: %r' % path)
    else:
        dct = m.groupdict()
        suffix = dct['suffix'][1:] if dct['suffix'] else ''
        return mangle(dct['module'], dct['cls'], dct['function'], suffix)

class OOCException(Exception):
    pass

class OOC(gdb.Function):
    """
        gdb: It's ooc, not OOC!

        However, used for mangling ooc names.
    """
    def __init__(self):
        gdb.Function.__init__(self, 'ooc')

    def invoke(self, symbol):
        path = str(symbol)[1:-1]
        return mangle_path(path)

OOC()
