from math import ceil

from processor_base import ProcessorBase
from metadata import Metadata
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
        self.fps = 30
        self.thrn = 8
        self.frames = int(ceil(self.metadata.length * self.fps))

    def default_name(self):
        return '.'.join(self.path.split('.')[:-1]) + '.mp4'

    def process_main(self):
        Renderer(self).initialize()

        self.logger.log('creating %s threads to render %s frames (%s fps)' % (self.thrn, self.frames, self.fps))
        render_threads = [RenderThread(self, i) for i in range(self.thrn)]
        for thread in render_threads:
            thread.start()
        ffmpeg = FFmpegThread(self)
        ffmpeg.start()
        monitor_thread = MonitorThread(self, ffmpeg)

        with open('exported.tmp', 'wb') as file:
            for frame in range(self.frames):
                file.write(render_threads[frame % self.thrn].get_next_frame())
        ffmpeg.join()
        monitor_thread.join()
