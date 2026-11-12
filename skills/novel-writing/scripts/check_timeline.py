#!/usr/bin/env python3
"""時間線驗算：讀 timeline.json，檢查時序、年紀、週期與因果。

用法：python3 check_timeline.py timeline.json
只用標準函式庫。有 error 時回傳 1，warning 只提醒。

timeline.json 格式（日數從故事第 0 天算起，不用真實日期）：
{
  "characters": [
    {"id": "liese", "name": "莉潔", "age": 19, "ageDay": 0}
  ],
  "cycles": [
    {"name": "補封霜", "every": 9, "startDay": 25, "chars": ["balder"]}
  ],
  "events": [
    {"id": "e1", "chapter": 1, "day": 0, "title": "鐘響",
     "chars": ["liese"], "ages": {"liese": 19},
     "duration": 0, "causedBy": [], "flashback": false}
  ]
}

檢查項目：
- 時序倒流：非回憶事件，章節較後但日數較早（error）
- 因果：causedBy 指向不存在、或發生在之後的事件（error）
- 年紀：ages 跟 characters 推算出的年紀不合（error）
- 同一角色在重疊的時間出現在兩個事件（warning，可能是筆誤）
- 長跳躍：相鄰章節日數相差超過 60 天（warning）
- 週期：列出每個週期在事件範圍內的到期日，方便對照正文（info）
"""
import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    chars = {c["id"]: c for c in data.get("characters", [])}
    events = data.get("events", [])
    by_id = {e["id"]: e for e in events}
    errors, warns = [], []

    live = [e for e in events if not e.get("flashback")]
    live.sort(key=lambda e: (e["chapter"], e["day"]))
    latest = None
    for e in live:
        if latest and e["day"] < latest["day"] and e["chapter"] > latest["chapter"]:
            errors.append(f"時序倒流：第{e['chapter']}章〈{e['title']}〉第{e['day']}天，"
                          f"早於第{latest['chapter']}章〈{latest['title']}〉第{latest['day']}天")
        if latest is None or e["day"] >= latest["day"]:
            latest = e

    for e in events:
        for cid in e.get("causedBy", []):
            cause = by_id.get(cid)
            if cause is None:
                errors.append(f"因果：〈{e['title']}〉的原因 {cid} 不存在")
            elif cause["day"] > e["day"] and not e.get("flashback"):
                errors.append(f"因果：〈{e['title']}〉（第{e['day']}天）的原因〈{cause['title']}〉"
                              f"發生在之後（第{cause['day']}天）")
        for cid, age in e.get("ages", {}).items():
            c = chars.get(cid)
            if c is None:
                errors.append(f"年紀：〈{e['title']}〉提到未登記的角色 {cid}")
                continue
            expect = c["age"] + (e["day"] - c.get("ageDay", 0)) // 365
            if age != expect:
                errors.append(f"年紀：〈{e['title']}〉寫{c['name']} {age} 歲，推算應為 {expect} 歲")

    spans = []
    for e in live:
        start, end = e["day"], e["day"] + e.get("duration", 0)
        for other, ostart, oend in spans:
            if other["id"] == e["id"]:
                continue
            shared = set(e.get("chars", [])) & set(other.get("chars", []))
            if shared and start < oend and ostart < end:
                warns.append(f"重疊：{'、'.join(chars.get(s, {}).get('name', s) for s in shared)}"
                             f"同時在〈{other['title']}〉和〈{e['title']}〉")
        spans.append((e, start, end))

    chapters = {}
    for e in live:
        chapters.setdefault(e["chapter"], e["day"])
    keys = sorted(chapters)
    for a, b in zip(keys, keys[1:]):
        if chapters[b] - chapters[a] > 60:
            warns.append(f"長跳躍：第{a}章到第{b}章隔了 {chapters[b] - chapters[a]} 天，正文有交代嗎？")

    last_day = max((e["day"] for e in events), default=0)
    for cyc in data.get("cycles", []):
        days = list(range(cyc["startDay"], last_day + cyc["every"] + 1, cyc["every"]))
        print(f"週期〈{cyc['name']}〉到期日：" + "、".join(f"第{d}天" for d in days))

    for w in warns:
        print("  ? " + w)
    for e in errors:
        print("  ✗ " + e)
    if not errors and not warns:
        print("  ✓ 時間線沒有發現問題")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
