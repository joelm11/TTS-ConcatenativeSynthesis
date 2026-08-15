from pathlib import Path

# Vocabulary lists for categorical fields
MANNERS = [
    "vowel",
    "plosive",
    "fricative",
    "affricate",
    "nasal",
    "liquid",
    "glide",
    "silence",
]
PLACES = [
    "bilabial",
    "labiodental",
    "dental",
    "alveolar",
    "postalveolar",
    "palatal",
    "velar",
    "glottal",
    "none",
]

PHONEME_PHONETIC_FEATURES = {
    # Silence / Pauses
    "pau": {"is_vowel": 0, "is_voiced": 0, "manner": "silence", "place": "none"},
    "ssil": {"is_vowel": 0, "is_voiced": 0, "manner": "silence", "place": "none"},
    # Vowels (All vowels are voiced)
    "aa": {"is_vowel": 1, "is_voiced": 1, "manner": "vowel", "place": "none"},
    "ae": {"is_vowel": 1, "is_voiced": 1, "manner": "vowel", "place": "none"},
    "ah": {"is_vowel": 1, "is_voiced": 1, "manner": "vowel", "place": "none"},
    "ao": {"is_vowel": 1, "is_voiced": 1, "manner": "vowel", "place": "none"},
    "aw": {"is_vowel": 1, "is_voiced": 1, "manner": "vowel", "place": "none"},
    "ax": {"is_vowel": 1, "is_voiced": 1, "manner": "vowel", "place": "none"},
    "ay": {"is_vowel": 1, "is_voiced": 1, "manner": "vowel", "place": "none"},
    "eh": {"is_vowel": 1, "is_voiced": 1, "manner": "vowel", "place": "none"},
    "er": {"is_vowel": 1, "is_voiced": 1, "manner": "vowel", "place": "none"},
    "ey": {"is_vowel": 1, "is_voiced": 1, "manner": "vowel", "place": "none"},
    "ih": {"is_vowel": 1, "is_voiced": 1, "manner": "vowel", "place": "none"},
    "iy": {"is_vowel": 1, "is_voiced": 1, "manner": "vowel", "place": "none"},
    "ow": {"is_vowel": 1, "is_voiced": 1, "manner": "vowel", "place": "none"},
    "oy": {"is_vowel": 1, "is_voiced": 1, "manner": "vowel", "place": "none"},
    "uh": {"is_vowel": 1, "is_voiced": 1, "manner": "vowel", "place": "none"},
    "uw": {"is_vowel": 1, "is_voiced": 1, "manner": "vowel", "place": "none"},
    # Stops / Plosives
    "p": {"is_vowel": 0, "is_voiced": 0, "manner": "plosive", "place": "bilabial"},
    "b": {"is_vowel": 0, "is_voiced": 1, "manner": "plosive", "place": "bilabial"},
    "t": {"is_vowel": 0, "is_voiced": 0, "manner": "plosive", "place": "alveolar"},
    "d": {"is_vowel": 0, "is_voiced": 1, "manner": "plosive", "place": "alveolar"},
    "k": {"is_vowel": 0, "is_voiced": 0, "manner": "plosive", "place": "velar"},
    "g": {"is_vowel": 0, "is_voiced": 1, "manner": "plosive", "place": "velar"},
    # Fricatives
    "f": {"is_vowel": 0, "is_voiced": 0, "manner": "fricative", "place": "labiodental"},
    "v": {"is_vowel": 0, "is_voiced": 1, "manner": "fricative", "place": "labiodental"},
    "th": {"is_vowel": 0, "is_voiced": 0, "manner": "fricative", "place": "dental"},
    "dh": {"is_vowel": 0, "is_voiced": 1, "manner": "fricative", "place": "dental"},
    "s": {"is_vowel": 0, "is_voiced": 0, "manner": "fricative", "place": "alveolar"},
    "z": {"is_vowel": 0, "is_voiced": 1, "manner": "fricative", "place": "alveolar"},
    "sh": {
        "is_vowel": 0,
        "is_voiced": 0,
        "manner": "fricative",
        "place": "postalveolar",
    },
    "zh": {
        "is_vowel": 0,
        "is_voiced": 1,
        "manner": "fricative",
        "place": "postalveolar",
    },
    "hh": {"is_vowel": 0, "is_voiced": 0, "manner": "fricative", "place": "glottal"},
    # Affricates
    "ch": {
        "is_vowel": 0,
        "is_voiced": 0,
        "manner": "affricate",
        "place": "postalveolar",
    },
    "jh": {
        "is_vowel": 0,
        "is_voiced": 1,
        "manner": "affricate",
        "place": "postalveolar",
    },
    # Nasals
    "m": {"is_vowel": 0, "is_voiced": 1, "manner": "nasal", "place": "bilabial"},
    "n": {"is_vowel": 0, "is_voiced": 1, "manner": "nasal", "place": "alveolar"},
    "ng": {"is_vowel": 0, "is_voiced": 1, "manner": "nasal", "place": "velar"},
    # Liquids & Glides
    "l": {"is_vowel": 0, "is_voiced": 1, "manner": "liquid", "place": "alveolar"},
    "r": {"is_vowel": 0, "is_voiced": 1, "manner": "liquid", "place": "alveolar"},
    "w": {"is_vowel": 0, "is_voiced": 1, "manner": "glide", "place": "bilabial"},
    "y": {"is_vowel": 0, "is_voiced": 1, "manner": "glide", "place": "palatal"},
}


def phonemes_from_lab(lab_file: Path):
    """Extracts per phoneme data for all phonemes in a label file."""
    def proc_line(line):
        t_end, _, ph = line.strip().split(" ")
        return float(t_end), ph

    file_stem = lab_file.stem
    phonemes = []
    with open(lab_file, "r", encoding="utf-8") as ph_src:
        lines = ph_src.readlines()
        for i in range(2, len(lines) - 2):
            t_end_cph, cph = proc_line(lines[i])
            t_end_pph, pph = proc_line(lines[i - 1])
            _, nph = proc_line(lines[i + 1])
            idx = len(phonemes)
            phonemes.append(
                {
                    "lab_file": file_stem,
                    "ph_idx": idx,
                    "ph": cph,
                    "nph": nph,
                    "pph": pph,
                    "start": t_end_pph,
                    "dur": t_end_cph - t_end_pph,
                }
            )
    return phonemes

def get_phoneme_feats(phoneme):
    return PHONEME_PHONETIC_FEATURES[phoneme]