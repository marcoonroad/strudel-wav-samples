// @ts-check

'use strict'

// NOTE: custom prebake strudel script but using async/await operations
// for additional module/scripting loading - DISCLAIMER:
//   POTENTIALLY DANGEROUS DON'T LOAD ANY RANDOM EXTERNAL SCRIPT
//   IN THIS WAY, ONLY LOAD TRUSTED SCRIPTS THAT ARE FIXED SNAPSHOTS,
//   THAT IS, THEIR CODE WON'T EVER CHANGE AGAIN, AVOID USING RELATIVE
//   VERSION TAGS LIKE latest AND SORT OF THAT -- YOU'VE BEEN WARNED --

var prebakeLoader = (async function () {
    const response = await fetch('https://unpkg.com/spadille@0.0.3/dist/index.js')
    const script = await response.text()
    const loader = new Function(script + ';return spadille;')
    const spadille = loader()
    /**
     * @param {Object} [options] - The object map for configuration flags here
     * @param {string} [options.payload] - Any string here provided as a seed for the random break pattern
     * @param {string} [options.sound] - The input break sound, might be amen, riffin, funkydrummer, etc
     * @param {number} [options.slices] - How much to slice the input break sound, it's often 8, 16 or 32
     * @param {number} [options.amount] - How long in cycles (non-fast yet) would be the whole break pattern
     * @param {number} [options.fast] - How fast would the break patterns be looped
     */
    const breakGen = async function (options) {
        options = options || {}
        const _PAYLOAD = options.payload || '424242'
        const _SOUND = options.sound || 'amen'
        const _SLICES = options.slices || 16
        const _AMOUNT = options.amount || (_SLICES * 2)
        const _FAST = options.fast || 1
        /** @type {number[]} */
        let _steps = await spadille.prng.generate({
            secret: _SOUND,
            payload: 'step-sample-n' + (_PAYLOAD || 1).toString(),
            minimum: 0,
            maximum: _SLICES - 1,
            amount: _AMOUNT,
            distinct: false,
        })
        /** @type {number[]} */
        let _indexes = await spadille.prng.generate({
            secret: _SOUND,
            payload: 'index-sample-n' + (_PAYLOAD || 1).toString(),
            minimum: 0,
            maximum: 7,
            amount: _AMOUNT,
            distinct: false,
        })
        /** @type {number[]} */
        let _gains = await spadille.prng.generate({
            secret: _SOUND,
            payload: 'gain-sample-n' + (_PAYLOAD || 1).toString(),
            minimum: 90,
            maximum: 100,
            amount: _AMOUNT,
            distinct: false,
        })
        /** @type {number[]} */
        let _pans = await spadille.prng.generate({
            secret: _SOUND,
            payload: 'pan-sample-n' + (_PAYLOAD || 1).toString(),
            minimum: 40,
            maximum: 60,
            amount: _AMOUNT,
            distinct: false,
        })
        /** @type {number[]} */
        let _driftsA = await spadille.prng.generate({
            secret: _SOUND,
            payload: 'start-drift-sample-n' + (_PAYLOAD || 1).toString(),
            minimum: 0,
            maximum: 2,
            amount: _AMOUNT,
            distinct: false,
        })
        /** @type {number[]} */
        let _driftsB = await spadille.prng.generate({
            secret: _SOUND,
            payload: 'end-drift-sample-n' + (_PAYLOAD || 1).toString(),
            minimum: 0,
            maximum: 2,
            amount: _AMOUNT,
            distinct: false,
        })
        let driftsA = arrange(..._driftsA.map(drift => [1, pure(drift / 100)]))
        let driftsB = arrange(..._driftsB.map(drift => [1, pure(1 - (drift / 100))]))
        let pans = arrange(..._pans.map(pan => [1, pure(pan / 100)]))
        let gains = arrange(..._gains.map(gain => [1, pure(gain / 100)]))
        // patterns based on indexes:
        // - 1 2 3 4 or 4 3 2 1
        // - 1 2 1 2 or 2 1 2 1
        // - 1 1 1 1
        // - 1 1
        // - 1 2 or 2 1
        /** @type {(step: number) => WaveForm} */
        const k = step => pure(step % _SLICES)
        /** @type {(steps: number[]) => WaveForm} */
        const ks = steps => fastcat(...steps.map(k))
        let steps = arrange(..._steps.map((step, index) => [1,
            _indexes[index] === 0 ? ks([step + 1, step]) :
            _indexes[index] === 1 ? ks([step, step + 1]) :
            _indexes[index] === 2 ? ks([step, step, step, step]) :
            _indexes[index] === 3 ? ks([step, step + 1, step, step + 1]) :
            _indexes[index] === 4 ? ks([step + 1, step, step + 1, step]) :
            _indexes[index] === 5 ? ks([step, step + 1, step + 2, step + 3]) :
            _indexes[index] === 6 ? ks([step + 3, step + 2, step + 1, step]) :
            _indexes[index] === 7 ? ks([step, step]) : silence // NOTE: silence is never reached here
        ]))
        return sound(_SOUND).splice(_SLICES, steps.fast(_FAST))
            .pan(pans).compress(driftsA, driftsB).mul(velocity(gains))
    }
    return {
        breakGen,
    }
})
