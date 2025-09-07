from pathlib import Path

from tools.create_dir import sanitize_name, get_user_dir


def convert_filename_to_path(user_id: int, filename: str) -> Path | None:
    """
    Преобразует имя файла в абсолютный путь внутри директории конкретного пользователя.
    Если файла нет — возвращает None.
    """
    safe_name = sanitize_name(filename.strip())
    user_dir = get_user_dir(user_id)

    filepath = user_dir / f"{safe_name}.md"

    if not filepath.exists():
        return None
    return filepath