from Cryptographer import ICipher as ic
from Cryptographer import utils_cg


class Caesar(ic.ICipher):
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
        step = utils_cg.HackCaesarStep(self.default_data, self.alphabet)
        self.decode(step)
        return step
