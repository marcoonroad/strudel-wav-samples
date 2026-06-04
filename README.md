# Strudel WAV Samples

### Example of Usage

```javascript
setcpm(135)

samples('github:marcoonroad/strudel-wav-samples')

$: sound("backspins:0/2")
  .mask("<0 0 [0!6 1!2] 0>/8")
  .cutoff(2500)
  .ftype("ladder")
  .velocity(0.25)

register('humanize', pattern => pattern.clip(rand.range(0.75, 1.0)))

$: stack(
    note("d#2 | f#2 | d#2 | g#2 | d#2 | c#2 | e2 | d#2".sub(9))
    .struct("<x x*2 x x?>").humanize()
    .sound("gm_slap_bass_1").velocity(0.25),
    sound("bd/8").bank("RolandTR808"),
    sound("<- [sd:0:.6,cp:0:.2] - [sd:0:.6,cp:0:.2]*2>").humanize().bank("RolandTR808"),
    sound("[- <- oh*2>]").bank("RolandTR808"),
    sound("[hh hh hh hh]").humanize().degradeBy("0.25".fast(4)).bank("RolandTR808")
  )
  .cutoff("<2700!2 [2400 2100 1800 1500 1200 900 600 300] 300>/8".add(1000))
  .ftype("24db")
  .mask("<1 1 [1!7 0!1] 0>/8")
  .pianoroll({ labels: 1 })
```

### Credits

WAV files retrieved from:

- `backspins/` (a.k.a spinbacks):
  + Thread: https://www.reddit.com/r/edmproduction/comments/7ojge8/i_made_some_backspin_samples_for_you/
  + Drive: https://drive.google.com/drive/folders/1A3hoQhpYkVq2ARXp9jJzwtK61iZ_ybOB
