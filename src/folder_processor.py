import codecs
import os
import subprocess
from math import ceil

from processor_base import ProcessorBase
from audio_processor.audio_processor import AudioProcessor
from common import seconds_to_string


class FolderProcessor(ProcessorBase):
    def __init__(self, path, output_fname=None):
        super().__init__(path, output_fname)
        self.fps = 30

    def default_name(self):
        return self.path + '.mp4'

    def process_main(self):
        tsfile = codecs.open(os.path.join(self.path, 'timestamps.txt'), 'w', encoding='utf-8')
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
