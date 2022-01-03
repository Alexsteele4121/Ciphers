uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def shift_cipher(deciphered_text: str, key: int):
    ciphered_text = ''
    for char in list(deciphered_text):
        if char in uppercase:
            ciphered_text += uppercase[uppercase.index(char) - 26 + key]
        elif char in uppercase.lower():
            ciphered_text += uppercase.lower()[uppercase.lower().index(char) - 26 + key]
        else:
            ciphered_text += char
    return ciphered_text


if __name__ == '__main__':
    text = 'This is a test: zebra'
    key = 3
    print(shift_cipher(text, key))
