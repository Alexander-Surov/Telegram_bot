from Cryptographer import ICipher as ic
from Cryptographer import utils_cg


class Vernam(ic.ICipher):
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
        default_data_copy = utils_cg.ConvertToNumbers(self.default_data)

        j = 0
        for i in range(len(default_data_copy)):
            if default_data_copy[i] != '\n':
                self.data += str(chr(default_data_copy[i] ^ ord(key_sequence[j])))
                j += 1
            else:
                self.data += '\n'


    def hack(self):
        self.data = "[TBD]"
