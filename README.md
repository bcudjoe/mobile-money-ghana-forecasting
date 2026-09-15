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
| RQ1 | Which factors most strongly drive mobile money adoption? | Individual (Findex, n = 2,000) | Logistic + RandomForest/XGBoost with SHAP driver ranking, near-proxy variables removed |
| RQ2 | Can models forecast transaction value and account growth? | National monthly (n = 84) | SARIMA, Prophet, and gradient boosting (XGBoost, LightGBM) on lag features, tuned |
| RQ3 | Which approach forecasts most accurately? | National monthly | Rolling-origin backtesting (RMSE/MAE/MAPE/R²) with a Diebold–Mariano test |
| RQ4 | What policy actions improve inclusion? | Synthesis | Driver-based scenario projection and an inclusion view |

## Results summary

The project is complete. Key findings (transaction value, GH¢ millions):

- **Forecasting (RQ2/RQ3).** On rolling-origin one-step backtesting across 24 origins, **SARIMA(0,1,0)(0,1,1,12)** is the most accurate model (MAPE ≈ 6.5%, R² ≈ 0.89). A Diebold–Mariano test confirms SARIMA beats the seasonal-naive benchmark (MAPE ≈ 35%) and LightGBM, and is statistically tied with Prophet and XGBoost. On the harder 12-month-ahead holdout, **Prophet** leads (MAPE ≈ 7.1%), with SARIMA close (≈ 8.2%). Selection rule: SARIMA for short-horizon operational forecasts, Prophet for the 12-month scenario horizon.
- **Drivers (RQ1).** After removing the two near-proxy variables (`has_account`, `made_digital_payment`), logistic accuracy settles at ≈ 77% (ROC-AUC ≈ 0.85) and the RandomForest reaches ROC-AUC ≈ 0.84. SHAP ranks **mobile phone ownership, formal saving, survey wave, education, and income** as the strongest drivers; every gradient is statistically significant.
- **Policy (RQ4).** Scenario projections show faster agent expansion (≈ +3%), wider account ownership (≈ +5%), and a lighter transfer levy (≈ +6%) each lift cumulative projected value over 12 months. The widest inclusion gaps are along income (≈ 32 pp) and education (≈ 42 pp).

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
│   └── figures/                     # EDA and result charts (Figures 1–12, SHAP, backtest, scenarios)
├── src/                             # reusable config, features, models, evaluate helpers
├── docs/
│   └── data_dictionary.md           # full variable definitions (also .csv)
├── requirements.txt
├── environment.yml                  # conda env "momo-ghana" (Python 3.11)
├── .gitignore
└── README.md
```

## Data inputs and sources

| Input file | Content | Source | Access |
|------------|---------|--------|--------|
| `monthly_series.xlsx` | Monthly transaction value & volume, accounts, agents, macro indicators, mobile and internet penetration | Bank of Ghana Database Portal, National Communications Authority | Public (app.datawarehousepro.com/go/bog/, nca.org.gh/mobile-voice/ and nca.org.gh/mobile-data) |
| `findex_ghana_2021.xlsx`, `findex_ghana_2025.xlsx` | Individual adoption and correlates | World Bank Global Findex | Public, free registration ([microdata.worldbank.org](https://microdata.worldbank.org/catalog/4646), [microdata.worldbank.org](https://microdata.worldbank.org/catalog/7860)) |
| `agent_density_population.xlsx` | Annual total and adult population, 2019–2025 | World Bank WDI (SP.POP.TOTL & SP.POP.1564.TO) | Public / API ([data.worldbank.org](https://data.worldbank.org/country/ghana)) |
| `yearly_account_ownership.xlsx` | Account ownership (% adults 15+), survey years 2011–2024 | World Bank Findex / WDI (FX.OWN.TOTL.ZS) | Public ([data.worldbank.org](https://data.worldbank.org/country/ghana)) / API |

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
# or, with conda:
conda env create -f environment.yml && conda activate momo-ghana
```

## Run on Google Colab

Each of notebooks 04–07 begins with a self-contained setup cell that installs the
dependencies, clones this repository if the processed data are not already present,
and fixes the random seed (`RANDOM_STATE = 42`). Open a notebook in Colab and run all
cells; no manual steps are needed. Notebooks 06 and 07 read the tuned settings written
by notebook 05 (`results/rq2_results.json`), so run 05 before 06 and 07.

## How to reproduce

1. Place the five raw files in `data/raw/` (already included in this repository).
2. Run `notebooks/02_cleaning.ipynb` to build `data/processed/monthly_series_clean.csv` and `findex_ghana_clean.csv`.
3. Run `03_eda.ipynb` for the EDA figures in `outputs/figures/`.
4. Run `04` (RQ1 driver model with SHAP), `05` (RQ2 forecasters), `06` (RQ3 rolling-origin backtest and Diebold–Mariano test), and `07` (RQ4 scenarios), in that order.

## Ethics and limitations

All data are public and either aggregate or anonymised, so there is no individual-privacy risk. The main caveats are the short monthly series (84 points), the interpolation of annual indicators to monthly frequency, only two Findex waves, and the May-2022 Electronic Transfer Levy, which is encoded as an indicator variable before modelling.

## Licence

Code released under the MIT Licence. Data remain under the terms of their respective sources.
