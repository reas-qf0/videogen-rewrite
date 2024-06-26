import subprocess


class FFmpegThread:
    def __init__(self, parent):
        self.args = [
            'ffmpeg', '-progress', '-', '-nostats', '-stats_period', '0.1',
            '-framerate', str(parent.fps), '-i', '-', '-i', parent.metadata.fname,
            '-vcodec', 'libx264', '-crf', '27', '-preset', 'ultrafast',
            '-vsync', '2', '-y', parent.output_fname
        ]
        self.thread = None

    def feed(self, frame):
        self.thread.stdin.write(frame)

    def start(self):
        self.thread = subprocess.Popen(self.args,
                                       stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)

    def join(self):
        self.thread.wait()
