# Data Dictionary

Project: *Predicting Mobile Money Transactions and Digital Financial Inclusion Growth in Ghana*

Variables are grouped by analytical track. Types follow the convention: **continuous**, **count**, **binary**, **categorical**, **date**. Role is one of **target**, **predictor**, **derived feature**, or **key**.

---

## 1. National monthly series — `data/processed/monthly_series.csv`

One row per calendar month (~2013–present). Used for RQ2 (forecasting) and RQ3 (model comparison).

| Variable | Description | Type | Unit / values | Range (typical) | Source | Frequency | Role |
|----------|-------------|------|---------------|-----------------|--------|-----------|------|
| `date` | Month of observation (month-end) | date | YYYY-MM-01 | 2013-01 → present | Constructed | Monthly | key |
| `mm_value` | Total value of mobile money transactions | continuous | GH¢ (millions) | 0 – 550,000+ | Bank of Ghana | Monthly | target |
| `mm_volume` | Number of mobile money transactions | count | transactions (millions) | 0 – 800+ | Bank of Ghana | Monthly | target / predictor |
| `mm_active_accts` | Active mobile money accounts | count | accounts (millions) | 0 – 25+ | Bank of Ghana | Monthly | target |
| `mm_registered_accts` | Registered mobile money accounts | count | accounts (millions) | 0 – 70+ | Bank of Ghana | Monthly | predictor |
| `mm_agents_active` | Active mobile money agents | count | agents | 0 – 900,000+ | Bank of Ghana | Monthly | predictor |
| `agent_density` | Active agents per 100,000 adults | continuous | ratio | 0 – 5,000+ | Derived (agents ÷ adult population) | Monthly | predictor |
| `mobile_pen` | Mobile subscription penetration | continuous | % of population | 100 – 140 | NCA | Monthly | predictor |
| `internet_pen` | Internet / data subscription penetration | continuous | % of population | 30 – 100 | NCA | Monthly | predictor |
| `account_ownership` | Adults with a financial account | continuous | % of adults | 40 – 95 | World Bank Findex / FAS | Annual (interpolated) | predictor |
| `inflation` | Year-on-year consumer price inflation | continuous | % | 5 – 55 | Bank of Ghana | Monthly | predictor |
| `policy_rate` | Bank of Ghana monetary policy rate | continuous | % | 13 – 30 | Bank of Ghana | Monthly | predictor |
| `exch_rate` | GH¢ per US dollar (period average) | continuous | ratio | 3 – 16 | Bank of Ghana | Monthly | predictor |
| `gdp_proxy` | Monthly GDP proxy / composite index of economic activity | continuous | index | varies | Bank of Ghana | Monthly | predictor |
| `elevy` | Electronic Transfer Levy in effect | binary | 0 = before May 2022, 1 = from May 2022 | {0, 1} | Constructed (policy event) | Monthly | predictor (structural break) |

### Derived features (created in `src/features.py`)

| Variable | Description | Type | Unit | Role |
|----------|-------------|------|------|------|
| `mm_value_lag1` … `mm_value_lag12` | Lagged transaction value (1–12 months) | continuous | GH¢ (millions) | derived feature |
| `mm_value_roll3`, `mm_value_roll6` | 3- and 6-month rolling mean of value | continuous | GH¢ (millions) | derived feature |
| `mm_value_yoy` | Year-on-year growth of transaction value | continuous | % | derived feature |
| `mm_active_accts_lag1` … `_lag12` | Lagged active accounts | count | accounts (millions) | derived feature |
| `month` | Calendar month (seasonality) | categorical | 1–12 | derived feature |
| `t_index` | Linear time index | count | months since start | derived feature |

---

## 2. Individual cross-sectional data — `data/processed/findex_ghana.csv`

One row per survey respondent (Global Findex Ghana, 2021 and 2025 waves; ~1,000 respondents per wave). Used for RQ1 (adoption drivers). Variable names below are harmonised labels; map to the official Findex codebook during cleaning.

| Variable | Description | Type | Unit / values | Source | Role |
|----------|-------------|------|---------------|--------|------|
| `resp_id` | Anonymised respondent identifier | key | integer | Findex | key |
| `wave` | Survey wave | categorical | {2021, 2025} | Findex | key |
| `adopts_mm` | Respondent uses a mobile money account | binary | 1 = yes, 0 = no | Findex | target |
| `has_account` | Owns any financial institution or mobile account | binary | {0, 1} | Findex | predictor |
| `made_digital_payment` | Made or received a digital payment in past year | binary | {0, 1} | Findex | predictor |
| `income_quintile` | Within-economy income quintile | categorical | 1 (poorest) – 5 (richest) | Findex | predictor |
| `education` | Highest education level | categorical | {primary or less, secondary, tertiary} | Findex | predictor |
| `age` | Respondent age | continuous | years | Findex | predictor |
| `female` | Respondent is female | binary | 1 = female, 0 = male | Findex | predictor |
| `urban` | Lives in an urban area | binary | 1 = urban, 0 = rural | Findex | predictor |
| `owns_mobile` | Owns a mobile phone | binary | {0, 1} | Findex | predictor |
| `has_internet` | Has internet access | binary | {0, 1} | Findex | predictor |
| `employed` | In the labour force / employed | binary | {0, 1} | Findex | predictor |
| `borrowed_formal` | Borrowed from a formal institution in past year | binary | {0, 1} | Findex | predictor |
| `saved_formal` | Saved at a formal institution in past year | binary | {0, 1} | Findex | predictor |
