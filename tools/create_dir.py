import regex as re
from pathlib import Path
from typing import Union



# Корневая папка для всех заметок
BASE_NOTES_DIR = Path("notes")


def sanitize_name(name: str) -> str:
    """
    Оставляем буквы (любые алфавиты), цифры, пробел, '_' и '-'.
    Заменяем подряд идущие пробелы на один underscore.
    """
    name = name.strip()
    # Убираем расширение .md
    if name.lower().endswith(".md"):
        name = name[:-3].strip()
    # Оставляем только буквы (\p{L}), цифры (\p{N}), пробел, '_' и '-'
    name = re.sub(r"[^\p{L}\p{N} _\-]", "", name)
    # Заменяем несколько пробелов/подчёркиваний подряд на один "_"
    name = re.sub(r"[\s]+", "_", name)
    return name


def get_user_dir(user_id: int) -> Path:
    return BASE_NOTES_DIR / str(user_id)


def ensure_user_dir(user_id: int) -> Path:
    path = get_user_dir(user_id)
    path.mkdir(parents=True, exist_ok=True)
    return path


def unique_md_path(user_dir: Path, base_name: str) -> Path:
    """
    Возвращает уникальный путь вида base_name.md, если есть конфликт —
    base_name(1).md, base_name(2).md и т.д.
    """
    base = f"{base_name}.md"
    candidate = user_dir / base
    counter = 1
    while candidate.exists():
        candidate = user_dir / f"{base_name}({counter}).md"
        counter += 1
    return candidate