import importlib
import subprocess
from sys import argv
from os import path


required_modules = ['PIL', 'mutagen']


if __name__ == "__main__":
    try:
        subprocess.Popen(['ffmpeg'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print('error: ffmpeg not installed or not found at given path')
        exit(1)

    for module in required_modules:
        try:
            importlib.import_module(module)
        except ModuleNotFoundError:
            print('error: module %s not installed' % module)
            exit(1)

    target_file = path.abspath(' '.join(argv[1:]))
    from process import process
    exit(process(target_file))
