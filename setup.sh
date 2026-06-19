#!/bin/bash
set -e

PYTHON="/c/Users/User/AppData/Local/Programs/Python/Python313/python.exe"

echo "==> Создаём виртуальное окружение..."
"$PYTHON" -m venv venv

echo "==> Активируем venv..."
source venv/Scripts/activate

echo "==> Обновляем pip..."
python -m pip install --upgrade pip

echo "==> Устанавливаем зависимости..."
pip install -r requirements.txt

echo ""
echo "✓ Готово! Теперь запусти: bash build.sh"
