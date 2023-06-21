import unittest
from unittest.mock import patch

from aksara.tokenizers import AbstractTokenizer

# pylint: disable=E0110
class TestAbsractTokenizer(unittest.TestCase):
    """Test AbstrcatTokenizer class
    
    """

    def test_must_have_abstract_tokenize_method(self):
        self.assertTrue('tokenize' in AbstractTokenizer.__abstractmethods__)

    @patch.object(AbstractTokenizer, '__abstractmethods__', set())
    def test_override_abstract_tokenize(self):
        mock_instance = AbstractTokenizer()

        with self.assertRaises(NotImplementedError):
            mock_instance.tokenize('dummy')
