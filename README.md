# MarkItDown Converter

Простое десктоп-приложение для Windows, которое конвертирует документы (PDF, Word, Excel, PowerPoint, изображения и др.) в **Markdown** — удобный формат для работы с ИИ (ChatGPT, Claude и т.п.).

A simple Windows desktop app that converts documents (PDF, Word, Excel, PowerPoint, images, etc.) into **Markdown** — a convenient format for working with AI (ChatGPT, Claude, etc.).

Графический интерфейс с переключателем языка **RU / EN**, перетаскиванием файлов и пакетной конвертацией. Под капотом — библиотека [`markitdown`](https://github.com/microsoft/markitdown) от Microsoft.

GUI with an **RU / EN** language switch, drag-and-drop, and batch conversion. Powered by Microsoft's [`markitdown`](https://github.com/microsoft/markitdown) library.

---

## 🇷🇺 Русский

> 👋 Привет! Я начинающий программист, и это приложение — моё хобби. Я сделал десктопную программу для конвертации файлов в Markdown, чтобы потом удобно использовать их в ИИ. Буду рад, если оно пригодится и тебе.

### Возможности
- Перетаскивание файлов в окно (drag & drop) или выбор через диалог
- Пакетная конвертация — сразу много файлов
- Прогресс по каждому файлу и в целом
- Переключатель языка интерфейса 🌐 **RU / EN** (выбор запоминается)

### Поддерживаемые форматы
PDF, Word (`.docx`), Excel (`.xlsx`, `.xls`), PowerPoint (`.pptx`, `.ppt`),
HTML, TXT, CSV, JSON, XML, ZIP, изображения (`.jpg`, `.png`, `.gif`, `.bmp`, `.webp`),
аудио (`.mp3`, `.wav`, `.m4a`).

### Установка и запуск (для обычного пользователя)
1. Скачай готовую папку приложения (из раздела **Releases** на GitHub или у автора).
2. Распакуй архив целиком — **не разбивай папку**: рядом с `MarkItDown Converter.exe` лежит папка `_internal` с движком, без неё работать не будет.
3. Запусти `MarkItDown Converter.exe`.
4. Перетащи файлы в окно → выбери папку для сохранения → нажми **«Конвертировать»**.
   Рядом появятся файлы `.md`.

### Сборка из исходников (для разработки)
Нужен **Python 3.10+** для Windows.
```bat
:: 1. Установить зависимости и собрать .exe одной командой:
build.bat
```
Или вручную:
```bat
python -m pip install -r requirements.txt
python -m pip install pyinstaller
build.bat
```
Готовое приложение появится в папке `dist\MarkItDown Converter\`.
Чтобы поделиться с друзьями — заархивируй всю эту папку целиком.

---

## 🇬🇧 English

> 👋 Hi! I'm a beginner programmer and this app is my hobby. I built a desktop program that converts files into Markdown so they're easy to use with AI afterwards. Hope it's useful to you too.

### Features
- Drag & drop files into the window, or pick them via a dialog
- Batch conversion — many files at once
- Per-file and overall progress
- Interface language switch 🌐 **RU / EN** (your choice is remembered)

### Supported formats
PDF, Word (`.docx`), Excel (`.xlsx`, `.xls`), PowerPoint (`.pptx`, `.ppt`),
HTML, TXT, CSV, JSON, XML, ZIP, images (`.jpg`, `.png`, `.gif`, `.bmp`, `.webp`),
audio (`.mp3`, `.wav`, `.m4a`).

### Install & run (for end users)
1. Download the ready app folder (from the GitHub **Releases** section or from the author).
2. Unzip the whole folder — **keep it together**: the `_internal` folder next to
   `MarkItDown Converter.exe` holds the engine; the app won't run without it.
3. Run `MarkItDown Converter.exe`.
4. Drag files into the window → choose an output folder → click **“Convert”**.
   The `.md` files appear next to it.

### Build from source (for development)
Requires **Python 3.10+** on Windows.
```bat
:: 1. Install deps and build the .exe in one command:
build.bat
```
Or manually:
```bat
python -m pip install -r requirements.txt
python -m pip install pyinstaller
build.bat
```
The finished app appears in `dist\MarkItDown Converter\`.
To share with friends, zip that whole folder.

---

## ⚙️ Технические детали / Tech notes
- GUI: `tkinter` + `tkinterdnd2` (drag & drop)
- Движок / engine: `markitdown[all]` (Microsoft)
- Сборка / packaging: `PyInstaller` (`--onedir --windowed`, см. `build.bat` / `build.sh`)
- Первый запуск свежесобранного `.exe` может быть медленным (~10 с): антивирус/OneDrive сканируют файлы.

## 📄 Лицензия / License
MIT — см. файл [LICENSE](LICENSE).
