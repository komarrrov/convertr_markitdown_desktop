# MarkItDown Converter

Простое десктоп-приложение для Windows, которое конвертирует документы (PDF, Word, Excel, PowerPoint, изображения и др.) в **Markdown** — удобный формат для работы с ИИ (ChatGPT, Claude и т.п.).

A simple Windows desktop app that converts documents (PDF, Word, Excel, PowerPoint, images, etc.) into **Markdown** — a convenient format for working with AI (ChatGPT, Claude, etc.).

Графический интерфейс с переключателем языка **RU / EN**, перетаскиванием файлов и пакетной конвертацией. Под капотом — библиотека [`markitdown`](https://github.com/microsoft/markitdown) от Microsoft.

GUI with an **RU / EN** language switch, drag-and-drop, and batch conversion. Powered by Microsoft's [`markitdown`](https://github.com/microsoft/markitdown) library.

![MarkItDown Converter — скриншот / screenshot](assets/screenshot.png)

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

### 📥 Установка и запуск (подробно, для обычного пользователя)
> 💡 **Python устанавливать НЕ нужно** — он уже встроен в приложение. Просто скачай и запусти.

**Шаг 1. Скачай приложение.** Есть два формата:

| Формат | Что качать | Плюсы | Минусы |
|---|---|---|---|
| **Один файл** (onefile) | один `MarkItDown Converter.exe` | ничего не надо распаковывать, удобно пересылать | первый запуск медленный (~10–40 с) |
| **Папка** (onedir) | архив с папкой → распаковать целиком | запускается быстро | папку **нельзя разбивать**: рядом с `.exe` обязана лежать папка `_internal` |

**Шаг 2. Запусти `MarkItDown Converter.exe`** (двойной клик).
- Если Windows покажет окно **«SmartScreen защитил ваш компьютер»** — это нормально для новых программ без цифровой подписи. Нажми **«Подробнее» → «Выполнить в любом случае»**.
- Первый запуск версии «один файл» может занять до ~40 секунд (распаковка во временную папку + проверка антивирусом). Следующие запуски — быстрее.

**Шаг 3. Добавь файлы** — двумя способами:
- **перетащи** файлы мышкой прямо в окно (в область с подсказкой «Перетащи файлы сюда»), либо
- нажми **«+ Добавить»** и выбери файлы в диалоге.

Файлы появятся списком. Лишний можно убрать крестиком **✕**, очистить весь список — кнопкой **«Очистить»**. Можно добавить сразу много файлов — они сконвертируются пакетом.

**Шаг 4. Укажи папку для сохранения** — нажми **«Обзор»** и выбери, куда положить результат.

**Шаг 5. Нажми «Конвертировать →».** Появится прогресс по каждому файлу и общий; внизу по завершении — **«Готово!»**.

**Где результат?** Для каждого исходного файла рядом в выбранной папке создаётся `.md`-файл с тем же именем (например, `отчёт.pdf` → `отчёт.md`). Его можно открыть любым текстовым редактором или сразу вставить содержимое в ИИ (ChatGPT, Claude и т.п.).

**Язык интерфейса** переключается кнопкой 🌐 **RU / EN** в правом верхнем углу; выбор запоминается.

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

Либо собери **один файл** (Python пользователю не нужен):
```bat
build_onefile.bat
```
Результат: `dist_onefile\MarkItDown Converter.exe` — его можно отдавать как есть.

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

### 📥 Install & run (step-by-step, for end users)
> 💡 **You do NOT need Python installed** — it's bundled inside the app. Just download and run.

**Step 1. Download the app.** Two formats are available:

| Format | What you download | Pros | Cons |
|---|---|---|---|
| **Single file** (onefile) | one `MarkItDown Converter.exe` | nothing to unpack, easy to send | first launch is slow (~10–40 s) |
| **Folder** (onedir) | a zip with a folder → unzip it whole | starts fast | **don't split the folder**: the `_internal` folder must stay next to the `.exe` |

**Step 2. Run `MarkItDown Converter.exe`** (double-click).
- If Windows shows **“SmartScreen protected your PC”**, that's normal for new unsigned apps. Click **“More info” → “Run anyway”**.
- The first launch of the single-file build can take up to ~40 s (it unpacks to a temp folder and the antivirus scans it). Later launches are faster.

**Step 3. Add files** — two ways:
- **drag & drop** files straight into the window (onto the “Drag files here” area), or
- click **“+ Add”** and pick files in the dialog.

Files show up as a list. Remove one with the **✕**, clear all with **“Clear”**. You can add many files at once — they convert as a batch.

**Step 4. Choose an output folder** — click **“Browse”** and pick where to save the results.

**Step 5. Click “Convert →”.** You'll see per-file and overall progress; **“Done!”** appears at the bottom when finished.

**Where's the output?** For each input file a `.md` file with the same name is created in the chosen folder (e.g. `report.pdf` → `report.md`). Open it in any text editor or paste its content straight into an AI (ChatGPT, Claude, etc.).

**Interface language** is toggled with the 🌐 **RU / EN** button in the top-right corner; your choice is remembered.

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

Or build a **single file** (no Python needed on the user's machine):
```bat
build_onefile.bat
```
Result: `dist_onefile\MarkItDown Converter.exe` — shareable as-is.

---

## ❓ Частые вопросы / FAQ

**Нужен ли Python / интернет?** / *Do I need Python or internet?*
Нет. Python встроен в `.exe`, а конвертация локальных файлов идёт офлайн. /
No. Python is bundled in the `.exe`, and converting local files works offline.

**Антивирус или SmartScreen ругается.** / *Antivirus or SmartScreen complains.*
Это типичное ложное срабатывание для неподписанных программ, собранных PyInstaller. Нажми «Подробнее» → «Выполнить в любом случае» или добавь файл в исключения антивируса. /
This is a common false positive for unsigned PyInstaller apps. Click “More info” → “Run anyway”, or add the file to your antivirus exceptions.

**Первый запуск долгий (версия «один файл»).** / *First launch is slow (single-file build).*
Файл распаковывается во временную папку, антивирус его сканирует. Следующие запуски быстрее. Нужен мгновенный старт — бери папочную версию (onedir). /
The file unpacks to a temp folder and gets scanned. Later launches are faster. Need instant start — use the folder (onedir) build.

**Один из файлов не сконвертировался.** / *One of the files failed.*
Остальные всё равно сконвертируются; в конце появится список файлов с ошибками и их причинами. Проверь, что файл не повреждён и его формат поддерживается. /
The rest still convert; a list of failed files with reasons is shown at the end. Make sure the file isn't corrupted and its format is supported.

**Где хранится выбранный язык?** / *Where is the chosen language stored?*
В файле `~/.markitdown_converter.json` (в папке профиля пользователя). /
In `~/.markitdown_converter.json` (in your user profile folder).

## ⚙️ Технические детали / Tech notes
- GUI: `tkinter` + `tkinterdnd2` (drag & drop)
- Движок / engine: `markitdown[all]` (Microsoft)
- Сборка / packaging: `PyInstaller` (`--onedir --windowed`, см. `build.bat` / `build.sh`)
- Первый запуск свежесобранного `.exe` может быть медленным (~10 с): антивирус/OneDrive сканируют файлы.

## ☕ Поддержать / Support

🇷🇺 Если приложение оказалось полезным и вы хотите поддержать его дальнейшее развитие — буду благодарен за любой вклад. Это совершенно добровольно. 🙏

🇬🇧 If this app was useful and you'd like to support its further development, any contribution is appreciated — entirely optional. 🙏

Для перевода USDT используйте следующие реквизиты / To send USDT, use these details:

- 💰 **Валюта / Currency:** USDT (Tether)
- 🌐 **Сеть / Network:** Ethereum (ERC-20)
- 📍 **Адрес кошелька / Wallet address:**
  `0x213FAEf3e8fC382954D41f492F973693025fA2F5`

> ⚠️ Перед отправкой убедитесь, что перевод осуществляется именно в **USDT** по сети **Ethereum (ERC-20)**.
> Before sending, make sure you send **USDT** over the **Ethereum (ERC-20)** network.

## 📄 Лицензия / License
MIT — см. файл [LICENSE](LICENSE).
