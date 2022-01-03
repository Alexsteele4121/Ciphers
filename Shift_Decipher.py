import enchant  # pip install pyenchant==3.2.2


class Shift_Solver:
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __init__(self, ciphered_text: str, dictionary: str = 'en_US'):
        self.ciphered_text = ciphered_text
        self.options = self.create_options()
        self.dictionary = enchant.Dict(dictionary)

    def create_options(self):
        results = []
        for key in range(1, 27):
            deciphered_text = ''
            for char in list(self.ciphered_text):
                if char in self.uppercase:
                    deciphered_text += self.uppercase[self.uppercase.index(char) - key]
                elif char in self.uppercase.lower():
                    deciphered_text += self.uppercase.lower()[self.uppercase.lower().index(char) - key]
                else:
                    deciphered_text += char
            results.append((deciphered_text, key))
        return results

    def start(self):
        results = []
        for option in self.options:
            separate_words = [word.strip(',')
                                  .strip('.')
                                  .strip('?')
                                  .strip('!')
                                  .strip(':') for word in option[0].split(' ')]
            dictionary_check = []
            for word in separate_words:
                if word:
                    dictionary_check.append(self.dictionary.check(word))
            results.append((dictionary_check.count(True) / len(dictionary_check) * 100, option[0], option[1]))

        best_guess = sorted(results, key=lambda x: x[0], reverse=True)[0]
        print(f'Best guess with {best_guess[0]}% accuracy:', best_guess[1])
        print('Key:', best_guess[2])


if __name__ == '__main__':
    text = 'Wklv lv d whvw: cheud'
    solver = Shift_Solver(text)
    solver.start()
