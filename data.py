#!/usr/bin/python3

import os
import tarfile
import urllib.request
from pathlib import Path

DATASET_URL = (
    "http://festvox.org/cmu_arctic/cmu_arctic/packed/cmu_us_awb_arctic-0.90-release.tar.bz2"
)
DATASET_ARCHIVE = "cmu_us_awb_arctic.tar.bz2"


# 2 data directories: data/raw/ and data/processed/
def setup_dir_structure(project_root: Path):
    raw = project_root / "data" / "raw"
    features = project_root / "data" / "features"

    raw.mkdir(parents=True, exist_ok=True)
    features.mkdir(parents=True, exist_ok=True)

    return raw


def download_extract_dataset(output_dir: Path):
    archive_path = output_dir / DATASET_ARCHIVE
    urllib.request.urlretrieve(DATASET_URL, archive_path)
    with tarfile.open(archive_path, "r:bz2") as tar:
        tar.extractall(path=output_dir)
    os.remove(archive_path)


if __name__ == "__main__":
    raw_data_dir = setup_dir_structure(Path(os.getcwd()))
    download_extract_dataset(raw_data_dir)
