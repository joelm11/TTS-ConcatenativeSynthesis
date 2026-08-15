from pathlib import Path

import pandas as pd

from ..data import gather_data_files
from .acoustic import _get_acoustic_feats
from .phoneme import PHONEME_PHONETIC_FEATURES, get_phoneme_feats, phonemes_from_lab


def _build_features(raw_data_triplet):
    phonemes = phonemes_from_lab(raw_data_triplet["ph"])

    # For each phoneme:
    # Format categorical features
    # Calculate acoustic features:
    # - Calculate its mfcc from the last ~10ms of its duration
    # - Calculate log power over its duration
    # - Calculate the log pitch from the pitch mark file and start/duration
    features = []
    for phone in phonemes:
        ph_feats = get_phoneme_feats(phone["ph"])
        acu_feats = _get_acoustic_feats(
            phone, raw_data_triplet["wav"], raw_data_triplet["pm"]
        )
        features.append(ph_feats | PHONEME_PHONETIC_FEATURES[phone["ph"]] | acu_feats)

    return features


def build_features(raw_data_files, output_dir: Path, batch_size=100):
    """Calculate features from files in batches and write them out."""

    for i in range(0, len(raw_data_files), batch_size):
        chunk = raw_data_files[i : i + batch_size]
        features = []
        for triplet in chunk:
            features.append(_build_features(triplet))

        # Write out features
        df = pd.DataFrame(features)
        df.to_parquet(output_dir, engine='pyarrow', compression='snappy', index=True)

def build_database(output_dir, num_train):
    """Builds the phoneme database from available data and returns the partition to be used for training."""
    raw_data_files = gather_data_files(
        Path.cwd() / "data" / "raw" / "cmu_us_awb_arctic"
    )
    database_data = raw_data_files[:-num_train]
    train_data = raw_data_files[-num_train:]
    build_features(database_data, output_dir)
    return train_data


if __name__ == "__main__":
    DATABASE_DIR = Path.cwd() / "data" / "features" / "phoneme_unit_db.parquet"
    build_database(DATABASE_DIR, 200)
