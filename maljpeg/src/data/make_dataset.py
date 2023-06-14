from sklearn.model_selection import train_test_split
import pandas as pd
import argparse


def arg_parser():
    parser = argparse.ArgumentParser(description="Make Dataset")
    parser.add_argument(
        "--benign",
        type=str,
        help="path to the benign dataset",
        default="data/interim/benign.csv",
    )
    parser.add_argument(
        "--malicious",
        type=str,
        help="path to the malicious dataset",
        default="data/interim/malicious.csv",
    )
    parser.add_argument(
        "--out_train",
        type=str,
        help="output train file",
        default="data/processed/train.csv",
    )
    parser.add_argument(
        "--out_test",
        type=str,
        help="output test file",
        default="data/processed/test.csv",
    )

    return parser.parse_args()


def main():
    args = arg_parser()

    print(f"Preparing dataset...")
    print(f"Output files: {args.out_train}, {args.out_test}")
    print(f"Path to the benign dataset: {args.benign}")
    print(f"Path to the malicious dataset: {args.malicious}")

    benign = pd.read_csv(args.benign)
    malicious = pd.read_csv(args.malicious)

    label = [0] * benign.shape[0] + [1] * malicious.shape[0]

    data = pd.concat([benign, malicious])

    X_train, X_test, y_train, y_test = train_test_split(
        data, label, test_size=0.25, stratify=label
    )

    X_train["label"] = y_train
    X_test["label"] = y_test

    X_train.to_csv(args.out_train, index=False)
    X_test.to_csv(args.out_test, index=False)

    pass


if __name__ == "__main__":
    main()
