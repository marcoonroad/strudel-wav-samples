#!/usr/bin/env bash

echo "Starting to process..."
dirs=(
  "gabber_kicks"
  "reese_bassline"
  "growl_bassline"
  "supersaws"
  "supersquares"
  "cowbells"
  "backspins"
)
function normalize-wav-audio {
  ffmpeg -y -v error -i "$1" -c:a pcm_s16le -ar 44100 "$2"
}
for dir in "${dirs[@]}"; do
  for src in "$dir"/*.wav; do
    [ -f "$src" ] || continue
    echo "Processing $src..."
    mv "$src" "$src.draft.wav"
    normalize-wav-audio "$src.draft.wav" "$src"
    rm "$src.draft.wav"
  done
done
echo "Done processing."
