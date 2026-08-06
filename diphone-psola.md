# Diphone PSOLA

This text to speech pipeline breaks text into diphones, then uses a PSOLA vocoder to synthesize the output waveforms.
DPSOLA is a concatenative TTS system, where we use unit selection methods to find synthesis segments that are chunks (diphones) of prerecorded speech.

## Diphone Deconstruction

The diphone deconstruction pipeline has several steps.

1. Text normalization
2. Normalized text to diphones

Step 2 is going to be tricky. References 14, 38, 99, 31, 50, 108 of the text.


## PSOLA Synthesis

We use PSOLA to synthesize the waveform given the calculated diphones.

## Simplest Implementation

## Thoughts as I read papers

Thus far *UNIT SELECTION IN A CONCATENATIVE SPEECH SYNTHESIS SYSTEM USING A LARGE SPEECH DATABASE* has been the most useful paper.

Input to the system is text. This text is transformed to a *target*. The target specification varies amongst implementations. The target includes the string of phonemes required to synthesize the text, and may have prosodic features like pitch and power.

## Algorithm Implementation

**TTS Online Algorithm**
1. Input text -> target feature vector of phonemes (and possibly additional features).
2. Synthesis unit selection to build output waveform. The output is simply concatenated rather than PSOLA'd for now.

**TTS Offline Algorithm**
1. Data shaping.
2. Train weights for cost function.

### Implementation Steps

- [x] Examine and understand the phoneme database shape. I may need to generate features via provided scripts.
- [x] Understand linear regression.
- [ ] Implement cost functions.
- [ ] Understand regression implementations for the weights of the cost functions.
- [ ] Decide how to store weights in file.
- [ ] Implement Viterbi search.
- [ ] Implement text analysis (text to phonemes (+other features)).
- [ ] Implement waveform reconstruction from constructed output unit selection vector.
- [ ] Evaluate against some benchmarks.

### Data Shape

The data gives the phoneme and its end time. The duration is calculated by `Ti - Ti-1`.

```
0.29950 125 pau
0.62450 125 pau
0.77450 125 ao
0.88700 125 th
0.95575 125 er
```

### Linear Regression

