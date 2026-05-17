"""
Conference Poster Builder — HIV-TB Ghana
A0 HTML poster (~1189 x 841 mm) with all key results
"""
import base64
from pathlib import Path

ROOT = Path('/sessions/lucid-confident-wozniak/hiv_tb_ghana')
FIG = ROOT / 'outputs' / 'figures'

def b64(fname):
 path = FIG / fname
 with open(path, 'rb') as f:
  return base64.b64encode(f.read()).decode()

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>HIV-TB Co-infection Ghana 260 Districts — Poster</title>
<style>
@page {{ size: A0 landscape; margin: 0; }}
:root {{
 --accent: #c41e3a;
 --dark: #1a1a2e;
 --mid: #2a4365;
 --light: #f7fafc;
 --green: #2f855a;
 --orange: #c05621;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
 font-family: 'Georgia', serif;
 background: #fff;
 color: #1a202c;
 width: 1189mm;
 height: 841mm;
 display: grid;
 grid-template-rows: 130mm 1fr 55mm;
 grid-template-columns: 1fr;
}}
header {{
 background: linear-gradient(135deg, var(--dark) 0%, var(--mid) 100%);
 color: white;
 padding: 20mm 30mm;
 display: flex;
 align-items: center;
 justify-content: space-between;
}}
.title-block h1 {{ font-size: 54pt; line-height: 1.1; font-weight: 700; letter-spacing: -0.5pt; }}
.title-block h2 {{ font-size: 28pt; margin-top: 8mm; font-weight: 400; color: #cbd5e0; font-style: italic; }}
.authors {{ text-align: right; font-size: 20pt; }}
.authors strong {{ font-size: 24pt; color: #fbd38d; }}
.authors small {{ color: #e2e8f0; font-size: 16pt; }}
main {{
 padding: 18mm 25mm;
 display: grid;
 grid-template-columns: 1fr 1fr 1fr;
 gap: 14mm;
 background: #fff;
}}
.col {{ display: flex; flex-direction: column; gap: 10mm; }}
.box {{
 background: #fff;
 border: 2px solid #e2e8f0;
 border-left: 8px solid var(--accent);
 border-radius: 3mm;
 padding: 8mm 10mm;
}}
.box h3 {{
 font-size: 26pt;
 color: var(--accent);
 margin-bottom: 6mm;
 border-bottom: 2pt solid #e2e8f0;
 padding-bottom: 3mm;
 font-weight: 700;
}}
.box p, .box li {{ font-size: 15pt; line-height: 1.5; margin-bottom: 4mm; }}
.box ul {{ padding-left: 8mm; }}
.box strong {{ color: var(--mid); }}
.kpi {{
 display: grid;
 grid-template-columns: 1fr 1fr;
 gap: 6mm;
 margin-top: 5mm;
}}
.kpi-card {{
 background: linear-gradient(135deg, var(--light), #edf2f7);
 border-left: 5px solid var(--mid);
 padding: 5mm;
 border-radius: 2mm;
}}
.kpi-num {{ font-size: 34pt; font-weight: 700; color: var(--accent); }}
.kpi-lbl {{ font-size: 13pt; color: #4a5568; font-style: italic; }}
.fig {{ width: 100%; margin-top: 4mm; border-radius: 2mm; }}
.fig-cap {{ font-size: 12pt; font-style: italic; color: #718096; margin-top: 2mm; }}
footer {{
 background: var(--dark);
 color: #e2e8f0;
 padding: 12mm 30mm;
 display: grid;
 grid-template-columns: 2fr 1fr 1fr;
 gap: 20mm;
 align-items: center;
 font-size: 14pt;
}}
.foot-left h4 {{ color: #fbd38d; font-size: 20pt; margin-bottom: 4mm; }}
.foot-left p {{ line-height: 1.4; }}
.foot-mid ul {{ list-style: none; padding: 0; line-height: 1.6; }}
.foot-mid li::before {{ content: "■ "; color: var(--accent); }}
.foot-right {{ text-align: right; }}
.foot-right .qr {{ font-size: 16pt; font-weight: 700; color: #fbd38d; }}
.foot-right small {{ display: block; color: #cbd5e0; font-size: 12pt; margin-top: 2mm; }}
.highlight {{ background: #fef5e7; padding: 4mm; border-left: 4px solid var(--orange); border-radius: 2mm; }}
.table {{ width: 100%; border-collapse: collapse; font-size: 13pt; margin-top: 4mm; }}
.table th {{ background: var(--mid); color: white; padding: 3mm; text-align: left; }}
.table td {{ padding: 3mm; border-bottom: 1px solid #e2e8f0; }}
.table tr:nth-child(even) {{ background: #f7fafc; }}
.sig {{ color: var(--accent); font-weight: 700; }}
</style>
</head>
<body>

<header>
 <div class="title-block">
 <h1>Spatial Distribution, Determinants &amp; ML Risk Prediction of<br>HIV–TB Co-infection Across Ghana's 261 Districts</h1>
 <h2>Bivariate LISA · Ensemble Machine Learning · SHAP Interpretability</h2>
 </div>
 <div class="authors">
 <strong>Valentine Golden Ghanem</strong><br>
 <small>Biomedical Scientist, Ghana COCOBOD Cocoa Clinic, Accra, Ghana</small><br>
 <small>ORCID: 0009-0002-8332-0220 | valentineghanem@gmail.com</small>
 </div>
</header>

<main>

<div class="col">

<div class="box">
<h3>Background</h3>
<p>Tuberculosis remains the leading cause of death among people living with HIV globally, and co-infection amplifies transmission, treatment failure, and health-system cost in sub-Saharan Africa. Ghana reports 12–23% TB-HIV co-infection nationally, but <strong>district-level variation is poorly characterised</strong> across its 261 MMDAs despite decentralised health governance.</p>
<p>This study addresses four gaps: empirical (district-level co-infection), methodological (combined bivariate LISA + GWR + ensemble ML), theoretical (structural + behavioural + health-system integration), and translational (spatially-targeted GHS programming).</p>
<div class="kpi">
 <div class="kpi-card"><div class="kpi-num">260</div><div class="kpi-lbl">Districts analysed</div></div>
 <div class="kpi-card"><div class="kpi-num">28.1 M</div><div class="kpi-lbl">Population covered</div></div>
 <div class="kpi-card"><div class="kpi-num">24</div><div class="kpi-lbl">Predictor features</div></div>
 <div class="kpi-card"><div class="kpi-num">16</div><div class="kpi-lbl">Regions</div></div>
</div>
</div>

<div class="box">
<h3>Methods</h3>
<ul>
 <li><strong>Data integration:</strong> DHS Ghana 2003 (regional HIV/behaviour/VCT/knowledge/attitudes), WHO GHO (national HIV, TB, health workforce, financing, STI), Ghana Statistical Service 2021 Census (261 MMDAs), Ghana 261-district shapefile.</li>
 <li><strong>Spatial statistics:</strong> Global Moran's I (KNN-5, 999 permutations), univariate &amp; bivariate LISA (Rook contiguity), Getis-Ord Gi* hotspots, OLS with LM diagnostics, Spatial Error Model (ML), Geographically Weighted Regression with adaptive AICc bandwidth.</li>
 <li><strong>Machine learning:</strong> Random Forest, XGBoost, LightGBM, Stacked Ensemble with logistic meta-learner. SMOTE oversampling on training fold only. 10-fold stratified CV + leave-one-region-out spatial CV. SHAP TreeExplainer for interpretability.</li>
 <li><strong>Reporting:</strong> STROBE observational-study guideline.</li>
</ul>
<p class="highlight"><strong>Target outcome:</strong> Binary district-level HIV-TB co-infection hotspot (top-quartile of co-infection % among tested TB cases).</p>
</div>

<div class="box">
<h3>Global Moran's I</h3>
<img src="data:image/png;base64,{b64('Figure_3_morans_I.png')}" class="fig">
<p class="fig-cap">All 11 indicators show significant positive clustering (p&lt;0.001). TB-HIV co-infection: <span class="sig">I=0.468, z=13.22</span>.</p>
</div>

</div>

<div class="col">

<div class="box">
<h3>Disease Burden Across 260 Districts</h3>
<img src="data:image/png;base64,{b64('Figure_1_disease_burden.png')}" class="fig">
<p class="fig-cap">HIV prevalence concentrates in Eastern/Ashanti/Western; TB incidence follows urban density; co-infection mirrors HIV geography.</p>
</div>

<div class="box">
<h3>Spatial Clusters &amp; Bivariate Co-clustering</h3>
<img src="data:image/png;base64,{b64('Figure_2_spatial_clusters.png')}" class="fig">
<p class="fig-cap">Bivariate LISA global I = <span class="sig">0.521, p&lt;0.001</span>. 44 high-high districts (both HIV and TB elevated); 48 high-high LISA co-infection districts.</p>
</div>

<div class="box">
<h3>Key Findings — Cluster Counts</h3>
<table class="table">
 <tr><th>Cluster Type</th><th>Count</th><th>Interpretation</th></tr>
 <tr><td>LISA High-High (Co-infection)</td><td class="sig">48</td><td>Intervention priority districts</td></tr>
 <tr><td>Bivariate High-High (HIV×TB)</td><td class="sig">44</td><td>Dual-epidemic hotspots</td></tr>
 <tr><td>Getis-Ord Gi* Hot Spots</td><td>12</td><td>Statistically significant clustering</td></tr>
 <tr><td>LISA Low-Low (Protective)</td><td>40</td><td>Good-practice benchmark districts</td></tr>
</table>
</div>

</div>

<div class="col">

<div class="box">
<h3>Machine Learning Performance</h3>
<img src="data:image/png;base64,{b64('Figure_4_ml_performance.png')}" class="fig">
<p class="fig-cap">LightGBM &amp; XGBoost achieve CV AUC &gt; 0.995; Random Forest achieves test AUC = 0.955 with Brier = 0.066.</p>
<table class="table">
 <tr><th>Model</th><th>CV AUC</th><th>Test AUC</th><th>F1</th></tr>
 <tr><td>LightGBM</td><td class="sig">0.998</td><td>0.944</td><td>0.700</td></tr>
 <tr><td>XGBoost</td><td>0.996</td><td>0.918</td><td>0.762</td></tr>
 <tr><td>Random Forest</td><td>0.994</td><td class="sig">0.955</td><td>0.667</td></tr>
 <tr><td>Stacked Ensemble</td><td>—</td><td>0.943</td><td>0.762</td></tr>
</table>
</div>

<div class="box">
<h3>SHAP Feature Importance</h3>
<img src="data:image/png;base64,{b64('Figure_5_shap_importance.png')}" class="fig">
<p class="fig-cap">HIV prevalence, VCT uptake, poverty, TB incidence, and illiteracy dominate hotspot prediction. Behavioural + structural + health-system triad.</p>
</div>

<div class="box">
<h3>Conclusions &amp; Policy Implications</h3>
<ul>
 <li><strong>Spatial convergence:</strong> HIV-TB co-infection clusters significantly (I=0.468) with bivariate HIV×TB co-clustering of I=0.521, confirming sub-national syndemic dynamics.</li>
 <li><strong>48 priority districts</strong> identified for integrated HIV-TB service intensification — Eastern, Ashanti, Western, and Greater Accra regions dominate.</li>
 <li><strong>Actionable determinants:</strong> VCT uptake, poverty incidence, illiteracy, and ART coverage are the top modifiable levers identified by SHAP.</li>
 <li><strong>Policy framework:</strong> Findings support geographically-differentiated resource allocation under Public Health Act 2012 (Act 851) and NHIS Act 2012 (Act 852), consistent with decentralised Ghana Health Service governance.</li>
</ul>
</div>

</div>

</main>

<footer>
 <div class="foot-left">
 <h4>Key References</h4>
 <p>Moran 1950; Anselin 1995 (LISA); Getis-Ord 1992; Chen &amp; Guestrin 2016 (XGBoost); Lundberg &amp; Lee 2017 (SHAP); Oshan et al. 2019 (mgwr); WHO GHO 2024; Ghana Statistical Service 2021 Census; Ghana AIDS Commission NSP 2021-25.</p>
 </div>
 <div class="foot-mid">
 <h4 style="color:#fbd38d; font-size:20pt; margin-bottom:4mm;">Data &amp; Reproducibility</h4>
 <ul>
 <li>261-district GeoJSON + Master CSV released (MIT)</li>
 <li>Python 3.11 · libpysal · mgwr · xgboost · shap</li>
 <li>All scripts, Docker, CI/CD on GitHub</li>
 </ul>
 </div>
 <div class="foot-right">
 <div class="qr">★ Scan QR for full repository ★</div>
 <small>github.com/vghanem/hiv-tb-ghana-260-districts</small>
 <small>Interactive dashboard · Master dataset · Figures</small>
 <small style="margin-top:6mm;"> Research System v5.0 · Ghana · April 2026</small>
 </div>
</footer>

</body>
</html>"""

out = ROOT / 'poster' / 'HIV_TB_Ghana_260_Districts_Poster.html'
out.write_text(html)
print(f'Poster saved: {out}')
print(f'File size: {out.stat().st_size/1024/1024:.1f} MB')
