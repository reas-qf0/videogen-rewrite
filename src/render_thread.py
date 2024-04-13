import io
import multiprocessing
import time
from renderer import Renderer


class RenderThread:
    def __init__(self, parent, i):
        self.parent = parent
        self.i = i
        self.renderer = Renderer(parent)
        self.exported_frames = multiprocessing.Queue()
        self.thread = multiprocessing.Process(target=self.run)

    def run(self):
        for frame in range(self.i, self.parent.frames, self.parent.thrn):
            b = io.BytesIO()
            self.renderer.generate_frame(frame).save(b, 'JPEG')
            self.exported_frames.put(b.getvalue())

    def start(self):
        self.thread.start()

    def get_next_frame(self):
        return self.exported_frames.get()
