import unittest

class TokenizerTestSetUp(unittest.TestCase):
    """
    Set up input and expected output for 
    base_tokenize and multiword_tokenize unit test
    """

    def setUp(self) -> None:
        self.one_sentence = "Ani suka apel."
        self.expected_one_sentence = ["Ani", "suka", "apel", "."]

        self.multiple_sentence = self.one_sentence + "Beni suka tidur"
        self.expected_multiple_sentence = self.expected_one_sentence + \
                                            ["Beni", "suka", "tidur"]

        self.multiword_input = "biarlah saja"
        return super().setUp()
