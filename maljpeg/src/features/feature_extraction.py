from const import feature_name
from feature_extractor import JPEG

import os
import sys
import argparse
import pandas as pd
from tqdm import tqdm


def arg_parser():
    parser = argparse.ArgumentParser(description="Feature Extraction")
    parser.add_argument("--path", type=str, help="path to the dataset", required=True)
    parser.add_argument("--output", type=str, help="output file name", required=True)

    return parser.parse_args()


def main():
    args = arg_parser()

    print(f"Output file: {args.output}")
    print(f"Path to the dataset: {args.path}")

    raw_jpgs = os.listdir(args.path)
    print(f"Number of images: {len(raw_jpgs)}")
    features = []

    for raw_jpg in tqdm(raw_jpgs):
        raw_jpg_path = os.path.join(args.path, raw_jpg)
        jpg = JPEG(raw_jpg_path)
        features.append(jpg.decode())

    features = pd.DataFrame(features, columns=feature_name)
    features.to_csv(args.output, index=False)

    pass


if __name__ == "__main__":
    main()
