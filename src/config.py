import os
import json

types = {
    "config_file": os.path.abspath,
    "ffmpeg_path": str,
    "fps": float,
    "thrn": int,
    "font": os.path.abspath
}

default_values = {
    "config_file": "config.json",
    "ffmpeg_path": "ffmpeg",
    "fps": 30,
    "thrn": 4
}


class Config:
    values = {}

    @staticmethod
    def set(key, value):
        if key not in Config.values:
            Config.values[key] = types[key](value)

    @staticmethod
    def init(argv):
        # 1. values from argv
        for i in range(1, len(argv), 2):
            if not argv[i].startswith('--'):
                break
            Config.set(argv[i][2:], argv[i + 1])

        # 2. values from config_file
        with open(Config.values['config_file'] if 'config_file' in Config.values else default_values['config_file']) as file:
            json_values = json.load(file)
        for key in json_values:
            Config.set(key, json_values[key])

        # 3. default values
        for key in default_values:
            Config.set(key, default_values[key])

        return i
