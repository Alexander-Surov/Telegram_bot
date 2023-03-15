import telebot
from telebot import types
import pandas as pd

from Cryptographer import Caesar_cipher as ca_c
from Cryptographer import Visener_cipher as vi_c
from Cryptographer import Vernam_cipher as ve_c

from api import utils_api


class TelegramBot():
    __menu = types.ReplyKeyboardMarkup(resize_keyboard=True).row('/cryptography', '/languages', '/help')
    __back = types.ReplyKeyboardMarkup(resize_keyboard=True).row('Return to menu')


    def __return_to_menu(self, message):
        """
        Возвращает пользователя в меню, выводя Emoji

        Note:   Ожидается, что после этой функции пользователь сам вызовет return
        """

        self.__bot.send_message(message.chat.id, "👌", reply_markup=self.__menu)


    def __delete_stuff_messages(self, previous_message, n):
        """ [TBD] """

        # Имеет смысл в __get_text отправлять сообщение с перечислением аргументов

        # for i in range(n):
        #     self.bot.delete_message(previous_message.chat.id, previous_message.message_id - n + i)


    def __init__(self, token, lang_address, rate_address):
        self.__bot = telebot.TeleBot(token)

        self.__lang_path = lang_address
        self.__rate_path = rate_address


        @self.__bot.message_handler(commands=['start'])
        def __process_start_command(message):

            hello_message = """Hello, I'm bot cryptographer!

                            I can encode, decode and even hack your data using 3 ciphers:
                            - Caesar (makes an alphabetical shift for each letter)
                            - Visener (makes a clever alphabetical shift)
                            - Vernam

                            I can also change my data base of languages.
                            It contains English and Russian by default.
                            """.replace(' ' * 28, '')

            pd.DataFrame(
                data=[['English', 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'],
                      ['Russian', 'абвгдеёжзийклмнопрстуфхцчшщьыъэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ']],
                columns=['language', 'alphabet']
            ).to_csv("Telegram Bot/languages.csv", index=False)

            self.__bot.send_message(message.chat.id, hello_message)
            self.__bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEICEtkBkHXD4V609-dZVHPTyeflb_tzQACBQADwDZPE_lqX5qCa011LgQ', reply_markup=self.__menu)


        @self.__bot.message_handler(commands=['cryptography'])
        def __process_chipher_command(message):
            """
            Отлавливает комманду /cryptography

            При вызове сообщает со сколькими шифрами и языками работает бот и выводит их названия по порядку.
            После перенаправляет в get_cipher для выбора шифра (1/5)

            Caesar - шифр Цезаря
            Visener - шифр Виженера
            Vernam - шифр Вернама

            Return to menu: отправляет в меню

            Note:   Если БД пуста, запустится процесс добавления нового языка (__get_lang_name);
                    Неправильный ввод перезапускает функцию
                    
            """

            languages = pd.read_csv(self.__lang_path)

            if len(languages.index) == 0:
                s = self.__bot.send_message(message.chat.id, "Oops, I don't know any langauge 😳\nIf you want to continue, you need to add at least one.\n\n⚙ Process of adding your first language was run automatically ⚙\n\n(1/2) Set the name for the language", reply_markup=self.__back)
                self.__bot.register_next_step_handler(s, self.__get_lang_name, 'Add')

            else:
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row('Caesar', 'Visener', 'Vernam', 'Return to menu')

                languages = pd.read_csv(self.__lang_path)

                if len(languages.index) == 1:
                    info_message = f"Only 1 language is available- {languages['language'].values[0]}"
                else:
                    info_message = f"{len(languages.index)} languages are available: " + ", ".join(languages['language'].values)

                s = self.__bot.send_message(message.chat.id, f"I know 3 ciphers: Caesar, Visener and Vernam\n{info_message}\n\n(1/5) Choose a cipher:", reply_markup=keyboard)
                self.__bot.register_next_step_handler(s, self.__get_cipher)


        @self.__bot.message_handler(commands=['languages'])
        def __process_language_command(message):
            """
            Отлавливает комманду /languages

            При вызове сообщает сколько языков есть в БД и выводит их названия по порядку.
            После перенаправляет в __process_language для выбора операции Add / Delete / View для БД языков по адресу __lang_address

            Add - добавить язык с алфавитом по названию
            Delete - удалить язык с алфавитом по названию
            View - см. __process_language

            Return to menu: отправляет в меню

            Note:   Неправильный ввод перезапускает функцию   
            """

            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row('View', 'Add', 'Delete', 'Return to menu')

            languages = pd.read_csv(self.__lang_path)

            if len(languages.index) == 0:
                info_message = "I don't know any language. It'd be nice if you could share some with me 😊"
            elif len(languages.index) == 1:
                info_message = f"I know only 1 language - {languages['language'].values[0]}"
            else:
                info_message = f"I know {len(languages.index)} languages: " + ", ".join(languages['language'].values)

            s = self.__bot.send_message(message.chat.id, info_message, reply_markup=keyboard)
            self.__bot.register_next_step_handler(s, self.__process_language)


        @self.__bot.message_handler(commands=['help'])
        def __process_help_command(message):

            help_message = """Hey! I'm here to help you :)

                           /cryptography - encodes, decodes and hacks text for you
                           /languages - shows languages the bot knows and allows to add new ones
                           """.replace(' ' * 27, '')

            self.__bot.send_message(message.chat.id, help_message, reply_markup=self.__menu)


    def run(self):
            """
            Запускает телеграм бота
            """

            self.__bot.polling()


    ### Cryptography ###
    def __get_cipher(self, message):
        """
        CIPHER -> mode--lang--arg--text

        Note:   Неправильный ввод перезапускает функцию 
        """

        if message.text in ['Caesar', 'Visener', 'Vernam']:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row('Encode', 'Decode', 'Hack', 'Return to menu')

            s = self.__bot.send_message(message.chat.id, "(2/5) Set mode:", reply_markup=keyboard)
            self.__bot.register_next_step_handler(s, self.__get_mode, message.text)

        elif message.text == 'Return to menu':
            self.__return_to_menu(message)

        else:
            s = self.__bot.send_message(message.chat.id, "I don't know such cipher. Please, try again", reply_markup=self.__back)
            self.__bot.register_next_step_handler(s, self.__get_cipher)


    def __get_mode(self, message, cipher):
        """
        cipher -> MODE -> lang--arg--text

        Note:   Неправильный ввод перезапускает функцию с тем же аргументом
        """

        languages = pd.read_csv(self.__lang_path)

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for lang in languages['language'].values:
            keyboard.add(lang)
        keyboard.add('Return to menu')

        if message.text in ['Encode', 'Decode', 'Hack']:
            s = self.__bot.send_message(message.chat.id, "(3/5) Set lang:", reply_markup=keyboard)
            self.__bot.register_next_step_handler(s, self.__get_lang, cipher, message.text)

        elif message.text == 'Return to menu':
            self.__return_to_menu(message)

        else:
            s = self.__bot.send_message(message.chat.id, "Wrong input. Please, try again", reply_markup=self.__back)
            self.__bot.register_next_step_handler(s, self.__get_mode, cipher)


    def __get_lang(self, message, cipher, mode):
        """
        cipher--mode -> LANG -> arg--text

        Note:   Пользователю доступен View (см. __process_language), после которого перезапускается функция с тем же аргументом;
                Если стоит режим Hack, то __get_arg будет автоматически пропущен;
                Неправильный ввод перезапускает функцию с теми же аргументами
        """

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row('View', 'Return to menu')

        languages = pd.read_csv(self.__lang_path)

        if message.text == 'View':
            msg = "· " + "\n· ".join([x[0] + " -> " + ' '.join([x[1][i].upper() + x[1][i] for i in range(len(x[1]) // 2)]) for x in pd.read_csv(self.__lang_path).values])

            s = self.__bot.send_message(message.chat.id, msg, reply_markup=keyboard)
            self.__bot.register_next_step_handler(s, self.__get_lang, cipher, mode)
            return

        if message.text == 'Return to menu':
            self.__return_to_menu(message)
            return

        if len(languages[languages['language'].isin([message.text])].values) == 1:
            if mode == 'Hack':
                s = self.__bot.send_message(message.chat.id, "(4-5/5) Set text:", reply_markup=types.ReplyKeyboardRemove())
                self.__bot.register_next_step_handler(s, self.__get_text, cipher, mode, message.text)

            else:
                s = self.__bot.send_message(message.chat.id, "(4/5) Set arg:", reply_markup=(types.ReplyKeyboardMarkup(resize_keyboard=True).row('Return to menu') if cipher == 'Caesar' else types.ReplyKeyboardRemove()))
                self.__bot.register_next_step_handler(s, self.__get_arg, cipher, mode, message.text)

        else:
            s = self.__bot.send_message(message.chat.id, "I don't know such language. Please, try again", reply_markup=keyboard)
            self.__bot.register_next_step_handler(s, self.__get_lang, cipher, mode)


    def __get_arg(self, message, cipher, mode, lang):
        """
        cipher--mode--lang -> ARG -> text

        Note:   Arg может быть как шагом для Цезаря, так и ключом / ключевой последовательностью для Виженера и Вернама;
                При шифре Цезаря возможно вернуться в меню ('Return to menu'), для остальных шифров любой текст будет восприниматься как ключ;
                Неправильный ввод шага для Цезаря (не цифра) перезапускает функцию с теми же аргументами
        """

        if message.text == 'Return to menu':
            self.__return_to_menu(message)
            return

        if cipher == 'Caesar' and not message.text.isdigit():
            s = self.__bot.send_message(message.chat.id, "Wrong input: number was expected, some cringe was found. Please, try again", reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True).add('Return to menu'))
            self.__bot.register_next_step_handler(s, self.__get_arg, cipher, mode, lang)

        else:
            s = self.__bot.send_message(message.chat.id, "(5/5) Set text:", reply_markup=types.ReplyKeyboardRemove())
            self.__bot.register_next_step_handler(s, self.__get_text, cipher, mode, lang, message.text)


    def __get_text(self, message, cipher, mode, lang, arg = None):
        """
        cipher--mode--lang--arg -> TEXT

        Note:   Неправильный ввод для расщифровки Вернама (см. IsCorrectEncodedVernam) перезапускает функцию с теми же аргументами;
                Если текст (для Цезаря) содержит буквы, отсутствующие в указанном алфавите, функция перезапускается с теми же аргументами
        """

        languages = pd.read_csv(self.__lang_path)

        if cipher == 'Caesar':
            if not utils_api.DoesBelongAlphabet(message.text, languages[languages['language'].isin([lang])]['alphabet'].values[0]):
                s = self.__bot.send_message(message.chat.id, "Wrong input: this text doen't belong to the alphabet. Please, try again", reply_markup=self.__back)
                self.__bot.register_next_step_handler(s, self.__get_text, cipher, mode, lang, arg)
                return

            processed_message = ca_c.Caesar(message.text, languages[languages['language'].isin([lang])]['alphabet'].values[0])

            if mode == 'Encode':
                processed_message.encode(int(arg))
            if mode == 'Decode':
                processed_message.decode(int(arg))
            if mode == 'Hack':
                step = processed_message.hack()
                self.__bot.send_message(message.chat.id, f"Found step is {step}. Hacked message:")

            self.__bot.send_message(message.chat.id, processed_message, reply_markup=self.__menu)

        if cipher == 'Visener':
            processed_message = vi_c.Visener(message.text, languages[languages['language'].isin([lang])]['alphabet'].values[0])

            if mode == 'Encode':
                processed_message.encode(arg)
            if mode == 'Decode':
                processed_message.decode(arg)
            if mode == 'Hack':
                processed_message.hack()

            self.__bot.send_message(message.chat.id, processed_message, reply_markup=self.__menu)

        if cipher == 'Vernam':
            if not utils_api.IsCorrectEncodedVernam(message.text):
                s = self.__bot.send_message(message.chat.id, "Wrong input: numbers and whitespaces were expected, some cringe was found. Please, try again", reply_markup=self.__back)
                self.__bot.register_next_step_handler(s, self.__get_text, cipher, mode, lang, arg)
                return

            processed_message = ve_c.Vernam(message.text, languages[languages['language'].isin([lang])]['alphabet'].values[0])

            if mode == 'Encode':
                processed_message.encode(arg)
            if mode == 'Decode':
                processed_message.decode(arg)
            if mode == 'Hack':
                processed_message.hack()

            self.__bot.send_message(message.chat.id, processed_message, reply_markup=self.__menu)


    ### Language ###
    def __process_language(self, message):
        """
        Определяет операцию Add / Delete / View для БД языков по адресу __lang_address

        View:   выводит все языки из БД с алфавитами вида: English -> Aa Bb Cc...
        Add:    перенаправляет в __get_lang_name для выбора языка с параметром 'Add' (1/2)
        Delete: перенаправляет в __get_lang_name для выбора языка с параметром 'Delete'

        Return to menu: отправляет в меню

        Note:   Неправильный ввод перезапускает функцию
        """

        if message.text == 'Return to menu':
            self.__return_to_menu(message)
            return

        if message.text == 'View':
            msg = "· " + "\n· ".join([x[0] + " -> " + ' '.join([x[1][i].upper() + x[1][i] for i in range(len(x[1]) // 2)]) for x in pd.read_csv(self.__lang_path).values])

            self.__bot.send_message(message.chat.id, msg, reply_markup=self.__menu)

        elif message.text == 'Add':
            s = self.__bot.send_message(message.chat.id, "(1/2) Set the name for the language", reply_markup=self.__back)
            self.__bot.register_next_step_handler(s, self.__get_lang_name, 'Add')

        elif message.text == 'Delete':
            languages = pd.read_csv(self.__lang_path)

            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            for lang in languages['language'].values:
                keyboard.add(lang)
            keyboard.add('Return to menu')

            s = self.__bot.send_message(message.chat.id, "Put the name of the language to delete", reply_markup=keyboard)
            self.__bot.register_next_step_handler(s, self.__get_lang_name, 'Delete')

        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row('View', 'Add', 'Delete', 'Return to menu')

            s = self.__bot.send_message(message.chat.id, "Wrong input. Please, try again", reply_markup=keyboard)
            self.__bot.register_next_step_handler(s, self.__process_language)


    def __get_lang_name(self, message, mode):
        """
        Определяет название языка для Add / Delete

        Add:    перенаправляет в __get_lang_alphabet для ввода алфавита (2/2)
        Delete: удаляет язык по названию из БД по адресу __lang_address

        Return to menu: отправляет в меню

        Note:   В аргументы передаётся имя операции: 'Add' или 'Delete';
                Пользователю доступен View (см. __process_language), после которого перезапускается функция с тем же аргументом;
                Проводится проверка на отсутствие / наличие языка для операций Add / Delete - соответственно;
                Неправильный ввод перезапускает функцию с тем же аргументом
        """

        languages = pd.read_csv(self.__lang_path)

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row('View', 'Return to menu')

        if message.text == 'View':
            if len(languages.index) == 0:
                info_message = "I don't know any language. It'd be nice if you could share some with me 😊"
            elif len(languages.index) == 1:
                info_message = f"I know only 1 language - {languages['language'].values[0]}"
            else:
                info_message = f"I know {len(languages.index)} languages: " + ", ".join(languages['language'].values)

            if mode == 'Add':
                msg = "(1/2) Set the name for the language"
            if mode == 'Delete':
                msg = "Put the name of the language to delete"

            s = self.__bot.send_message(message.chat.id, info_message + '\n' + msg, reply_markup=self.__back)
            self.__bot.register_next_step_handler(s, self.__get_lang_name, mode)
            return

        if message.text == 'Return to menu':
            self.__return_to_menu(message)
            return

        if mode == 'Add':
            if len(languages[languages['language'].isin([message.text])].values) == 0:
                s = self.__bot.send_message(message.chat.id, f"(2/2) (no blanks) Set the alphabet for \'{message.text}\'", reply_markup=self.__back)
                self.__bot.register_next_step_handler(s, self.__get_lang_alphabet, message.text)

            else:
                s = self.__bot.send_message(message.chat.id, "I already know such language. Please, try again", reply_markup=keyboard)
                self.__bot.register_next_step_handler(s, self.__get_lang_name, mode)

        if mode == 'Delete':
            if len(languages[languages['language'].isin([message.text])].values) == 1:
                languages[languages['language'].values != message.text].to_csv(self.__lang_path, index=False)
                self.__bot.send_message(message.chat.id, f"Language \'{message.text}\' was deleted", reply_markup=self.__menu)

            else:
                s = self.__bot.send_message(message.chat.id, "I don't know such language. Please, try again", reply_markup=keyboard)
                self.__bot.register_next_step_handler(s, self.__get_lang_name, mode)


    def __get_lang_alphabet(self, message, lang):
        """
        Получает алфавит для Add и записывает новый язык в БД по адресу __lang_address

        Return to menu: отправляет в меню

        Note:   Алфавит должен состоять из неповторяющихся символов-букв (isalpha);
                В БД лежит строка вида: English, a..zA..Z;
                Неправильный ввод перезапускает функцию с теми же аргументами
        """

        if message.text == 'Return to menu':
            self.__return_to_menu(message)
            return

        if not utils_api.IsAlphabet(message.text):
            s = self.__bot.send_message(message.chat.id, "Wrong input. Please, try again", reply_markup=self.__back)
            self.__bot.register_next_step_handler(s, self.__get_lang_alphabet, lang)
        
        else:
            pd.concat([pd.read_csv(self.__lang_path), pd.DataFrame({'language': [lang], 'alphabet': [utils_api.NormalizeAlphabet(message.text)]})]).to_csv(self.__lang_path, index=False)

            self.__bot.send_message(message.chat.id, f"Language \'{lang}\' was added", reply_markup=self.__menu)


    def __get_lang_frq_rate(self, message, lang):
        """ [TBD] """
        pass
