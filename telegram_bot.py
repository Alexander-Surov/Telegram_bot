import telebot
from telebot import types

import pandas as pd

from pathlib import Path

import cryptographer as cg

import utils


class Telegram_Bot():
    bot = telebot.TeleBot(Path("Telegram Bot/Token.txt").read_text())

    lang_address = "Telegram Bot/languages.csv"

    menu = types.ReplyKeyboardMarkup(resize_keyboard=True).row('/cryptography', '/languages')
    back = types.ReplyKeyboardMarkup(resize_keyboard=True).row('Return to menu')


    def back_to_menu(self, message):
        """ Возвращает пользователя в меню, выводя Emoji """

        self.bot.send_message(message.chat.id, "👌", reply_markup=self.menu)


    def __init__(self):
        @self.bot.message_handler(commands=['start'])
        def process_start_command(message):

            hello_message = """Hello, I'm bot cryptographer\n \
            ...
            """# этот backslash ничего не меняет: есть сдвиг

            self.bot.send_message(message.chat.id, hello_message)
            self.bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEICEtkBkHXD4V609-dZVHPTyeflb_tzQACBQADwDZPE_lqX5qCa011LgQ', reply_markup=self.menu)


        @self.bot.message_handler(commands=['cryptography'])
        def process_chipher_command(message):
            """ ...
            """

            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
                types.KeyboardButton(text='Caesar'),
                types.KeyboardButton(text='Visener'),
                types.KeyboardButton(text='Vernam'),
                types.KeyboardButton(text='Return to menu')
            )

            s = self.bot.send_message(message.chat.id, "(1/5) Choose a cipher:", reply_markup=keyboard)
            self.bot.register_next_step_handler(s, self.get_cipher)


        @self.bot.message_handler(commands=['languages'])
        def process_language_command(message):
            """ ...
            """

            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row('View', 'Add', 'Delete', 'Return to menu')

            languages = pd.read_csv(self.lang_address)

            if len(languages.index) == 0:
                info_message = "I don't know any language. Please, share some with me 👉 👈"
            elif len(languages.index) == 1:
                info_message = f"I know only 1 language - {languages['language'].values[0]}"
            else:
                info_message = f"I know {len(languages.index)} languages:\n· " + "\n· ".join(languages['language'].values)

            s = self.bot.send_message(message.chat.id, info_message, reply_markup=keyboard)
            self.bot.register_next_step_handler(s, self.process_language)


        @self.bot.message_handler(commands=['help'])
        def process_help_command(message):

            help_message = """Hey! I'm here to help you\n\

            /cryptography - encodes and decodes text for you\n\
            /languages    - shows languages the bot knows or allows to add new ones
            """

            self.bot.send_message(message.chat.id, help_message, reply_markup=self.menu)


    ### Language ###
    def process_language(self, message):
        """ ...
        """

        if message.text == 'View':
            languages = pd.read_csv(self.lang_address)

            msg = "· " + "\n· ".join([x[0] + " -> " + ' '.join([x[1][i].upper() + x[1][i] for i in range(len(x[1]) // 2)]) for x in languages.values])

            self.bot.send_message(message.chat.id, msg, reply_markup=self.menu)

        elif message.text == 'Add':
            s = self.bot.send_message(message.chat.id, "(1/2) Set name for the language", reply_markup=self.back)
            self.bot.register_next_step_handler(s, self.get_lang_name, 'Add')

        elif message.text == 'Delete':
            s = self.bot.send_message(message.chat.id, "Put name of the language to delete", reply_markup=self.back)
            self.bot.register_next_step_handler(s, self.get_lang_name, 'Delete')

        elif message.text == 'Return to menu':
            self.back_to_menu(message)

        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).row('View', 'Add', 'Delete', 'Return to menu')

            s = self.bot.send_message(message.chat.id, "Wrong input. Please, try again", reply_markup=keyboard)
            self.bot.register_next_step_handler(s, self.process_language)


    def get_lang_name(self, message, mode):
        """ ...
        """

        languages = pd.read_csv(self.lang_address)

        if message.text == 'Return to menu':
            self.back_to_menu(message)

        if len(languages[languages['language'].values == message.text].values) != 0:
            s = self.bot.send_message(message.chat.id, "Wrong input. Please, try again", reply_markup=self.back)
            self.bot.register_next_step_handler(s, self.get_lang_name, mode)
            return

        if mode == 'Add':
            s = self.bot.send_message(message.chat.id, f"(2/2) Set alphabet for \'{message.text}\' (no blanks)", reply_markup=self.back)
            self.bot.register_next_step_handler(s, self.get_lang_alphabet, message.text)

        if mode == 'Delete':
            languages = languages[languages['language'].values != message.text]
            languages.to_csv(self.lang_address, index=False)

            self.bot.send_message(message.chat.id, f"Language \'{message.text}\' was deleted", reply_markup=self.menu)


    def get_lang_alphabet(self, message, name):
        """ ...
        """

        if not utils.is_alphabet(message.text):
            s = self.bot.send_message(message.chat.id, "Wrong input. Please, try again", reply_markup=self.back)
            self.bot.register_next_step_handler(s, self.get_lang_alphabet, name)
            return

        languages = pd.read_csv(self.lang_address)
        pd.concat([languages, pd.DataFrame({'language': [name], 'alphabet': [utils.normalize_alphabet(message.text)]})]).to_csv(self.lang_address, index=False)

        self.bot.send_message(message.chat.id, f"Language \'{name}\' was added", reply_markup=self.menu)
        

Telegram_Bot().bot.polling()
