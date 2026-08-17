"""Using learned weights and the synthesis unit database, synthesize an output waveform."""

# Transform an input phoneme sequence to a target feature sequence
from concatenative_synthesis.features.phoneme import get_phoneme_feats


def ph_seq_to_feats(ph_seq):
    """
    Transforms a list of phonemes to a list of features.
    In the current approach, this list of phonemes communicates little information.
    We look solely at the proceeding and following phonemes.
    """
    ph_feats = []
    for ph in range(1, len(ph_seq)):
        pass
    return ph_feats


# Find 20 best candidates for each phoneme in the target sequence

# Use Viterbi to find the best (min cost) path through all candidates in target sequence

# Construct the output waveform from the candidate sequence
