# videogen-rewrite

an extremely hacky program i wrote back in 2020 to upload my albums to youtube, now rewritten to be slightly less embarrassing

# what it can do

it can take your audio files (or folders/zips with audio files) and turn them into beautiful videos with a progress bar and everything

[see it in action](https://www.youtube.com/@Slushwave)

(currently the only supported formats are mp3 and flac)

(the files have to have proper metadata i.e. embedded covers, set title/artist/album name)

# usage

it's simple: open up your favorite command prompt and type

```commandline
git clone https://github.com/reas-qf0/videogen-rewrite
cd videogen-rewrite
python3 src/main.py (your file/folder here)
```

e.g.

`python3 src/main.py my_awesome_audio_file.flac`

use python instead of python3 if you're on windows

# requirements

* python (obviously. duh. this thing is written in python)
* `mutagen` (in order to retrieve information about audio files)
* `pillow` (in order to generate frames)

install them with `python3 -m pip install mutagen` and `python3 -m pip install pillow` respectively

# todo

* error checking/code cleanup
* configuration (was somewhat implemented in the old version but i was kinda lazy to implement it rn i wrote this in like a day)
* more features: more audio formats, more archive formats, potentially bandcamp links/any direct download links?
* gui interface