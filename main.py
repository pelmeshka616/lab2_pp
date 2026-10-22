# Лаб 2: проверка и поиск синтаксически корректных паспортных данных (паспорт РФ).


import re
import sys
 

PASSPORT_PATTERN = r"(?<!\d)(?!00)\d{2}[ ]?\d{2}[ ]?(?:№[ ]?)?\d{6}(?!\d)"
PASSPORT_RE = re.compile(PASSPORT_PATTERN)
 

DEPT_CODE_RE = re.compile(r"(?<!\d)\d{3}-\d{3}(?!\d)")
 
 
def is_valid_passport(text: str) -> bool:
    # True, если вся строка — корректные серия и номер паспорта.
    return bool(PASSPORT_RE.fullmatch(text.strip()))


 
def find_passports(text: str) -> list[str]:
    # Все паспортные данные, найденные в тексте.
    return [m.group(0) for m in PASSPORT_RE.finditer(text)]
 
 
def find_in_file(path: str) -> list[str]:
    with open(path, encoding="utf-8") as f:
        return find_passports(f.read())
 
 
def find_in_url(url: str) -> list[str]:
    import requests
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return find_passports(resp.text)
 