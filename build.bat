@echo off
REM ============================================================
REM  Сборка MarkItDown Converter в .exe (Windows, без bash)
REM  Просто дважды кликни по этому файлу или запусти из cmd.
REM ============================================================
setlocal

cd /d "%~dp0"

REM --- Ищем Python: сначала launcher py, потом python из PATH ---
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
    echo [ОШИБКА] Не удалось установить зависимости. См. сообщения выше.
    pause
    exit /b 1
)

echo ==^> Удаляю старую сборку...
if exist build rmdir /s /q build
if exist dist  rmdir /s /q dist

echo ==^> Собираю .exe (это займёт пару минут)...
%PY% -m PyInstaller ^
  --noconfirm --clean ^
  --onedir --windowed ^
  --name "MarkItDown Converter" ^
  --icon "assets\icon.ico" ^
  --add-data "assets\icon.ico;." ^
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
echo [ГОТОВО] Папка с приложением: dist\MarkItDown Converter\
echo Запускай: dist\MarkItDown Converter\MarkItDown Converter.exe
echo Чтобы поделиться с друзьями - заархивируй всю папку "MarkItDown Converter".
pause
