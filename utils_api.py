import string
import re


def IsCorrectEncodedVernam(text) -> bool:
    """
    Проверяет, является ли текст зашифрованным с помощью шифра Вернама

    Input:  Текст (str)

    Output: (bool)

    Note:   Нужен для коррекстной работы ConvertToNumbers;
            Допускаются только цифры и пробельные символы

    Ex.:    "\n1 2 3\n\n10 100 1000\n" -> True
            "\n1 2 3\n\n10 100 1000\n @6c" -> False
    """

    return re.compile(f"^[{string.digits + string.whitespace}]+$").search(text) is not None


def DoesBelongAlphabet(text, alphabet) -> bool:
    """
    Проверяет, если ли в тексте буквы, отсутствующие в алфавите

    Input:  Текст (str),
            Алфавит (str)

    Output: (bool)

    Ex.:    ("abcd", "a..zA..Z") -> True
            ("абвг", "a..zA..Z") -> False
    """

    return set(text).issubset(set(alphabet))


def IsAlphabet(text) -> bool:
    """
    Проверяет, можно ли из текста сделать алфавит: без дубликатов и только из символов-букв (isalpha)

    Input:  Текст (str)

    Output: (bool)

    Note:   Регистр не важен

    Ex.:    "abcd" -> True
            "a1 cc" -> False
    """

    return text.isalpha() and len(list(text)) == len(set(text))


def NormalizeAlphabet(text) -> str:
    """
    Приводит алфавит к виду: сначала все строчные, потом все заглавные буквы по порядку без пробелов

    Input:  Алфавит (str)

    Output: Двойной алфавит (str)

    Note:   Ожидается, что перед этим текст прогнали через is_alphabet;
            регистр не важен

    Ex.:    "abcd" -> "abcdABCD"
            "QйlД" -> "qйlдQЙLД"
    """

    return text.lower() + text.upper()
