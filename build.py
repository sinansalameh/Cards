"""Build a standalone, pure-ASCII copy of the app.

shadda.html is the editable source (UTF-8, published as the Claude artifact).
This script writes index.html: a complete HTML document in which every
non-ASCII character is escaped, so it renders correctly in any viewer,
whatever text encoding that viewer assumes.

Usage:  python build.py
"""
import re
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "shadda.html"
OUT = HERE / "index.html"


def esc_html(text):
    return "".join(c if ord(c) < 128 else f"&#x{ord(c):X};" for c in text)


def esc_js(text):
    out = []
    for c in text:
        o = ord(c)
        if o < 128:
            out.append(c)
        elif o <= 0xFFFF:
            out.append(f"\\u{o:04X}")
        else:
            out.append(f"\\u{{{o:X}}}")
    return "".join(out)


def esc_css(text):
    return "".join(c if ord(c) < 128 else f"\\{ord(c):X} " for c in text)


def main():
    src = SRC.read_text(encoding="utf-8").lstrip("﻿")
    # Escape each region with the syntax that region understands.
    parts = re.split(r"(<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>)", src, flags=re.S | re.I)
    body = []
    for p in parts:
        if p.lower().startswith("<script"):
            body.append(esc_js(p))
        elif p.lower().startswith("<style"):
            body.append(esc_css(p))
        else:
            body.append(esc_html(p))
    body = "".join(body)
    # The artifact host adds the document shell; a standalone file needs its own.
    body = re.sub(r'<meta charset="utf-8">\s*', "", body, flags=re.I)
    doc = (
        "<!DOCTYPE html>\n"
        '<html lang="ar" dir="rtl">\n<head>\n<meta charset="utf-8">\n'
        + body.replace("<div id=\"app\"", "</head>\n<body>\n<div id=\"app\"", 1)
        + "\n</body>\n</html>\n"
    )
    doc.encode("ascii")  # fails loudly if anything slipped through
    OUT.write_text(doc, encoding="ascii", newline="\n")
    print(f"wrote {OUT.name}: {len(doc):,} bytes, pure ASCII")


if __name__ == "__main__":
    main()
