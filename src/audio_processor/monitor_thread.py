import threading
from common import seconds_to_string


class MonitorThread:
    def __init__(self, parent, ffmpeg):
        self.parent = parent
        self.ffmpeg_thread = ffmpeg.thread
        self.total = parent.frames
        self.amount = 0
        self.duration = self.total / parent.fps
        self.running = True

        self.thread = threading.Thread(target=self.monitor_ffmpeg)
        self.thread.start()

    def print_progress(self):
        print('\b' * 200,end='',flush=True)
        self.parent.logger.log('rendering %s/%s (%s/%s)' % (
            str(self.amount).rjust(len(str(self.total)), ' '), self.total,
            seconds_to_string(self.amount / self.parent.fps, self.duration),
            seconds_to_string(self.duration)
        ), end='')

    def monitor_ffmpeg(self):
        for line in self.ffmpeg_thread.stdout:
            line = str(line, 'utf-8')
            if line == 'progress=end':
                return
            if line.startswith('frame='):
                try:
                    self.amount = int(line[6:])
                    self.print_progress()
                except ValueError:
                    pass

    def join(self):
        self.running = False
        self.thread.join()
        self.print_progress()
        print()
