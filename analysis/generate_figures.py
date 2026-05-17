"""
Publication Figures — HIV-TB Co-infection Ghana 260 Districts
==============================================================
Generates 8 publication-ready figures at 300 DPI
"""
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import seaborn as sns
from pathlib import Path
import shap
import warnings
warnings.filterwarnings('ignore')

OUT = Path('/sessions/lucid-confident-wozniak/hiv_tb_ghana/outputs')
FIG = OUT / 'figures'
FIG.mkdir(parents=True, exist_ok=True)

# Style
plt.rcParams.update({
 'font.family': 'DejaVu Serif',
 'font.size': 11,
 'axes.spines.top': False,
 'axes.spines.right': False,
 'figure.facecolor': 'white',
 'axes.facecolor': '#fafafa',
 'savefig.dpi': 300,
 'savefig.bbox': 'tight',
})
TITLE_KW = dict(fontsize=13, fontweight='bold', color='#000', pad=12)
CAP_KW = dict(ha='center', fontsize=12, style='italic', color='#333333')

gdf = gpd.read_file(OUT / 'data' / 'ghana_260_final_results.geojson')
print(f'Loaded: {len(gdf)} districts')

# ============================================================
# FIGURE 1 — Study Area & Disease Burden Choropleths (2×2)
# ============================================================
print('[1/8] Fig 1: Disease burden choropleths...')
fig, axes = plt.subplots(2, 2, figsize=(15, 14))
panels = [
 ('HIV_Prev_Total_pct', 'A. HIV Prevalence (%)', 'OrRd'),
 ('TB_Incidence_per100k', 'B. TB Incidence (per 100,000)', 'YlOrBr'),
 ('TB_HIV_CoInfection_pct', 'C. TB-HIV Co-infection (%)', 'Reds'),
 ('ART_Coverage_pct', 'D. ART Coverage (%)', 'BuGn'),
]
for ax, (var, title, cmap) in zip(axes.flat, panels):
 gdf.plot(column=var, cmap=cmap, legend=True, ax=ax, edgecolor='white',
 linewidth=0.3, legend_kwds={'shrink': 0.6})
 ax.set_title(title, **TITLE_KW)
 ax.axis('off')
plt.tight_layout(rect=[0, 0.04, 1, 1])
fig.text(0.5, 0.01,
 'Figure 1. Spatial distribution of HIV prevalence, TB incidence, TB-HIV co-infection, '
 'and ART coverage across 260 districts in Ghana.',
 **CAP_KW)
plt.savefig(FIG / 'Figure_1_disease_burden.png', dpi=300)
plt.close()

# ============================================================
# FIGURE 2 — LISA & Getis-Ord Hotspot Maps
# ============================================================
print('[2/8] Fig 2: LISA + Getis-Ord...')
fig, axes = plt.subplots(2, 2, figsize=(15, 14))

# Panel A: LISA for TB-HIV co-infection
lisa_cmap = {'High-High': '#d7191c', 'Low-Low': '#2c7bb6',
 'High-Low': '#fdae61', 'Low-High': '#abd9e9',
 'Not Significant': '#f0f0f0'}
ax = axes[0, 0]
for cluster, color in lisa_cmap.items():
 sub = gdf[gdf['LISA_cluster'] == cluster]
 if len(sub) > 0:
  sub.plot(ax=ax, color=color, edgecolor='white', linewidth=0.2,
  label=f'{cluster} (n={len(sub)})')
ax.set_title('A. LISA Cluster Map — TB-HIV Co-infection', **TITLE_KW)
ax.legend(loc='lower left', fontsize=8, frameon=True)
ax.axis('off')

# Panel B: Bivariate LISA (HIV × TB)
ax = axes[0, 1]
for cluster, color in lisa_cmap.items():
 sub = gdf[gdf['BvLISA_cluster'] == cluster]
 if len(sub) > 0:
  sub.plot(ax=ax, color=color, edgecolor='white', linewidth=0.2,
  label=f'{cluster} (n={len(sub)})')
ax.set_title('B. Bivariate LISA — HIV × TB', **TITLE_KW)
ax.legend(loc='lower left', fontsize=8, frameon=True)
ax.axis('off')

# Panel C: Getis-Ord Gi*
ax = axes[1, 0]
gi_cmap = {'Hot Spot 99%': '#d73027', 'Hot Spot 95%': '#fc8d59', 'Hot Spot 90%': '#fee090',
 'Cold Spot 99%': '#313695', 'Cold Spot 95%': '#4575b4', 'Cold Spot 90%': '#91bfdb',
 'Not Significant': '#f0f0f0'}
for cluster, color in gi_cmap.items():
 sub = gdf[gdf['Gi_cluster'] == cluster]
 if len(sub) > 0:
  sub.plot(ax=ax, color=color, edgecolor='white', linewidth=0.2,
  label=f'{cluster} (n={len(sub)})')
ax.set_title('C. Getis-Ord Gi* Hotspots', **TITLE_KW)
ax.legend(loc='lower left', fontsize=8, frameon=True)
ax.axis('off')

# Panel D: GWR local R²
ax = axes[1, 1]
if 'GWR_local_R2' in gdf.columns:
 gdf.plot(column='GWR_local_R2', cmap='viridis', legend=True, ax=ax,
 edgecolor='white', linewidth=0.2, legend_kwds={'shrink': 0.6})
 ax.set_title('D. GWR Local R² (Model Fit)', **TITLE_KW)
else:
 ax.axis('off')
ax.axis('off')

plt.tight_layout(rect=[0, 0.04, 1, 1])
fig.text(0.5, 0.01,
 'Figure 2. Spatial cluster analyses. A: Univariate LISA for TB-HIV co-infection; '
 'B: Bivariate LISA (HIV×TB); C: Getis-Ord Gi* hotspots; D: GWR local R² showing spatial non-stationarity.',
 **CAP_KW)
plt.savefig(FIG / 'Figure_2_spatial_clusters.png', dpi=300)
plt.close()

# ============================================================
# FIGURE 3 — Global Moran's I bar plot with significance
# ============================================================
print('[3/8] Fig 3: Global Moran\'s I...')
moran_df = pd.read_csv(OUT / 'tables' / 'global_morans_I.csv')
moran_df = moran_df.sort_values("Moran's I", ascending=True)
fig, ax = plt.subplots(figsize=(12, 8))
colors = ['#d7191c' if p < 0.001 else ('#fdae61' if p < 0.05 else '#bdbdbd')
 for p in moran_df['p-value']]
bars = ax.barh(moran_df['Variable'], moran_df["Moran's I"], color=colors,
 edgecolor='black', linewidth=0.5)
morans_col = "Moran's I"
for bar, (_, row) in zip(bars, moran_df.iterrows()):
 i_val = row[morans_col]
 p_val = row['p-value']
 ax.text(i_val + 0.01, bar.get_y() + bar.get_height()/2,
 'I={:.3f} (p={:.3f})'.format(i_val, p_val),
 va='center', fontsize=9)
ax.set_xlabel("Global Moran's I", fontsize=12, fontweight='semibold')
ax.set_title("Global Moran's I — Spatial Autocorrelation Across Key Indicators", **TITLE_KW)
ax.axvline(0, color='black', linestyle='-', linewidth=0.5)
ax.set_xlim(-0.1, 1.0)
legend_handles = [mpatches.Patch(color='#d7191c', label='p < 0.001 (highly significant)'),
 mpatches.Patch(color='#fdae61', label='p < 0.05 (significant)'),
 mpatches.Patch(color='#bdbdbd', label='p ≥ 0.05 (random)')]
ax.legend(handles=legend_handles, loc='lower right', frameon=True)
plt.tight_layout(rect=[0, 0.05, 1, 1])
fig.text(0.5, 0.01,
 "Figure 3. Global Moran's I values across 11 HIV, TB, and socioeconomic indicators "
 "(KNN-5 weight matrix, 999 permutations).",
 **CAP_KW)
plt.savefig(FIG / 'Figure_3_morans_I.png', dpi=300)
plt.close()

# ============================================================
# FIGURE 4 — ML Model Comparison (ROC + Performance bar)
# ============================================================
print('[4/8] Fig 4: ML comparison...')
perf = pd.read_csv(OUT / 'tables' / 'ml_test_set_performance.csv')
cv = pd.read_csv(OUT / 'tables' / 'ml_10fold_cv_results.csv')

fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# Panel A: CV AUC with error bars
ax = axes[0]
x = np.arange(len(cv))
ax.bar(x, cv['AUC_mean'], yerr=cv['AUC_SD'], capsize=5,
 color=['#3182bd', '#e6550d', '#31a354', '#756bb1'][:len(cv)],
 edgecolor='black', linewidth=0.6)
for i, (_, row) in enumerate(cv.iterrows()):
 ax.text(i, row['AUC_mean'] + 0.02, f"{row['AUC_mean']:.3f}",
 ha='center', fontsize=10, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(cv['Model'], rotation=15, ha='right')
ax.set_ylim(0.7, 1.05)
ax.set_ylabel('AUC-ROC (mean ± SD)', fontsize=12, fontweight='semibold')
ax.set_title('A. 10-Fold Cross-Validation AUC', **TITLE_KW)
ax.axhline(0.5, color='red', linestyle=':', linewidth=1, alpha=0.5, label='Random')

# Panel B: Test-set metrics comparison
ax = axes[1]
metrics = ['AUC', 'Accuracy', 'Precision', 'Recall', 'F1']
x = np.arange(len(perf))
w = 0.15
for i, metric in enumerate(metrics):
 ax.bar(x + i*w, perf[metric], w, label=metric,
 edgecolor='black', linewidth=0.3)
ax.set_xticks(x + 2*w)
ax.set_xticklabels(perf['Model'], rotation=15, ha='right')
ax.set_ylabel('Metric Value', fontsize=12, fontweight='semibold')
ax.set_ylim(0, 1.05)
ax.set_title('B. Test-Set Performance (25% held-out)', **TITLE_KW)
ax.legend(loc='upper right', ncol=2, fontsize=9)

plt.tight_layout(rect=[0, 0.04, 1, 1])
fig.text(0.5, 0.01,
 'Figure 4. ML model performance. A: 10-fold stratified CV AUC with SD error bars; '
 'B: Test-set metrics across four classifiers predicting HIV-TB co-infection hotspots.',
 **CAP_KW)
plt.savefig(FIG / 'Figure_4_ml_performance.png', dpi=300)
plt.close()

# ============================================================
# FIGURE 5 — SHAP Summary Plot
# ============================================================
print('[5/8] Fig 5: SHAP importance + summary...')
shap_vals = np.load(OUT / 'models' / 'shap_values.npy')
X_test_arr = np.load(OUT / 'models' / 'shap_X_test.npy')
shap_imp = pd.read_csv(OUT / 'tables' / 'shap_feature_importance.csv')
features = shap_imp['Feature'].tolist()

# Clean labels
LABEL_MAP = {
 'HIV_Prev_Total_pct': 'HIV Prevalence (Total)',
 'HIV_Prev_Women_pct': 'HIV Prevalence (Women)',
 'HIV_Prev_Men_pct': 'HIV Prevalence (Men)',
 'HIV_Awareness_Women_pct': 'HIV Awareness',
 'Condom_Use_pct': 'Condom Use',
 'High_Risk_Sex_pct': 'High-Risk Sex',
 'Ever_Tested_HIV_pct': 'Ever Tested for HIV',
 'Know_Where_Test_pct': 'Knows Where to Test',
 'Accepting_Attitudes_pct': 'Accepting Attitudes',
 'Poverty_Incidence_pct': 'Poverty Incidence',
 'Poverty_Intensity_pct': 'Poverty Intensity',
 'Unemployment_Rate_pct': 'Unemployment Rate',
 'Illiteracy_Rate_pct': 'Illiteracy Rate',
 'Uninsurance_Rate_pct': 'Uninsurance Rate',
 'Youth_Dependency_Ratio': 'Youth Dependency',
 'Sex_Ratio_15_64': 'Sex Ratio (15-64)',
 'Sexually_Active_Pop_pct': 'Sexually Active Pop.',
 'TB_Incidence_per100k': 'TB Incidence (/100k)',
 'ART_Coverage_pct': 'ART Coverage',
 'VCT_Uptake_pct': 'VCT Uptake',
 'Doctors_per10k': 'Doctors / 10,000',
 'Nurses_per10k': 'Nurses / 10,000',
 'OOP_Expenditure_pct': 'OOP Expenditure',
 'TB_Treatment_Success_pct': 'TB Treatment Success',
}

# SHAP summary bar plot (top 15)
fig, ax = plt.subplots(figsize=(14, 10))
top15 = shap_imp.head(15).iloc[::-1]
colors_grad = plt.cm.Blues(np.linspace(0.4, 0.9, len(top15)))
bars = ax.barh([LABEL_MAP.get(f, f) for f in top15['Feature']], top15['Mean_abs_SHAP'],
 color=colors_grad, edgecolor='black', linewidth=0.5)
for bar, val in zip(bars, top15['Mean_abs_SHAP']):
 ax.text(val + 0.03, bar.get_y() + bar.get_height()/2,
 f'{val:.3f}', va='center', fontsize=10)
ax.set_xlabel('Mean |SHAP value|', fontsize=13, fontweight='semibold', labelpad=8)
ax.set_title('Top 15 Feature Importance (LightGBM)', **TITLE_KW)
ax.tick_params(axis='y', labelsize=12)
plt.tight_layout(rect=[0, 0.05, 1, 1])
fig.text(0.5, 0.02,
 'Figure 5. SHAP-derived mean absolute feature importance for HIV-TB co-infection hotspot prediction '
 '(LightGBM model, test set).',
 **CAP_KW)
plt.savefig(FIG / 'Figure_5_shap_importance.png', dpi=300)
plt.close()

# SHAP beeswarm (top 10)
fig = plt.figure(figsize=(12, 9))
top10_idx = [features.index(f) for f in shap_imp['Feature'].head(10)]
shap_top = shap_vals[:, top10_idx]
X_top = X_test_arr[:, top10_idx]
top_labels = [LABEL_MAP.get(f, f) for f in shap_imp['Feature'].head(10)]
shap.summary_plot(shap_top, X_top, feature_names=top_labels, show=False, max_display=10)
plt.title('SHAP Summary — Directional Impact on Hotspot Probability', fontsize=13,
 fontweight='bold', pad=10)
plt.tight_layout()
plt.savefig(FIG / 'Figure_5b_shap_beeswarm.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================
# FIGURE 6 — ML Risk Prediction Map
# ============================================================
print('[6/8] Fig 6: Ensemble risk map...')
fig, axes = plt.subplots(1, 2, figsize=(16, 9))
ax = axes[0]
gdf.plot(column='Ensemble_Risk_Score', cmap='RdYlGn_r', legend=True, ax=ax,
 edgecolor='white', linewidth=0.3,
 legend_kwds={'label': 'Hotspot Probability', 'shrink': 0.6})
ax.set_title('A. Ensemble-Predicted Hotspot Risk', **TITLE_KW)
ax.axis('off')

ax = axes[1]
# Top 20 high-risk districts
top20 = gdf.nlargest(20, 'Ensemble_Risk_Score')[['District', 'REGION', 'Ensemble_Risk_Score']]
y_pos = np.arange(len(top20))
bars = ax.barh(y_pos, top20['Ensemble_Risk_Score'],
 color=plt.cm.Reds(top20['Ensemble_Risk_Score']),
 edgecolor='black', linewidth=0.4)
for i, (_, row) in enumerate(top20.iterrows()):
 ax.text(row['Ensemble_Risk_Score'] + 0.005,
 i,
 f' ({row["REGION"]})',
 va='center', fontsize=8, color='#555')
ax.set_yticks(y_pos)
ax.set_yticklabels(top20['District'], fontsize=9)
ax.invert_yaxis()
ax.set_xlabel('Ensemble Hotspot Probability', fontsize=12, fontweight='semibold')
ax.set_title('B. Top 20 High-Risk Districts', **TITLE_KW)
ax.set_xlim(0, 1.05)

plt.tight_layout(rect=[0, 0.04, 1, 1])
fig.text(0.5, 0.01,
 'Figure 6. Machine-learning-derived HIV-TB co-infection hotspot risk. A: Ensemble-averaged '
 'district-level risk map; B: Top-20 predicted high-risk districts.',
 **CAP_KW)
plt.savefig(FIG / 'Figure_6_ml_risk_map.png', dpi=300)
plt.close()

# ============================================================
# FIGURE 7 — Correlation Matrix (FULL, no masking)
# ============================================================
print('[7/8] Fig 7: Correlation matrix...')
corr_vars = [
 'HIV_Prev_Total_pct', 'TB_Incidence_per100k', 'TB_HIV_CoInfection_pct',
 'ART_Coverage_pct', 'VCT_Uptake_pct',
 'Condom_Use_pct', 'Ever_Tested_HIV_pct', 'HIV_Awareness_Women_pct',
 'Poverty_Incidence_pct', 'Poverty_Intensity_pct',
 'Unemployment_Rate_pct', 'Illiteracy_Rate_pct', 'Uninsurance_Rate_pct',
 'Doctors_per10k', 'Nurses_per10k', 'OOP_Expenditure_pct',
 'Youth_Dependency_Ratio', 'Sexually_Active_Pop_pct',
 'TB_Treatment_Success_pct',
]
corr = gdf[corr_vars].corr()
short_labels = [LABEL_MAP.get(v, v) for v in corr_vars]
corr.columns = short_labels
corr.index = short_labels

fig, ax = plt.subplots(figsize=(14, 12))
cmap = LinearSegmentedColormap.from_list('rdbu', ['#2166ac', '#f7f7f7', '#b2182b'])
sns.heatmap(corr, annot=True, fmt='.2f', cmap=cmap, center=0,
 vmin=-1, vmax=1, linewidths=0.4, cbar_kws={'shrink': 0.7},
 annot_kws={'size': 7}, square=True, ax=ax)
ax.set_title('Pearson Correlation Matrix (260 Districts, All 19 Key Variables)',
 **TITLE_KW)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout(rect=[0, 0.04, 1, 1])
fig.text(0.5, 0.01,
 'Figure 7. Pearson correlation matrix of 19 HIV, TB, healthcare-access, and '
 'socioeconomic determinants across 260 Ghanaian districts.',
 **CAP_KW)
plt.savefig(FIG / 'Figure_7_correlation.png', dpi=300)
plt.close()

# ============================================================
# FIGURE 8 — GWR Local Coefficient Maps
# ============================================================
print('[8/8] Fig 8: GWR coefficients...')
gwr_vars = [c for c in gdf.columns if c.startswith('GWR_coef_')]
if len(gwr_vars) >= 4:
 fig, axes = plt.subplots(2, 2, figsize=(15, 14))
 for ax, var in zip(axes.flat, gwr_vars[:4]):
  label = var.replace('GWR_coef_', '')
  label_pretty = LABEL_MAP.get(label, label)
  gdf.plot(column=var, cmap='RdBu_r', legend=True, ax=ax,
  edgecolor='white', linewidth=0.2,
  legend_kwds={'shrink': 0.6})
  ax.set_title(f'GWR β: {label_pretty}', **TITLE_KW)
  ax.axis('off')
  plt.tight_layout(rect=[0, 0.04, 1, 1])
  fig.text(0.5, 0.01,
  'Figure 8. GWR local coefficients showing spatial non-stationarity in predictor effects on '
  'TB-HIV co-infection prevalence.',
  **CAP_KW)
  plt.savefig(FIG / 'Figure_8_gwr_coefficients.png', dpi=300)
  plt.close()

print('\n✓ All 8 figures saved at 300 DPI.')
print(f' Location: {FIG}')
for f in sorted(FIG.glob('*.png')):
 print(f' {f.name}')
