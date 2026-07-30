"""Read the raw input files.

Downloading from the portals is done by hand or with an API key (see the
README). This just reads the files already saved in data/raw/.
"""
import pandas as pd
from .config import RAW

def load_monthly():
    return pd.read_excel(RAW / "monthly_series.xlsx")

def load_findex():
    f21 = pd.read_excel(RAW / "findex_ghana_2021.xlsx")
    f25 = pd.read_excel(RAW / "findex_ghana_2025.xlsx")
    return f21, f25

def load_population():
    return pd.read_excel(RAW / "agent_density_population.xlsx")

def load_account_ownership():
    return pd.read_excel(RAW / "yearly_account_ownership.xlsx")
