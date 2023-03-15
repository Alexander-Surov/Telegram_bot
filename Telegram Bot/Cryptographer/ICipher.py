class ICipher():
    def __init__(self, x, y):
        self.alphabet = y
        self.default_data = x
        self.data = "__no_cipher_methods_have_been_called__"


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
