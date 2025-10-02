import hashlib
import os
from glob import glob
from pathlib import Path

DATA_DIR = Path("data")


def hash(value: str, len=7) -> str:
    md5_hash = hashlib.md5()
    md5_hash.update(str(value).encode("utf-8"))
    return md5_hash.hexdigest()[:len]


def get_basename(file: str) -> str:
    name = os.path.basename(file)
    return os.path.splitext(name)[0]


def get_company_files(company: str, limit: int = 100) -> list[str] | str | None:
    glob_path = DATA_DIR / f"{company}_*.json"
    res = [(file) for file in sorted(glob(str(glob_path)), reverse=True)]
    if not res:
        return None
    if limit == 1:
        return res[0]
    return res[:limit]
