import codecs
import os
import subprocess
import time
from math import ceil
import tempfile

from logger import Logger
from audio_processor import AudioProcessor
from common import seconds_to_string


class FolderProcessor:
    def __init__(self, path, output_fname=None):
        self.path = path
        self.logger = Logger(path)
        self.output_fname = self.path + '.mp4' if output_fname is None else output_fname
        self.fps = 30

    def process(self):
        self.logger.log('begin processing')
        start = time.time()
        tsfile = codecs.open('timestamps.txt', 'w', encoding='utf-8')

        tmp_dir = tempfile.TemporaryDirectory()
        old_cwd = os.getcwd()
        os.chdir(tmp_dir.name)
        flist = codecs.open('mylist.txt', 'w', encoding='utf-8')
        i = 1
        timecounter = 0

        for file in sorted(os.listdir(self.path)):
            absfile = os.path.join(self.path, file)
            target_fname = os.path.abspath('%s.mp4' % i)
            try:
                processor = AudioProcessor(absfile, target_fname)
            except ValueError:
                continue
            if not processor.process():
                flist.write('file \'%s\'\n' % target_fname)
                tsfile.write('%s %s - %s\n' % (
                    seconds_to_string(timecounter / self.fps),
                    processor.metadata.artist,
                    processor.metadata.title
                ))
                timecounter += int(ceil(processor.metadata.length * self.fps))
                i += 1
            else:
                self.logger.log('error during processing. Ignoring.')

        flist.close()
        tsfile.close()
        self.logger.log('combining files')

        if subprocess.run(['ffmpeg', '-safe', '0', '-f', 'concat', '-i', flist.name,
                           '-c', 'copy', '-y', self.output_fname],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode:
            self.logger.log('error during file concatenation.')

        self.logger.log('removing temporary files')
        os.chdir(old_cwd)
        tmp_dir.cleanup()

        end = time.time()
        self.logger.log('finished in', seconds_to_string(end - start))
