# Strudel WAV Samples

### Example of Usage

```javascript
setcpm(105)

samples('github:marcoonroad/strudel-wav-samples')

$: sound("backspins:0/2")
  .mask("<0 0 [0!6 1!2] 0>/8")
  .cutoff(2500)
  .ftype("ladder")
  .velocity(0.25)
  .orbit(3)

register('pitchBend', (semitones, pattern) =>
  pattern.speed(pure(2).pow(pure(1).div(12).mul(semitones))))

register('humanize', pattern =>
  pattern.clip(rand.range(0.75, 1.0)))

$: stack(
    note("d#2 | f#2 | d#2 | g#2 | d#2 | c#2 | e2 | d#2".sub(9))
    .struct("<x x*2 x x?>").humanize().orbit(1)
    .sound("gm_slap_bass_1").velocity(0.125),
    sound("bd/8").bank("RolandTR808").soft("1")
    .orbit(2).duckorbit(1).duckonset(0.005).duckattack(0.25).duckdepth(0.9)
    .room(0.5).roomsize(5).pitchBend(-1).crush(12).velocity(0.75),
    sound("<- [sd:0:.6,cp:0:.2] - [sd:0:.6,cp:0:.2]*2>").humanize().bank("RolandTR808")
    .pitchBend(-1).velocity(0.75).orbit(1),
    sound("[- <- oh*2>]").bank("RolandTR808").pitchBend(-5).velocity(0.25).orbit(1),
    sound("[hh hh <hh -> <hh ->]").humanize().degradeBy("0.25".fast(4)).bank("RolandTR808")
    .pitchBend(-3).velocity(0.75).orbit(1)
  )
  .cutoff("<2700!2 [2400 2100 1800 1500 1200 900 600 300] 300>/8".add(1000))
  .ftype("24db")
  .mask("<1 1 [1!7 0!1] 0>/8")
  .pianoroll({ labels: 1 })
```

### Tips & Tricks

For the plucks/percussion instruments, it's not needed, but due being samples loaded fully, most sounds here need
a `.clip(1)` / `.legato(1)` to stop playing once the pattern note finishes, otherwise a lot of note sounds would be mixed,
phased and cancelled, with the sound sounding heavily metallic like a guitar.

Also, I did not apply any loudness normalization for this set of samples, it's recommended to initially load and play such samples with `.velocity(0.5)`, just to avoid some sudden huge bumps higher than other instruments played along.

### Instruments Tunings

WAV file | Detected note | Detected pitch
-------- | ------------- | --------------
supersaws/01 D#4.wav | D#4 | 312.90Hz
supersaws/02 C#4.wav | C#4 | 278.23Hz
supersaws/03 C4.wav | C4 | 261.85Hz
supersaws/04 D4.wav | D4 | 289.44Hz
supersaws/05 E5.wav | E5 | 648.41Hz
supersaws/06 D5.wav | D5 | 579.99Hz
supersquares/01 G#3.wav | G#3 | 209.14Hz
cowbells/01 A5.wav | A5 | 855.09Hz
backspins/01 B4.wav | B4 | 482.00Hz
backspins/02 E5.wav | E5 | 667.52Hz
backspins/03 G5.wav | G5 | 785.60Hz
backspins/04 C5.wav | C5 | 529.52Hz
backspins/05 A6.wav | A6 | 1726.05Hz
backspins/06 A6.wav | A6 | 1759.62Hz
backspins/07 G#7.wav | G#7 | 3358.02Hz
backspins/08 C2.wav | C2 | 66.60Hz
backspins/09 E4.wav | E4 | 336.42Hz
backspins/10 A3.wav | A3 | 222.29Hz
backspins/11 D#3.wav | D#3 | 156.20Hz
backspins/12 A#3.wav | A#3 | 228.88Hz
backspins/13 F3.wav | F3 | 174.87Hz

### Credits

WAV files retrieved from:

- `backspins/` (a.k.a spinbacks):
  + Thread: https://www.reddit.com/r/edmproduction/comments/7ojge8/i_made_some_backspin_samples_for_you/
  + Drive: https://drive.google.com/drive/folders/1A3hoQhpYkVq2ARXp9jJzwtK61iZ_ybOB
- `supersaws/`: created with Sox CLI tool or extracted from SF2/SFZ free soundfiles
- `supersquares/`: extracted from free SF2/SFZ soundfiles
- `cowbells/`: extracted from free SF2/SFZ soundfiles
