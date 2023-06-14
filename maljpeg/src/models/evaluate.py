import pickle
import argparse
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
    roc_curve,
)


def arg_parser():
    parser = argparse.ArgumentParser(description="Evaluation")
    parser.add_argument(
        "--test",
        type=str,
        help="path to the test dataset",
        default="data/processed/test.csv",
    )
    parser.add_argument(
        "--models",
        type=str,
        help="path to the trained models",
        default="models/",
    )
    parser.add_argument(
        "--outdir", type=str, help="folder to store report", default="reports/"
    )

    return parser.parse_args()


def tpr_fpr_idr(y_true, y_pred):
    TN, FP, FN, TP = confusion_matrix(y_true, y_pred).ravel()

    TPR = TP / (TP + FN)
    FPR = FP / (FP + TN)
    IDR = TPR * (1 - FPR)

    return TPR, FPR, IDR


def main():
    args = arg_parser()

    print(f"Testing models...")
    print(f"Output folder: {args.outdir}")
    print(f"Path to the test dataset: {args.test}")

    print(f"Loading models...")

    with open(args.models + "xgb.pkl", "rb") as f:
        clf_xgb = pickle.load(f)

    with open(args.models + "lgbm.pkl", "rb") as f:
        clf_lgbm = pickle.load(f)

    with open(args.models + "rf.pkl", "rb") as f:
        clf_rf = pickle.load(f)

    with open(args.models + "dt.pkl", "rb") as f:
        clf_dt = pickle.load(f)

    print(f"Models loaded!")

    print(f"Loading test dataset...")

    test = pd.read_csv(args.test)

    X_test = test.iloc[:, :-1]
    y_test = test.iloc[:, -1]

    print(f"Test dataset loaded!")

    print(f"Predicting test dataset...")

    y_pred_xgb = clf_xgb.predict(X_test)
    y_pred_lgbm = clf_lgbm.predict(X_test)
    y_pred_rf = clf_rf.predict(X_test)
    y_pred_dt = clf_dt.predict(X_test)

    print(f"Predictions completed!")

    print(f"Evaluating models...")

    report = pd.DataFrame(
        columns=[
            "Model",
            "AUC",
            "TPR",
            "FPR",
            "IDR",
        ]
    )

    report.loc[0] = [
        "XGBoost",
        roc_auc_score(y_test, y_pred_xgb),
        tpr_fpr_idr(y_test, y_pred_xgb)[0],
        tpr_fpr_idr(y_test, y_pred_xgb)[1],
        tpr_fpr_idr(y_test, y_pred_xgb)[2],
    ]

    report.loc[1] = [
        "LightGBM",
        roc_auc_score(y_test, y_pred_lgbm),
        tpr_fpr_idr(y_test, y_pred_lgbm)[0],
        tpr_fpr_idr(y_test, y_pred_lgbm)[1],
        tpr_fpr_idr(y_test, y_pred_lgbm)[2],
    ]

    report.loc[2] = [
        "Random Forest",
        roc_auc_score(y_test, y_pred_rf),
        tpr_fpr_idr(y_test, y_pred_rf)[0],
        tpr_fpr_idr(y_test, y_pred_rf)[1],
        tpr_fpr_idr(y_test, y_pred_rf)[2],
    ]

    report.loc[3] = [
        "Decision Tree",
        roc_auc_score(y_test, y_pred_dt),
        tpr_fpr_idr(y_test, y_pred_dt)[0],
        tpr_fpr_idr(y_test, y_pred_dt)[1],
        tpr_fpr_idr(y_test, y_pred_dt)[2],
    ]

    print(f"Models evaluated!")

    print(f"Saving report...")

    report.to_csv(args.outdir + "report.csv", index=False)

    ax = report.plot.bar(
        x="Model", y=["TPR", "FPR", "IDR", "AUC"], rot=0, figsize=(8, 6)
    )

    for container in ax.containers:
        ax.bar_label(container, padding=3, color="black", fontsize=8, fmt="%0.3f")

    ax.legend(
        loc="best",
        ncol=4,
        bbox_to_anchor=[1, 1.04],
        borderaxespad=0,
        frameon=False,
        fontsize=8,
    )
    fig = ax.get_figure()

    ax.grid(which="major", axis="y", color="#DAD8D7", alpha=0.5, zorder=1)
    ax.set_xlabel("", fontsize=12, labelpad=10)
    ax.xaxis.set_label_position("bottom")
    ax.xaxis.set_tick_params(
        pad=2, labelbottom=True, bottom=True, labelsize=12, labelrotation=0
    )
    ax.spines[["top", "bottom"]].set_visible(False)
    ax.spines["right"].set_linewidth(1.1)

    ax.plot(
        [0.12, 0.9],
        [0.98, 0.98],
        transform=fig.transFigure,
        clip_on=False,
        color="#E3120B",
        linewidth=0.6,
    )
    ax.add_patch(
        plt.Rectangle(
            (0.12, 0.98),
            0.04,
            -0.02,
            facecolor="#E3120B",
            transform=fig.transFigure,
            clip_on=False,
            linewidth=0,
        )
    )

    ax.text(
        x=0.12,
        y=0.93,
        s="Detection results of classifiers on the dataset",
        transform=fig.transFigure,
        ha="left",
        fontsize=14,
        weight="bold",
        alpha=0.8,
    )
    ax.text(
        x=0.12,
        y=0.90,
        s="TPR: True Positive Rate, FPR: False Positive Rate, IDR: Integrated Detection Rate",
        transform=fig.transFigure,
        ha="left",
        fontsize=12,
        alpha=0.8,
    )

    plt.subplots_adjust(
        left=None,
        bottom=0.1,
        right=None,
        top=0.85,
        wspace=None,
        hspace=None,
    )

    fig.patch.set_facecolor("white")

    fig.savefig(args.outdir + "report.png", dpi=96)

    cm = confusion_matrix(y_test, y_pred_xgb, normalize="true")
    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm, display_labels=["benign", "malicious"]
    )
    disp.plot(cmap="Blues")
    disp.ax_.set_title("XGBoost")
    disp.ax_.set_xlabel("Predicted label")
    disp.ax_.set_ylabel("True label")
    disp.figure_.savefig(args.outdir + "xgb_cm.png")

    cm = confusion_matrix(y_test, y_pred_lgbm, normalize="true")
    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm, display_labels=["benign", "malicious"]
    )
    disp.plot(cmap="Blues")
    disp.ax_.set_title("LightGBM")
    disp.ax_.set_xlabel("Predicted label")
    disp.ax_.set_ylabel("True label")
    disp.figure_.savefig(args.outdir + "lgbm_cm.png")

    cm = confusion_matrix(y_test, y_pred_rf, normalize="true")
    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm, display_labels=["benign", "malicious"]
    )
    disp.plot(cmap="Blues")
    disp.ax_.set_title("Random Forest")
    disp.ax_.set_xlabel("Predicted label")
    disp.ax_.set_ylabel("True label")
    disp.figure_.savefig(args.outdir + "rf_cm.png")

    cm = confusion_matrix(y_test, y_pred_dt, normalize="true")
    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm, display_labels=["benign", "malicious"]
    )
    disp.plot(cmap="Blues")
    disp.ax_.set_title("Decision Tree")
    disp.ax_.set_xlabel("Predicted label")
    disp.ax_.set_ylabel("True label")
    disp.figure_.savefig(args.outdir + "dt_cm.png")

    return


if __name__ == "__main__":
    main()
