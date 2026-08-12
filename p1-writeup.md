# Concatenative Text-To-Speech

_Notes to self_

I don't know what style to write these in. I want to be able to share this on my blog and socials, for a technical audience but appreciable by laymen as well. Formal, but using I and we.

Already I am seeing that more examples are needed!

- Target and candidate sequence illustrations!

To understand modern text to speech systems, I thought it would be useful to start at the beginning. Before deep learning approaches used today, problems like text-to-speech (tts) were solved algorithmically. This meant applying complex rule-based and statistical algorithms on input data to produce the desired results. Contrast this approach to deep learning, where rules are learned by processing vast amounts of data. While these early algorithms are in my opinion somewhat more complicated, they are not without their merits. Implementing algorithms in this manner requires a deep understanding of the domain and the data. Something I hoped to gain as I set out to implement one of the first sota tts implementations - speech synthesis via concatenation of phonemes.

## Reference Paper(s) and Dataset

My implementation was based on this paper _Speech Synthesis by Rule Using an Optimal Selection of Non-Uniform Synthesis Units_, and I used the corresponding CMU Arctic dataset. The dataset contains audio files of speech, and label files that identify and locate phonemes within the speech.

### Algorithm

Synthesis of output waveforms is done by concatenating phonemes from the database. Given a sequence of target phonemes, we search for an optimal sequence of phonemes from the database from which to compose our speech. Corresponding phoneme audio data is then concatenated to the output sequence (more advanced concatenation techniques maybe used e.g./tdpsola).

The database in this algorithm is treated as a state transition network. Given the target sequence, we want to select units such that we minimize some cost function for the sequence as a whole. Two costs are used: target and concatenative cost, which will be discussed in more detail later.

![Unit Selection Costs](resources/UnitSelectionCosts.png)

## Data

The extracted data contained ~1000 .wav files of labelled speech. Speech was labelled with composite phonemes and their locations in the file. Pitch mark files were also available for extracting fundamental frequency of the phonemes.

## Features and Cost Functions

For this application (and most if not all) raw data must be massaged into compute friendly features. Features are required for the target and concatenation cost functions, the training of their weights, and synthesis.

### Target Cost Function and Features

The target cost function describes the difference between the target unit and the candidate unit. Features for calculation of the target cost include phonetic identity of the current, preceding, and following phonemes (e.g./ vowel or consonant, consonant type, voicing, manner, placement). As these are all discrete features, they receive a binary score. Each of the $p$ sub-cost functions has a unique weight.

$$ C^{t}(t_i, u_i) = \sum_{j=1}^{p} w_j C^{t}_{j}(t_i, u_i) $$

### Concatenation Cost Function and Features

The concatenation cost function describes the cost of joining two units. The concatenation cost uses acoustic features of the phonemes (e.g./ cepstral distance at the concatenation point, differences in log power and log pitch).

### Final Cost Function

$$ C(t_1^n, u_1^n) = \sum_{i=1}^{n} \sum_{j=1}^{p} w_j^tC_j^t(t_i, u_i^t) + \sum_{i=2}^{n} \sum_{j=1}^{q} w_j^cC_j^c(u_j, u_i) + C^s(S, u_1) + C^c(u_n, S) $$

Where $S$ is silence.

## Training

## Model

## Synthesis

## Evals
