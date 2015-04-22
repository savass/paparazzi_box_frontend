# -*- coding: utf8 -*-
import shlex,subprocess32
import sys
ON_POSIX = 'posix' in sys.builtin_module_names

class ProcessHolder:

    ProcessAgent = None
    ProcessRunning = False

    def __init__(self, ProcName, ProcCommand, RunProcess):

        self.ProcName = ProcName
        self.ProcArg = ProcCommand[(ProcCommand.find(' ')+1):]
        self.ProcCommand = shlex.split(ProcCommand)
        self.RunProcess = RunProcess

    def run(self):
        self.ProcessAgent = subprocess32.Popen(self.ProcCommand, stdout=subprocess32.PIPE, stderr=subprocess32.STDOUT, bufsize=1,close_fds=ON_POSIX, shell=False)


