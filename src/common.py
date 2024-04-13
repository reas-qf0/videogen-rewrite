from shutil import rmtree
import os


def seconds_to_string(secs,duration=0):
    secs = int(secs)
    if secs >= 3600 or duration >= 3600:
        return '%02d' % (secs // 3600) + \
               ':' + \
               '%02d' % ((secs % 3600) // 60) + \
               ':' + \
               '%02d' % (secs % 60)
    else:
        return '%02d' % (secs // 60) + \
               ':' + \
               '%02d' % (secs % 60)


def mkdir(name):
    name = os.path.abspath(name)
    try:
        os.mkdir(name)
    except FileExistsError:
        rmtree(name)
        os.mkdir(name)
