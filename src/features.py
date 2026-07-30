"""Feature engineering and interpolation helpers."""
import numpy as np
import pandas as pd

def interpolate_to_monthly(annual_df, date_col, value_col, calendar, anchor_month="-07-01"):
    """Interpolate an annual series onto a monthly calendar (time-based)."""
    s = annual_df.copy()
    s["_d"] = pd.to_datetime(s[date_col].astype(str) + anchor_month)
    s = s.set_index("_d")[value_col].sort_index()
    return (s.reindex(s.index.union(calendar)).interpolate("time")
             .reindex(calendar).ffill().bfill())

def add_agent_density(m, population, calendar):
    adult = interpolate_to_monthly(population, "year", "adult_population", calendar)
    m["agent_density"] = m["mm_agents_active"].values / (adult.values / 100_000)
    return m

def add_account_ownership(m, own, calendar):
    m["account_ownership"] = interpolate_to_monthly(own, "YEAR", "account_ownership", calendar).values
    return m

def add_time_features(m, target="mm_value", lags=12):
    for L in range(1, lags + 1):
        m[f"{target}_lag{L}"] = m[target].shift(L)
        m[f"mm_active_accts_lag{L}"] = m["mm_active_accts"].shift(L)
    m["mm_value_roll3"] = m[target].rolling(3).mean()
    m["mm_value_roll6"] = m[target].rolling(6).mean()
    m["mm_value_yoy"] = m[target].pct_change(12) * 100
    m["month"] = pd.to_datetime(m["date"]).dt.month
    m["t_index"] = np.arange(1, len(m) + 1)
    return m

# Findex recoding
YN2 = ["female", "urban", "employed"]
YN4 = ["owns_mobile", "borrowed_formal", "saved_formal"]

def recode_findex(fx):
    fx = fx.copy()
    for c in YN2 + YN4:
        fx[c] = fx[c].map({1: 1, 2: 0})           # 3,4 -> NaN
    fx["has_internet"] = fx["has_internet"].map({0: 0, 1: 1})  # 2 -> NaN
    fx.loc[~fx["education"].isin([1, 2, 3]), "education"] = np.nan
    fx["age"] = fx["age"].fillna(fx["age"].median())
    fx["education"] = fx["education"].fillna(fx["education"].mode()[0])
    for c in YN2 + YN4 + ["has_internet"]:
        fx[c] = fx[c].fillna(fx[c].mode()[0]).astype(int)
    return fx
