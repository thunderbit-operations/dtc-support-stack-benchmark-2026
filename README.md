# DTC Support Stack Benchmark 2026

Source materials for Thunderbit Research's DTC customer-support tooling report:

**Report:** [DTC Support Runs on Commerce, Not SaaS](https://thunderbit.com/blog/dtc-support-run-commerce)

## Summary

This repository contains the public data outputs, scripts, report drafts, and visual assets behind a May 2026 static scan of visible customer-support widgets and vendor fingerprints on DTC brand home pages.

Headline sample:

- 1,148 DTC brand home pages in the effective static scan.
- Snapshot date: 2026-05-12 UTC.
- 397 home pages exposed at least one support widget in static HTML.
- Gorgias appeared on 267 scanned home pages, or 23.3% of the sample, with sample-echo caveats.
- Zendesk appeared on 49 home pages, or 4.3%.
- Intercom appeared on only 7 home pages, or 0.6%.
- 13 brands, or 1.1%, publicly surfaced AI customer-support language on the home page.

## Repository Contents

| Path | Description |
|---|---|
| `process_files/out/` | Parsed widget CSV, aggregate JSON, and final report check. |
| `process_files/scripts/` | Reproducible scripts for widget detection, stats, figures, report build, and final checks. |
| `process_files/_shared/dtc_brand_pool_source/out/` | DTC brand pool and shared website-detection outputs used by the support report. |
| `figures/` | Original chart outputs from the local report pipeline. |
| `article_assets/` | Web images used in the published Thunderbit article. |
| `reports/` | Published article Markdown plus earlier English, Chinese, and HTML report drafts. |
| `social_assets/` | LinkedIn editorial explainer image for the support-stack post. |
| `source_package/` | Original public process-files ZIP package uploaded with the article. |

## Key Files

- `process_files/out/widgets.csv`: one row per scanned home page, with detected support-widget and AI-chat signals.
- `process_files/out/analysis_stats.json`: aggregate metrics used in the report.
- `process_files/out/widget_stats.json`: detailed widget coverage and vendor summary.
- `process_files/scripts/01_detect_widgets.py`: rule-based visible-widget detector.
- `process_files/scripts/02_compute_stats.py`: aggregate statistics builder.
- `process_files/scripts/03_make_figs.py`: chart generation script.

## Reproduce

The parsed outputs are included, so core stats and figures can be regenerated from the public CSV/JSON files.

```bash
python3 -m pip install -r requirements.txt
cd process_files
python3 scripts/02_compute_stats.py
python3 scripts/03_make_figs.py
python3 scripts/04_build_report_bilingual.py
python3 scripts/05_module_i_check.py
```

`01_detect_widgets.py` documents the original static detection flow. Raw HTML home-page caches are not included in this repository; the published source package focuses on structured outputs, scripts, figures, and report materials.

## Method Notes

This report uses public home-page HTML signals from a DTC-heavy brand pool. The detector is intentionally transparent and rule-based.

Important caveats:

- Static HTML parsing can miss widgets injected only after JavaScript execution.
- Vendor detection should be read as a visible lower bound, not a full backend install-rate estimate.
- The DTC brand pool is Shopify-ecosystem-leaning, so vendor shares should be interpreted with sample-echo caveats.
- The report measures public storefront signals, not the full support backend.

## Citation

If referencing this work, cite the published article and this repository:

- Article: https://thunderbit.com/blog/dtc-support-run-commerce
- Repository: https://github.com/thunderbit-operations/dtc-support-stack-benchmark-2026
