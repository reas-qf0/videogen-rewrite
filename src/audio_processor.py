import math
import os
import time
import tempfile

from logger import Logger
from metadata import Metadata
from render_thread import RenderThread
from monitor_thread import MonitorThread
from ffmpeg_thread import FFmpegThread
from renderer import Renderer
from common import seconds_to_string


class AudioProcessor:
    def __init__(self, path, output_fname=None):
        self.path = path
        self.logger = Logger(path)
        self.metadata = Metadata.get(path)
        if self.metadata is None:
            self.logger.log('unsupported format. Ignoring')
            raise ValueError()

        self.fps = 30
        self.thrn = 8
        self.output_fname = '.'.join(path.split('.')[:-1]) + '.mp4' if output_fname is None else output_fname
        self.frames = int(math.ceil(self.metadata.length * self.fps))

    def process(self):
        start = time.time()

        self.logger.log('init rendering')
        tmp_dir = tempfile.TemporaryDirectory()
        old_cwd = os.getcwd()
        os.chdir(tmp_dir.name)
        Renderer(self).initialize()

        self.logger.log('creating %s threads to render %s frames (%s fps)' % (self.thrn, self.frames, self.fps))
        monitor_thread = MonitorThread(self)
        render_threads = [RenderThread(self, i) for i in range(self.thrn)]
        for thread in render_threads:
            thread.start()
        with open('exported.tmp','wb') as file:
            for frame in range(self.frames):
                file.write(render_threads[frame % self.thrn].get_next_frame())
                monitor_thread.frame_exported()

        ffmpeg = FFmpegThread(self)
        ffmpeg.start()
        monitor_thread.start_monitoring_ffmpeg(ffmpeg)
        ffmpeg.join()
        monitor_thread.join()

        self.logger.log('removing temporary files')
        os.chdir(old_cwd)
        tmp_dir.cleanup()

        end = time.time()
        self.logger.log('finished in', seconds_to_string(end - start))
