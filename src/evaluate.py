"""Evaluation metrics for classification (RQ1) and forecasting (RQ2/RQ3)."""
import numpy as np

def classification_metrics(y, pred, proba=None):
    y = np.asarray(y); pred = np.asarray(pred)
    TP = int(((pred == 1) & (y == 1)).sum()); TN = int(((pred == 0) & (y == 0)).sum())
    FP = int(((pred == 1) & (y == 0)).sum()); FN = int(((pred == 0) & (y == 1)).sum())
    acc = (TP + TN) / len(y)
    prec = TP / (TP + FP) if TP + FP else 0.0
    rec = TP / (TP + FN) if TP + FN else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    out = {"accuracy": acc, "precision": prec, "recall": rec, "f1": f1,
           "confusion": {"TP": TP, "TN": TN, "FP": FP, "FN": FN}}
    if proba is not None:
        pos = np.asarray(proba)[y == 1]; neg = np.asarray(proba)[y == 0]
        if len(pos) and len(neg):
            gt = (pos[:, None] > neg[None, :]).sum()
            eq = (pos[:, None] == neg[None, :]).sum()
            out["auc"] = float((gt + 0.5 * eq) / (len(pos) * len(neg)))
    return out

def forecast_metrics(y, pred):
    y = np.asarray(y, float); pred = np.asarray(pred, float); e = y - pred
    return {"RMSE": float(np.sqrt(np.mean(e ** 2))),
            "MAE": float(np.mean(np.abs(e))),
            "MAPE": float(np.mean(np.abs(e / y)) * 100),
            "R2": float(1 - np.sum(e ** 2) / np.sum((y - y.mean()) ** 2))}
