"""Simple models written with numpy only, for the interim results.

Kept to numpy so the notebooks run without any extra libraries. The final
report adds scikit-learn and statsmodels versions of these.
"""
import numpy as np

def _standardise(X, mu=None, sd=None):
    if mu is None:
        mu = X.mean(0); sd = X.std(0); sd[sd == 0] = 1
    return (X - mu) / sd, mu, sd

def logistic_fit(X, y, lr=0.3, iters=4000, seed=42):
    Xz, mu, sd = _standardise(X.astype(float))
    Xb = np.c_[np.ones(len(Xz)), Xz]
    w = np.zeros(Xb.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-Xb @ w))
        w -= lr * Xb.T @ (p - y) / len(y)
    return {"w": w, "mu": mu, "sd": sd}

def logistic_predict_proba(model, X):
    Xz, _, _ = _standardise(X.astype(float), model["mu"], model["sd"])
    Xb = np.c_[np.ones(len(Xz)), Xz]
    return 1 / (1 + np.exp(-Xb @ model["w"]))

def ols_fit(X, y):
    Xz, mu, sd = _standardise(X.astype(float))
    Xb = np.c_[np.ones(len(Xz)), Xz]
    beta, *_ = np.linalg.lstsq(Xb, y, rcond=None)
    return {"beta": beta, "mu": mu, "sd": sd}

def ols_predict(model, X):
    Xz, _, _ = _standardise(X.astype(float), model["mu"], model["sd"])
    Xb = np.c_[np.ones(len(Xz)), Xz]
    return Xb @ model["beta"]
