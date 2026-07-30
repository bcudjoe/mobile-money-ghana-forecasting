# Data Dictionary

Project: *Predicting Mobile Money Transactions and Digital Financial Inclusion Growth in Ghana*

Types follow the convention **continuous**, **count**, **binary**, **categorical**, **date**. Role is one of **target**, **predictor**, **derived feature**, **key**, or **input**.

---

## 1. National monthly series — `data/processed/monthly_series_clean.csv`

One row per calendar month, **2019-01 → 2025-12 (84 months)**. Used for RQ2 (forecasting) and RQ3 (model comparison).

| Variable | Description | Type | Unit / values | Source | Frequency | Role |
|----------|-------------|------|---------------|--------|-----------|------|
| `date` | Month of observation (month start) | date | YYYY-MM-01 | Constructed | Monthly | key |
| `mm_value` | Total value of mobile money transactions | continuous | GH¢ millions | Bank of Ghana | Monthly | target |
| `mm_volume` | Number of mobile money transactions | count | transactions | Bank of Ghana | Monthly | predictor |
| `mm_active_accts` | Active mobile money accounts | count | accounts | Bank of Ghana | Monthly | target |
| `mm_registered_accts` | Registered mobile money accounts | count | accounts | Bank of Ghana | Monthly | predictor |
| `mm_agents_active` | Active mobile money agents | count | agents | Bank of Ghana | Monthly | predictor |
| `agent_density` | Active agents per 100,000 adults | continuous | ratio | **Computed** (agents ÷ adult population ÷ 100,000; population interpolated to monthly) | Monthly | predictor |
| `mobile_pen` | Mobile subscription penetration | continuous | % of population | NCA | Monthly | predictor |
| `internet_pen` | Internet / data subscription penetration | continuous | % of population | NCA | Monthly | predictor |
| `account_ownership` | Adults with a financial account | continuous | % of adults | **Computed** (interpolated from survey-year points 2011–2024) | Monthly (interpolated) | predictor |
| `inflation` | Year-on-year consumer price inflation | continuous | % | Bank of Ghana | Monthly | predictor |
| `policy_rate` | Bank of Ghana monetary policy rate | continuous | % | Bank of Ghana | Monthly | predictor |
| `exch_rate` | GH¢ per US dollar (period average) | continuous | ratio | Bank of Ghana | Monthly | predictor |
| `gdp_proxy` | Composite index of economic activity (real) | continuous | index | Bank of Ghana | Monthly | predictor |
| `elevy` | Electronic Transfer Levy in effect | binary | 0 = before May 2022, 1 = from May 2022 (44 months) | Constructed | Monthly | predictor (break) |

### Engineered features (built in `02_cleaning.ipynb`)

| Variable | Description | Type | Role |
|----------|-------------|------|------|
| `mm_value_lag1` … `mm_value_lag12` | Transaction value lagged 1–12 months | continuous | derived feature |
| `mm_active_accts_lag1` … `mm_active_accts_lag12` | Active accounts lagged 1–12 months | count | derived feature |
| `mm_value_roll3`, `mm_value_roll6` | 3- and 6-month rolling mean of value | continuous | derived feature |
| `mm_value_yoy` | Year-on-year % growth of value | continuous | derived feature |
| `month` | Calendar month (seasonality) | categorical | derived feature |
| `t_index` | Linear time index (1…84) | count | derived feature |

> The first 12 months carry missing lag values by construction and are dropped for models that use 12-month lags.

---

## 2. Individual cross-sectional data — `data/processed/findex_ghana_clean.csv`

One row per respondent; **2,000 records** pooled across the 2021 and 2025 Global Findex waves (1,000 each). Used for RQ1. Raw survey codes are **recoded** as shown; don't-know/refused codes are set to missing and then a small number of gaps are imputed (age by median, categorical by mode).

| Variable | Description | Type | Raw codes → recoded | Role |
|----------|-------------|------|---------------------|------|
| `resp_id` | Anonymised respondent identifier | key | — | key |
| `wave` | Survey wave | categorical | {2021, 2025} | key |
| `adopts_mm` | Uses a mobile money account | binary | already 0/1 | target |
| `has_account` | Owns any financial or mobile account | binary | already 0/1 | predictor |
| `made_digital_payment` | Made/received a digital payment in past year | binary | already 0/1 | predictor |
| `income_quintile` | Within-economy income quintile | categorical | 1 (poorest) – 5 (richest) | predictor |
| `education` | Highest education level | categorical | 1 = primary or less, 2 = secondary, 3 = tertiary; **code 5 → missing** | predictor |
| `age` | Respondent age | continuous | years; 4 missing → median imputed | predictor |
| `female` | Respondent is female | binary | 1→1, 2→0 | predictor |
| `urban` | Lives in an urban area | binary | 1→1, 2→0 | predictor |
| `owns_mobile` | Owns a mobile phone | binary | 1→1, 2→0; **3,4 (DK/refused) → missing** | predictor |
| `has_internet` | Has internet access | binary | 1→1, 0→0; **2 (DK) → missing** | predictor |
| `employed` | In the labour force / employed | binary | 1→1, 2→0 | predictor |
| `borrowed_formal` | Borrowed from a formal institution in past year | binary | 1→1, 2→0; **3,4 → missing** | predictor |
| `saved_formal` | Saved at a formal institution in past year | binary | 1→1, 2→0; **3,4 → missing** | predictor |

---

## 3. Supporting inputs (interpolation sources)

### `data/raw/agent_density_population.xlsx`
| Variable | Description | Type | Unit |
|----------|-------------|------|------|
| `year` | Calendar year, 2019–2025 | date | year |
| `total_population` | Total population of Ghana | count | persons |
| `adult_population` | Population aged 15+ | count | persons |

Used to interpolate adult population to monthly frequency and compute `agent_density`.

### `data/raw/yearly_account_ownership.xlsx`
| Variable | Description | Type | Unit |
|----------|-------------|------|------|
| `YEAR` | Survey year: 2011, 2014, 2017, 2021, 2024 | date | year |
| `account_ownership` | Adults (15+) with an account | continuous | % |

Values: 2011 = 29.4, 2014 = 40.5, 2017 = 57.7, 2021 = 68.2, 2024 = 81.2. Interpolated across the 2019–2025 window to build the monthly `account_ownership` column (values held flat after the 2024 anchor).

---

## Notes

- `mm_value` is stored in GH¢ millions; observed range across the panel is roughly 20,900 – 518,400.
- Annual inputs (population, account ownership) are interpolated to monthly; treat `account_ownership` and `agent_density` as smooth structural trends rather than high-frequency signals.
- Missing values are stored as blanks (NaN), never as 0.
