#!/usr/bin/env python3
"""連載小說章節自檢：數口癖、套話訊號、禁用名稱。

用法：
  python3 check_chapter.py [--config novel-check.json] 章節.md [更多章節.md ...]

只用標準函式庫，不連網。超過硬上限或出現禁用名稱時回傳 1。
訊號詞只是提示，要回到上下文判斷（見 references/self-check.md 第 5 節）。

novel-check.json 可覆寫的欄位（都可省略）：
  {
    "hard":    {"很久": 3},              # 每章次數上限，超過算失敗
    "per_k":   {"弱化副詞": 1.0},         # 每千字上限，超過算失敗
    "soft_per_k": {"像": 2.0},            # 每千字建議值，超過只提醒
    "flip_max": 1,                        # 「不是…是…」每章上限
    "signals_extra": ["停了一下"],         # 加進套話訊號的作者口癖
    "banned": ["參考作品的國名"],           # 一出現就失敗
    "meta_words": ["本章目標", "TODO"]      # 寫作說明漏進正文，一出現就失敗
  }

另外固定檢查：最後一段沒有句末標點（可能寫到一半斷掉）。
"""
import argparse
import json
import re
import sys
from pathlib import Path

DEFAULTS = {
    "hard": {},
    "per_k": {"弱化副詞": 1.0},
    "soft_per_k": {"像": 2.0},
    "flip_max": 1,
    "signals_extra": [],
    "banned": [],
    "meta_words": ["本章目標", "伏筆：", "TODO", "待補", "（注：", "[說明]", "【說明】"],
}
WEAK = ["微微", "淡淡", "緩緩", "輕輕", "默默", "悄然", "隱隱", "一絲", "一抹", "慢慢"]
SIGNALS = [
    "只見", "此時此刻", "映入眼簾", "與此同時", "不由自主", "情不自禁", "話鋒一轉",
    "取而代之", "不禁", "深吸一口氣", "嘴角微揚", "嘴角勾起", "眼中閃過", "瞳孔一縮",
    "心頭一震", "心中暗道", "眉頭微皺", "宛如", "猶如", "彷彿", "這意味著", "終於明白",
    "從這一刻開始", "注定", "殊不知", "他不知道的是", "她不知道的是", "從而", "因而",
    "誠然", "於是乎", "綜上所述",
    "看了很久", "過了很久", "想了很久", "這輩子", "這讓", "這使",
]


def load_config(path):
    cfg = json.loads(json.dumps(DEFAULTS))
    if path:
        user = json.loads(Path(path).read_text(encoding="utf-8"))
        for key, val in user.items():
            if isinstance(val, dict) and isinstance(cfg.get(key), dict):
                cfg[key].update(val)
            else:
                cfg[key] = val
    return cfg


def body_text(raw):
    raw = re.sub(r"^---\n.*?\n---\n", "", raw, flags=re.S)  # front matter
    raw = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", raw)  # 圖片
    return raw


def count(text, name):
    if name == "弱化副詞":
        return sum(text.count(w) for w in WEAK)
    return text.count(name)


def check(path, cfg):
    text = body_text(path.read_text(encoding="utf-8"))
    n = len(re.findall(r"[一-鿿]", text))
    k = max(n / 1000, 0.001)
    ok = True
    print(f"== {path.name}  漢字 {n}")

    flips = len(re.findall(r"不是[^。！？\n]{1,30}?[，,。]\s*(?:而|那)?是", text))
    bad = flips > cfg["flip_max"]
    print(f"  {'✗' if bad else '✓'} 不是…是…: {flips}（上限 {cfg['flip_max']}）")
    ok = ok and not bad

    for name, limit in cfg["hard"].items():
        c = count(text, name)
        bad = c > limit
        print(f"  {'✗' if bad else '✓'} {name}: {c}（上限 {limit}）")
        ok = ok and not bad

    for name, limit in cfg["per_k"].items():
        c = count(text, name)
        bad = c / k > limit
        print(f"  {'✗' if bad else '✓'} {name}: {c}，每千字 {c / k:.1f}（上限 {limit}）")
        ok = ok and not bad

    for name, limit in cfg["soft_per_k"].items():
        c = count(text, name)
        mark = "?" if c / k > limit else "✓"
        print(f"  {mark} {name}: {c}，每千字 {c / k:.1f}（建議 {limit}）")

    words = SIGNALS + list(cfg["signals_extra"])
    hits = [(w, text.count(w)) for w in words if w in text]
    if hits:
        print("  ? 套話訊號（回上下文判斷）：" + "、".join(f"{w}×{c}" for w, c in hits))

    leaks = [w for w in cfg["meta_words"] if w in text]
    if leaks:
        print("  ✗ 寫作說明漏進正文：" + "、".join(leaks))
        ok = False

    paras = [p.strip() for p in text.split("\n") if p.strip() and p.strip() != "---"]
    if paras and not re.search(r"[。！？」』…）\)*_]$", paras[-1]):
        print(f"  ✗ 最後一段沒有收尾標點，可能斷掉：{paras[-1][-20:]}")
        ok = False

    banned = [w for w in cfg["banned"] if w.lower() in text.lower()]
    if banned:
        print("  ✗ 禁用名稱：" + "、".join(banned))
        ok = False
    return ok


def main():
    ap = argparse.ArgumentParser(description="連載小說章節自檢")
    ap.add_argument("--config", help="novel-check.json 路徑")
    ap.add_argument("files", nargs="+", help="章節 Markdown 檔")
    args = ap.parse_args()
    cfg = load_config(args.config)
    results = [check(Path(p), cfg) for p in args.files]
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
