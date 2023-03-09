from Cryptographer import ICipher as ic


class Visener(ic.ICipher):
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
