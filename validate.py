# Sample tool to validate the list of WAV files

import os
import json
import sys
from pathlib import Path

def main():
    ignore = {'.git', 'node_modules', 'bin', 'obj', '.vs', '.venv', 'venv', '__pycache__', 'packages', 'TRASH'}
    root = Path.cwd()
    found = {}
    for item in root.iterdir():
        if item.is_dir():
            if item.name in ignore:
                continue
            for base, directories, files in os.walk(item):
                directories[:] = [directory for directory in directories if directory not in ignore]
                for file in files:
                    if not file.endswith(".wav"):
                        continue
                    if not str(item.name) in found:
                        found[ str(item.name) ] = []
                    found[ str(item.name) ].append(str(Path(item.name) / file).replace("\\", "/"))
    with open("strudel.json", "rt", encoding="utf-8") as handler:
        spec: dict = json.load(handler)
        for key, value in spec.items():
            if key == "_base":
                continue
            value.sort()
            found[key].sort()
            message = "Found a mismatch of files in key instrument " + key + ", please review that."
            if len(value) != len(found[key]):
                raise Exception(message)
            for index in range(len(value)):
                if value[index] != found[key][index]:
                    raise Exception(message)

if __name__ == "__main__":
    main()
