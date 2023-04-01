#################################################################################
# Class ConlluData
#
# represents a token (a row of 10 columns) in CoNLLU format
#
# Author: Ika Alfina (ika.alfina@cs.ui.ac.id)
#
#################################################################################

"""
Class Wrapper for ConLLU format 
"""


class ConlluData:
    """
    A class to represent a token or a row in CoNLLU format defined in 
    here: https://universaldependencies.org/format.html
    """

    def __init__(self, idx: str, form: str = "_",
                 lemma: str = '_', upos: str = '_',
                 xpos: str = '_', feat: str = '_',
                 head_id: str = '_', deprel: str = '_'):
        """
        Initialize ConnlluData
        """

        self.__idx = idx  # colomn 1
        self.__lemma = lemma  # colomn 2
        self.__form = form  # colomn 3
        self.__upos = upos  # colomn 4
        self.__xpos = xpos  # colomn 5
        self.__feat = feat  # colomn 6
        self.__head_id = head_id  # colomn 7
        self.deprel = deprel  # colomn 8

    def get_id(self) -> str:
        """id getter"""

        return self.__idx

    def get_lemma(self) -> str:
        """lemma getter"""

        return self.__lemma

    def get_form(self) -> str:
        """form getter"""

        return self.__form

    def get_upos(self) -> str:
        """upos getter"""

        return self.__upos

    def get_xpos(self) -> str:
        """xpos getter"""

        return self.__xpos

    def get_feat(self) -> str:
        """feat getter"""

        return self.__feat

    def get_head_id(self) -> str:
        """head_id getter"""

        return self.__head_id

    def get_deprel(self) -> str:
        """dependency relation(deprel) getter"""

        return self.deprel

    def get_conllu_str(self) -> str:
        """ConnluData string representation"""

        the_string = self.__idx + "\t" + self.__form + "\t" + self.__lemma + "\t" + \
                     self.__upos + "\t" + self.__xpos + "\t" + self.__feat + "\t" + \
                     self.__head_id + "\t" + self.deprel + "\t" + "_" + "\t" + "_"

        return the_string

    def __str__(self) -> str:
        return self.get_conllu_str()

    # -------------------------
    # changing value

    def set_form(self, form: str):
        """form setter"""

        self.__form = form

    def set_lemma(self, lemma: str):
        """lemma setter"""

        self.__lemma = lemma

    def set_upos(self, upos: str):
        """upos setter"""

        self.__upos = upos

    def set_feat(self, feat: str):
        """feat setter"""

        self.__feat = feat

    def set_head_id(self, head_id: str):
        """set self.head_id to head_id"""

        self.__head_id = head_id

    def set_deprel(self, deprel):
        """Dependency relation setter"""

        self.deprel = deprel

    def __eq__(self, other):
        """check if 2 objects of ConlluData have the same attributes"""
        if isinstance(other, ConlluData):
            return (
                    self.__idx == other.get_id()
                    and self.__lemma == other.get_lemma()
                    and self.__form == other.get_form()
                    and self.__upos == other.get_upos()
                    and self.__xpos == other.get_xpos()
                    and self.__feat == other.get_feat()
                    and self.__head_id == other.get_head_id()
                    and self.deprel == other.get_deprel()
            )

        return False
