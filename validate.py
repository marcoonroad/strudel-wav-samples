# Sample tool to validate the list of WAV files

import os
import json
import struct
import sys
import wave
from detect import detect_pitch_note
from pathlib import Path

def validate_wav(file_path: Path):
    errors = []
    try:
        with wave.open(str(file_path), "rb") as wav:
            if wav.getcomptype() != "NONE":
                errors.append(f"compression must be PCM, found {wav.getcomptype()}")
            if wav.getsampwidth() != 2:
                errors.append(f"sample width must be 16-bit, found {wav.getsampwidth() * 8}-bit")
            if wav.getframerate() != 44100:
                errors.append(f"sample rate must be 44100 Hz, found {wav.getframerate()} Hz")

            frame_size = wav.getnchannels() * wav.getsampwidth()
            remaining = wav.getnframes()
            while remaining > 0:
                frame_count = min(65536, remaining)
                data = wav.readframes(frame_count)
                if len(data) != frame_count * frame_size:
                    errors.append("audio data is truncated or does not match its WAV header")
                    break
                remaining -= frame_count
    except (wave.Error, EOFError, OSError, struct.error) as error:
        errors.append(f"invalid WAV header or data: {error}")

    return errors

def main():
    ignore = {'.git', 'electroclash_vox', 'amenlike', 'dnb_breaks', 'node_modules', 'bin', 'obj', '.vs', '.venv', 'venv', '__pycache__', 'packages', 'TRASH'}
    scan_ignore = {'.git', 'node_modules', 'bin', 'obj', '.vs', '.venv', 'venv', '__pycache__', 'packages', 'TRASH'}
    root = Path(__file__).resolve().parent

    checked = 0
    failures = []
    for base, directories, files in os.walk(root):
        directories[:] = [directory for directory in directories if directory not in scan_ignore]
        for file in files:
            if Path(file).suffix.lower() != ".wav":
                continue
            file_path = Path(base) / file
            checked += 1
            errors = validate_wav(file_path)
            if errors:
                failures.append((file_path.relative_to(root).as_posix(), errors))

    print(f"Checked {checked} WAV files for PCM 16-bit 44.1 kHz format.")
    if failures:
        for file_path, errors in failures:
            print(f"INVALID: {file_path}")
            for error in errors:
                print(f"  - {error}")
        sys.exit(f"{len(failures)} WAV file(s) failed validation.")

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
    with open(root / "strudel.json", "rt", encoding="utf-8") as handler:
        spec: dict = json.load(handler)
        print("WAV file | Detected note | Detected pitch")
        print("-------- | ------------- | --------------")
        for key, value in spec.items():
            if key == "_base":
                continue
            if key in ignore:
                continue
            value.sort()
            found[key].sort()
            message = "Found a mismatch of files in key instrument " + key + ", please review that."
            if len(value) != len(found[key]):
                raise Exception(message)
            for index in range(len(value)):
                if value[index] != found[key][index]:
                    raise Exception(message)
                detection = detect_pitch_note(str(root / value[index]))
                if detection is None:
                    continue
                (detected_note, detected_pitch) = detection
                # if detected_note == "C3":
                #    continue
                detected_note = detected_note.replace("♯", "#")
                if not value[index].endswith(detected_note + ".wav"):
                    raise Exception("File " + value[index] + " must specify and end with note " + detected_note + ".wav")
                print(f"{value[index]} | {detected_note} | {detected_pitch:.2f}Hz")

if __name__ == "__main__":
    main()
