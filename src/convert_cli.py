"""Headless smoke-test: конвертирует файл через тот же движок, что и GUI.
Использование: convert_cli <input> <output.md>
Нужен только для проверки frozen-сборки."""
import sys
from pathlib import Path
from markitdown import MarkItDown


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: convert_cli <input> <output.md>")
        return 2
    src, dst = sys.argv[1], sys.argv[2]
    md = MarkItDown()
    res = md.convert(src)
    Path(dst).write_text(res.text_content, encoding="utf-8")
    print(f"OK chars={len(res.text_content)} -> {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
