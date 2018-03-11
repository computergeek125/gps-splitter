from out.out_base import out_base

class out_buf(out_base):
    def __init__(self, name, buf, closable=False):
        self.name = name
        self.buf = buf
        self.closable = closable
    def start(self):
        pass
    def write(self, buf):
        return self.buf.write(buf)
    def read(self):
        return self.buf.read()
    def read(self, size):
        return self.buf.read(size)
    def flush(self):
        return self.buf.flush()
    def error(self):
        pass
    def close(self):
        if self.closable:
            return self.buf.close()
