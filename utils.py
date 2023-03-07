def ConvertToNumbers(data) -> list:
    """ Вычленяет все числа и '\n' из текста

    Input:  текст (str)

    Output: список символов (list[str, int])

    Note:   нужен для шифра Вернама;
            бессмысленные пробелы игнорируются

    Ex.:    "\n1 2 3\n\n10 100 1000\n" -> ['\n', 1, 2, 3, '\n', '\n', 10, 100, 1000, '\n']
    """

    data_numbers = []
    length = len(data)
    data += ' '

    i = 0
    while i != length:
        if data[i] in "0123456789":
            number = ''
            while data[i] in "0123456789":
                number += data[i]
                i += 1

            data_numbers.append(int(number))
            continue

        if data[i] == '\n':
            data_numbers.append('\n')
            i += 1
            continue

        i += 1

    return data_numbers


def is_alphabet(text) -> bool:
    """ Проверяет, можно ли из текста сделать алфавит: без дубликатов и только из букв

    Input:  текст (str)

    Output: (bool)

    Note:   регистр не важен

    Ex.:    "abcd" -> True
            "a1 cc" -> False
    """

    return text.isalpha() and len(list(text)) == len(set(text))


def normalize_alphabet(text) -> str:
    """ Приводит алфавит к виду: сначала все строчные, потом все заглавные буквы по порядку без пробелов

    Input:  алфавит (str)

    Output: двойной алфавит (str)

    Note:   ожидается, что перед этим текст прогнали через is_alphabet;
            регистр не важен

    Ex.:    "qйLД" -> "qйlдQЙLД"
    """

    return text.lower() + text.upper()
