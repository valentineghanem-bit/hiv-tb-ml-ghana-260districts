# Spatial Distribution, Determinants, and Machine Learning–Based Risk Prediction of HIV-TB Co-infection Across Ghana's 260 Districts

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/) [![ORCID](https://img.shields.io/badge/ORCID-0009--0002--8332--0220-green.svg)](https://orcid.org/0009-0002-8332-0220)

**Author:** Valentine Golden Ghanem | Ghana COCOBOD Cocoa Clinic, Accra, Ghana
**ORCID:** [0009-0002-8332-0220](https://orcid.org/0009-0002-8332-0220)
**Reporting standard:** STROBE
**Date:** April 2026

> Ghanem VG. *Spatial distribution, determinants, and machine learning–based risk prediction of HIV-TB co-infection across Ghana's 260 districts: an ensemble geospatial intelligence study.* 2026.

---

## Overview

A nationwide district-level analysis of HIV-TB co-infection in Ghana combining spatial statistics, geographically weighted regression, and ensemble machine learning across all 260 health districts. The study integrates Ghana DHS, WHO Global Health Observatory, and Census 2021 data to delineate spatial clusters, identify socioeconomic determinants, and produce district-level risk scores with full SHAP interpretability.

---

## Key Findings

| Metric | Value |
|--------|-------|
| Districts analysed | 260 |
| Population covered | 28.14 million |
| Global Moran's I (TB-HIV co-infection) | 0.468 (p < 0.001) |
| Bivariate Moran's I (HIV × TB) | 0.521 (p < 0.001) |
| LISA High-High clusters | 48 districts |
| Bivariate High-High clusters | 44 districts |
| Best ML CV AUC (LightGBM) | 0.998 ± 0.003 |
| GWR R² | 0.916 |
| Top SHAP predictors | HIV prevalence, VCT uptake, poverty, TB incidence, illiteracy |

---

## Repository Structure

```
hiv-tb-ml-ghana-260districts/
├── analysis/
│   ├── build_master_dataset.py     # Data integration pipeline
│   ├── spatial_analysis.py         # Moran's I, LISA, GWR, SEM
│   ├── ml_pipeline.py              # RF, XGBoost, LightGBM, Stacked, SHAP
│   └── generate_figures.py         # 300 DPI publication figures
├── app.py                          # Plotly Dash interactive web application
├── analysis.R                      # R: spatial regression + GWR diagnostics
├── dashboard/
│   ├── HIV_TB_Ghana_Dashboard.html # Self-contained HTML dashboard
│   ├── run_dashboard.command       # macOS launcher
│   ├── run_dashboard.bat           # Windows launcher
│   └── run_dashboard.sh            # Linux launcher
├── poster/
│   ├── create_poster.py
│   └── HIV_TB_Ghana_260_Districts_Poster.html
├── outputs/
│   ├── data/
│   │   ├── Ghana_HIV_TB_Master_Dataset.csv   # Master dataset (260 × 52)
│   │   ├── ghana_260_final_results.geojson
│   │   └── ghana_260_final_results.csv
│   ├── figures/                    # 9 PNG figures at 300 DPI
│   ├── tables/                     # CSV result tables
│   └── models/                     # Pickled models + SHAP values
├── requirements.txt
├── renv.lock
├── CITATION.cff
└── README.md
```

---

## Quick Start

### 1. Clone

```bash
git clone https://github.com/valentineghanem-bit/hiv-tb-ml-ghana-260districts.git
cd hiv-tb-ml-ghana-260districts
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the pipeline

```bash
cd analysis/
python3 build_master_dataset.py
python3 spatial_analysis.py
python3 ml_pipeline.py
python3 generate_figures.py
```

### 4. Run tests

```bash
pytest tests/ -v
```

### 5. Open the interactive dashboard

```bash
python app.py
# Visit http://127.0.0.1:8050
```

Or open `dashboard/HIV_TB_Ghana_Dashboard.html` directly in any modern browser. No server required.

---

## Data Sources

| Source | Variables | Year | Access |
|--------|-----------|------|--------|
| Ghana DHS 2003 | Regional HIV prevalence, behaviour, VCT, attitudes | 2003 | [dhsprogram.com](https://dhsprogram.com) |
| WHO Global Health Observatory | National HIV, TB, workforce, financing | 2001–2022 | [who.int/data/gho](https://www.who.int/data/gho) |
| Ghana Statistical Service 2021 Census | District socioeconomic variables | 2021 | [statsghana.gov.gh](https://statsghana.gov.gh) |
| Ghana 260-District Shapefile | District boundary polygons | 2021 | Local Governance (Amendment) Act 2018 |

> DHS data accessed under signed Data Use Agreement (ICF International).

---

## Methods Summary

| Method | Tool | Purpose |
|--------|------|---------|
| Global Moran's I | esda / libpysal | HIV-TB spatial autocorrelation |
| Univariate & Bivariate LISA | esda | Local cluster delineation |
| Getis-Ord Gi* | esda | Hotspot / coldspot detection |
| OLS + LM diagnostics | spreg | Spatial model selection |
| Spatial Error Model | spreg | Spatial dependency correction |
| Geographically Weighted Regression | mgwr | Spatially varying coefficient estimation |
| Random Forest | scikit-learn | Ensemble risk prediction |
| XGBoost | xgboost | Gradient boosted risk prediction |
| LightGBM | lightgbm | Best-performing classifier (AUC 0.998) |
| Stacked Ensemble | scikit-learn | Meta-learner combining RF + XGB + LGBM |
| SMOTE | imbalanced-learn | Class imbalance correction |
| SHAP | shap | TreeExplainer interpretability |
| GWR (R) | GWmodel (R) | Spatial non-stationarity diagnostics |

---

## Reproducibility

- Random seed: 42 throughout
- Reporting: STROBE
- All random seeds set explicitly (`random_state=42`)
- 10-fold stratified CV + leave-one-region-out spatial CV
- Python 3.12 | R 4.3+

---

## Ethical Statement

This study used exclusively de-identified, publicly available secondary data from the Ghana DHS, WHO, and Ghana Statistical Service. No primary data collection from human participants was conducted. DHS data accessed under signed Data Use Agreement (ICF International).

---

## Citation

```bibtex
@misc{ghanem2026hivtb,
  author = {Ghanem, Valentine Golden},
  title  = {Spatial Distribution, Determinants, and Machine Learning--Based Risk Prediction of HIV-TB Co-infection Across Ghana's 260 Districts},
  year   = {2026},
  url    = {https://github.com/valentineghanem-bit/hiv-tb-ml-ghana-260districts}
}
```

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

## Contact

Valentine Golden Ghanem
Ghana COCOBOD Cocoa Clinic, Accra, Ghana
valentineghanem@gmail.com
ORCID: [0009-0002-8332-0220](https://orcid.org/0009-0002-8332-0220)
