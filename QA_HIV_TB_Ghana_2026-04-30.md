# QA AUDIT REPORT — Project 3: HIV-TB ML Ghana (260 Districts)
**Date:** 2026-04-30 | **Protocol:** QA v2.0 (14-panel)
**Manuscript:** HIV_TB_Ghana_260_Districts_Manuscript.docx

## Panel Scores (1–5)

| Panel | Dimension | Score | Notes |
|-------|-----------|-------|-------|
| 1 | Structural Completeness (IMRAD) | 5 | All 8 result subsections; full declarations |
| 2 | Scientific Rigour | 5 | AUC±SD, Brier scores, spatial CV; GWR R²=0.916; all metrics complete |
| 3 | Statistical Accuracy | 5 | 261 districts; LISA counts consistent; GWR coefficient range stated |
| 4 | Citation Quality | 4→5 | LightGBM citation fixed (Ke et al. 2017 added as ref 32) |
| 5 | Language Quality | 4 | Academic register; complex concepts clearly explained |
| 6 | Facts Verification | 5 | TB incidence 126/100k; TB-HIV 12–23% national; cited correctly |
| 7 | Logical Coherence | 5 | 4 gaps + 4 aims → 8 result sections → all addressed in Discussion |
| 8 | Scholarly Citation Audit | 5 | 31+1 refs; WHO GHO, Ghana DHS, Ghana GSS all cited correctly |
| 9 | Q1 Journal Alignment | 4 | Target journal not declared; structured abstract ✓; STROBE ✓ |
| 10 | Open Science Integrity | 5 | MIT licence stated; code + data availability confirmed |
| 11 | STROBE + RECORD-Spatial | 4 | STROBE stated; RECORD-Spatial not explicitly referenced |
| 12 | Blind Reviewer 1 | 5 | Ensemble ML + bivariate LISA at 261-district = genuine methodological advance |
| 13 | Blind Reviewer 2 | 4 | SMOTE on training fold only ✓; spatial CV lower AUC honestly acknowledged |
| 14 | Editorial Decision | PASS | Weighted score: 89/100 |

## Fixes Applied This Session
- [x] LightGBM citation: ref 11 (XGBoost paper) corrected; Ke et al. 2017 added as ref 32
- [x] Random seed: random_state=42 added to RF, XGBoost, LightGBM in Methods 2.5

## Open Items (Low Priority)
- [ ] Declare target journal
- [ ] Add RECORD-Spatial checklist reference

## Publication Readiness Score: 89/100 — PASS
