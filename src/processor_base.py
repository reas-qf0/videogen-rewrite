import os.path
import time
import tempfile

from logger import Logger
from common import seconds_to_string


class ProcessorBase:
    def __init__(self, path, output_fname=None):
        path = os.path.abspath(path)
        self.path = path
        self.logger = Logger(path)
        self.output_fname = self.default_name() if output_fname is None else output_fname

    def process(self):
        start = time.time()
        self.logger.log('init rendering')
        tmp_dir = tempfile.TemporaryDirectory()
        old_cwd = os.getcwd()
        os.chdir(tmp_dir.name)

        self.process_main()

        self.logger.log('removing temporary files')
        os.chdir(old_cwd)
        tmp_dir.cleanup()
        end = time.time()
        self.logger.log('finished in', seconds_to_string(end - start))

    # to reimplement
    def default_name(self):
        raise NotImplementedError()

    def process_main(self):
        raise NotImplementedError()