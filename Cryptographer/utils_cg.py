import string


def ConvertToNumbers(data) -> list:
    """
    Вычленяет все числа и '\n' из зашифрованного текста

    Input:  Текст, зашифрованный Вернамом (str)

    Output: Список символов (list[str, int])

    Note:   Нужен для расшифровки Вернама;
            бессмысленные пробелы игнорируются

    Ex.:    "\n1 2 3\n\n10 100 1000\n" -> ['\n', 1, 2, 3, '\n', '\n', 10, 100, 1000, '\n']
    """

    data_numbers = []
    length = len(data)
    data += ' '

    i = 0
    while i != length:
        if data[i] in string.digits:
            number = ''
            while data[i] in string.digits:
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


def FrequencyAnalyzer(given_frequency, actual_frequency) -> list:
    """
    Определяет сумму разниц между истинными (Wikipedia) и текущими значениями частот (%) букв для каждого сдвига Цезаря

    Input:  Частоты (доли) всех букв исходного текста (list[double]),
            Истинные частоты букв языка (list[double])

    Output: Список значений (list[double])

    Note:   Нужен для HackCaesarStep;
            Если шаг совпадает (в примере он 0) и нормальное статистическое распределение букв, то обычно сумма не доходит выше 0.2, иначе колеблется в районе 1.0

    Ex.:    ([...], [...]) -> [0.10203040506070809, 0,90807060504030201, 1,12345678987654321, ...]
    """

    given_frequency = list(given_frequency.values())
    frequency_rate_values = list(actual_frequency.values())

    differences = []
    length = len(given_frequency)

    for stp in range(length):
        diff = 0
        for i in range(length):
            diff += abs(given_frequency[(i + stp) % length] - frequency_rate_values[i])

        differences.append(diff)

    return differences


def HackCaesarStep(data, alphabet) -> int:  # нужно оформить новую БД
    """
    Определяет шаг шифра Цезаря, применяя частотный анализ

    Input:  Текст (str)

    Output: Шаг шифра Цезаря (int)

    Note:   В бесплатной версии доступны только два языка, чтобы открыть остальные перейдите по ссылке: https://youtu.be/kC7-tW0QPJ4
    """

    if alphabet == 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
        frequency_rate = {'a': 0.0820, 'b': 0.0150, 'c': 0.0280, 'd': 0.0430, 'e': 0.1300, 'f': 0.0220, 'g': 0.0200,
                          'h': 0.0610, 'i': 0.0700, 'j': 0.0015, 'k': 0.0077, 'l': 0.0400, 'm': 0.0240, 'n': 0.0670,
                          'o': 0.0750, 'p': 0.0190, 'q': 0.0095, 'r': 0.0600, 's': 0.0630, 't': 0.0910, 'u': 0.0280,
                          'v': 0.0098, 'w': 0.0240, 'x': 0.0015, 'y': 0.0200, 'z': 0.0074}

    if alphabet == 'абвгдеёжзийклмнопрстуфхцчшщьыъэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ':
        frequency_rate = {'а': 0.0801, 'б': 0.0159, 'в': 0.0454, 'г': 0.0170, 'д': 0.0298, 'е': 0.0845, 'ё': 0.0004, 
                          'ж': 0.0094, 'з': 0.0165, 'и': 0.0735, 'й': 0.0121, 'к': 0.0349, 'л': 0.0440, 'м': 0.0321,
                          'н': 0.0670, 'o': 0.1097, 'п': 0.0281, 'р': 0.0473, 'с': 0.0547, 'т': 0.0626, 'у': 0.0262,
                          'ф': 0.0026, 'х': 0.0097, 'ц': 0.0048, 'ч': 0.0144, 'ш': 0.0073, 'щ': 0.0036, 'ъ': 0.0004,
                          'ы': 0.0190, 'ь': 0.0174, 'э': 0.0032, 'ю': 0.0064, 'я': 0.0201}

    our_frequency = {letter: data.casefold().count(letter) for letter in alphabet[0:len(alphabet) // 2]}

    num_of_letters = sum(our_frequency.values())
    for key in our_frequency.keys():
        our_frequency[key] /= num_of_letters

    differences = FrequencyAnalyzer(our_frequency, frequency_rate)
    step = differences.index(min(differences))

    return step
