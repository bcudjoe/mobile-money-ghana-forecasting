"""Project paths and data-source URLs."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
FIGURES = ROOT / "outputs" / "figures"
for p in (PROCESSED, FIGURES):
    p.mkdir(parents=True, exist_ok=True)

# Public data sources (see README for access notes)
SOURCES = {
    "bog_portal": "https://app.datawarehousepro.com/go/bog/",
    "bog_summary": "https://www.bog.gov.gh/economic-data/",
    "findex": "https://microdata.worldbank.org/index.php/catalog/global-findex",
    "wdi_account_ownership": "FX.OWN.TOTL.ZS",
    "nca": "https://nca.org.gh/",
    "imf_fas": "https://data.imf.org/en/datasets/IMF.STA:FAS",
}
ELEVY_START = "2022-05-01"
