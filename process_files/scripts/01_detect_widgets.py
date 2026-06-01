"""
01_detect_widgets.py — 扫 1429 个 DTC 首页 HTML,识别客服 / chat widget

输入: dtc_dual_report_2026/raw_pages/{domain}/home.html
输出: out/widgets.csv (domain × widget detection 矩阵)
      out/widget_stats.json

识别规则(20+ vendor):正则匹配 JS src / class / dom marker。
AI 信号:扫主页是否提 "AI chatbot / AI assistant / AI agent / autonomously" 等。
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out"
OUT.mkdir(parents=True, exist_ok=True)

RAW_BASE = Path("../raw_pages")

# ============================================================
# 客服 widget vendor 指纹(基于 2024-2026 公开 JS host / inline marker)
# ============================================================

VENDORS: dict[str, list[re.Pattern]] = {
    "Gorgias":       [re.compile(r"\bgorgias\.(?:io|com|chat)\b", re.I),
                       re.compile(r"gorgias-chat", re.I),
                       re.compile(r"\bgorgiasChat\b", re.I)],
    "Intercom":      [re.compile(r"widget\.intercom\.io", re.I),
                       re.compile(r"\bintercomSettings\b", re.I),
                       re.compile(r"js\.intercomcdn\.com", re.I)],
    "Zendesk":       [re.compile(r"static\.zdassets\.com", re.I),
                       re.compile(r"\bzopim\b", re.I),
                       re.compile(r"zendesk\.com/embeddable", re.I),
                       re.compile(r"\bzE\(.*?webWidget", re.I)],
    "Tidio":         [re.compile(r"\btidio\.com\b", re.I),
                       re.compile(r"\btidio\.co\b", re.I),
                       re.compile(r"\btidiochat\b", re.I),
                       re.compile(r"code\.tidio\.co", re.I)],
    "Crisp":         [re.compile(r"\bcrisp\.chat\b", re.I),
                       re.compile(r"\bcrisp\.im\b", re.I),
                       re.compile(r"\$crisp\b", re.I),
                       re.compile(r"client\.crisp\.chat", re.I)],
    "Drift":         [re.compile(r"\bdrift\.com\b", re.I),
                       re.compile(r"js\.driftt\.com", re.I),
                       re.compile(r"\bdriftt\.com\b", re.I)],
    "HubSpot Chat":  [re.compile(r"js\.hs-scripts\.com", re.I),
                       re.compile(r"js\.hs-banner\.com", re.I),
                       re.compile(r"\bhubspot.*?conversations", re.I)],
    "Reamaze":       [re.compile(r"cdn\.reamaze\.com", re.I),
                       re.compile(r"\breamaze\b", re.I)],
    "Help Scout":    [re.compile(r"\bhelpscout\.(?:com|net)\b", re.I),
                       re.compile(r"beacon-v2\.helpscout", re.I),
                       re.compile(r"\bBeacon\(['\"]\w+['\"]", re.I)],
    "Tawk.to":       [re.compile(r"\btawk\.to\b", re.I),
                       re.compile(r"embed\.tawk\.to", re.I)],
    "LiveChat":      [re.compile(r"\blivechatinc\.com\b", re.I),
                       re.compile(r"cdn\.livechatinc\.com", re.I)],
    "Olark":         [re.compile(r"\bolark\.com\b", re.I),
                       re.compile(r"static\.olark\.com", re.I)],
    "Freshchat":     [re.compile(r"\bfreshchat\.com\b", re.I),
                       re.compile(r"wchat\.freshchat\.com", re.I),
                       re.compile(r"wchat\.eu\.freshchat", re.I)],
    "JivoChat":      [re.compile(r"\bjivosite\.com\b", re.I),
                       re.compile(r"\bjivochat\b", re.I),
                       re.compile(r"code\.jivosite\.com", re.I)],
    "Smartsupp":     [re.compile(r"\bsmartsupp\.com\b", re.I)],
    "Front":         [re.compile(r"\bfrontapp\.com\b", re.I),
                       re.compile(r"chat-assets\.frontapp", re.I)],
    "Kustomer":      [re.compile(r"\bkustomer\.com\b", re.I),
                       re.compile(r"cdn\.kustomerapp\.com", re.I)],
    "Userlike":      [re.compile(r"\buserlike\.com\b", re.I)],
    "Klaviyo Customer Hub": [re.compile(r"static-forms\.klaviyo\.com.*?support", re.I),
                              re.compile(r"customer-portal\.klaviyo", re.I)],
    "Chatra":        [re.compile(r"\bchatra\.io\b", re.I),
                       re.compile(r"call\.chatra\.io", re.I)],
    "Re:plain":      [re.compile(r"\breplain\.cc\b", re.I)],
    "Pylon":         [re.compile(r"\bpylon\.com\b", re.I),
                       re.compile(r"chat\.pylon\.com", re.I)],
    "Crisp (legacy)": [re.compile(r"\bgo\.crisp\.chat\b", re.I)],
    "Shopify Inbox": [re.compile(r"shopify-chat", re.I),
                       re.compile(r"\bshopify_chat\b", re.I),
                       re.compile(r"shopify\.com/chat", re.I)],
    "Facebook Messenger Plugin": [re.compile(r"messenger-checkbox", re.I),
                                   re.compile(r"customerchat", re.I),
                                   re.compile(r"messenger\.com.*?embed", re.I)],
    "WhatsApp Button": [re.compile(r"wa\.me/\d", re.I),
                         re.compile(r"api\.whatsapp\.com/send", re.I)],
}

# AI 信号(主页提及)
AI_SIGNAL_RE = re.compile(
    r"\b(?:AI\s+(?:chatbot|assistant|agent|support|chat)|"
    r"chatbot\s+(?:powered\s+by\s+AI|with\s+AI)|"
    r"GPT[-\s]?powered|"
    r"powered\s+by\s+(?:ChatGPT|OpenAI|Anthropic|Claude|GPT-4)|"
    r"AI[-\s]?powered\s+(?:chat|support|customer\s+service)|"
    r"intelligent\s+(?:agent|chatbot|assistant)|"
    r"24/7\s+AI|"
    r"Gorgias\s+(?:Automate|AI\s+Agent)|"
    r"Intercom\s+Fin|"
    r"Zendesk\s+(?:AI|Advanced\s+AI)|"
    r"\bFin\s+(?:AI|by\s+Intercom)\b)\b",
    re.I,
)

# 全无 chat 信号(供「沉默」分桶)
GENERIC_CHAT_HINT = re.compile(r"\b(?:chat\s+with\s+us|live\s+chat|contact\s+us|help\s+center|support)\b", re.I)


def detect_widgets(html: str) -> tuple[list[str], bool, bool]:
    """返回 (命中 vendor 列表, ai_signal, generic_chat_hint)"""
    hits: list[str] = []
    for vendor, patterns in VENDORS.items():
        for p in patterns:
            if p.search(html):
                hits.append(vendor)
                break
    ai = bool(AI_SIGNAL_RE.search(html))
    generic = bool(GENERIC_CHAT_HINT.search(html))
    return hits, ai, generic


def main():
    if not RAW_BASE.exists():
        print(f"❌ 找不到 raw_pages: {RAW_BASE}", file=sys.stderr)
        sys.exit(1)
    domains = sorted([d for d in RAW_BASE.iterdir() if d.is_dir()])
    print(f"扫 {len(domains)} 个域名...")

    rows: list[dict] = []
    vendor_counts: Counter = Counter()
    coverage: Counter = Counter()  # widget_count_bucket
    ai_count = 0
    none_chat_count = 0
    generic_hint_count = 0

    for i, dom_dir in enumerate(domains, 1):
        home = dom_dir / "home.html"
        if not home.exists() or home.stat().st_size == 0:
            continue
        try:
            html = home.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if len(html) < 1000:
            continue

        hits, ai, generic = detect_widgets(html)
        for v in hits:
            vendor_counts[v] += 1
        if ai:
            ai_count += 1
        if not hits and not generic:
            none_chat_count += 1
        elif not hits and generic:
            generic_hint_count += 1

        n = len(hits)
        bucket = "none" if n == 0 else ("1" if n == 1 else "2" if n == 2 else "3+")
        coverage[bucket] += 1

        rows.append({
            "domain": dom_dir.name,
            "html_size": home.stat().st_size,
            "widget_count": n,
            "widgets": ";".join(hits),
            "ai_signal": int(ai),
            "generic_chat_hint": int(generic),
        })
        if i % 200 == 0 or i == len(domains):
            print(f"  [{i}/{len(domains)}]")

    # 写 CSV
    csv_path = OUT / "widgets.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as fp:
        w = csv.DictWriter(fp, fieldnames=list(rows[0].keys()))
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"\n✅ {csv_path} ({len(rows)} 行)")

    # 写 stats JSON
    total = len(rows)
    stats = {
        "_meta": {
            "source": "DTC brand pool home.html scan (1238 effective sample)",
            "raw_input_total": len(domains),
            "effective_rows": total,
            "snapshot_date": "2026-05-12",
        },
        "vendor_share": {
            v: {"count": c, "pct": round(c / total * 100, 1)}
            for v, c in vendor_counts.most_common()
        },
        "widget_coverage": {
            k: {"count": v, "pct": round(v / total * 100, 1)}
            for k, v in coverage.items()
        },
        "ai_signal": {
            "count": ai_count,
            "pct_of_total": round(ai_count / total * 100, 1),
        },
        "no_chat_widget_at_all": {
            "count": none_chat_count,
            "pct": round(none_chat_count / total * 100, 1),
        },
        "generic_chat_hint_but_no_vendor": {
            "count": generic_hint_count,
            "pct": round(generic_hint_count / total * 100, 1),
            "note": "可能用了 native chat / 自建 / 我们没识别到的 vendor",
        },
    }
    (OUT / "widget_stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2))

    # Console
    print(f"\n=== Vendor share (Top 15) ===")
    for v, d in list(stats["vendor_share"].items())[:15]:
        print(f"  {v:<28} {d['count']:>4} ({d['pct']:>5.1f}%)")
    print(f"\n=== Widget coverage ===")
    for k, d in stats["widget_coverage"].items():
        print(f"  {k:<6} {d['count']:>4} ({d['pct']:>5.1f}%)")
    print(f"\n=== AI signal: {ai_count} ({stats['ai_signal']['pct_of_total']}%) ===")
    print(f"=== No chat widget at all: {none_chat_count} ({stats['no_chat_widget_at_all']['pct']}%) ===")


if __name__ == "__main__":
    main()
