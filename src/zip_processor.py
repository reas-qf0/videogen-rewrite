import tempfile
from zipfile import ZipFile
from logger import Logger
from folder_processor import FolderProcessor


class ZipProcessor:
    def __init__(self, path, output_fname=None):
        self.path = path
        self.logger = Logger(path)
        self.output_fname = '.'.join(path.split('.')[:-1]) + '.mp4' if output_fname is None else output_fname

    def process(self):
        self.logger.log('extracting')
        tmp_dir = tempfile.TemporaryDirectory()
        with ZipFile(self.path, 'r') as zip_ref:
            zip_ref.extractall(tmp_dir.name)
        FolderProcessor(tmp_dir.name, self.output_fname).process()

        self.logger.log('removing temporary files')
        tmp_dir.cleanup()
