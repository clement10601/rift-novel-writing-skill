# rift-novel-writing-skill

中文連載小說的寫作技能，給 Claude Code 用。一章一章寫，用檔案記住設定、時間線和伏筆，寫完跑自檢。不呼叫外部 API、不需要金鑰。

最早是為《裂谷鐘聲》（The Bells of the Rift）做的，現在整理成通用版，作品自己的規則放在專案設定檔裡。

## 內容

| 路徑 | 用途 |
|---|---|
| `skills/novel-writing/SKILL.md` | 寫一章、改稿、審稿、擴充設定、匯出電子書的流程 |
| `references/planning.md` | 開新書與開新卷：大綱三層、揭露帳本、進度錨點、拍子表、節奏選項 |
| `references/self-check.md` | 寫完每章的自檢表（節奏、時間線、因果、結尾、語言、名字） |
| `references/revision.md` | 兩遍法潤稿、修改權限分級、每十章體檢 |
| `references/deconstruct.md` | 拆解別本書的結構，只學骨架不抄內容 |
| `references/project-config-template.md` | 專案設定檔 `novel.config.md` 的範本 |
| `references/facts-template.md` | 事實登記表的範本 |
| `references/library/` | 第三方原文（MIT、GPL-3.0），依主題索引，見其中的 README |
| `scripts/check_chapter.py` | 章節檢查：口癖、套話、禁用名稱、寫作說明漏進正文、章尾斷掉 |
| `scripts/check_timeline.py` | 時間線檢查：時間倒流、因果順序、年齡、週期事件 |
| `scripts/export_epub.py` | 把 Markdown 章節匯出成 EPUB 3 |
| `skills/novel-writing/THIRD_PARTY.md` | 參考來源、收錄哪些原文、各自授權 |
| `examples/bells-of-the-rift/` | 實際作品的設定、檢查設定與時間線範例 |

（表中 `references/`、`scripts/` 都在 `skills/novel-writing/` 底下。）

## 安裝

把 `skills/novel-writing/` 複製到 `<專案>/.claude/skills/` 或 `~/.claude/skills/`，重開 Claude Code。

## 開一個新作品

1. 把 `references/project-config-template.md` 裡的範本存成專案根目錄的 `novel.config.md`，填好。
2. 用 `references/facts-template.md` 建事實登記表，放在設定檔指定的位置。
3. 需要的話，照 `examples/bells-of-the-rift/` 寫自己的 `novel-check.json`（口癖、上限、禁用名稱）和 `timeline.json`。
4. 跟 Claude 說「開新書」或「寫第一章」。

## 檢查程式

都只用 Python 標準函式庫，不連網。

```bash
# 章節自檢，超過硬上限或有禁用名稱時回傳 1，可以放進 CI
python3 skills/novel-writing/scripts/check_chapter.py --config novel-check.json chapters/*.md

# 時間線
python3 skills/novel-writing/scripts/check_timeline.py timeline.json

# 匯出電子書
python3 skills/novel-writing/scripts/export_epub.py --title 書名 --author 作者 --cover cover.jpg --out book.epub chapters/*.md
```

## 授權

GPL-3.0，全文見 `LICENSE`。`references/library/` 收錄的第三方原文保留原作者與原授權：MIT 的部分授權文字在 `licenses/`，GPL-3.0 的部分與本專案相同。來源與版本見 `skills/novel-writing/THIRD_PARTY.md`。
