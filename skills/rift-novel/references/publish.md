# 上架、插圖、翻譯

## 網站檔（本 repo）

- 一章一個檔：`content/lore/chNN.md`。
- 從 `/mnt/project-files/lore/chNN-標題.md` 轉：刪掉第一行標題和其後空行，前面加 front matter。

```
---
title: 裂谷鐘聲　第X章　標題
date: YYYY-MM-DD
cover: /lore/chNN-cover.webp
coverAlt: 一句話描述封面畫面
summary: 兩三句簡介，最後一句「《裂谷鐘聲》第X章。」
---
```

- 圖放 `public/lore/`：封面 `chNN-cover.webp`，另存一份 `chNN-cover.jpg` 給社群預覽（og:image）。內頁插圖用 `![說明](/lore/檔名.webp)`，放在對應場景的分隔線後面。
- 篇尾兩行固定：

```
《裂谷鐘聲》每週四更新，下一章〈標題〉回到莉潔／凱爾的視角。
本作的世界觀與小說由 AI 協助撰寫，經開發者審閱與編修。
```

- `npm run build` 通過再推。
- 從 origin/main 開分支，開 draft PR，Kc 自己合併。合併後頁面在 `https://fezone.tw/lore/chNN/`。
- 上架順序：每週四一章，不提早，除非 Kc 說要加快。

## 插圖需求

- 每章一張封面、一到兩張內頁插圖。
- 給美術串的需求寫：畫面、在場角色（外型照外型單）、光線與情緒、構圖、要避開的東西。
- 已知限制：刻字的牆和小道具畫不好，挑最好的種子；莉潔要寫明短髮到肩，負面詞放 long hair。

## 社群貼文

- `chNN-discord-post.md`：Discord #公告，三段：上線一句、兩三句劇情、全文連結，最後一句對玩家，結尾「（世界觀與小說由 AI 協助撰寫，我自己審過改過）」。
- `chNN-post.md`：FB 社團版，語氣隨意，不寫「測試」「免費」。
- `storyteller-weekN.ts`：遊戲裡說書人每國第 2 句，中英各一組。

## 翻譯交接

- 譯本在 `/mnt/project-files/lore/en/chNN.md`、`lore/ja/chNN.md`，由「校對英文和日文翻譯」串負責。
- 中文章節上線那天通知它，它會開英文頁的 PR（`content/lore/en/`）。
- 已翻譯的章節改了稿，列出「舊句 → 新句」給它。
