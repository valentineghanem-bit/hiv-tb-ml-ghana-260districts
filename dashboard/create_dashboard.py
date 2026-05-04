"""
Interactive HTML Dashboard Builder — HIV-TB Ghana
Self-contained Plotly.js dashboard (no server required)
"""
import json
import pandas as pd
import geopandas as gpd
from pathlib import Path

ROOT = Path('/sessions/lucid-confident-wozniak/hiv_tb_ghana')
OUT = ROOT / 'outputs'
gdf = gpd.read_file(OUT / 'data' / 'ghana_260_final_results.geojson')

# Simplify geometry for web performance
gdf['geometry'] = gdf['geometry'].simplify(0.005, preserve_topology=True)
geojson = json.loads(gdf[['DISTRICT', 'REGION', 'geometry']].to_json())

df = gdf.drop(columns='geometry').copy()

# Variables for the dropdowns
map_vars = {
 'HIV_Prev_Total_pct': 'HIV Prevalence (%)',
 'TB_Incidence_per100k': 'TB Incidence (per 100k)',
 'TB_HIV_CoInfection_pct': 'TB-HIV Co-infection (%)',
 'ART_Coverage_pct': 'ART Coverage (%)',
 'VCT_Uptake_pct': 'VCT Uptake (%)',
 'Ensemble_Risk_Score': 'ML Hotspot Risk Score',
 'Poverty_Incidence_pct': 'Poverty Incidence (%)',
 'Illiteracy_Rate_pct': 'Illiteracy (%)',
 'Uninsurance_Rate_pct': 'Uninsurance (%)',
 'Doctors_per10k': 'Doctors / 10,000',
 'Nurses_per10k': 'Nurses / 10,000',
}

# Prepare per-district data for interactivity
districts_data = df.to_dict(orient='records')
regions = sorted(df['REGION'].unique().tolist())

# KPIs
kpi = {
 'n_districts': len(df),
 'n_regions': df['REGION'].nunique(),
 'mean_hiv': round(df['HIV_Prev_Total_pct'].mean(), 2),
 'mean_tb': round(df['TB_Incidence_per100k'].mean(), 1),
 'mean_coin': round(df['TB_HIV_CoInfection_pct'].mean(), 1),
 'n_hotspots_lisa': int((df['LISA_cluster'] == 'High-High').sum()),
 'n_hotspots_bv': int((df['BvLISA_cluster'] == 'High-High').sum()),
 'n_ml_hotspots': int((df['Ensemble_Risk_Score'] > 0.5).sum()),
 'best_ml_auc': 0.998,
 'morans_I': 0.468,
 'bv_morans': 0.521,
 'gwr_r2': 0.916,
}

# SHAP importance
shap_imp = pd.read_csv(OUT / 'tables' / 'shap_feature_importance.csv').head(10)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>HIV-TB Ghana Interactive Dashboard · 260 Districts</title>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>
body {{ font-family: 'Segoe UI', system-ui, sans-serif; margin: 0; background: #f7fafc; color: #1a202c; }}
.header {{ background: linear-gradient(135deg, #1a202c 0%, #2a4365 100%);
 color: white; padding: 25px 35px; }}
.header h1 {{ font-size: 26pt; margin: 0; font-weight: 700; }}
.header p {{ margin: 6px 0 0; color: #cbd5e0; font-size: 13pt; font-style: italic; }}
.container {{ max-width: 1600px; margin: 0 auto; padding: 25px; }}
.kpi-row {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 15px; margin-bottom: 25px; }}
.kpi {{ background: white; padding: 18px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08);
 border-left: 5px solid #c41e3a; }}
.kpi .num {{ font-size: 26pt; font-weight: 700; color: #c41e3a; line-height: 1; }}
.kpi .lbl {{ font-size: 10pt; color: #4a5568; margin-top: 6px; }}
.controls {{ background: white; padding: 18px 22px; border-radius: 8px; margin-bottom: 20px;
 box-shadow: 0 1px 3px rgba(0,0,0,0.08); display: flex; gap: 20px; align-items: center;
 flex-wrap: wrap; }}
.controls label {{ font-weight: 600; color: #2d3748; font-size: 11pt; }}
.controls select {{ padding: 8px 12px; border: 1px solid #cbd5e0; border-radius: 5px;
 font-size: 11pt; background: white; }}
.grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }}
.full {{ grid-column: 1 / -1; }}
.card {{ background: white; padding: 20px; border-radius: 8px;
 box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
.card h3 {{ margin: 0 0 12px; color: #1a202c; font-size: 15pt; border-bottom: 2pt solid #c41e3a;
 padding-bottom: 6px; }}
.card p {{ font-size: 10pt; color: #4a5568; margin: 6px 0 0; font-style: italic; }}
.table-wrap {{ max-height: 360px; overflow-y: auto; }}
table {{ width: 100%; border-collapse: collapse; font-size: 10pt; }}
th {{ background: #2a4365; color: white; padding: 8px; text-align: left; position: sticky; top: 0; }}
td {{ padding: 7px 8px; border-bottom: 1px solid #edf2f7; }}
tr:nth-child(even) td {{ background: #f7fafc; }}
tr:hover td {{ background: #fffaf0; }}
footer {{ text-align: center; padding: 25px; color: #4a5568; font-size: 10pt; }}
.footer-link {{ color: #c41e3a; text-decoration: none; }}
</style>
</head>
<body>

<div class="header">
 <h1>HIV-TB Co-infection Spatial &amp; Machine Learning Dashboard — Ghana 260 Districts</h1>
 <p>Valentine Golden Ghanem · Biomedical Scientist · Ghana COCOBOD Cocoa Clinic · April 2026</p>
</div>

<div class="container">

 <div class="kpi-row">
 <div class="kpi"><div class="num">{kpi['n_districts']}</div><div class="lbl">Districts analysed</div></div>
 <div class="kpi"><div class="num">{kpi['mean_coin']}%</div><div class="lbl">Mean TB-HIV co-infection</div></div>
 <div class="kpi"><div class="num">{kpi['n_hotspots_lisa']}</div><div class="lbl">LISA high-high clusters</div></div>
 <div class="kpi"><div class="num">{kpi['n_hotspots_bv']}</div><div class="lbl">Bivariate HIV×TB hotspots</div></div>
 <div class="kpi"><div class="num">{kpi['best_ml_auc']}</div><div class="lbl">Best ML CV AUC (LightGBM)</div></div>
 <div class="kpi"><div class="num">{kpi['bv_morans']}</div><div class="lbl">Bivariate Moran's I</div></div>
 </div>

 <div class="controls">
 <label>Variable:
 <select id="varSelect">
 {''.join(f'<option value="{k}">{v}</option>' for k, v in map_vars.items())}
 </select>
 </label>
 <label>Region filter:
 <select id="regionSelect">
 <option value="all">All regions</option>
 {''.join(f'<option value="{r}">{r}</option>' for r in regions)}
 </select>
 </label>
 <label>Top-N districts:
 <select id="topN">
 <option value="10">Top 10</option>
 <option value="20" selected>Top 20</option>
 <option value="30">Top 30</option>
 </select>
 </label>
 </div>

 <div class="grid">
 <div class="card">
 <h3>A. District Choropleth</h3>
 <div id="map" style="height: 600px;"></div>
 <p>Interactive district map. Hover for values; change variable and region filter above.</p>
 </div>
 <div class="card">
 <h3>B. LISA Cluster Map — TB-HIV Co-infection</h3>
 <div id="lisamap" style="height: 600px;"></div>
 <p>High-High = hotspot; Low-Low = cold-spot; High-Low/Low-High = spatial outliers.</p>
 </div>
 </div>

 <div class="grid">
 <div class="card">
 <h3>C. Top-N High-Risk Districts</h3>
 <div id="topbar" style="height: 480px;"></div>
 <p>Ranked by selected variable (or ML ensemble risk score).</p>
 </div>
 <div class="card">
 <h3>D. SHAP Feature Importance (Top 10)</h3>
 <div id="shap" style="height: 480px;"></div>
 <p>Mean |SHAP value| from LightGBM model — strength of each predictor.</p>
 </div>
 </div>

 <div class="grid">
 <div class="card">
 <h3>E. Bivariate LISA Clusters (HIV × TB)</h3>
 <div id="bvlisa" style="height: 520px;"></div>
 <p>Bivariate Moran's I = {kpi['bv_morans']}, p&lt;0.001. 44 high-high districts.</p>
 </div>
 <div class="card">
 <h3>F. Ensemble ML Risk Score</h3>
 <div id="riskmap" style="height: 520px;"></div>
 <p>Average of Random Forest, XGBoost, LightGBM, and Stacked Ensemble probabilities.</p>
 </div>
 </div>

 <div class="card full">
 <h3>G. District-level Data Browser</h3>
 <div class="table-wrap">
 <table id="dataTable">
 <thead>
 <tr>
 <th>District</th><th>Region</th><th>HIV %</th><th>TB /100k</th>
 <th>Co-inf %</th><th>ART %</th><th>VCT %</th><th>Poverty %</th>
 <th>Ensemble Risk</th><th>LISA</th>
 </tr>
 </thead>
 <tbody id="tbody"></tbody>
 </table>
 </div>
 </div>

</div>

<footer>
 <p>© 2026 Valentine Golden Ghanem · Released under MIT licence · Research System v5.0 ·
 <a class="footer-link" href="#">github.com/vghanem/hiv-tb-ghana-260-districts</a></p>
 <p>Global Moran's I (co-infection) = {kpi['morans_I']} · GWR R² = {kpi['gwr_r2']} ·
 Best ML CV AUC = {kpi['best_ml_auc']}</p>
</footer>

<script>
const GEOJSON = {json.dumps(geojson)};
const DATA = {json.dumps(districts_data, default=str)};
const MAP_VARS = {json.dumps(map_vars)};
const SHAP_IMP = {json.dumps(shap_imp.to_dict(orient='records'))};

const LABEL_MAP = {{
 'HIV_Prev_Total_pct': 'HIV Prevalence',
 'HIV_Prev_Men_pct': 'HIV Prevalence (Men)',
 'VCT_Uptake_pct': 'VCT Uptake',
 'Poverty_Incidence_pct': 'Poverty Incidence',
 'TB_Incidence_per100k': 'TB Incidence',
 'Illiteracy_Rate_pct': 'Illiteracy Rate',
 'Accepting_Attitudes_pct': 'Accepting Attitudes',
 'Uninsurance_Rate_pct': 'Uninsurance Rate',
 'Unemployment_Rate_pct': 'Unemployment Rate',
 'ART_Coverage_pct': 'ART Coverage'
}};

function choropleth(elId, valueKey, title, cmap='YlOrRd') {{
 const locations = DATA.map(d => d.DISTRICT);
 const values = DATA.map(d => d[valueKey]);
 const hover = DATA.map(d =>
 `<b>${{d.DISTRICT}}</b><br>Region: ${{d.REGION}}<br>` +
 `HIV: ${{d.HIV_Prev_Total_pct?.toFixed(2)}}%<br>` +
 `TB: ${{d.TB_Incidence_per100k?.toFixed(1)}}/100k<br>` +
 `Co-inf: ${{d.TB_HIV_CoInfection_pct?.toFixed(1)}}%<br>` +
 `Risk: ${{d.Ensemble_Risk_Score?.toFixed(2)}}`);
 const trace = {{
 type: 'choropleth', geojson: GEOJSON, locations: locations,
 z: values, featureidkey: 'properties.DISTRICT',
 colorscale: cmap, hovertemplate: '%{{text}}<extra></extra>', text: hover,
 colorbar: {{ title: title, thickness: 14 }},
 marker: {{ line: {{ width: 0.4, color: 'white' }} }}
 }};
 const layout = {{
 geo: {{ fitbounds: 'locations', visible: false, projection: {{ type: 'mercator' }} }},
 margin: {{ l: 0, r: 0, t: 10, b: 0 }}, height: 580
 }};
 Plotly.newPlot(elId, [trace], layout, {{ responsive: true, displayModeBar: false }});
}}

function lisaMap(elId, clusterKey, title) {{
 const cmap = {{
 'High-High': '#d7191c', 'Low-Low': '#2c7bb6',
 'High-Low': '#fdae61', 'Low-High': '#abd9e9', 'Not Significant': '#f0f0f0'
 }};
 const traces = [];
 for (const cl of ['High-High', 'Low-Low', 'High-Low', 'Low-High', 'Not Significant']) {{
 const locs = DATA.filter(d => d[clusterKey] === cl).map(d => d.DISTRICT);
 if (locs.length === 0) continue;
 traces.push({{
 type: 'choropleth', geojson: GEOJSON, locations: locs,
 z: locs.map(() => 1), featureidkey: 'properties.DISTRICT',
 colorscale: [[0, cmap[cl]], [1, cmap[cl]]], showscale: false,
 name: `${{cl}} (n=${{locs.length}})`, showlegend: true,
 hovertemplate: '<b>%{{location}}</b><br>' + cl + '<extra></extra>',
 marker: {{ line: {{ width: 0.4, color: 'white' }} }}
 }});
 }}
 const layout = {{
 geo: {{ fitbounds: 'locations', visible: false, projection: {{ type: 'mercator' }} }},
 margin: {{ l: 0, r: 120, t: 10, b: 0 }}, height: 500,
 legend: {{ x: 1.02, y: 0.5, font: {{ size: 10 }} }}
 }};
 Plotly.newPlot(elId, traces, layout, {{ responsive: true, displayModeBar: false }});
}}

function topBar() {{
 const v = document.getElementById('varSelect').value;
 const r = document.getElementById('regionSelect').value;
 const n = parseInt(document.getElementById('topN').value);
 let filt = DATA;
 if (r !== 'all') filt = DATA.filter(d => d.REGION === r);
 filt = filt.slice().sort((a, b) => (b[v] ?? 0) - (a[v] ?? 0)).slice(0, n);
 const trace = {{
 type: 'bar', orientation: 'h',
 x: filt.map(d => d[v]).reverse(),
 y: filt.map(d => `${{d.DISTRICT}} (${{d.REGION}})`).reverse(),
 marker: {{ color: filt.map(d => d[v]).reverse(), colorscale: 'Reds' }}
 }};
 Plotly.newPlot('topbar', [trace], {{
 margin: {{ l: 240, r: 30, t: 20, b: 40 }},
 xaxis: {{ title: MAP_VARS[v] }}, height: 460
 }}, {{ responsive: true, displayModeBar: false }});
}}

function shapBar() {{
 const features = SHAP_IMP.map(d => LABEL_MAP[d.Feature] || d.Feature).reverse();
 const vals = SHAP_IMP.map(d => d.Mean_abs_SHAP).reverse();
 const trace = {{
 type: 'bar', orientation: 'h', x: vals, y: features,
 marker: {{ color: vals, colorscale: 'Blues' }},
 text: vals.map(v => v.toFixed(2)), textposition: 'outside'
 }};
 Plotly.newPlot('shap', [trace], {{
 margin: {{ l: 200, r: 50, t: 20, b: 40 }},
 xaxis: {{ title: 'Mean |SHAP value|' }}, height: 460
 }}, {{ responsive: true, displayModeBar: false }});
}}

function renderTable() {{
 const r = document.getElementById('regionSelect').value;
 let filt = DATA;
 if (r !== 'all') filt = DATA.filter(d => d.REGION === r);
 filt = filt.slice().sort((a, b) => (b.Ensemble_Risk_Score ?? 0) - (a.Ensemble_Risk_Score ?? 0));
 const tbody = document.getElementById('tbody');
 tbody.innerHTML = '';
 for (const d of filt) {{
 const row = document.createElement('tr');
 row.innerHTML = `
 <td>${{d.DISTRICT || ''}}</td>
 <td>${{d.REGION || ''}}</td>
 <td>${{(d.HIV_Prev_Total_pct ?? 0).toFixed(2)}}</td>
 <td>${{(d.TB_Incidence_per100k ?? 0).toFixed(1)}}</td>
 <td>${{(d.TB_HIV_CoInfection_pct ?? 0).toFixed(1)}}</td>
 <td>${{(d.ART_Coverage_pct ?? 0).toFixed(1)}}</td>
 <td>${{(d.VCT_Uptake_pct ?? 0).toFixed(1)}}</td>
 <td>${{(d.Poverty_Incidence_pct ?? 0).toFixed(1)}}</td>
 <td>${{(d.Ensemble_Risk_Score ?? 0).toFixed(3)}}</td>
 <td>${{d.LISA_cluster || ''}}</td>`;
 tbody.appendChild(row);
 }}
}}

function refresh() {{
 const v = document.getElementById('varSelect').value;
 choropleth('map', v, MAP_VARS[v]);
 topBar();
 renderTable();
}}

document.getElementById('varSelect').addEventListener('change', refresh);
document.getElementById('regionSelect').addEventListener('change', refresh);
document.getElementById('topN').addEventListener('change', topBar);

// Initial render
choropleth('map', 'TB_HIV_CoInfection_pct', 'TB-HIV Co-infection (%)', 'Reds');
lisaMap('lisamap', 'LISA_cluster', 'LISA');
lisaMap('bvlisa', 'BvLISA_cluster', 'Bivariate LISA');
choropleth('riskmap', 'Ensemble_Risk_Score', 'Ensemble Risk', 'RdYlGn');
topBar();
shapBar();
renderTable();
</script>

</body>
</html>"""

out = ROOT / 'dashboard' / 'HIV_TB_Ghana_Dashboard.html'
out.write_text(html)
print(f'Dashboard saved: {out}')
print(f'File size: {out.stat().st_size/1024/1024:.1f} MB')
