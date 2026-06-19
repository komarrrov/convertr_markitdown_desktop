import os
import sys

# В windowed-сборке (PyInstaller --windowed) sys.stdout/stderr == None,
# и любой print() или вывод библиотеки уронит приложение. Подменяем заглушкой.
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

import json
import re
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

from tkinterdnd2 import TkinterDnD, DND_FILES
from markitdown import MarkItDown

# ── Цвета ──────────────────────────────────────────────────────────────────
BG          = "#F5F5F5"
SURFACE     = "#FFFFFF"
BORDER      = "#E0E0E0"
DROP_BG     = "#EFF6FF"
DROP_BORDER = "#93C5FD"
PRIMARY     = "#2563EB"
PRIMARY_HOV = "#1D4ED8"
DANGER      = "#DC2626"
TEXT        = "#111827"
SUBTEXT     = "#6B7280"
SUCCESS     = "#16A34A"

SUPPORTED = {
    ".pdf", ".docx", ".xlsx", ".xls",
    ".pptx", ".ppt", ".html", ".htm", ".txt",
    ".csv", ".json", ".xml", ".zip",
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp",
    ".mp3", ".wav", ".m4a",
}

FILE_ICONS = {
    ".pdf": "📄", ".docx": "📝",
    ".xlsx": "📊", ".xls": "📊",
    ".pptx": "📋", ".ppt": "📋",
    ".jpg": "🖼", ".jpeg": "🖼", ".png": "🖼",
    ".gif": "🖼", ".bmp": "🖼", ".webp": "🖼",
    ".mp3": "🎵", ".wav": "🎵", ".m4a": "🎵",
    ".html": "🌐", ".htm": "🌐",
    ".txt": "📃", ".csv": "📃",
    ".json": "📃", ".xml": "📃",
    ".zip": "📦",
}

# ── Локализация ──────────────────────────────────────────────────────────────
TR = {
    "ru": {
        "subtitle":      "Конвертируй документы в Markdown",
        "files":         "Файлы",
        "add":           "+ Добавить",
        "clear":         "Очистить",
        "drop_hint":     "Перетащи файлы сюда\nили нажми «+ Добавить»",
        "count":         "{n} файл(ов)",
        "out_label":     "Папка для сохранения",
        "browse":        "Обзор",
        "convert":       "  Конвертировать →",
        "prog_files":    "Файлы",
        "cur_file":      "Текущий файл",
        "need_files":    "⚠ Добавьте файлы для конвертации",
        "need_out":      "⚠ Выберите папку для сохранения",
        "starting":      "Начинаю…",
        "done":          "Готово!",
        "errors":        "Ошибки: {n} файл(ов)",
        "dlg_files":     "Выберите файлы",
        "dlg_out":       "Папка для сохранения",
        "dlg_err_title": "Ошибки конвертации",
        "ft_supported":  "Поддерживаемые файлы",
        "ft_all":        "Все файлы",
        "lang_btn":      "EN",
    },
    "en": {
        "subtitle":      "Convert documents to Markdown",
        "files":         "Files",
        "add":           "+ Add",
        "clear":         "Clear",
        "drop_hint":     "Drag files here\nor click «+ Add»",
        "count":         "{n} file(s)",
        "out_label":     "Output folder",
        "browse":        "Browse",
        "convert":       "  Convert →",
        "prog_files":    "Files",
        "cur_file":      "Current file",
        "need_files":    "⚠ Add files to convert",
        "need_out":      "⚠ Choose an output folder",
        "starting":      "Starting…",
        "done":          "Done!",
        "errors":        "Errors: {n} file(s)",
        "dlg_files":     "Select files",
        "dlg_out":       "Output folder",
        "dlg_err_title": "Conversion errors",
        "ft_supported":  "Supported files",
        "ft_all":        "All files",
        "lang_btn":      "RU",
    },
}

CONFIG_PATH = Path.home() / ".markitdown_converter.json"


def load_lang() -> str:
    try:
        lang = json.loads(CONFIG_PATH.read_text(encoding="utf-8")).get("lang")
        if lang in TR:
            return lang
    except Exception:
        pass
    return "ru"


def save_lang() -> None:
    try:
        CONFIG_PATH.write_text(json.dumps({"lang": LANG}), encoding="utf-8")
    except Exception:
        pass


LANG = load_lang()


def t(key: str, **kw) -> str:
    s = TR.get(LANG, TR["ru"]).get(key) or TR["ru"].get(key, key)
    return s.format(**kw) if kw else s


def filetypes():
    return [
        (t("ft_supported"), " ".join(f"*{e}" for e in SUPPORTED)),
        ("PDF", "*.pdf"), ("Word", "*.docx"),
        ("Excel", "*.xlsx *.xls"), ("PowerPoint", "*.pptx *.ppt"),
        (t("ft_all"), "*.*"),
    ]


selected_files: list[str] = []


# ── Парсинг путей из DnD ────────────────────────────────────────────────────
def parse_drop(data: str) -> list[str]:
    """Разбирает строку DnD: пути в {} или пробел-разделённые."""
    paths = re.findall(r'\{([^}]+)\}|(\S+)', data)
    return [a or b for a, b in paths]


# ── UI-хелперы ─────────────────────────────────────────────────────────────
def make_btn(parent, text, command, style="primary", **kw):
    palette = {
        "primary": (PRIMARY, "white",  PRIMARY_HOV),
        "outline": (SURFACE,  PRIMARY, "#DBEAFE"),
        "danger":  (SURFACE,  DANGER,  "#FEE2E2"),
    }
    bg, fg, hov = palette[style]
    kw.setdefault("font", ("Segoe UI", 10))
    btn = tk.Button(
        parent, text=text, command=command,
        bg=bg, fg=fg, activebackground=hov, activeforeground=fg,
        relief="flat", cursor="hand2", bd=0, padx=16, pady=8, **kw
    )
    btn.bind("<Enter>", lambda _: btn.config(bg=hov))
    btn.bind("<Leave>", lambda _: btn.config(bg=bg))
    return btn


def add_paths(paths: list[str]):
    added = 0
    for p in paths:
        path = Path(p)
        if path.is_file() and path.suffix.lower() in SUPPORTED and str(path) not in selected_files:
            selected_files.append(str(path))
            added += 1
    if added:
        refresh_list()


def refresh_list():
    for w in list_frame.winfo_children():
        w.destroy()

    if not selected_files:
        drop_hint()
        count_lbl.config(text="")
        return

    count_lbl.config(text=t("count", n=len(selected_files)))

    for i, fp in enumerate(selected_files):
        ext = Path(fp).suffix.lower()
        icon = FILE_ICONS.get(ext, "📁")
        name = Path(fp).name

        row = tk.Frame(list_frame, bg=SURFACE)
        row.pack(fill="x")

        tk.Label(row, text=icon, bg=SURFACE, font=("Segoe UI", 11)).pack(side="left", padx=(10, 4), pady=4)
        tk.Label(row, text=name, bg=SURFACE, fg=TEXT,
                 font=("Segoe UI", 10), anchor="w").pack(side="left", fill="x", expand=True)

        def remove(i=i):
            selected_files.pop(i)
            refresh_list()

        tk.Button(row, text="✕", command=remove, bg=SURFACE, fg=SUBTEXT,
                  activebackground="#FEE2E2", relief="flat",
                  font=("Segoe UI", 9), cursor="hand2", padx=8).pack(side="right", padx=4)

        tk.Frame(list_frame, bg=BORDER, height=1).pack(fill="x")

    canvas.configure(scrollregion=canvas.bbox("all"))


def drop_hint():
    tk.Label(
        list_frame,
        text=t("drop_hint"),
        bg=SURFACE, fg=SUBTEXT,
        font=("Segoe UI", 10), justify="center"
    ).pack(expand=True, pady=30)


# ── Drag & Drop обработчики ─────────────────────────────────────────────────
def on_drag_enter(e):
    drop_frame.config(highlightbackground=DROP_BORDER, bg=DROP_BG)
    canvas.config(bg=DROP_BG)
    list_frame.config(bg=DROP_BG)

def on_drag_leave(e):
    drop_frame.config(highlightbackground=BORDER, bg=SURFACE)
    canvas.config(bg=SURFACE)
    list_frame.config(bg=SURFACE)

def on_drop(e):
    on_drag_leave(e)
    add_paths(parse_drop(e.data))


# ── Действия ───────────────────────────────────────────────────────────────
def pick_files():
    files = filedialog.askopenfilenames(title=t("dlg_files"), filetypes=filetypes())
    if files:
        add_paths(list(files))


def clear_files():
    selected_files.clear()
    refresh_list()


def pick_output():
    folder = filedialog.askdirectory(title=t("dlg_out"))
    if folder:
        output_var.set(folder)


def toggle_lang():
    global LANG
    LANG = "en" if LANG == "ru" else "ru"
    save_lang()
    apply_language()


def apply_language():
    """Перевести все статичные надписи на текущий язык."""
    subtitle_lbl.config(text=t("subtitle"))
    files_title_lbl.config(text=t("files"))
    add_btn.config(text=t("add"))
    clear_btn.config(text=t("clear"))
    out_title_lbl.config(text=t("out_label"))
    browse_btn.config(text=t("browse"))
    convert_btn.config(text=t("convert"))
    prog_files_lbl.config(text=t("prog_files"))
    cur_file_lbl.config(text=t("cur_file"))
    lang_btn.config(text="🌐 " + t("lang_btn"))
    status_lbl.config(text="")
    refresh_list()


def convert():
    out = output_var.get()
    if not selected_files:
        status_lbl.config(text=t("need_files"), fg=DANGER)
        return
    if not out:
        status_lbl.config(text=t("need_out"), fg=DANGER)
        return

    total = len(selected_files)
    convert_btn.config(state="disabled")
    progress["maximum"] = total
    progress["value"] = 0
    files_counter_lbl.config(text=f"0 / {total}")
    status_lbl.config(text=t("starting"), fg=SUBTEXT)
    file_progress.config(mode="indeterminate", value=0)

    def worker():
        md = MarkItDown()
        ok, fail = 0, []

        for i, fp in enumerate(selected_files):
            name = Path(fp).name
            root.after(0, lambda n=name: (
                status_lbl.config(text=n),
                file_progress.config(mode="indeterminate"),
                file_progress.start(10),
            ))

            try:
                res = md.convert(fp)
                out_path = Path(out) / (Path(fp).stem + ".md")
                out_path.write_text(res.text_content, encoding="utf-8")
                ok += 1
            except Exception as ex:
                fail.append(f"{name}: {ex}")

            v = i + 1
            root.after(0, lambda v=v: (
                file_progress.stop(),
                file_progress.config(mode="determinate", value=100),
                progress.config(value=v),
                files_counter_lbl.config(text=f"{v} / {total}"),
            ))

        def done():
            convert_btn.config(state="normal")
            file_progress.stop()
            file_progress.config(mode="determinate", value=0)
            if fail:
                status_lbl.config(text=t("errors", n=len(fail)), fg=DANGER)
                files_counter_lbl.config(text=f"{ok} / {total}", fg=DANGER)
                messagebox.showerror(t("dlg_err_title"), "\n".join(fail))
            else:
                status_lbl.config(text=t("done"), fg=SUCCESS)
                files_counter_lbl.config(text=f"✓ {ok} / {total}", fg=SUCCESS)

        root.after(0, done)

    threading.Thread(target=worker, daemon=True).start()


# ── Окно ───────────────────────────────────────────────────────────────────
root = TkinterDnD.Tk()
root.title("MarkItDown Converter")
root.configure(bg=BG)
root.resizable(False, False)
root.geometry("620x680")

# Шапка
header = tk.Frame(root, bg=PRIMARY, pady=18)
header.pack(fill="x")
tk.Label(header, text="MarkItDown Converter", bg=PRIMARY, fg="white",
         font=("Segoe UI", 16, "bold")).pack()
subtitle_lbl = tk.Label(header, text=t("subtitle"),
                        bg=PRIMARY, fg="#BFDBFE", font=("Segoe UI", 9))
subtitle_lbl.pack()

# Переключатель языка (правый верхний угол шапки)
lang_btn = tk.Button(header, text="🌐 " + t("lang_btn"), command=toggle_lang,
                     bg=PRIMARY, fg="white", activebackground=PRIMARY_HOV,
                     activeforeground="white", relief="flat", bd=0,
                     cursor="hand2", font=("Segoe UI", 9, "bold"), padx=8, pady=2)
lang_btn.place(relx=1.0, x=-12, y=12, anchor="ne")

body = tk.Frame(root, bg=BG, padx=20, pady=16)
body.pack(fill="both", expand=True)

# Строка заголовка + кнопки
row1 = tk.Frame(body, bg=BG)
row1.pack(fill="x", pady=(0, 8))
files_title_lbl = tk.Label(row1, text=t("files"), bg=BG, fg=TEXT, font=("Segoe UI", 10, "bold"))
files_title_lbl.pack(side="left")
count_lbl = tk.Label(row1, text="", bg=BG, fg=SUBTEXT, font=("Segoe UI", 9))
count_lbl.pack(side="left", padx=8)
btn_row = tk.Frame(row1, bg=BG)
btn_row.pack(side="right")
add_btn = make_btn(btn_row, t("add"), pick_files)
add_btn.pack(side="left", padx=(0, 6))
clear_btn = make_btn(btn_row, t("clear"), clear_files, "outline")
clear_btn.pack(side="left")

# Drop-зона
drop_frame = tk.Frame(body, bg=SURFACE, highlightbackground=BORDER,
                      highlightthickness=1)
drop_frame.pack(fill="x")

canvas = tk.Canvas(drop_frame, bg=SURFACE, highlightthickness=0, height=160)
scrollbar = tk.Scrollbar(drop_frame, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

list_frame = tk.Frame(canvas, bg=SURFACE)
canvas.create_window((0, 0), window=list_frame, anchor="nw", width=595)
list_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Регистрация DnD
for widget in (drop_frame, canvas, list_frame):
    widget.drop_target_register(DND_FILES)
    widget.dnd_bind("<<DropEnter>>", on_drag_enter)
    widget.dnd_bind("<<DropLeave>>", on_drag_leave)
    widget.dnd_bind("<<Drop>>",      on_drop)

refresh_list()

# Разделитель
tk.Frame(body, bg=BORDER, height=1).pack(fill="x", pady=14)

# Папка назначения
out_title_lbl = tk.Label(body, text=t("out_label"), bg=BG, fg=TEXT,
                         font=("Segoe UI", 10, "bold"))
out_title_lbl.pack(anchor="w")
out_row = tk.Frame(body, bg=BG)
out_row.pack(fill="x", pady=(6, 0))
output_var = tk.StringVar()
tk.Entry(out_row, textvariable=output_var, font=("Segoe UI", 10),
         relief="flat", bg=SURFACE,
         highlightbackground=BORDER, highlightthickness=1).pack(
    side="left", fill="x", expand=True, ipady=7, padx=(0, 8))
browse_btn = make_btn(out_row, t("browse"), pick_output, "outline")
browse_btn.pack(side="right")

# Разделитель
tk.Frame(body, bg=BORDER, height=1).pack(fill="x", pady=14)

# Кнопка конвертации
convert_btn = make_btn(body, t("convert"), convert, font=("Segoe UI", 11, "bold"))
convert_btn.pack(fill="x", ipady=4)

# Прогресс
style = ttk.Style()
style.theme_use("clam")
style.configure("Blue.Horizontal.TProgressbar",
                troughcolor=BORDER, background=PRIMARY,
                thickness=8, borderwidth=0)
style.configure("Gray.Horizontal.TProgressbar",
                troughcolor=BORDER, background="#93C5FD",
                thickness=5, borderwidth=0)

# Строка с подписью и счётчиком для общего прогресса
prog_row = tk.Frame(body, bg=BG)
prog_row.pack(fill="x", pady=(12, 2))
prog_files_lbl = tk.Label(prog_row, text=t("prog_files"), bg=BG, fg=SUBTEXT,
                          font=("Segoe UI", 8))
prog_files_lbl.pack(side="left")
files_counter_lbl = tk.Label(prog_row, text="", bg=BG, fg=SUBTEXT,
                             font=("Segoe UI", 8))
files_counter_lbl.pack(side="right")

progress = ttk.Progressbar(body, style="Blue.Horizontal.TProgressbar", mode="determinate")
progress.pack(fill="x", pady=(0, 6))

# Текущий файл
cur_file_lbl = tk.Label(body, text=t("cur_file"), bg=BG, fg=SUBTEXT,
                        font=("Segoe UI", 8))
cur_file_lbl.pack(anchor="w")
file_progress = ttk.Progressbar(body, style="Gray.Horizontal.TProgressbar", mode="indeterminate")
file_progress.pack(fill="x", pady=(2, 4))

status_lbl = tk.Label(body, text="", bg=BG, fg=SUBTEXT, font=("Segoe UI", 9))
status_lbl.pack()

root.mainloop()
