# NAME

python-cmdline – Cmdline module

# GETTING STARTED

Assuming you're writing a tool called **foo** after which you'll
name the Cmdline class:

```python
#! /usr/bin/env python

import sys
import cmdline

class Foo(cmdline.Cmdline):
    def __init__(self):
        cmdline.Cmdline.__init__(self)

def main():
    Foo().loop()

if __name__ == '__main__':
    sys.exit(main())
```

# CLASS PARAMETERS 

**directory**
:   Directory in which the program directory lives. Defaults to the home
    directory.

**history**
:   Possible values are **true** and **false**, depending on whether you
    want to keep a command history or not.  Default is **false**.

**bell**
:   Possible values are **true** and **false**, depending on whether you want
    to ring a bell at the end of each command completion. Default is **false**.

**time**
:   Possible values are **true** and **false**, depending on whether you
    want to add the **--time** option to each command to measure the time it
    takes to run it. Default is **false**.

# DEFINING COMMANDS

Unlike **Cmd**, **Cmdline** expects command definitions in **run_** functions
taking an **args** namespace parameter:

```python
def run_dothings(self, args):
    self.dothings(args.stuff)
```

An argument parser **fooparser**
will be created for each command **foo** that will be defined as such.

If you need to add an argument to the command, do so by calling the
**foo.add_argument()** function with the appropriate parameters.

Likewise, if you need to add a description to the command, do so by setting
the **foo.description** string.  (Not sure to which point one is supposed
to do so with **argparse** but, but I haven't found any better suggestion
in the doc.)

# COMMODITY COMMANDS

Some commodity functions are already defined:

**run_EOF()**
:   Close temporary files and exit.

**run_edit()**
:   Edit a command line.

**run_page()**
:   Page output.

Any of these can be overridden the usual way, should you need to add features.
Example:

```python
def run_EOF(self, _):
    clean_everything_up()

    cmdline.Cmdline.run_EOF(self, None)
```

# PAGING

The **page** command is made available to you for free, but you still
need to implement what has to be paged. This is done by writing data to a
temporary file which will be loaded into Vim next time you run **page**.

As the temporary file is kept open at all times, you need to run
**tempreset()** to rewind and truncate it before writing anything to it.
After this, it's only a matter of writing to **self.temp** as well as to
**sys.stdout**. There is no need to **flush()** because **Cmdline** does
that anyway after each command runs.
