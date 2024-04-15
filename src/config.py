import os
import json

default_values = {
    "config_file": "config.json",
    "ffmpeg_path": "ffmpeg",
    "fps": 30,
    "thrn": 4
}

types = {
    "config_file": str,
    "ffmpeg_path": str,
    "fps": float,
    "thrn": int,
    "font": str
}


class Config:
    values = {}

    @staticmethod
    def set(key, value):
        if types[key] == str and os.path.exists(value):
            Config.values[key] = os.path.abspath(value)
        else:
            Config.values[key] = types[key](value)

    @staticmethod
    def init(argv):
        # 1. default values
        for key in default_values:
            Config.set(key, default_values[key])

        # 2. values from argv
        for i in range(1, len(argv), 2):
            if not argv[i].startswith('--'):
                break
            Config.set(argv[i][2:], argv[i + 1])

        # 3. values from config_file
        if 'config_file' in Config.values:
            with open(Config.values['config_file']) as file:
                json_values = json.load(file)
            for key in json_values:
                if key not in Config.values:
                    Config.set(key, json_values[key])

        return i
