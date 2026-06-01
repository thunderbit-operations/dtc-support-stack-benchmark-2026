"""
03_make_figs.py — DTC 客服工具地图图表
"""

from __future__ import annotations
import json
import sys
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib import rcParams

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out"
FIGS = ROOT / "figs"
FIGS.mkdir(parents=True, exist_ok=True)

PRIMARY = "#FF6B35"
ACCENT = "#3A6BD8"
GREEN = "#5E8F4E"
DARK = "#1F2937"
MUTED = "#9CA3AF"

rcParams["font.family"] = ["PingFang SC", "Helvetica Neue", "Arial", "sans-serif"]
rcParams["axes.spines.top"] = False
rcParams["axes.spines.right"] = False
rcParams["figure.dpi"] = 130
rcParams["axes.titleweight"] = "bold"
rcParams["axes.titlesize"] = 13


def load(): return json.loads((OUT / "analysis_stats.json").read_text())


def fig_vendor_share(stats):
    """Top 10 vendor share, with Gorgias 单独标"""
    top = stats["vendor_share"][:10]
    vendors = [v["vendor"] for v in top][::-1]
    pcts = [v["pct"] for v in top][::-1]
    colors = [PRIMARY if v == "Gorgias" else ACCENT for v in vendors]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.barh(vendors, pcts, color=colors, edgecolor="white")
    for bar, p, item in zip(bars, pcts, top[::-1]):
        ax.text(p + 0.4, bar.get_y() + bar.get_height() / 2,
                f"{p}% ({item['count']})", va="center", fontsize=10, color=DARK)
    ax.set_xlabel("Share of 1148 DTC brands (%)", fontsize=10)
    ax.set_title("Customer-support widget vendors detected on DTC home pages\n"
                 "(static scan — represents a lower bound, see methodology)",
                 loc="left", pad=12)
    ax.set_xlim(0, max(pcts) + 7)
    fig.tight_layout()
    fig.savefig(FIGS / "vendor_share.png", bbox_inches="tight")
    plt.close(fig)
    print("  ✅ vendor_share.png")


def fig_coverage_donut(stats):
    cov = stats["widget_coverage"]
    labels = ["≥1 widget", "Static scan missed / no widget"]
    vals = [cov["any_widget_count"], cov["no_widget_count"]]
    colors = [PRIMARY, "#E5E7EB"]

    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, _ = ax.pie(vals, colors=colors, startangle=90,
                       wedgeprops={"edgecolor": "white", "linewidth": 3, "width": 0.4})
    ax.text(0, 0.08, f"{cov['any_widget_pct']}%", ha="center", va="center",
            fontsize=34, fontweight="bold", color=DARK)
    ax.text(0, -0.11, f"of {sum(vals)} DTC brands\nshow a chat widget", ha="center", va="center",
            fontsize=10, color="#6B7280")
    ax.set_title("Detected chat-widget coverage on DTC home pages",
                 loc="center", pad=15)
    fig.tight_layout()
    fig.savefig(FIGS / "coverage_donut.png", bbox_inches="tight")
    plt.close(fig)
    print("  ✅ coverage_donut.png")


def fig_ai_contrast(stats):
    """AI 反差:DTC 客服 1.1% vs AI Required 招聘 35.6%"""
    ai_pct = stats["ai_signal"]["pct_of_total"]
    # AI Required Position Rate 报告 2026-05 数字
    ai_jd_pct = 35.6
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(
        ["AI mention in HN hiring JDs\n(AI Required report, 2026-05)",
         "AI signal on DTC home pages\n(this report, 2026-05)"],
        [ai_jd_pct, ai_pct], color=[ACCENT, PRIMARY],
        edgecolor="white", width=0.55,
    )
    for bar, v in zip(bars, [ai_jd_pct, ai_pct]):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 1, f"{v}%",
                ha="center", va="bottom", fontsize=13, fontweight="bold", color=DARK)
    ax.set_ylabel("Share (%)", fontsize=11)
    ax.set_ylim(0, max(ai_jd_pct, ai_pct) + 8)
    ax.set_title("\"AI tools\" in hiring text vs AI-chat on DTC home pages\n"
                 "(HN hiring is talk; DTC sites are what shipped)",
                 loc="left", pad=12)
    fig.tight_layout()
    fig.savefig(FIGS / "ai_jd_vs_home_contrast.png", bbox_inches="tight")
    plt.close(fig)
    print("  ✅ ai_jd_vs_home_contrast.png")


def fig_long_tail(stats):
    """Long tail:Top 1 vs Top 2-10 vs 11+"""
    vendors = stats["vendor_share"]
    top1 = vendors[0]["pct"] if vendors else 0
    top_2_10 = sum(v["pct"] for v in vendors[1:10])
    tail = sum(v["pct"] for v in vendors[10:])
    fig, ax = plt.subplots(figsize=(7, 5))
    labels = [f"#1 (Gorgias)", "Top 2-10", "Long tail (#11+)"]
    vals = [top1, top_2_10, tail]
    colors = [PRIMARY, ACCENT, MUTED]
    bars = ax.bar(labels, vals, color=colors, edgecolor="white")
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 0.4, f"{v:.1f}%",
                ha="center", va="bottom", fontsize=11, fontweight="bold", color=DARK)
    ax.set_ylabel("Share of DTC brands (%)", fontsize=10)
    ax.set_title("Market concentration: #1 Gorgias vs rest\n"
                 "(note: Gorgias appears inflated due to sample echo, see §Methodology)",
                 loc="left", pad=12)
    ax.set_ylim(0, max(vals) + 5)
    fig.tight_layout()
    fig.savefig(FIGS / "concentration.png", bbox_inches="tight")
    plt.close(fig)
    print("  ✅ concentration.png")


def fig_ai_brand_table(stats):
    ai_list = stats["ai_signal"]["ai_signal_brand_list_sample"]
    if not ai_list:
        return
    fig, ax = plt.subplots(figsize=(8, max(3.5, 0.36 * len(ai_list) + 1.5)))
    ax.axis("off")
    rows = [[b["domain"], b["widgets"]] for b in ai_list]
    table = ax.table(cellText=rows,
                     colLabels=["Brand domain", "Detected chat widget(s)"],
                     cellLoc="left", colLoc="left", loc="center",
                     colWidths=[0.42, 0.58])
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.4)
    for ci in range(2):
        cell = table[0, ci]
        cell.set_facecolor(PRIMARY)
        cell.set_text_props(color="white", fontweight="bold")
    for ri in range(1, len(rows) + 1):
        for ci in range(2):
            cell = table[ri, ci]
            cell.set_facecolor("#FAFBFD" if ri % 2 else "#FFFFFF")
            cell.set_edgecolor("#E5E7EB")
    ax.set_title(f"DTC brands that publicly signal an AI-powered customer chat ({stats['ai_signal']['count']} brands, 2026-05)",
                 loc="left", pad=10, fontsize=12, fontweight="bold")
    fig.tight_layout()
    fig.savefig(FIGS / "ai_brand_list.png", bbox_inches="tight")
    plt.close(fig)
    print("  ✅ ai_brand_list.png")


def main():
    stats = load()
    fig_vendor_share(stats)
    fig_coverage_donut(stats)
    fig_ai_contrast(stats)
    fig_long_tail(stats)
    fig_ai_brand_table(stats)
    print(f"\n→ {FIGS}/")


if __name__ == "__main__":
    main()
