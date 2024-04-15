from mutagen import mp3, flac


class Metadata:
    def __init__(self, fname):
        self.fname = fname

    @staticmethod
    def get(fname):
        supported = {
            'mp3': MP3Metadata,
            'flac': FLACMetadata
        }
        for format in supported:
            if fname.endswith('.' + format):
                return supported[format](fname)
        return None


class MP3Metadata(Metadata):
    def __init__(self, fname):
        super().__init__(fname)
        self.md = mp3.MP3(fname)
        self.title = self.md.tags['TIT2'].text[0]
        self.artist = self.md.tags['TPE1'].text[0]
        self.album = self.md.tags['TALB'].text[0]
        self.length = self.md.info.length


class FLACMetadata(Metadata):
    def __init__(self, fname):
        super().__init__(fname)
        self.md = flac.FLAC(fname)
        self.title = self.md.tags['TITLE'][0]
        self.artist = self.md.tags['ARTIST'][0]
        self.album = self.md.tags['ALBUM'][0]
        self.length = self.md.info.length
