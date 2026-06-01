"""
02_compute_stats.py — 汇总客服工具地图统计

输入: out/widgets.csv
输出: out/analysis_stats.json
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out"


def main():
    rows = list(csv.DictReader((OUT / "widgets.csv").open(encoding="utf-8")))
    total = len(rows)

    vendor_counts = Counter()
    for r in rows:
        for v in (r.get("widgets") or "").split(";"):
            v = v.strip()
            if v:
                vendor_counts[v] += 1

    pct = lambda c, t=total: round(c / t * 100, 1) if t else 0

    ai_count = sum(1 for r in rows if r["ai_signal"] == "1")
    no_widget_n = sum(1 for r in rows if int(r["widget_count"]) == 0)
    no_chat_signal = sum(1 for r in rows if int(r["widget_count"]) == 0 and r["generic_chat_hint"] == "0")
    multi_widget = sum(1 for r in rows if int(r["widget_count"]) >= 2)

    # Gorgias 用户里 AI signal 比例
    gorgias_rows = [r for r in rows if "Gorgias" in (r.get("widgets") or "")]
    gorgias_ai = sum(1 for r in gorgias_rows if r["ai_signal"] == "1")

    # AI signal 的具体公司
    ai_brands_list = [
        {
            "domain": r["domain"],
            "widgets": r["widgets"] or "(static scan未识别到 vendor)",
        }
        for r in rows if r["ai_signal"] == "1"
    ]

    # 多 widget 的 27 家
    multi_brands_list = [
        {"domain": r["domain"], "widgets": r["widgets"]}
        for r in rows if int(r["widget_count"]) >= 2
    ]

    stats = {
        "_meta": {
            "source": "1238 DTC brand pool home.html static scan",
            "effective_rows": total,
            "snapshot_date": "2026-05-12",
            "method": "static HTML widget detection (no JS execution); represents lower bound — actually-loaded widgets via JS not captured",
        },
        "vendor_share": [
            {"vendor": v, "count": c, "pct": pct(c)}
            for v, c in vendor_counts.most_common()
        ],
        "widget_coverage": {
            "any_widget_count": total - no_widget_n,
            "any_widget_pct": pct(total - no_widget_n),
            "single_widget_count": sum(1 for r in rows if int(r["widget_count"]) == 1),
            "multi_widget_count": multi_widget,
            "multi_widget_pct": pct(multi_widget),
            "no_widget_count": no_widget_n,
            "no_widget_pct": pct(no_widget_n),
            "no_chat_signal_at_all": no_chat_signal,
            "no_chat_signal_pct": pct(no_chat_signal),
        },
        "ai_signal": {
            "count": ai_count,
            "pct_of_total": pct(ai_count),
            "gorgias_with_ai_signal_count": gorgias_ai,
            "gorgias_with_ai_signal_pct_within_gorgias": pct(gorgias_ai, len(gorgias_rows)),
            "ai_signal_brand_list_sample": ai_brands_list[:15],
        },
        "multi_widget_examples": multi_brands_list[:20],
        "total_widget_vendors_identified": len(vendor_counts),
    }

    out_path = OUT / "analysis_stats.json"
    out_path.write_text(json.dumps(stats, ensure_ascii=False, indent=2))
    print(f"✅ {out_path}")
    print(f"\nTop 10 vendors:")
    for v in stats["vendor_share"][:10]:
        print(f"  {v['vendor']:<28} {v['count']:>4} ({v['pct']}%)")


if __name__ == "__main__":
    main()
