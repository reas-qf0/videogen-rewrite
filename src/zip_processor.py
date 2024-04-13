import os.path
from shutil import rmtree
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
        dest = os.path.join(os.path.dirname(self.path), 'tmp_zip')
        with ZipFile(self.path, 'r') as zip_ref:
            zip_ref.extractall(dest)
        FolderProcessor(dest, self.output_fname).process()

        self.logger.log('removing temporary files')
        rmtree(dest)
