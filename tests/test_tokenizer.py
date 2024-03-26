import unittest

from src.tokenizer import Tokenizer


class TestTokenizer(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.tokenizer = Tokenizer()
        #Tokenizer.load_files("trained_vocab.txt", "trained_merges.txt")

    
    def test_hello_world(self):
        text = "Hello, world!"
        tokens = self.tokenizer.tokenize(text)
        self.assertEqual(tokens, ["Hello", ",", "world", "!"])

if __name__ == '__main__':
    unittest.main()