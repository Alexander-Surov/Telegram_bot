import utils


class ICipher():
    def __init__(self, x, y):
        self.alphabet = y
        self.default_data = x
        self.data = "__no_cipher_methods_were_called__"


    def __repr__(self) -> str:
        return self.data


    def __call__(self) -> str:
        return f"The text:\t\t\"{self.default_data}\"\nWas turned into:\t\"{self.data}\"\nUsing the alphabet:\t\"{self.alphabet[0:len(self.alphabet) // 2]}\""


    def encode(self, arg) -> None:
        pass
    def decode(self, arg) -> None:
        pass
    def hack(self) -> None:
        pass


class Caesar(ICipher):
    def encode(self, step):
        self.data = ""
        n = len(self.alphabet) / 2

        for i in range(len(self.default_data)):
            if self.default_data[i] in self.alphabet:
                self.data += self.alphabet[int((self.alphabet.index(self.default_data[i]) + step) % n + (n if self.alphabet.index(self.default_data[i]) > n - 1 else 0))]
            else:
                self.data += self.default_data[i]


    def decode(self, step):
        self.encode(-step)


    def hack(self):
        step = utils.HackCaesarStep(self.default_data, self.alphabet)
        self.decode(step)
        return step


class Visener(ICipher):
    def encode(self, arg):
        key_sequence = (arg.lower() * ((len(self.default_data) - 1) // len(arg) + 1))[0:len(self.default_data)]

        self.data = ""
        n = len(self.alphabet) / 2

        j = 0
        for i in range(len(self.default_data)):
            if self.default_data[i] in self.alphabet:
                self.data += self.alphabet[int((self.alphabet.index(self.default_data[i]) % n + self.alphabet.index(key_sequence[j])) % n + (n if self.alphabet.index(self.default_data[i]) > n - 1 else 0))]
                j += 1
            else:
                self.data += self.default_data[i]


    def decode(self, arg):
        key_sequence = (arg.lower() * ((len(self.default_data) - 1) // len(arg) + 1))[0:len(self.default_data)]

        self.data = ""
        n = len(self.alphabet) / 2

        j = 0
        for i in range(len(self.default_data)):
            if self.default_data[i] in self.alphabet:
                self.data += self.alphabet[int((-1) * (self.alphabet.index(self.default_data[i]) % n + self.alphabet.index(key_sequence[j])) % n + (n if self.alphabet.index(self.default_data[i]) > n - 1 else 0))]
                j += 1
            else:
                self.data += self.default_data[i]


    def hack(self, arg):
        self.data = "[TBD]"


class Vernam(ICipher):
    def encode(self, arg):
        key_sequence = (arg * ((len(self.default_data) - 1) // len(arg) + 1))[0:len(self.default_data)]

        self.data = ""
        default_data_copy = self.default_data + '\n'

        j = 0
        for i in range(len(default_data_copy) - 1):
            if default_data_copy[i] != '\n':
                self.data += str(ord(default_data_copy[i]) ^ ord(key_sequence[j])) + (' ' if default_data_copy[i + 1] != '\n' else '')
                j += 1
            else:
                self.data += '\n'


    def decode(self, arg):
        key_sequence = (arg * ((len(self.default_data) - 1) // len(arg) + 1))[0:len(self.default_data)]

        self.data = ""
        default_data_copy = utils.ConvertToNumbers(self.default_data)

        j = 0
        for i in range(len(default_data_copy)):
            if default_data_copy[i] != '\n':
                self.data += str(chr(default_data_copy[i] ^ ord(key_sequence[j])))
                j += 1
            else:
                self.data += '\n'


    def hack(self):
        self.data = "[TBD]"
