def transposition_cipher(text: str, key: list) -> str:
    ciphering_key = [key.index(i + 1) + 1 for i in range(len(key))]
    deciphered_text = text
    ciphered_text = ''

    while len(deciphered_text) % len(ciphering_key):
        deciphered_text += ' '

    for start_pos in range(0, len(deciphered_text), len(ciphering_key)):
        for i in ciphering_key:
            ciphered_text += deciphered_text[start_pos + i - 1]
    return ciphered_text


if __name__ == '__main__':
    text = 'You can never catch the Alphabet Bandit, My next Target is Calvins House'
    key = [3, 4, 1, 2, 5, 6]
    print(transposition_cipher(text, key))
