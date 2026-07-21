# Predicting Mobile Money Transactions and Digital Financial Inclusion Growth in Ghana

Forecasting Ghana's mobile money growth and explaining its drivers with machine learning and publicly available financial-access indicators.

**Author:** Nana Asomia · **Course:** QM640 Data Analytics Capstone, Walsh College · **Term:** Summer 2026

---

## Overview

This project models digital financial inclusion in Ghana along two tracks that are kept deliberately separate because they use different units of analysis:

- **National time-series track** — monthly Bank of Ghana payment data (~2013–present) is used to forecast mobile money transaction value and active-account growth six to twelve months ahead.
- **Individual cross-sectional track** — World Bank Global Findex survey records are used to identify which socioeconomic and financial factors drive individual adoption.

The two tracks are analysed independently and their results are combined only at the interpretation stage to produce policy recommendations.

## Research questions

| RQ | Question | Track | Method |
|----|----------|-------|--------|
| RQ1 | Which factors most strongly drive mobile money adoption? | Individual (Findex) | Logistic regression + SHAP on a tree model |
| RQ2 | Can ML accurately forecast transaction value and account growth? | National monthly | SARIMA / Prophet baselines + gradient boosting on lag features |
| RQ3 | Which algorithm forecasts most accurately? | National monthly | Rolling-origin backtest + Diebold–Mariano test |
| RQ4 | What policy actions improve inclusion? | Synthesis | Driver-based scenario analysis |

## Repository structure

```
mobile-money-ghana-forecasting/
├── data/
│   ├── raw/                     # original downloads (large files git-ignored)
│   ├── interim/                 # cleaned, pre-merge
│   └── processed/               # model-ready tables
│       ├── monthly_series.csv   # national monthly panel (RQ2/RQ3)
│       └── findex_ghana.csv     # individual records (RQ1)
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_cleaning_merge.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_rq1_adoption_drivers.ipynb
│   ├── 05_rq2_forecasting.ipynb
│   ├── 06_rq3_model_comparison.ipynb
│   └── 07_rq4_scenarios.ipynb
├── src/
│   ├── config.py                # paths, source URLs, constants
│   ├── data_collection.py       # download / API pulls (FRED, World Bank)
│   ├── features.py              # lags, rolling means, YoY, E-Levy flag
│   ├── models.py                # model definitions and tuning
│   └── evaluate.py              # RMSE / MAE / MAPE / R2, Diebold–Mariano
├── outputs/
│   ├── figures/                 # EDA and result charts
│   ├── models/                  # serialized fitted models
│   └── forecasts/               # forecast tables with error bands
├── docs/
│   └── data_dictionary.md       # full variable definitions (also .csv)
├── requirements.txt
├── environment.yml
├── .gitignore
└── README.md
```

## Data sources and licences

| Source | Content used | Frequency | Access | Licence / terms |
|--------|--------------|-----------|--------|-----------------|
| [Bank of Ghana – Payment Systems Statistics](https://www.bog.gov.gh/banking-and-payments-system/payment-systems-statistics/) | Transaction value & volume, accounts, agents | Monthly, ~2013–present | Public download | Open, attribution |
| [Bank of Ghana – Statistical Bulletin](https://www.bog.gov.gh/publications/statistical-bulletin/) | Inflation, policy rate, exchange rate | Monthly / quarterly | Public download | Open, attribution |
| [World Bank Global Findex](https://www.worldbank.org/en/publication/globalfindex) | Individual adoption & correlates | Survey waves (2011–2025) | Free registration (microdata library) | CC BY 4.0 |
| [IMF Financial Access Survey](https://data.imf.org/en/datasets/IMF.STA:FAS) | Annual mobile money indicators | Annual, 2004–present | Public / [FRED API mirror](https://fred.stlouisfed.org/series/GHAFCMARNUM) | Open, attribution |
| [National Communications Authority (Ghana)](https://nca.org.gh) | Mobile & data subscriptions | Monthly / quarterly | Public | Open, attribution |
| [World Bank WDI](https://data.worldbank.org/country/ghana) | Internet users, GDP, population | Annual | Public API | CC BY 4.0 |

> Raw files are not redistributed in this repository. `src/data_collection.py` downloads them from the sources above so the pipeline stays reproducible without violating any source's terms.

## Data dictionary

Full variable definitions are in [`docs/data_dictionary.md`](docs/data_dictionary.md) (machine-readable version: `docs/data_dictionary.csv`).

## Environment setup

Python 3.11 is recommended.

```bash
# with pip
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# or with conda
conda env create -f environment.yml
conda activate momo-ghana
```

## How to reproduce

Run the notebooks in order, or the equivalent scripts in `src/`:

1. **`01_data_collection.ipynb`** — pull all sources into `data/raw/`. Set a free [FRED API key](https://fred.stlouisfed.org/docs/api/api_key.html) as the environment variable `FRED_API_KEY`, and place the Findex Ghana extract (downloaded after free registration) in `data/raw/findex/`.
2. **`02_cleaning_merge.ipynb`** — clean, align to a monthly calendar, and write `data/processed/monthly_series.csv` and `findex_ghana.csv`.
3. **`03_eda.ipynb`** — exploratory figures and the sample-size checks.
4. **`04_rq1_adoption_drivers.ipynb`** — logistic regression + SHAP driver ranking.
5. **`05_rq2_forecasting.ipynb`** — SARIMA / Prophet baselines and gradient boosting forecasts.
6. **`06_rq3_model_comparison.ipynb`** — rolling-origin backtest and Diebold–Mariano test.
7. **`07_rq4_scenarios.ipynb`** — scenario analysis and the regional inclusion map.

All figures and forecast tables are written to `outputs/`.

## Outputs

- `outputs/forecasts/` — 6–12 month forecasts of transaction value and active accounts with error bands.
- `outputs/figures/` — EDA charts, SHAP driver rankings, model-comparison plots, and the regional inclusion map.
- `outputs/models/` — serialized fitted models for reuse.

## Ethics and limitations

All data are public and aggregate or anonymised, so there is no individual-privacy risk. The main analytical caveats are survey waves spaced years apart, macroeconomic series that may be revised after first release, and a structural break from the **Electronic Transfer Levy (May 2022)**, which is encoded as an indicator variable before modelling.

## Citation

If you use this work, please cite:

> Asomia, N. (2026). *Predicting mobile money transactions and digital financial inclusion growth in Ghana using machine learning and financial access indicators* [QM640 Data Analytics Capstone]. Walsh College.

## Licence

Code released under the MIT Licence. Data remain under the terms of their respective sources listed above.
