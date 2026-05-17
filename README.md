# Spatial Distribution, Determinants, and Machine Learning–Based Risk Prediction of HIV-TB Co-infection Across Ghana's 260 Districts

[![CI](https://github.com/valentineghanem-bit/hiv-tb-ml-ghana-260districts/actions/workflows/ci.yml/badge.svg)](https://github.com/valentineghanem-bit/hiv-tb-ml-ghana-260districts/actions) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/) [![R 4.3+](https://img.shields.io/badge/R-4.3+-blue.svg)](https://www.r-project.org/) [![ORCID](https://img.shields.io/badge/ORCID-0009--0002--8332--0220-green.svg)](https://orcid.org/0009-0002-8332-0220)

**Author:** Valentine Golden Ghanem | Ghana COCOBOD Cocoa Clinic, Accra, Ghana
**ORCID:** [0009-0002-8332-0220](https://orcid.org/0009-0002-8332-0220)
**Affiliation:** Ghana COCOBOD Cocoa Clinic, Accra, Ghana
**Reporting standard:** STROBE
**Date:** April 2026
**Status:** Manuscript in preparation

> Valentine Golden Ghanem (2026). *Spatial Distribution, Determinants, and Machine Learning–Based Risk Prediction of HIV-TB Co-infection Across Ghana's 260 Districts.* GitHub repository. https://github.com/valentineghanem-bit/hiv-tb-ml-ghana-260districts

---

## 1. Abstract

A nationwide district-level analysis of HIV-TB co-infection in Ghana combining spatial statistics, geographically weighted regression, and ensemble machine learning across all 260 health districts. The study integrates Ghana DHS, WHO Global Health Observatory, and Census 2021 data to delineate spatial clusters, identify socioeconomic determinants, and produce district-level risk scores with full SHAP interpretability.

---

## 2. Research Question & Aims

- **Primary:** Map district-level HIV-TB co-infection burden and identify spatial co-clusters across Ghana's 260 districts.
- **Secondary:** (a) Identify socioeconomic and behavioural determinants of co-infection burden using GWR; (b) build an ensemble ML risk-prediction pipeline (RF + XGB + LightGBM + Stacked) with LORO spatial CV; (c) produce a SHAP-interpreted district risk map for programme planning.

---

## 3. Methods Summary

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
| GWR diagnostics (R) | GWmodel (R) | Spatial non-stationarity validation |

---

## 4. Data Sources

| Source | Variables | Year | Access |
|--------|-----------|------|--------|
| Ghana DHS 2003 | Regional HIV prevalence, behaviour, VCT, attitudes | 2003 | [dhsprogram.com](https://dhsprogram.com) |
| WHO Global Health Observatory | National HIV, TB, workforce, financing | 2001–2022 | [who.int/data/gho](https://www.who.int/data/gho) |
| Ghana Statistical Service 2021 Census | District socioeconomic variables | 2021 | [statsghana.gov.gh](https://statsghana.gov.gh) |
| Ghana 260-District Shapefile | District boundary polygons | 2021 | Local Governance (Amendment) Act 2018 |

> DHS data accessed under signed Data Use Agreement (ICF International).

---

## 5. Key Findings

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

## 6. Repository Structure

```
hiv-tb-ml-ghana-260districts/
├── analysis/
│   ├── build_master_dataset.py     # Data integration pipeline
│   ├── spatial_analysis.py         # Moran's I, LISA, GWR, SEM
│   ├── ml_pipeline.py              # RF, XGBoost, LightGBM, Stacked, SHAP
│   └── generate_figures.py         # 300 DPI publication figures
├── app.py                          # Plotly Dash interactive application
├── analysis.R                      # R: spatial regression + GWR diagnostics
├── dashboard/
│   ├── HIV_TB_Ghana_Dashboard.html
│   ├── run_dashboard.command       # macOS launcher
│   ├── run_dashboard.bat           # Windows launcher
│   └── run_dashboard.sh            # Linux launcher
├── poster/
│   ├── create_poster.py
│   └── HIV_TB_Ghana_260_Districts_Poster.html
├── outputs/
│   ├── data/
│   │   ├── Ghana_HIV_TB_Master_Dataset.csv   # Master dataset (260 × 52)
│   │   └── ghana_260_final_results.geojson
│   ├── figures/                    # 9 PNG figures at 300 DPI
│   ├── tables/                     # CSV result tables
│   └── models/                     # Pickled models + SHAP values
├── requirements.txt
├── renv.lock
├── CITATION.cff
└── README.md
```

---

## 7. Reproducibility

### 7.1 Requirements
- Python 3.12 (see `requirements.txt` for pinned versions)
- R 4.3+ (for R scripts; see `renv.lock` or `analysis.R` header for pinned packages)
- Random seed: 42 throughout (set via `random_state=42` and `np.random.seed(42)`)
- Estimated runtime: ~10–15 minutes on a standard laptop (longer with LightGBM)
- Tested on: Ubuntu 22.04 / macOS 14 / Windows 11 (CI: GitHub Actions)

### 7.2 Clone & install
```bash
git clone https://github.com/valentineghanem-bit/hiv-tb-ml-ghana-260districts.git
cd hiv-tb-ml-ghana-260districts
pip install -r requirements.txt
# For R scripts (optional):
Rscript -e "if (!requireNamespace('renv', quietly=TRUE)) install.packages('renv'); renv::restore()"
```

### 7.3 Run the analytical pipeline
```bash
cd analysis/
python build_master_dataset.py
python spatial_analysis.py
python ml_pipeline.py
python generate_figures.py
```

### 7.4 Run the test suite
```bash
pytest tests/ -v
```

### 7.5 Launch the interactive Dash application
```bash
python app.py
# Navigate to http://127.0.0.1:8050 in your browser
```

### 7.6 Open the static HTML dashboard
Open `dashboard/HIV_TB_Ghana_Dashboard.html` in any modern browser, or launch via the platform-specific scripts (`run_dashboard.command` / `.bat` / `.sh`).

---

## 8. Outputs

- **Interactive Dash app:** `app.py` — `python app.py` → http://127.0.0.1:8050
- **Static HTML dashboard:** `dashboard/HIV_TB_Ghana_Dashboard.html`
- **A0 poster:** `poster/HIV_TB_Ghana_260_Districts_Poster.html`
- **Master dataset:** `outputs/data/Ghana_HIV_TB_Master_Dataset.csv` (260 × 52)
- **GeoJSON:** `outputs/data/ghana_260_final_results.geojson`
- **Figures:** `outputs/figures/*.png` — 9 figures (300 DPI)
- **Pickled models + SHAP values:** `outputs/models/`

---

## 9. Reporting Standard

This study follows the **STROBE** (Strengthening the Reporting of Observational Studies in Epidemiology) reporting guideline for observational ecological studies.

---

## 10. Ethical Statement

This study used exclusively de-identified, publicly available secondary data from the Ghana DHS, WHO, and Ghana Statistical Service. No primary data collection from human participants was conducted. DHS data accessed under signed Data Use Agreement (ICF International).

---

## 11. Citation

**APA:**
Ghanem, V. G. (2026). *Spatial Distribution, Determinants, and Machine Learning–Based Risk Prediction of HIV-TB Co-infection Across Ghana's 260 Districts*. GitHub. https://github.com/valentineghanem-bit/hiv-tb-ml-ghana-260districts

**BibTeX:**
```bibtex
@misc{ghanem2026hivtb,
  author = {Ghanem, Valentine Golden},
  title  = {Spatial Distribution, Determinants, and Machine Learning–Based Risk Prediction of HIV-TB Co-infection Across Ghana's 260 Districts},
  year   = {2026},
  url    = {https://github.com/valentineghanem-bit/hiv-tb-ml-ghana-260districts}
}
```

A machine-readable citation is provided in `CITATION.cff`.

---

## 12. License

Code is released under the **MIT License** — see [LICENSE](LICENSE) for details. Outputs and figures: CC BY 4.0.

---

## 13. Author & Contact

- **Valentine Golden Ghanem**
  Ghana COCOBOD Cocoa Clinic, Accra, Ghana
  Email: [valentineghanem@gmail.com](mailto:valentineghanem@gmail.com)
  ORCID: [0009-0002-8332-0220](https://orcid.org/0009-0002-8332-0220)

---

## 14. Acknowledgements

- **Ghana Demographic and Health Survey programme** (ICF International) for survey data access under signed Data Use Agreement.
- **Ghana Statistical Service** for the 2021 Population and Housing Census and administrative boundary data.
- **WHO Global Health Observatory** for national-level indicators.
- **AIPOCH** (Anti-hallucination Pipeline for Open Computational Health) v6.0 quad-connector citation verification (PubMed · Consensus · Scholar · Scite).

---

*This README follows the AIPOCH v6.0 standardised research-output template (May 2026). All repository READMEs in the [valentineghanem-bit](https://github.com/valentineghanem-bit) organisation share this structure.*
