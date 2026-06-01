"""05_module_i_check.py — Module I final check (DTC CX map)"""
from __future__ import annotations
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out"
ZH = ROOT / "dtc_cx_map_2026_zh.md"
EN = ROOT / "dtc_cx_map_2026_en.md"
HTML = ROOT / "dtc_cx_map_2026.html"

FORBIDDEN = ["curl_cffi", "Playwright", "Selenium", "anti-bot", "anti bot", "fingerprint bypass", "绕过反", "反爬"]
ZH_NOTICE = ["样本", "DTC", "数据源回声", "不能解读为", "不代表"]
EN_NOTICE = ["sample", "DTC", "sample echo", "cannot be read", "not"]


def count_cjk(t): return sum(1 for c in t if "一" <= c <= "鿿")


def main():
    zh = ZH.read_text() if ZH.exists() else ""
    en = EN.read_text() if EN.exists() else ""
    html = HTML.read_text() if HTML.exists() else ""
    rows = []
    hits = [t for t in FORBIDDEN if t.lower() in (zh+en+html).lower()]
    rows.append(("1. 法律红线(无抓取技术名词)", not hits, f"hits:{hits}" if hits else "OK"))
    neg = re.compile(r"\b(?:awful|terrible|worst|backward)\b|\b(?:落后|垫底|垃圾)\b", re.I).findall(zh+" "+en)
    rows.append(("2. 法律红线(无负面 brand 描述)", not neg, f"hits:{neg[:3]}" if neg else "OK"))
    # 300 字符以上的连续引号(避免误判嵌套了短术语 quote 的正常段落)
    cands = re.findall(r'"[^"\n]{300,}"', zh+" "+en)
    lq = [q for q in cands if q.strip('"').count('"')<2 and q.strip('"').count(',')<5]
    rows.append(("3. 无外部 >300 字符 paste", not lq, f"{len(lq)}"))
    zn = sum(1 for t in ZH_NOTICE if t in zh)
    rows.append(("4. 样本声明 zh ≥3/5", zn>=3, f"{zn}/5"))
    en_n = sum(1 for t in EN_NOTICE if t.lower() in en.lower())
    rows.append(("5. 样本声明 en ≥3/5", en_n>=3, f"{en_n}/5"))
    mz = zh.split("Methodology")[-1] if "Methodology" in zh else ""
    me = en.split("Methodology")[-1] if "Methodology" in en else ""
    bz = len(re.findall(r"^\s*-\s+", mz, re.M)) + len(re.findall(r"\*\*[^*]{2,80}\*\*[::]", mz)) + len(re.findall(r"^\*\*[^*]{2,80}\*\*", mz, re.M))
    be = len(re.findall(r"^\s*-\s+", me, re.M)) + len(re.findall(r"\*\*[^*]{2,80}\*\*[::]", me)) + len(re.findall(r"^\*\*[^*]{2,80}\*\*", me, re.M))
    rows.append(("6. Caveats ≥5 zh", bz>=5, f"{bz}"))
    rows.append(("6b. Caveats ≥5 en", be>=5, f"{be}"))
    dh = len(re.findall(r"20\d{2}-\d{2}-\d{2}|20\d{2}-05", zh+en+html))
    rows.append(("7. 日期 stamp ≥2", dh>=2, f"{dh}"))
    rows.append(("8. 三件套齐全", ZH.exists() and EN.exists() and HTML.exists(), ""))
    zc = count_cjk(zh)
    ew = len(en.split())
    rows.append(("9. 中文 ≥4000", zc>=4000, f"{zc}"))
    rows.append(("9b. 英文 ≥3500", ew>=3500, f"{ew}"))
    rd = re.findall(r"\.csv|download.*\.json", zh+en+html, re.I)
    rows.append(("10. 无 raw 下载链", len(rd)<=2, f"{len(rd)}"))
    iz = len(re.findall(r"!\[.*?\]\(figs/.*?\.png\)", zh))
    ie = len(re.findall(r"!\[.*?\]\(figs/.*?\.png\)", en))
    rows.append(("11. 图表引用 ≥4", iz>=4 and ie>=4, f"zh:{iz} en:{ie}"))
    rows.append(("12. HTML lang toggle", "lang-zh" in html and "setLang" in html, ""))

    print(f"\n{'='*60}")
    print(f"DTC CX Tooling Map 2026 — Module I Final Check")
    print(f"{'='*60}\n")
    p = 0
    for n, ok, note in rows:
        flag = "✅ PASS" if ok else "❌ FAIL"
        if ok: p += 1
        print(f"{flag}  {n:<45} {note}")
    print(f"\n汇总: {p} / {len(rows)} PASS")

    md = [f"# Module I Final Check — DTC CX Tooling Map 2026", "",
          f"- 中文: {zc}, 英文: {ew}, 图表 zh:{iz}/en:{ie}", "", "## Items", ""]
    for n, ok, note in rows:
        md.append(f"- **{'PASS' if ok else 'FAIL'}** — {n}: {note}")
    md.append(f"\n## 汇总: {p} / {len(rows)} PASS")
    (OUT / "module_i_final_check.md").write_text("\n".join(md))
    if p != len(rows):
        sys.exit(1)


if __name__ == "__main__":
    main()
