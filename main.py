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
 

def main() -> None:
    print("1 - найти в строке\n2 - найти в файле\n3 - найти на веб-странице")
    choice = input("Выбор: ").strip()
    if choice == "1":
        s = input("Введите серию и номер: ")
        if is_valid_passport(s):
            print("Корректные паспортные данные")
        else:
            print("Некорректные паспортные данные!")

    elif choice == "2":
        print(find_in_file(input("Путь к файлу: ").strip()))
    elif choice == "3":
        print(find_in_url(input("URL: ").strip()))
    else:
        sys.exit("Неизвестный пункт меню")
 
 
if __name__ == "__main__":
    main()