# Predicting Mobile Money Transactions and Digital Financial Inclusion Growth in Ghana

Forecasting Ghana's mobile money growth and explaining its drivers with machine learning and publicly available financial-access indicators.

**Author:** Benjamin Asomia Cudjoe · **Course:** QM640 Data Analytics Capstone, Walsh College · **Term:** Third Term 2026

---

## Overview

This project studies digital financial inclusion in Ghana along two tracks that are kept separate because they use different units of analysis:

- **National time-series track** — a monthly Bank of Ghana payment panel of **84 months (January 2019 – December 2025)** is used to forecast mobile money transaction value and active-account growth six to twelve months ahead.
- **Individual cross-sectional track** — **2,000 pooled Global Findex respondents** (1,000 from the 2021 wave and 1,000 from the 2025 wave) are used to identify which socioeconomic and financial factors drive individual adoption.

The two tracks are analysed on their own and their results are combined only at the interpretation stage to produce policy recommendations.

## Research questions

| RQ | Question | Track | Method |
|----|----------|-------|--------|
| RQ1 | Which factors most strongly drive mobile money adoption? | Individual (Findex, n = 2,000) | Logistic regression + tree model with driver ranking |
| RQ2 | Can models forecast transaction value and account growth? | National monthly (n = 84) | Lag-feature regression, with SARIMA/Prophet and gradient boosting to follow |
| RQ3 | Which approach forecasts most accurately? | National monthly | Holdout comparison (RMSE/MAE/MAPE/R²) |
| RQ4 | What policy actions improve inclusion? | Synthesis | Driver-based scenario analysis |

## Repository structure

```
mobile-money-ghana-forecasting/
├── data/
│   ├── raw/                         # source downloads
│   │   ├── monthly_series.xlsx          # BoG monthly panel (raw columns)
│   │   ├── findex_ghana_2021.xlsx       # Findex 2021 wave
│   │   ├── findex_ghana_2025.xlsx       # Findex 2025 wave
│   │   ├── agent_density_population.xlsx # annual adult population 2019–2025
│   │   └── yearly_account_ownership.xlsx# Findex/WDI account ownership 2011–2024
│   └── processed/                   # model-ready tables (built by 02_cleaning.ipynb)
│       ├── monthly_series_clean.csv     # national monthly panel + engineered features
│       └── findex_ghana_clean.csv       # pooled, recoded respondent records
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_cleaning.ipynb            # recoding, interpolation, feature engineering
│   ├── 03_eda.ipynb
│   ├── 04_rq1_adoption_drivers.ipynb
│   ├── 05_rq2_forecasting.ipynb
│   ├── 06_rq3_model_comparison.ipynb
│   └── 07_rq4_scenarios.ipynb
├── outputs/
│   └── figures/                     # EDA and result charts (Figures 1–8)
├── docs/
│   └── data_dictionary.md           # full variable definitions (also .csv)
├── requirements.txt
├── .gitignore
└── README.md
```

## Data inputs and sources

| Input file | Content | Source | Access |
|------------|---------|--------|--------|
| `monthly_series.xlsx` | Monthly transaction value & volume, accounts, agents, macro indicators, mobile and internet penetration | Bank of Ghana Database Portal, National Communications Authority | Public (app.datawarehousepro.com/go/bog/, nca.org.gh/mobile-voice/ and nca.org.gh/mobile-data) |
| `findex_ghana_2021.xlsx`, `findex_ghana_2025.xlsx` | Individual adoption and correlates | World Bank Global Findex | Public, free registration (microdata.worldbank.org) |
| `agent_density_population.xlsx` | Annual total and adult population, 2019–2025 | World Bank WDI | Public / API ([data.worldbank.org](https://data.worldbank.org/country/ghana)) |
| `yearly_account_ownership.xlsx` | Account ownership (% adults 15+), survey years 2011–2024 | World Bank Findex / WDI (FX.OWN.TOTL.ZS) | Public (https://data.worldbank.org/country/ghana) / API |

`agent_density_population.xlsx` supports interpolation of the `agent_density` variable; `yearly_account_ownership.xlsx` supports interpolation of the monthly `account_ownership` variable.

## What `02_cleaning.ipynb` produces

- Computes `agent_density` = active agents ÷ (adult population ÷ 100,000), after interpolating annual population to monthly.
- Computes monthly `account_ownership` by interpolating the five survey-year points (2011–2024) across the 2019–2025 window.
- Engineers 1–12 month lags of value and active accounts, 3- and 6-month rolling means, year-on-year growth, calendar month, a linear time index, and confirms the E-Levy indicator (44 months from May 2022).
- Pools the two Findex waves (2,000 rows) and **recodes** the raw survey codes to 0/1, mapping don't-know/refused (codes 3, 4, and a stray 5 in education) to missing, then imputes the few remaining gaps.

## Environment setup

Python 3.11 recommended.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## How to reproduce

1. Place the five raw files in `data/raw/`.
2. Run `notebooks/02_cleaning.ipynb` to build `data/processed/monthly_series_clean.csv` and `findex_ghana_clean.csv`.
3. Run `03_eda.ipynb` for the figures in `outputs/figures/`.
4. Run `04`–`07` for the RQ1 adoption model, the RQ2/RQ3 forecasts and comparison, and the RQ4 scenarios.

## Ethics and limitations

All data are public and either aggregate or anonymised, so there is no individual-privacy risk. The main caveats are the short monthly series (84 points), the interpolation of annual indicators to monthly frequency, only two Findex waves, and the May-2022 Electronic Transfer Levy, which is encoded as an indicator variable before modelling.

## Licence

Code released under the MIT Licence. Data remain under the terms of their respective sources.
