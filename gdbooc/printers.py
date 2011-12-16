import ctypes

import gdb

def is_pointer_to(val, struct):
    """
        Is this value a pointer to the struct type `struct` (as string)?
        Return a boolean.
    """
    try:
        target = val.type.target().strip_typedefs()
        if (target is not None and target.tag == struct):
            return True
    except (RuntimeError, ValueError):
        pass
    return False

def get_bytestring_at(val, size):
    """
        Return the string at this particular address with this particular
        size.
    """
    return val.string('unicode_escape', 'replace', length=size)

class BufferPrinter(object):
    """
        Prints buffers in the following form:

           $1 = <Buffer "hai" at 0x6d8690>

    """
    def __init__(self, val):
        self.val = val

    def get_string(self):
        """
            Return the raw string value as unicode. Assume it's utf8-encoded.
        """
        return get_bytestring_at(self.val['data'], int(self.val['size']))

    def to_string(self):
        """
            Return an actual string representation of the value.
        """
        s = self.get_string().encode('raw_unicode_escape').encode('hex_codec') # TODO: good codec?
        return '<Buffer "%s" at %s>' % (s, self.val.address)

    @classmethod
    def lookup(cls, val):
        if is_pointer_to(val, '_lang_Buffer__Buffer'):
            return cls(val)

class StringPrinter(object):
    """
        Prints strings in the following form:

            $1 = "hai" at 0x7fffffffe698

    """
    def __init__(self, val):
        self.val = val

    def to_string(self):
        buf = self.val['_buffer'].dereference()
        s = BufferPrinter(buf).get_string().encode('unicode_escape')
        return '"%s" at %s' % (s, self.val.address)

    @classmethod
    def lookup(cls, val):
        if is_pointer_to(val, '_lang_String__String'):
            return cls(val)

PRINTERS = (
    StringPrinter.lookup,
    BufferPrinter.lookup,
)

def register_printers(objfile):
    objfile.pretty_printers.extend(PRINTERS)
