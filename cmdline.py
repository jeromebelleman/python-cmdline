import sys
import os, os.path
import cmd, readline
import argparse
import tempfile
import shlex
import subprocess

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
    def __init__(self, history=False):
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
        self.name = self.__class__.__name__.lower()
        self.prompt = self.name + '% '
        wintitle(self.name)

        # Create directory
        self.directory = os.path.expanduser('~/.%s' % self.name)
        if not os.path.lexists(self.directory):
            os.mkdir(self.directory)

        # Set up base argument parsers
        self.editparser.description = "Edit command line."
        self.editparser.add_argument('command', help="command")
        self.editparser.add_argument('argument', help="arguments", nargs='*')

        self.EOFparser.description = "Exit. You could also use Ctrl-D."

        # History
        self.history = history
        histfile = self.directory + '/histfile'
        if self.history and os.path.exists(histfile):
            readline.read_history_file(histfile)

    def emptyline(self):
        pass

    def precmd(self, line):
        readline.set_pre_input_hook()
        if self.history:
            readline.write_history_file(self.directory + '/histfile')
        return line

    def loop(self):
        while True:
            try:
                self.cmdloop()
            except KeyboardInterrupt:
                readline.set_pre_input_hook()
                print

    def run_EOF(self, _):
        print
        sys.exit(0)

    def run_edit(self, args):
        '''
        Edit command line
        '''

        # Open command line in editor
        tmpw = tempfile.NamedTemporaryFile(prefix='edit-', dir=self.directory)
        print >> tmpw, ' '.join([args.command] + args.argument)
        tmpw.flush()
        subprocess.call(['vim', '-n', '+set titlestring=' + self.name,
                         tmpw.name])
        wintitle(self.name)

        # Read edited command line
        tmpr = open(tmpw.name)
        line = tmpr.read().strip() # Can't cope with any trailing newline

        def hook():
            '''
            Insert text in command line
            '''

            readline.insert_text(line)
            readline.redisplay()

        readline.set_pre_input_hook(hook)
