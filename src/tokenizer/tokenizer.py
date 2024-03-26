import re
from collections import defaultdict, Counter
import torch


class BPETokenizer:
    def __init__(
            self, 
            max_len=512,
            target_vocab_size = 50257,
            vocab_file = None,
            merges_file = None
        ):
        
        self.max_len = max_len
        self.target_vocab_size = target_vocab_size
        self.vocab_file = vocab_file
        self.merges_file = merges_file
        self.vocab = defaultdict(int)

        if vocab_file and merges_file:
            self.load_files(vocab_file, merges_file)
        else:
            Warning("No vocab and merges files provided. Training tokenizer from scratch.")
                
    
    def load_files(vocab_file: str , merges_file: str) -> None:
        raise NotImplementedError


    def save_files(self, vocab_file: str, merges_file: str) -> None:
        raise NotImplementedError
    
    
    def tokenize(self, text: str) -> list[str]:
        words = text.split()
        tokens = []
        for word in words:
            tokens += self.tokenize_word(word)
        return tokens


    def tokenize_word(self, word: str) -> list[str]:
        word = word + '</w>'
        pairs = self.get_pairs(word)

        if not pairs:
            return [word]

        while True:
            bigram = max(pairs, key=pairs.get)
            if bigram in self.word_ends:
                break

            first, second = bigram
            new_word = []
            i = 0
            while i < len(word):
                try:
                    j = word.index(first, i)
                    new_word.extend(word[i:j])
                    i = j
                except:
                    new_word.extend(word[i:])
                    break

                try:
                    i = word.index(second, i) + 1
                except:
                    new_word.append(first)
                    i += 1
                    continue

                new_word.append(first + second)

            word = ''.join(new_word)
            pairs = self.get_pairs(word)

        word = word.replace('</w>', '')
        tokens = [token for token in word.split(' ') if token]
        return tokens


    def get_pairs(self, word: str) -> dict[tuple[str, str], int]:
        pairs = defaultdict(int)
        prev_char = word[0]
        for char in word[1:]:
            pairs[prev_char, char] += 1
            prev_char = char
        return pairs


    def train(self, texts: list[str]) -> None:
        vocab = Counter()
        for text in texts:
            tokens = self.tokenize(text)
            vocab.update(tokens)

        self.vocab = {token: idx for idx, (token, count) in enumerate(
            vocab.most_common(self.vocab_size))}
        self.vocab.update({token: len(self.vocab) for token in self.word_ends})


    def encode(self, text: str) -> list[int]:
        tokens = self.tokenize(text)
        return [self.vocab.get(token, len(self.vocab)) for token in tokens]


    def decode(self, tokens: list[int]) -> str:
        text = ''.join([self.rev_vocab[token] for token in tokens])
        text = re.sub(r'(/w>)', '', text)
        return text
