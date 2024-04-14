import threading
import time
from common import seconds_to_string


class MonitorThread:
    def __init__(self, parent):
        self.parent = parent
        self.ffmpeg_thread = None
        self.total = parent.frames
        self.amount = 0
        self.duration = self.total / parent.fps
        self.running = True
        self.message = 'exporting'

        self.thread = threading.Thread(target=self.progress_thread)
        self.thread.start()

    def print_progress(self):
        print('\b' * 200,end='',flush=True)
        self.parent.logger.log('%s %s/%s (%s/%s)' % (
            self.message, str(self.amount).rjust(len(str(self.total)), ' '), self.total,
            seconds_to_string(self.amount / self.parent.fps, self.duration),
            seconds_to_string(self.duration)
        ), end='')

    def progress_thread(self):
        while self.running:
            self.print_progress()
            time.sleep(0.1)

    def frame_exported(self):
        self.amount += 1

    def monitor_ffmpeg(self):
        for line in self.ffmpeg_thread.stdout:
            line = str(line, 'utf-8')
            if line == 'progress=end':
                return
            if line.startswith('frame='):
                try:
                    framen = int(line[6:])
                    self.amount = framen
                except ValueError:
                    pass

    def start_monitoring_ffmpeg(self, ffmpeg_thread):
        self.amount = 0
        self.message = 'rendering'
        self.ffmpeg_thread = ffmpeg_thread.thread
        self.ffthread = threading.Thread(target=self.monitor_ffmpeg)
        self.ffthread.start()

    def join(self):
        self.running = False
        self.thread.join()
        self.print_progress()
        print()
