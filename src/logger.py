class Logger:
    def __init__(self, prefix):
        self.prefix = str(prefix)

    def log(self, *args, **kwargs):
        if self.prefix:
            print(self.prefix, ': ', sep='', end='')
        print(*args, **kwargs)
