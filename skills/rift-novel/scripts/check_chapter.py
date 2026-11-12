#!/usr/bin/env python3
"""《裂谷鐘聲》章節自檢：數口癖、套話訊號、FEZ 名稱。

用法：python3 check_chapter.py <章節.md> [更多章節.md ...]
只用標準函式庫，不連網。超過硬上限時回傳 1。
訊號詞只是提示，要回到上下文判斷（見 references/self-check.md 第 5 節）。
"""
import re
import sys
from pathlib import Path

# 硬上限：超過就要改
HARD = {
    "不是…是…": 3,
    "很久": 3,
}
# 每千字上限
PER_K = {
    "像": 2.0,
    "弱化副詞": 1.0,
}
WEAK = ["微微", "淡淡", "緩緩", "輕輕", "默默", "悄然", "隱隱", "一絲", "一抹", "慢慢"]
SIGNALS = [
    "只見", "此時此刻", "映入眼簾", "與此同時", "不由自主", "情不自禁", "話鋒一轉",
    "取而代之", "不禁", "深吸一口氣", "嘴角微揚", "嘴角勾起", "眼中閃過", "瞳孔一縮",
    "心頭一震", "心中暗道", "眉頭微皺", "宛如", "猶如", "彷彿", "這意味著", "終於明白",
    "從這一刻開始", "注定", "殊不知", "他不知道的是", "她不知道的是", "從而", "因而",
    "誠然", "於是乎", "綜上所述", "停了一下", "看了很久", "聲音很平", "張開嘴，又閉上",
]
# 原作名稱（不得出現）
FEZ = [
    "Fantasy Earth", "ファンタジーアース", "Netzawar", "ネツァワル", "Hordaine", "ホルデイン",
    "Geburand", "ゲブランド", "カセドリア", "Elsword", "エルソード",
]


def body_text(raw: str) -> str:
    # 去掉 front matter 和圖片行
    raw = re.sub(r"^---\n.*?\n---\n", "", raw, flags=re.S)
    raw = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", raw)
    return raw


def han_count(s: str) -> int:
    return len(re.findall(r"[一-鿿]", s))


def check(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    text = body_text(raw)
    n = han_count(text)
    k = max(n / 1000, 0.001)
    ok = True
    print(f"== {path.name}  漢字 {n}")

    flips = len(re.findall(r"不是[^。！？\n]{1,30}?[，,]\s*(?:而)?是", text))
    likes = text.count("像")
    weak = sum(text.count(w) for w in WEAK)
    long_ = text.count("很久")

    rows = [
        ("不是…是…", flips, HARD["不是…是…"], None),
        ("很久", long_, HARD["很久"], None),
        ("像", likes, None, PER_K["像"]),
        ("弱化副詞", weak, None, PER_K["弱化副詞"]),
    ]
    for name, c, hard, perk in rows:
        if hard is not None:
            bad = c > hard
            print(f"  {'✗' if bad else '✓'} {name}: {c}（上限 {hard}）")
        else:
            rate = c / k
            over = rate > perk
            # 「像」只提醒，不算失敗（第一章的比喻密度本來就高，是刻意的）
            bad = over and name != "像"
            mark = "✗" if bad else ("?" if over else "✓")
            print(f"  {mark} {name}: {c}，每千字 {rate:.1f}（建議 {perk}）")
        ok = ok and not bad

    hits = [(w, text.count(w)) for w in SIGNALS if w in text]
    if hits:
        print("  ? 套話訊號（回上下文判斷）：" + "、".join(f"{w}×{c}" for w, c in hits))
    fez = [w for w in FEZ if w.lower() in text.lower()]
    if fez:
        print("  ✗ 原作名稱：" + "、".join(fez))
        ok = False
    return ok


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    results = [check(Path(p)) for p in sys.argv[1:]]
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
