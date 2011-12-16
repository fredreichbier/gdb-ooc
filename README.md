# gdb for ooc

Since ooc is C, one can just use the [GNU Debugger](http://gnu.org/software/gdb) to debug ooc executables. It works, but it's not fun. But it should be fun!

So, just use `gdbooc`!

## What does it do?

Current, not too much. It's a Python extension for gdb and provides the following features:

 * pretty-printing of ooc `String` and `Buffer` objects
 * name mangling with the `$ooc` convenience function
 * lazy breakpoints with the `booc` command.

## How do I test it?

Just get you a gdb with Python extension support, clone this repository and type `make` to get an example executable. Now you can use the example gdb command file to test it:

    gdb test -x test.gdb

This sets two breakpoints and executes the program. See `test.gdb` for more information.

## How to use it?

The easiest way is to place the `gdbooc` package somewhere in your PYTHONPATH (a proper `setup.py` will follow!). Now, for every executable you want to debug using gdb, create a file named `<name>-gdb.py` containing the following:

    import gdbooc

    gdbooc.register_printers(gdb.current_objfile())

For an ooc file `foo.ooc`, you would create a `foo-gdb.py` file.

Then, just compile your executable with the `rock -g` flag and run `gdb <name>`.
