from queue import Queue
from threading import Thread
from time import sleep
import enchant  # pip install pyenchant==3.2.2
from itertools import permutations


class Transposition_Solver:

    def __init__(self, ciphered_text: str, dictionary: str = 'en_US', target_accuracy: float = 90.0,
                 start_depth: int = 2, end_depth: int = 9, thread_count: int = 1, buffer: int = 100):
        """
        This object is designed to find the key of any transposition cipher by testing if the result
        of the deciphered text forms words belonging in the language selected (default is US english).
        :param ciphered_text: Ciphered text.
        :param dictionary: What language / region do you want to test the results against.
        :param target_accuracy: At what accuracy should the program stop. If the accuracy is never reached the program
                                will try every key and spit out the best result.
        :param start_depth: What depth should the key start at? A depth of 2 would be (1, 2)
        :param end_depth: What depth should the key end at? A depth of 9 would be (9, 8, 7, 6, 5, 4, 3, 2, 1)
        :param thread_count: How many threads the program will run on. Must have at least one.
        :param buffer: How many keys are kept in memory for every thread.
        """
        self.key_queue = Queue()
        self.ciphered_text = ciphered_text
        self.dictionary = enchant.Dict(dictionary)
        self.target_accuracy = target_accuracy
        self.start_depth = start_depth if start_depth >= 2 else 2  # Start depth can't be less than 2
        self.end_depth = end_depth if end_depth >= self.start_depth else self.start_depth
        self.options = self.create_options()
        self.thread_count = thread_count if thread_count >= 1 else 1
        self.buffer = buffer if buffer >= 1 else 1
        self.end = False
        self.threads = []
        self.approval_queue = Queue()
        self.best_option = (None, 0.0, '')  # (key, accuracy, result)

    def create_options(self):
        """
        This function creates a generator object that returns every permutation of key within start and end depth.
        """
        for i in range(self.start_depth, self.end_depth + 1):
            for option in permutations(list(range(1, i + 1))):
                yield option

    def test_combination(self):
        """
        This is the code all the threads will be running, trying to determine what the best key might be.
        """
        while not self.end:  # Used as a fail-safe encase the threads operate faster than the core
            while not self.key_queue.empty() and not self.end:
                key = self.key_queue.get()
                ciphered_text = self.ciphered_text
                while len(ciphered_text) % len(key):
                    ciphered_text += ' '
                deciphered_text = ''
                for start_pos in range(0, len(ciphered_text), len(key)):
                    for i in key:
                        deciphered_text += ciphered_text[start_pos + i - 1]
                separate_words = [word.strip(',')
                                      .strip('.')
                                      .strip('?')
                                      .strip('!') for word in deciphered_text.split(' ')]
                results = []
                for word in separate_words:
                    if word:
                        results.append(self.dictionary.check(word))
                accuracy = sum(results) / len(results) * 100
                if accuracy >= self.best_option[1]:
                    self.approval_queue.put((key, accuracy, deciphered_text))
            sleep(.0001)

    def start(self):
        """
        This is the core of the class object. Opens and closes threads while also providing a flow of new keys
        for the threads to try.
        """
        for _ in range(self.thread_count * 100):
            try:
                self.key_queue.put(next(self.options))
            except StopIteration:
                break

        for _ in range(self.thread_count):
            self.threads.append(Thread(target=self.test_combination))
            self.threads[-1].start()

        try:
            for count, option in enumerate(self.options):
                while self.key_queue.qsize() >= self.thread_count * 100 and not self.end:
                    sleep(.0001)
                if self.end:
                    break
                self.key_queue.put(option)
                if count % 100 == 0:
                    print(f'\rCurrent Attempt: {count}\tCurrent best: {round(self.best_option[1], 2)}%', end='')
                while self.approval_queue.qsize():
                    contender = self.approval_queue.get()
                    if contender[1] >= self.best_option[1]:
                        self.best_option = contender
                if self.best_option[1] >= self.target_accuracy:
                    self.end = True
                    print(f'\rWith {round(self.best_option[1], 2)}% accuracy:', self.best_option[2])
                    print(f'Key: {self.best_option[0]}')
                    break
        except KeyboardInterrupt:
            print('\rKeyboard Interrupt. Killing threads and exiting.')

        if not self.end:
            self.end = True
            print(f'\rProgram finished. Best result found with {round(self.best_option[1], 2)}% accuracy:',
                  self.best_option[2])
            print('Key:', self.best_option[0])


if __name__ == '__main__':
    text = "u Yocanen vecar tcthh e phAlab Betant,di Mney xtar Tgeist  Cvialnsou Hse"
    solver = Transposition_Solver(text, thread_count=1, target_accuracy=90.0)
    solver.start()
