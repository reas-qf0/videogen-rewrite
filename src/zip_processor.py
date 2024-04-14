from zipfile import ZipFile
from folder_processor import FolderProcessor
from processor_base import ProcessorBase


class ZipProcessor(ProcessorBase):
    def __init__(self, path, output_fname=None):
        super().__init__(path, output_fname)

    def default_name(self):
        return '.'.join(self.path.split('.')[:-1]) + '.mp4'

    def process_main(self):
        self.logger.log('extracting')
        with ZipFile(self.path, 'r') as zip_ref:
            zip_ref.extractall()
        FolderProcessor('.', self.output_fname).process()
