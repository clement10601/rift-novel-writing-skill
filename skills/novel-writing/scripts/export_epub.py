#!/usr/bin/env python3
"""把 Markdown 章節匯出成 EPUB 3 電子書。

用法：
  python3 export_epub.py --title 書名 --author 作者 --out 書.epub [--cover 封面.jpg] [--lang zh-Hant] 章節1.md 章節2.md ...

只用標準函式庫。章節依參數順序排列。
- 檔案開頭的 front matter（--- 包起來的區塊）會被略過，title 欄位拿來當章名。
- 沒有 front matter 時，用第一行 # 標題當章名。
- 支援段落、--- 分隔線、**粗體**、*斜體*。圖片行會被略過（電子書版不放插圖）。
"""
import argparse
import html
import re
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path


def parse_chapter(path):
    raw = Path(path).read_text(encoding="utf-8")
    title = None
    m = re.match(r"^---\n(.*?)\n---\n", raw, flags=re.S)
    if m:
        for line in m.group(1).splitlines():
            if line.startswith("title:"):
                title = line.split(":", 1)[1].strip()
        raw = raw[m.end():]
    lines = raw.splitlines()
    if lines and lines[0].startswith("# "):
        title = title or lines[0][2:].strip()
        lines = lines[1:]
    title = title or Path(path).stem
    parts = []
    para = []

    def flush():
        if para:
            text = html.escape("".join(para))
            text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
            text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
            parts.append(f"<p>{text}</p>")
            para.clear()

    for line in lines:
        s = line.strip()
        if not s:
            flush()
        elif s == "---":
            flush()
            parts.append('<hr class="scene"/>')
        elif s.startswith("!["):
            continue
        elif s.startswith("#"):
            flush()
            parts.append(f"<h2>{html.escape(s.lstrip('#').strip())}</h2>")
        else:
            para.append(s)
    flush()
    return title, "\n".join(parts)


def xhtml(title, body, lang):
    return (f'<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n'
            f'<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" '
            f'lang="{lang}" xml:lang="{lang}"><head><meta charset="utf-8"/><title>{html.escape(title)}</title>'
            f'<link rel="stylesheet" href="style.css"/></head><body>{body}</body></html>')


CSS = ("body{line-height:1.8;margin:0 1em;}p{text-indent:2em;margin:0 0 .6em;}"
       "h1{font-size:1.4em;margin:2em 0 1.5em;}hr.scene{border:0;text-align:center;margin:1.2em 0;}"
       "hr.scene:after{content:'＊';}")


def main():
    ap = argparse.ArgumentParser(description="Markdown 章節匯出 EPUB 3")
    ap.add_argument("--title", required=True)
    ap.add_argument("--author", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--cover")
    ap.add_argument("--lang", default="zh-Hant")
    ap.add_argument("chapters", nargs="+")
    a = ap.parse_args()

    book_id = f"urn:uuid:{uuid.uuid4()}"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    chapters = [parse_chapter(p) for p in a.chapters]
    manifest, spine, nav = [], [], []

    with zipfile.ZipFile(a.out, "w") as z:
        z.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml",
                   '<?xml version="1.0"?><container version="1.0" '
                   'xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles>'
                   '<rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>'
                   '</rootfiles></container>', compress_type=zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/style.css", CSS, compress_type=zipfile.ZIP_DEFLATED)
        manifest.append('<item id="css" href="style.css" media-type="text/css"/>')

        cover_meta = ""
        if a.cover:
            ext = Path(a.cover).suffix.lower().lstrip(".")
            mime = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png", "webp": "image/webp"}[ext]
            z.write(a.cover, f"OEBPS/cover.{ext}", compress_type=zipfile.ZIP_DEFLATED)
            manifest.append(f'<item id="cover-img" href="cover.{ext}" media-type="{mime}" properties="cover-image"/>')
            z.writestr("OEBPS/cover.xhtml",
                       xhtml(a.title, f'<img src="cover.{ext}" alt="{html.escape(a.title)}" style="max-width:100%"/>', a.lang),
                       compress_type=zipfile.ZIP_DEFLATED)
            manifest.append('<item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>')
            spine.append('<itemref idref="cover"/>')
            cover_meta = '<meta name="cover" content="cover-img"/>'

        for i, (title, body) in enumerate(chapters, 1):
            name = f"ch{i:03d}.xhtml"
            z.writestr(f"OEBPS/{name}", xhtml(title, f"<h1>{html.escape(title)}</h1>\n{body}", a.lang),
                       compress_type=zipfile.ZIP_DEFLATED)
            manifest.append(f'<item id="c{i}" href="{name}" media-type="application/xhtml+xml"/>')
            spine.append(f'<itemref idref="c{i}"/>')
            nav.append(f'<li><a href="{name}">{html.escape(title)}</a></li>')

        z.writestr("OEBPS/nav.xhtml",
                   xhtml("目錄", f'<nav epub:type="toc"><h1>目錄</h1><ol>{"".join(nav)}</ol></nav>', a.lang),
                   compress_type=zipfile.ZIP_DEFLATED)
        manifest.append('<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>')

        opf = (f'<?xml version="1.0" encoding="utf-8"?><package xmlns="http://www.idpf.org/2007/opf" '
               f'version="3.0" unique-identifier="bookid"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'
               f'<dc:identifier id="bookid">{book_id}</dc:identifier><dc:title>{html.escape(a.title)}</dc:title>'
               f'<dc:creator>{html.escape(a.author)}</dc:creator><dc:language>{a.lang}</dc:language>'
               f'<meta property="dcterms:modified">{now}</meta>{cover_meta}</metadata>'
               f'<manifest>{"".join(manifest)}</manifest><spine>{"".join(spine)}</spine></package>')
        z.writestr("OEBPS/content.opf", opf, compress_type=zipfile.ZIP_DEFLATED)

    print(f"已輸出 {a.out}：{len(chapters)} 章")


if __name__ == "__main__":
    main()
