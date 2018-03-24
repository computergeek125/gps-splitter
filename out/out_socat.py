import os
import shutil
import time

from out.out_base import out_base
from out.OutputError import OutputError
from subprocess import Popen, PIPE

class out_socat(out_base):
    def __init__(self, name, port, socat="socat"):
        self.name = name
        self.port = port
        self.socat = socat
        self.argv = [self.socat, "-", "pty,link=\"{0}\",raw".format(self.port)]
    def start(self):
        self.process = Popen(self.argv, stdin=PIPE, stdout=PIPE, stderr=PIPE, bufsize=0)
        time.sleep(1)
        os.chmod(self.port, 0o660)
        shutil.chown(self.port, user="root", group="dialout")
    def write(self, buf):
        try:
            self.process.stdin.write(buf)
        except BrokenPipeError:
            raise OutputError(self.error())
    def read(self):
        return self.process.stdout.read()
    def read(self, size):
        return self.process.stdout.read(size)
    def flush(self):
        self.process.stdout.flush()
    def error(self):
        return self.process.stderr.read().decode("UTF-8")
    def close(self):
        try:
            self.process.terminate()
        except ProcessLookupError:
            pass # It's already dead, Jim!
        return self.process.wait()
