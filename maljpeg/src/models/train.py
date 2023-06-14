import pickle
import argparse
import pandas as pd

import xgboost as xgb
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

clf_xgb = xgb.XGBClassifier()
clf_lgbm = LGBMClassifier()
clf_rf = RandomForestClassifier()
clf_dt = DecisionTreeClassifier()


def arg_parser():
    parser = argparse.ArgumentParser(description="Train")
    parser.add_argument(
        "--train",
        type=str,
        help="path to the train dataset",
        default="data/processed/train.csv",
    )
    parser.add_argument(
        "--outdir", type=str, help="folder to contain trained model", default="models/"
    )

    return parser.parse_args()


def main():
    args = arg_parser()

    print(f"Training models...")
    print(f"Output folder: {args.outdir}")
    print(f"Path to the train dataset: {args.train}")

    train = pd.read_csv(args.train)

    X_train = train.iloc[:, :-1]
    y_train = train.iloc[:, -1]

    print(f"Training XGBoost...")
    clf_xgb.fit(X_train, y_train)

    print(f"Training LightGBM...")
    clf_lgbm.fit(X_train, y_train)

    print(f"Training Random Forest...")
    clf_rf.fit(X_train, y_train)

    print(f"Training Decision Tree...")
    clf_dt.fit(X_train, y_train)

    print(f"Training completed!")
    print(f"Saving models...")

    with open(args.outdir + "xgb.pkl", "wb") as f:
        pickle.dump(clf_xgb, f)

    with open(args.outdir + "lgbm.pkl", "wb") as f:
        pickle.dump(clf_lgbm, f)

    with open(args.outdir + "rf.pkl", "wb") as f:
        pickle.dump(clf_rf, f)

    with open(args.outdir + "dt.pkl", "wb") as f:
        pickle.dump(clf_dt, f)

    return


if __name__ == "__main__":
    main()
