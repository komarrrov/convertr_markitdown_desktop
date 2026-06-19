@echo off
REM ============================================================
REM  Сборка ОДНОГО самодостаточного .exe (Windows, без bash).
REM  Результат: один файл, Python на машине НЕ нужен.
REM  Минус: первый запуск медленнее (распаковка во временную папку).
REM  Для быстрого старта используй build.bat (режим --onedir).
REM ============================================================
setlocal
cd /d "%~dp0"

set "PY="
where py >nul 2>nul && set "PY=py -3"
if "%PY%"=="" (
    where python >nul 2>nul && set "PY=python"
)
if "%PY%"=="" (
    echo [ОШИБКА] Python не найден в PATH. Установи Python 3.10+ и повтори.
    pause
    exit /b 1
)

echo ==^> Проверяю зависимости...
%PY% -m pip install --upgrade pip
%PY% -m pip install -r requirements.txt
if errorlevel 1 (
    echo [ОШИБКА] Не удалось установить зависимости.
    pause
    exit /b 1
)

echo ==^> Удаляю старую onefile-сборку...
if exist build_onefile rmdir /s /q build_onefile
if exist dist_onefile  rmdir /s /q dist_onefile

echo ==^> Собираю один .exe (это займёт несколько минут)...
%PY% -m PyInstaller ^
  --noconfirm --onefile --windowed ^
  --name "MarkItDown Converter" ^
  --icon "assets\icon.ico" ^
  --add-data "assets\icon.ico;." ^
  --distpath dist_onefile ^
  --workpath build_onefile ^
  --specpath build_onefile ^
  --collect-all markitdown ^
  --collect-all magika ^
  --collect-all onnxruntime ^
  --collect-all pdfminer ^
  --collect-all pptx ^
  --collect-all tkinterdnd2 ^
  --copy-metadata markitdown ^
  src\app.py

if errorlevel 1 (
    echo.
    echo [ОШИБКА] Сборка не удалась. Смотри сообщения выше.
    pause
    exit /b 1
)

echo.
echo [ГОТОВО] Один файл: dist_onefile\MarkItDown Converter.exe
echo Его можно отдавать друзьям как есть - Python им не нужен.
pause
