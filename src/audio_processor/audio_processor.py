import tempfile
from math import ceil

from processor_base import ProcessorBase
from metadata import Metadata
from config import Config
from .render_thread import RenderThread
from .monitor_thread import MonitorThread
from .ffmpeg_thread import FFmpegThread
from .renderer import Renderer


class AudioProcessor(ProcessorBase):
    def __init__(self, path, output_fname=None):
        super().__init__(path, output_fname)

        self.metadata = Metadata.get(path)
        if self.metadata is None:
            self.logger.log('unsupported format. Ignoring')
            raise ValueError()
        self.fps = Config.values['fps']
        self.thrn = Config.values['thrn']
        self.frames = int(ceil(self.metadata.length * self.fps))

    def default_name(self):
        return '.'.join(self.path.split('.')[:-1]) + '.mp4'

    def process_main(self):
        try:
            Renderer(self).initialize()
        except KeyError:
            return

        self.logger.log('creating %s threads to render %s frames (%s fps)' % (self.thrn, self.frames, self.fps))
        render_threads = [RenderThread(self, i) for i in range(self.thrn)]
        for thread in render_threads:
            thread.start()

        ffmpeg = FFmpegThread(self)
        ffmpeg.start()
        monitor_thread = MonitorThread(self, ffmpeg)

        for frame in range(self.frames):
            ffmpeg.feed(render_threads[frame % self.thrn].get_next_frame())
        ffmpeg.thread.stdin.close()
        ffmpeg.join()
        monitor_thread.join()
