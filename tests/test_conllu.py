import unittest

from aksara.conllu import ConlluData

class ConlluTest(unittest.TestCase):
    """Test Conllu Data"""

    def setUp(self) -> None:
        self.connlu_data = ConlluData(idx='1', form="berjalan", lemma="jalan",
                                      upos="VERB", xpos='_', feat='Voice=Act',
                                      head_id='0', deprel='root')

        return super().setUp()

    def test_constructor(self):
        self.assertEqual(self.connlu_data.get_id(), '1')
        self.assertEqual(self.connlu_data.get_form(), "berjalan")
        self.assertEqual(self.connlu_data.get_lemma(), "jalan")
        self.assertEqual(self.connlu_data.get_upos(), "VERB")
        self.assertEqual(self.connlu_data.get_xpos(), "_")
        self.assertEqual(self.connlu_data.get_feat(), "Voice=Act")
        self.assertEqual(self.connlu_data.get_head_id(), '0')
        self.assertEqual(self.connlu_data.get_deprel(), 'root')

    def test_setter_getter(self):
        new_form = 'jalan'
        new_lemma = 'jalan'
        new_upos = 'NOUN'
        new_feat = 'Number=Sing'
        new_head_id = '0'
        new_deprel = 'root'

        self.connlu_data.set_form(new_form)
        self.connlu_data.set_lemma(new_lemma)
        self.connlu_data.set_upos(new_upos)
        self.connlu_data.set_feat(new_feat)
        self.connlu_data.set_head_id(new_head_id)
        self.connlu_data.set_deprel(new_deprel)

        self.assertEqual(self.connlu_data.get_id(), '1')
        self.assertEqual(self.connlu_data.get_form(), new_form)
        self.assertEqual(self.connlu_data.get_lemma(), new_lemma)
        self.assertEqual(self.connlu_data.get_upos(), new_upos)
        self.assertEqual(self.connlu_data.get_xpos(), "_")
        self.assertEqual(self.connlu_data.get_feat(), new_feat)
        self.assertEqual(self.connlu_data.get_head_id(), new_head_id)
        self.assertEqual(self.connlu_data.get_deprel(), new_deprel)

    def test_default_underscore_value(self):
        default_val_connlu = ConlluData('1', head_id='0')

        self.assertEqual(default_val_connlu.get_id(), '1')
        self.assertEqual(default_val_connlu.get_form(), '_')
        self.assertEqual(default_val_connlu.get_lemma(), '_')
        self.assertEqual(default_val_connlu.get_upos(), '_')
        self.assertEqual(default_val_connlu.get_xpos(), '_')
        self.assertEqual(default_val_connlu.get_feat(), '_')
        self.assertEqual(default_val_connlu.get_head_id(), '0')
        self.assertEqual(default_val_connlu.get_deprel(), '_')

    def test_get_conllu_str_and__str__must_be_the_same(self):
        self.assertEqual(str(self.connlu_data), self.connlu_data.get_conllu_str())

    def test_get_connllu_str_should_replace_missing_column_with_underscore(self):
        all_default = ConlluData(idx='1', head_id='0')

        num_of_underscore = all_default.get_conllu_str().count('_')
        max_conllu_underscore = 6  # id and headID must not be null
        self.assertGreaterEqual(num_of_underscore, max_conllu_underscore)

    def test_two_conllu_is_equal_if_have_same_attributes(self):
        other_conllu = ConlluData(idx='1', form="berjalan", lemma="jalan",
                                  upos="VERB", xpos='_', feat='Voice=Act',
                                  head_id='0', deprel='root')
        self.assertEqual(self.connlu_data, other_conllu)

    def test_two_conllu_is_not_equal_if_do_not_have_same_attributes(self):
        other_conllu = ConlluData(idx='1', form="jalan", lemma="jalan",
                                  upos="VERB", xpos='_', feat='_',
                                  head_id='0', deprel='root')
        self.assertNotEqual(self.connlu_data, other_conllu)

    def test_conllu_is_not_equal_with_non_conllu(self):
        self.assertNotEqual(self.connlu_data, "")

    def test_multiword_token(self):
        multi_word_conllu = ConlluData(idx='1-2', head_id='0')

        self.assertEqual(multi_word_conllu.get_id(), '1-2')
