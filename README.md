# HIV-TB Co-infection Spatial Analysis — Ghana 260 Districts

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Spatial distribution, determinants, and machine-learning–based risk prediction of HIV-TB co-infection across Ghana's 260 districts.**

Valentine Golden Ghanem · Biomedical Scientist · Ghana COCOBOD Cocoa Clinic · April 2026

## Overview

This repository provides a complete, reproducible pipeline for nationwide district-level HIV-TB co-infection analysis in Ghana, combining:

- **Spatial statistics**: Global Moran's I, univariate & bivariate LISA, Getis-Ord Gi*, OLS with Lagrange-Multiplier diagnostics, Spatial Error Model, Geographically Weighted Regression (GWR).
- **Machine learning**: Random Forest, XGBoost, LightGBM, Stacked Ensemble. SMOTE oversampling. 10-fold stratified CV + leave-one-region-out spatial CV. SHAP interpretability.
- **Interactive outputs**: A0 conference poster (.html), interactive HTML dashboard + Dash app.

## Key findings

| Metric | Value |
|---|---|
| Districts analysed | 260 |
| Population covered | 28.14 million |
| Global Moran's I (TB-HIV co-infection) | 0.468, p < 0.001 |
| Bivariate Moran's I (HIV × TB) | 0.521, p < 0.001 |
| LISA high-high clusters | 48 districts |
| Bivariate high-high clusters | 44 districts |
| Best ML CV AUC (LightGBM) | 0.998 ± 0.003 |
| GWR R² | 0.916 |
| Top SHAP predictors | HIV prevalence, VCT uptake, poverty, TB incidence, illiteracy |

## Repository structure

```
hiv_tb_ghana/
├── README.md, LICENSE, requirements.txt, .gitignore
├── analysis/
│ ├── build_master_dataset.py # Data integration pipeline
│ ├── spatial_analysis.py # Moran's I, LISA, GWR, SEM
│ ├── ml_pipeline.py # RF, XGBoost, LGBM, Stacked, SHAP
│ └── generate_figures.py # 300 DPI publication figures
├── dashboard/
│ ├── app.py # Python Dash application
│ ├── HIV_TB_Ghana_Dashboard.html # Self-contained HTML dashboard
│ ├── run_dashboard.command # macOS launcher
│ ├── run_dashboard.bat # Windows launcher
│ └── run_dashboard.sh # Linux launcher
├── poster/
│ ├── create_poster.py
│ └── HIV_TB_Ghana_260_Districts_Poster.html # A0 conference poster
└── outputs/
 ├── data/
 │ ├── Ghana_HIV_TB_Master_Dataset.csv # Master dataset (260 x 52)
 │ ├── ghana_260_final_results.geojson # With spatial + ML outputs
 │ └── ghana_260_final_results.csv
 ├── figures/ # 9 PNG figures at 300 DPI
 ├── tables/ # All CSV result tables
 └── models/ # Pickled models + SHAP values
```

## Quick start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the full pipeline (reproduces everything)
cd analysis/
python3 build_master_dataset.py
python3 spatial_analysis.py
python3 ml_pipeline.py
python3 generate_figures.py

# 3. View the dashboard
cd ../dashboard/
python3 app.py
# Open http://127.0.0.1:8050

# OR open the self-contained HTML:
open HIV_TB_Ghana_Dashboard.html
```

## Data sources

- **Ghana DHS 2003** — Regional HIV prevalence, behaviour, knowledge, VCT, attitudes (https://dhsprogram.com)
- **WHO Global Health Observatory** — National HIV, TB, workforce, financing, STI (https://www.who.int/data/gho)
- **Ghana Statistical Service 2021 Census** — District socioeconomic variables (https://statsghana.gov.gh)
- **Ghana 260-District Shapefile** — Derived from Local Governance (Amendment) Act 2018

## Citation

If you use this code or dataset, please cite:

> Ghanem VG. (2026). Spatial Distribution, Determinants, and Machine Learning–Based Risk Prediction of HIV-TB Co-infection Across Ghana's 260 Districts: An Ensemble Geospatial Intelligence Study. *[Target Journal]*.

## Licence

MIT Licence. See [LICENSE](LICENSE) for details.

## Contact

Valentine Golden Ghanem · valentineghanem@gmail.com · ORCID: [0009-0002-8332-0220](https://orcid.org/0009-0002-8332-0220)
