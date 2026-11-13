# 參考來源與第三方內容

本技能以 GPL-3.0 授權（見 repo 根目錄 `LICENSE`）。內容分兩種：

1. **我們自己寫的**：`SKILL.md`、`references/*.md`（library 以外）、`scripts/*.py`。參考了下列專案的想法，全部用自己的話重寫。
2. **第三方原文**：`references/library/` 底下，內文未修改，只在開頭加一行來源註記。來源、授權與收錄版本列在 `references/library/README.md`，授權全文在 repo 根目錄 `licenses/`。

| 專案 | 授權 | 想法用在哪裡 | 收錄原文 |
|---|---|---|---|
| leenbj/novel-creator-skill | MIT | 一章一件大事、事件冷卻、拍子表、大綱錨點、兩遍潤稿、每十章體檢、改綱級聯、開書五問 | 4 份 |
| xindoo/sumeru | MIT | 撞名與原作名稱檢查、時間線驗算、拆書不抄書、EPUB 匯出 | 2 份 |
| zenstory-ai/oh-story-claudecode | MIT | 套話要回上下文判斷、因果與資訊邊界、修改權限分級、大綱四問、揭露帳本、正文斷尾檢查 | 9 份 |
| lingfengQAQ/webnovel-writer | GPL-3.0 | 多線輪替、名字與口吻差異 | 4 份 |
| PenglongHuang/chinese-novelist-skill | MIT | 事實登記表、資訊邊界、章節摘要 | 無 |
| pin0513/de-ai-flavor（gist） | 未標示授權 | 去 AI 味的檢查項目（否定翻轉、資訊密度、沒有後果的停頓、不替作者編經驗、風格錨）。只用想法，改寫成小說版 `references/de-ai-flavor.md`，沒有收錄原文 | 無 |
| ExplosiveCoderflome/AI-Novel-Writing-Assistant | AGPL-3.0 與商業雙授權 | 只參考產品構想（角色庫、世界觀庫、拆書），沒有使用任何文字或程式碼 | 無 |

沒有收錄：會呼叫外部 API 或需要金鑰的腳本、排行榜爬蟲、瀏覽器自動化、會寫入 Claude Code 設定的 hooks、封面生圖。
