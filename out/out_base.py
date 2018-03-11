class out_base:
    def __init__(self, name):
        self.name = name
        raise NotImplemented("Cannot run a prototype class")
    def start(self):
        raise NotImplemented("Cannot run a prototype class")
    def write(self, buf):
        raise NotImplemented("Cannot run a prototype class")
    def read(self):
        raise NotImplemented("Cannot run a prototype class")
    def read(self, size):
        raise NotImplemented("Cannot run a prototype class")
    def flush(self):
        raise NotImplemented("Cannot run a prototype class")
    def error(self):
        raise NotImplemented("Cannot run a prototype class")
    def close(self):
        raise NotImplemented("Cannot run a prototype class")
