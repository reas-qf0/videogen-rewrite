import importlib
import subprocess
import sys
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

    sys.path.append(path.dirname(__file__))

    target_file = path.abspath(' '.join(sys.argv[1:]))
    from process import process
    exit(process(target_file))
