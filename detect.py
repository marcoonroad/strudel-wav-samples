# Sample tool to detect a note/pitch from a WAV sound

import librosa
import sys
import numpy as np

def detect_pitch_note(file_path: str):
    # 1. Load the wav file
    y, sr = librosa.load(file_path, sr=None)

    # 2. Estimate pitch using the YIN algorithm
    # fmin and fmax define the expected pitch range (e.g., standard vocal range)
    fmin = librosa.note_to_hz('C-1')
    fmax = librosa.note_to_hz('G9')
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr, S=None, fmin=fmin, fmax=fmax)

    # 3. Filter out low-magnitude noise
    pitches = pitches[magnitudes > np.max(magnitudes) * 0.1]

    if len(pitches) > 0:
        # Get the most prominent pitch
        dominant_pitch = np.median(pitches)

        # 4. Convert frequency to a musical note (e.g., "C4")
        note = librosa.hz_to_note(dominant_pitch)
        return (note, dominant_pitch)
    else:
        return None

def main():
    file_path = sys.argv[1]
    result = detect_pitch_note(file_path)
    if result is None:
        print("No pitch detected.")
    else:
        (note, dominant_pitch) = result
        print(f"Detected Note: {note} at {dominant_pitch:.2f} Hz")

if __name__ == "__main__":
    main()
