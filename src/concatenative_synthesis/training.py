"""
Calculation of training weights for synthesis.
We use sequences of phonemes and speech from the train set as the target sequence.
Target and concatenative cost functions are then used to find the 20 best candidates for each phoneme.
We calculate the distances between the target phoneme and the 20 best candidates from their feature vectors.
We accumulate the results then learn the weights via multiple linear regression.
"""

import time
from pathlib import Path

import numpy as np
import pandas as pd

from .features.extract import build_database, features_from_triplet


def target_seq_subcosts(target_seq_feats, subcost_feat_cols, synthesis_db: Path):
    """Compute and accumulate normal equations of subcosts for target_seq."""
    N_BEST = 20
    P_FEAT_COLS = len(subcost_feat_cols)

    # Accumulators for normal equations:  A += X^T X,  b += X^T y
    a_total = np.zeros((P_FEAT_COLS, P_FEAT_COLS))
    b_total = np.zeros(P_FEAT_COLS)

    # For each target in sequence, pull top 20 matches by cepstral distance
    for target_ph in target_seq_feats:
        matching_ph = pd.read_parquet(
            synthesis_db, filters=[("ph", "==", target_ph["ph"])]
        )
        target_mfcc = target_ph["mfcc"]
        candidate_mfccs = np.array(matching_ph["mfcc"].tolist())
        candidates = (
            matching_ph.assign(
                dist=np.linalg.norm(target_mfcc - candidate_mfccs, axis=1)
            )
            .sort_values(by="dist", ascending=True)
            .head(N_BEST)
        )

        n = len(candidates)
        assert n == 20, f"Less than 20 candidates found for {target_ph['ph']}"

        # Build X: (n x p) sub-cost matrix
        x_batch = np.zeros((n, P_FEAT_COLS))

        # Binary match sub-costs (1 = same, 0 = different)
        x_batch[:, 0] = (candidates["nph"].values == target_ph["nph"]).astype(float)
        x_batch[:, 1] = (candidates["pph"].values == target_ph["pph"]).astype(float)

        # Float absolute-difference sub-costs
        x_batch[:, 2] = np.abs(candidates['dur'].values - target_ph['dur'])
        x_batch[:, 3] = np.abs(candidates['log_power'].values - target_ph['log_power'])
        x_batch[:, 4] = np.abs(candidates['log_pitch'].values - target_ph['log_pitch'])

        # y: (n,) vector of acoustic (cepstral) distances
        y_batch = candidates['dist'].values

        # Accumulate normal equations
        a_total += x_batch.T @ x_batch
        b_total += x_batch.T @ y_batch

    return a_total, b_total


def train_weights(training_triplets, synthesis_db: Path):
    SUBCOST_FEAT_COLS = ["nph", "pph", "dur", "log_power", "log_pitch"]
    p = len(SUBCOST_FEAT_COLS)

    # Accumulate A and b over all training sequences
    A_total = np.zeros((p, p))
    b_total = np.zeros(p)

    for triplet in training_triplets:
        target_seq_feats = features_from_triplet(triplet)
        A, b = target_seq_subcosts(target_seq_feats, SUBCOST_FEAT_COLS, synthesis_db)
        A_total += A
        b_total += b

    # Solve once after all sequences
    w = np.linalg.solve(A_total, b_total)
    print("Learned weights:")
    for col, val in zip(SUBCOST_FEAT_COLS, w):
        print(col, ":", val)

    return w

if __name__ == "main":
    start = time.perf_counter()

    DATABASE_PATH = Path.cwd() / "data" / "features" / "phoneme_unit_db.parquet"
    training_triplets = build_database(DATABASE_PATH, 200)
    weights = train_weights(training_triplets, DATABASE_PATH)

    elapsed = time.perf_counter() - start
    print("Elapsed time: ", elapsed)