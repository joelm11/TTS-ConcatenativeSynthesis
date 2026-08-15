from pathlib import Path

import librosa
import numpy as np


def _mfcc(samples, sr, k=12):
    n_fft = 512
    n_pad = n_fft - len(samples)

    if n_pad > 0:
        samples = np.pad(samples, (0, n_pad))
    else:
        samples = samples[:n_fft]  # Take first 512 samples if longer

    # Compute MFCCs without centering/padding extra frames
    mfcc = librosa.feature.mfcc(
        y=samples,
        sr=sr,
        n_mfcc=k,
        n_fft=n_fft,
        hop_length=n_fft + 1,  # Prevents librosa from trying to frame into step 2
        center=False,  # Prevents zero-padding at boundaries
    )
    return mfcc.squeeze()


def log_power(samples):
    e = 0.01
    return np.log(np.sqrt(np.mean(samples**2)) + e)


def log_pitch(periods, duration):
    return np.log(periods / duration + 0.0001)


def count_periods(pitchmarks, t_start, t_dur):
    def extract_line(line):
        t_curr, _ = line.strip().split(" ")
        return float(t_curr)

    pitchmarks = pitchmarks[8:-1]
    count = 0
    for line in pitchmarks:
        t_curr = extract_line(line)
        if t_start <= t_curr <= t_start + t_dur:
            count += 1
        elif t_curr > t_start + t_dur:
            break
    return count


# TODO: This could be cleaned up (pass in file and pitchmarks instead of opening file each time)
def _get_acoustic_feats(phoneme, wav_file: Path, pm_file: Path):
    t_start = phoneme["start"]
    t_dur = phoneme["dur"]

    # Retrieve samples from wav file
    samples, sr = librosa.load(wav_file, sr=None)

    # Pull raw pitchmarks from file
    pms = []
    with open(pm_file, "r", encoding="utf-8") as cpm_file:
        pms = cpm_file.readlines()
        pms = pms[8:]

    mfcc = _mfcc(samples, sr)
    lpwr = log_power(samples)
    lppm = log_pitch(count_periods(pms, t_start, t_dur), t_dur)
    return {"mfcc": mfcc, "log_power": lpwr, "log_pitch": lppm}