# rift-novel-writing-skill

奇幻之境連載小說《裂谷鐘聲》（The Bells of the Rift）的寫作技能，給 Claude Code 用。

內容在 `skills/rift-novel/`：

| 檔案 | 用途 |
|---|---|
| `SKILL.md` | 寫一章、改稿、審稿、擴充設定的流程與固定設定 |
| `references/self-check.md` | 寫完每章的自檢表 |
| `references/publish.md` | 上架到 fezone.tw/lore、插圖需求、社群貼文、翻譯交接 |
| `scripts/check_chapter.py` | 章節檢查程式（只用 Python 標準函式庫，不連網） |
| `THIRD_PARTY.md` | 參考來源與授權 |

## 安裝

把 `skills/rift-novel/` 整個資料夾複製到下面其中一處：

- 專案內：`<專案>/.claude/skills/rift-novel/`
- 個人全域：`~/.claude/skills/rift-novel/`

重開 Claude Code 後，寫或改《裂谷鐘聲》時會自動載入。

## 檢查程式

```bash
python3 skills/rift-novel/scripts/check_chapter.py 章節.md [更多章節.md ...]
```

數「不是…是…」「很久」「像」、弱化副詞、套話訊號，並掃原作名稱。超過硬上限時回傳 1。

## 資料位置

技能會讀專案共用資料夾 `/mnt/project-files/lore/` 底下的 `facts.md`、外型單和用詞表，那些是小說的正式設定，不放在這個 repo。
