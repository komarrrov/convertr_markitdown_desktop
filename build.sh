#!/bin/bash
set -e
cd "$(dirname "$0")"

# Python: используем venv, если он рабочий, иначе системный
PY="python"
if [ -x "venv/Scripts/python.exe" ]; then
  PY="venv/Scripts/python.exe"
fi

echo "==> Проверяю зависимости..."
"$PY" -m pip install -r requirements.txt

echo "==> Удаляю старую сборку..."
rm -rf build dist

echo "==> Собираю .exe..."
"$PY" -m PyInstaller \
  --noconfirm --clean \
  --onedir --windowed \
  --name "MarkItDown Converter" \
  --collect-all markitdown \
  --collect-all magika \
  --collect-all onnxruntime \
  --collect-all pdfminer \
  --collect-all pptx \
  --collect-all tkinterdnd2 \
  --copy-metadata markitdown \
  src/app.py

echo ""
echo "✓ Готово! Папка: dist/MarkItDown Converter/"
echo "  Запуск: 'dist/MarkItDown Converter/MarkItDown Converter.exe'"
