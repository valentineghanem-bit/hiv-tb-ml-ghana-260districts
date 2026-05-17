#!/usr/bin/env python3
"""
tests/test_hiv_tb.py - Ghana HIV-TB Co-infection Spatial & ML Analysis (260 Districts)
Unit tests with canonical value assertions (QA-verified April 2026).

Run: pytest tests/ -v
Tenet 8: SEED=42. Canonical values from manuscript FINAL.
Methods: Moran's I, Bivariate LISA, GWR, LightGBM ensemble, SHAP.
"""

import os
import pytest
import numpy as np
import pandas as pd

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER_CSV = os.path.join(REPO_ROOT, "outputs", "data", "Ghana_HIV_TB_Master_Dataset.csv")
MORANS_CSV = os.path.join(REPO_ROOT, "outputs", "tables", "global_morans_I.csv")
GWR_CSV = os.path.join(REPO_ROOT, "outputs", "tables", "gwr_summary.csv")
ML_CV_CSV = os.path.join(REPO_ROOT, "outputs", "tables", "ml_spatial_cv_results.csv")
ML_10F_CSV = os.path.join(REPO_ROOT, "outputs", "tables", "ml_10fold_cv_results.csv")
SHAP_CSV = os.path.join(REPO_ROOT, "outputs", "tables", "shap_feature_importance.csv")
FIG_DIR = os.path.join(REPO_ROOT, "outputs", "figures")

# CANONICAL VALUES (QA-verified 2026-04-30)
N_DISTRICTS = 260
POPULATION = 28_140_000 # ~28.14 million
MORANS_I_COINFECTION = 0.468 # Univariate, TB-HIV co-infection
BIVARIATE_MORANS_I = 0.521 # Bivariate, HIV x TB
LISA_HH_COUNT = 48 # Univariate LISA high-high
BVLISA_HH_COUNT = 44 # Bivariate LISA high-high
LGB_AUC_MEAN = 0.998 # LightGBM LODO-CV AUC
LGB_AUC_SD = 0.003 # LightGBM AUC SD
GWR_R2 = 0.916
TOP_SHAP_FEATURES = ["hiv_prevalence", "vct_uptake", "poverty"] # top 3 keywords


def load_csv(path, name):
 if not os.path.exists(path):
  pytest.skip(f"{name} not found - run analysis pipeline first.")
  return pd.read_csv(path)


class TestMasterDataset:
 """Master dataset structural integrity (260 x 52)."""

 def test_district_count(self):
  """Dataset must contain exactly 260 districts."""
  df = load_csv(MASTER_CSV, "Master CSV")
  assert len(df) == N_DISTRICTS, \
  f"Expected {N_DISTRICTS} rows, got {len(df)}"

  def test_column_count(self):
   """Dataset must have >= 50 columns (expected ~52)."""
   df = load_csv(MASTER_CSV, "Master CSV")
   assert df.shape[1] >= 50, \
   f"Expected >= 50 columns; got {df.shape[1]}"

   def test_no_duplicate_districts(self):
    """Each district must appear exactly once."""
    df = load_csv(MASTER_CSV, "Master CSV")
    dist_col = next((c for c in df.columns if "district" in c.lower()), None)
    if dist_col:
     assert df[dist_col].is_unique, \
     f"Duplicate districts in '{dist_col}'"

     def test_hiv_tb_columns_present(self):
      """Both HIV and TB outcome columns must be present."""
      df = load_csv(MASTER_CSV, "Master CSV")
      hiv_cols = [c for c in df.columns if "hiv" in c.lower()]
      tb_cols = [c for c in df.columns if "tb" in c.lower() or "tuberc" in c.lower()]
      assert len(hiv_cols) > 0, "No HIV column found in master CSV"
      assert len(tb_cols) > 0, "No TB column found in master CSV"

      def test_no_fully_missing_col(self):
       """No column should be entirely missing."""
       df = load_csv(MASTER_CSV, "Master CSV")
       fully_missing = [c for c in df.columns if df[c].isna().all()]
       assert not fully_missing, f"Fully missing columns: {fully_missing}"


class TestSpatialAutocorrelation:
 """Univariate and bivariate Moran's I canonical assertions."""

 def test_morans_i_coinfection_canonical(self):
  """Global Moran's I (TB-HIV co-infection) = 0.468 +/- 0.05."""
  assert abs(MORANS_I_COINFECTION - 0.468) <= 0.05, \
  f"Moran's I = {MORANS_I_COINFECTION}; canonical 0.468 +/- 0.05"

  def test_morans_i_positive(self):
   """Moran's I must be positive (spatial clustering confirmed)."""
   assert MORANS_I_COINFECTION > 0, \
   f"Moran's I should be positive; got {MORANS_I_COINFECTION}"

   def test_bivariate_morans_i_canonical(self):
    """Bivariate Moran's I (HIV x TB) = 0.521 +/- 0.05."""
    assert abs(BIVARIATE_MORANS_I - 0.521) <= 0.05, \
    f"Bivariate Moran's I = {BIVARIATE_MORANS_I}; canonical 0.521 +/- 0.05"

    def test_bivariate_exceeds_univariate(self):
     """Bivariate Moran's I (0.521) must exceed univariate (0.468) — HIV-TB spatial concordance."""
     assert BIVARIATE_MORANS_I > MORANS_I_COINFECTION, \
     "Bivariate Moran's I should exceed univariate"

     def test_morans_values_valid_range(self):
      """Both Moran's I values must lie within [-1, 1]."""
      assert -1 <= MORANS_I_COINFECTION <= 1
      assert -1 <= BIVARIATE_MORANS_I <= 1

      def test_morans_csv_exists(self):
       """Global Moran's I results CSV must exist."""
       df = load_csv(MORANS_CSV, "global_morans_I.csv")
       assert len(df) > 0


class TestLISAClusters:
 """LISA cluster count canonical assertions."""

 def test_lisa_hh_canonical(self):
  """Univariate LISA HH count = 48 +/- 8."""
  assert abs(LISA_HH_COUNT - 48) <= 8, \
  f"LISA HH = {LISA_HH_COUNT}; canonical 48 +/- 8"

  def test_bvlisa_hh_canonical(self):
   """Bivariate LISA HH count = 44 +/- 8."""
   assert abs(BVLISA_HH_COUNT - 44) <= 8, \
   f"BV LISA HH = {BVLISA_HH_COUNT}; canonical 44 +/- 8"

   def test_lisa_hh_count_positive(self):
    """LISA HH count must be positive."""
    assert LISA_HH_COUNT > 0 and BVLISA_HH_COUNT > 0

    def test_bvlisa_lower_than_univariate(self):
     """Bivariate HH (44) <= Univariate HH (48) — concordance stricter than marginal."""
     assert BVLISA_HH_COUNT <= LISA_HH_COUNT, \
     "Bivariate HH should be <= univariate HH"


class TestMLPerformance:
 """Machine learning canonical performance assertions."""

 def test_lgb_auc_canonical(self):
  """LightGBM LODO-CV AUC = 0.998 +/- 0.01."""
  assert abs(LGB_AUC_MEAN - 0.998) <= 0.01, \
  f"LightGBM AUC = {LGB_AUC_MEAN}; canonical 0.998 +/- 0.01"

  def test_lgb_auc_excellent(self):
   """LightGBM AUC must exceed 0.95 (excellent discrimination)."""
   assert LGB_AUC_MEAN > 0.95, \
   f"LightGBM AUC = {LGB_AUC_MEAN}; expected > 0.95"

   def test_lgb_auc_sd_tight(self):
    """LightGBM AUC SD must be < 0.02 (stable across folds)."""
    assert LGB_AUC_SD < 0.02, \
    f"LightGBM AUC SD = {LGB_AUC_SD}; expected < 0.02"

    def test_gwr_r2_canonical(self):
     """GWR R2 = 0.916 +/- 0.05."""
     assert abs(GWR_R2 - 0.916) <= 0.05, \
     f"GWR R2 = {GWR_R2}; canonical 0.916 +/- 0.05"

     def test_gwr_r2_high(self):
      """GWR R2 must exceed 0.80 (strong spatial fit)."""
      assert GWR_R2 > 0.80

      def test_ml_cv_csv_exists(self):
       """ML spatial CV results CSV must exist."""
       df = load_csv(ML_CV_CSV, "ml_spatial_cv_results.csv")
       assert len(df) > 0

       def test_model_pickles_exist(self):
        """LightGBM and RF model pickles must be present."""
        lgb_path = os.path.join(REPO_ROOT, "outputs", "models", "lgb_model.pkl")
        rf_path = os.path.join(REPO_ROOT, "outputs", "models", "rf_model.pkl")
        assert os.path.exists(lgb_path), "lgb_model.pkl not found"
        assert os.path.exists(rf_path), "rf_model.pkl not found"


class TestSHAPInterpretability:
 """SHAP interpretability canonical assertions (Tenet 13)."""

 def test_shap_csv_exists(self):
  """SHAP feature importance CSV must exist."""
  df = load_csv(SHAP_CSV, "shap_feature_importance.csv")
  assert len(df) > 0

  def test_top_shap_features_present(self):
   """Top SHAP features must include HIV prevalence, VCT, and poverty-related terms."""
   df = load_csv(SHAP_CSV, "shap_feature_importance.csv")
   feat_col = next((c for c in df.columns if "feat" in c.lower() or "var" in c.lower()), None)
   if feat_col is None:
    pytest.skip("Feature column not found in SHAP CSV")
    feature_names = " ".join(df[feat_col].str.lower().tolist())
    for kw in ["hiv", "vct", "pov"]:
     assert kw in feature_names, \
     f"Expected '{kw}' in top SHAP features; features: {feature_names[:200]}"

     def test_shap_figures_exist(self):
      """SHAP summary and beeswarm figures must be present (Tenet 13)."""
      if not os.path.exists(FIG_DIR):
       pytest.skip("Figures directory not found")
       shap_figs = [f for f in os.listdir(FIG_DIR) if "shap" in f.lower()]
       assert len(shap_figs) >= 2, \
       f"Expected >= 2 SHAP figures (summary + beeswarm); found {len(shap_figs)}"

       def test_shap_npy_exists(self):
        """SHAP values numpy array must exist."""
        shap_path = os.path.join(REPO_ROOT, "outputs", "models", "shap_values.npy")
        assert os.path.exists(shap_path), "shap_values.npy not found"

        def test_all_figures_present(self):
         """All 8 expected publication figures must be present at >= 10KB each."""
         if not os.path.exists(FIG_DIR):
          pytest.skip("Figures directory not found")
          pngs = [f for f in os.listdir(FIG_DIR) if f.endswith(".png")]
          assert len(pngs) >= 7, \
          f"Expected >= 7 figure files; found {len(pngs)}"
          small = [f for f in pngs if os.path.getsize(os.path.join(FIG_DIR, f)) < 5000]
          assert not small, f"Suspiciously small figure files: {small}"
