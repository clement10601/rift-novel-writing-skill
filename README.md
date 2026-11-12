# rift-novel-writing-skill

中文連載小說的寫作技能，給 Claude Code 用。一章一章寫，用檔案記住設定、時間線和伏筆，寫完跑自檢。不呼叫外部 API、不需要金鑰。

最早是為《裂谷鐘聲》（The Bells of the Rift）做的，現在整理成通用版，作品自己的規則放在專案設定檔裡。

## 內容

| 路徑 | 用途 |
|---|---|
| `skills/novel-writing/SKILL.md` | 寫一章、改稿、審稿、擴充設定的流程 |
| `skills/novel-writing/references/self-check.md` | 寫完每章的自檢表（節奏、時間線、因果、結尾、語言、名字） |
| `skills/novel-writing/references/project-config-template.md` | 專案設定檔 `novel.config.md` 的範本 |
| `skills/novel-writing/references/facts-template.md` | 事實登記表的範本 |
| `skills/novel-writing/scripts/check_chapter.py` | 章節檢查程式（Python 標準函式庫） |
| `skills/novel-writing/THIRD_PARTY.md` | 參考來源與授權 |
| `examples/bells-of-the-rift/` | 實際作品的設定範例 |

## 安裝

把 `skills/novel-writing/` 複製到 `<專案>/.claude/skills/` 或 `~/.claude/skills/`，重開 Claude Code。

## 開一個新作品

1. 把 `references/project-config-template.md` 裡的範本存成專案根目錄的 `novel.config.md`，填好。
2. 用 `references/facts-template.md` 建事實登記表，放在設定檔指定的位置。
3. 需要的話，照 `examples/bells-of-the-rift/novel-check.json` 寫一份自己的 `novel-check.json`（口癖、上限、禁用名稱）。
4. 跟 Claude 說「寫第一章」。

## 檢查程式

```bash
python3 skills/novel-writing/scripts/check_chapter.py --config novel-check.json chapters/*.md
```

數「不是…是…」、弱化副詞、「像」、套話訊號和你的口癖，並掃禁用名稱。超過硬上限時回傳 1，可以放進 CI。
