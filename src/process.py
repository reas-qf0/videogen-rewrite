import zipfile
from os import path


def process(fpath):
    if not path.exists(fpath):
        print('error: %s: no such file or folder' % fpath)
        return False

    if path.isdir(fpath):
        from folder_processor import FolderProcessor
        processor = FolderProcessor(fpath)
    elif zipfile.is_zipfile(fpath):
        from zip_processor import ZipProcessor
        processor = ZipProcessor(fpath)
    else:
        from audio_processor import AudioProcessor
        try:
            processor = AudioProcessor(fpath)
        except ValueError:
            exit(1)
    return processor.process()