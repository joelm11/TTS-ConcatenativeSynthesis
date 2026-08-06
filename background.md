# TTS Background

Fundamental components of a TTS system include: text analysis, acoustic modelling, vocoders, and fully end to end models.

## Text Analysis

Transforms text into linguistic features for speech synthesis. Also called the frontend of TTS, the frontend is responsible for normalization of input text and various feature extraction depending on the pipeline.

## Acoustic Models

Acoustic models generate acoustic features from linguistic features e.g./ characters to mel spectrograms. The output of the acoustic model would then be fed to a vocoder for synthesis.

## Vocoders

While vocoders may include an analysis stage, more typical to this work is using vocoders for waveform synthesis from features. There are many flavours of vocoder: algorithmic, neural, or otherwise.

## End to End Models

End to end models are the end goal of TTS and synthesis speech waveforms from character sequences directly.
