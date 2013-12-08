import sys
import os, os.path
import cmd
import argparse
import tempfile
import shlex

def wintitle(name):
    print "\033]0;%s\007\r" % name,

def mkdo(cbk):
    def do(self, line):
        try:
            split = shlex.split(line)
            args = getattr(Cmdline, cbk + 'parser').parse_args(split)
        except SystemExit:
            return
        getattr(Cmdline, 'run_' + cbk)(self, args)

    return do

class Cmdline(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)

        # Create argument parsers and callbacks
        for cbk in [cbk[4:] for cbk in dir(self) if cbk.startswith('run_')]:
            # Create argument parser
            setattr(Cmdline, cbk + 'parser', argparse.ArgumentParser(prog=cbk))

            # Create help function
            setattr(Cmdline, 'help_' + cbk, getattr(Cmdline, cbk + 'parser').print_help)

            # Create do function
            setattr(Cmdline, 'do_' + cbk, mkdo(cbk))

        # Set prompt and title
        name = self.__class__.__name__.lower()
        self.prompt = name + '% '
        wintitle(name)

        # Create directory
        directory = os.path.expanduser('~/.%s' % name)
        if not os.path.lexists(directory):
            os.mkdir(directory)

        # Write help for base callbacks
        self.EOFparser.description = "Exit. You could also use Ctrl-D."

    def emptyline(self):
        pass

    def loop(self):
        while True:
            try:
                self.cmdloop()
            except KeyboardInterrupt:
                print

    def run_EOF(self, _):
        print
        sys.exit(0)

    def run_edit(self, line):
        '''
        Edit command line
        '''

        print "Will do some editing"
