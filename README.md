# Summary

Aksara is an Indonesian NLP tool that conforms to the [Universal Dependencies (UD) v2](https://universaldependencies.org/) annotation guidelines. Aksara can perform four tasks:
* Word segmentation (tokenization)
* Lemmatization
* POS tagging
* Morphological features analysis

The output is in the [CoNLL-U format](https://universaldependencies.org/format.html).

# Installation

1. Clone this [repository](https://github.com/ir-nlp-csui/aksara). `git clone https://github.com/ir-nlp-csui/aksara`

1. Install [Foma](https://fomafst.github.io/). For Debian/Ubuntu packaging, `apt-get install foma-bin`. Make sure you have the privilege to install package or use `sudo`.

1. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required packages (it is recommended to use virtual environment to avoid dependency conflicts).

    ```console
    foo@bar:~$ cd aksara
    foo@bar:~/aksara$ python3 -m pip install -r requirements.txt
    ```

    If [pip](https://pip.pypa.io/en/stable/) is not installed, please install pip first. `apt-get install python3-pip`

# Usage

Use console with `aksara.py`.

Example to process formal Indonesian text:
```console
foo@bar:~/aksara$ python3 aksara.py -s "Pengeluaran baru ini dipasok oleh rekening bank gemuk Clinton."
# sent_id = 1
# text = Pengeluaran baru ini dipasok oleh rekening bank gemuk Clinton.
1	Pengeluaran	keluar	NOUN	_	Number=Sing	_	_	_	Morf=peN+keluar<VERB>+an_NOUN
2	baru	baru	ADJ	_	_	_	_	_	Morf=baru<ADJ>_ADJ
3	ini	ini	DET	_	PronType=Dem	_	_	_	Morf=ini<DET>_DET
4	dipasok	pasok	VERB	_	Voice=Pass	_	_	_	Morf=di+pasok<VERB>_VERB
5	oleh	oleh	ADP	_	_	_	_	_	Morf=oleh<ADP>_ADP
6	rekening	rekening	NOUN	_	Number=Sing	_	_	_	Morf=rekening<NOUN>_NOUN
7	bank	bank	NOUN	_	Number=Sing	_	_	_	Morf=bank<NOUN>_NOUN
8	gemuk	gemuk	ADJ	_	_	_	_	_	Morf=gemuk<ADJ>_ADJ
9	Clinton	Clinton	PROPN	_	_	_	_	_	Morf=Clinton<PROPN>_PROPN
10	.	.	PUNCT	_	_	_	_	_	Morf=.<PUNCT>_PUNCT

```

Example to process informal Indonesian text:
```console
foo@bar:~/aksara$ python3 aksara.py -s "Sering ngikutin gayanya lg nyanyi." --informal
# sent_id = 1
# text = Sering ngikutin gayanya lg nyanyi.
1	Sering	sering	ADV	_	_	_	_	Morf=sering<ADV>_ADV
2	ngikutin	ikut	VERB	_	Polite=Infm|Voice=Act	_	_	_	Morf=NGE+ikut<VERB>+in_VERB
3-4	gayanya	_	_	_	_	_	_	_	_
3	gaya	gaya	NOUN	_	Number=Sing	_	_	_	Morf=gaya<NOUN>_NOUN
4	nya	nya	PRON	_	Number=Sing|Person=3|Poss=Yes|PronType=Prs	_	_	_	Morf=nya<PRON>_PRON
5	lg	lagi	ADV	_	Abbr=Yes|Polite=Infm	_	_	_	Morf=lagi<ADV>_ADV
6	nyanyi	nyanyi	VERB	_	Polite=Infm	_	_	_	Morf=nyanyi<VERB>_VERB|SpaceAfter=No
7	.	.	PUNCT	_	_	_	_	_	Morf=.<PUNCT>_PUNCT

```

Accepting text file as input and write to file.

```console
foo@bar:~/aksara$ python3 aksara.py -f "input_example.txt" --output "output_example.conllu" --informal
Processing inputs...
100%|██████████████████████████████████████████████████| 5/5 [00:32<00:00,  6.45s/it]
foo@bar:~/aksara$
```

# Documentation

* Use `-s [SENTENCES]` or `--string [SENTENCES]` to analyze a sentence.
* Use `-f [FILE]` or `--file [FILE]` to analyze multiple sentences in a file.
* Use  `--output [FILE]` to select a file for the output. Otherwise, the output will be displayed in the standard output. 
* Use `--lemma` option to get only the output of lemmatization task.
* Use `--postag` option to get only the output of POS tagging task.
* Use `--informal` option to use the informal word handler.
* Please use option `-h` or `--help` for further documentation.

# Acknowledgments
* Aksara conforms to the annotation guidelines for Indonesian dependency treebank proposed by Alfina et al. (2019) and Alfina et al. (2020)
* Aksara v1.0 was built by M. Yudistira Hanifmuti and Ika Alfina, as the reseach project for Yudistira's undergraduate thesis at Faculty of Computer Science, Universitas Indonesia in 2020.
* Aksara v1.1 was built by Muhammad Ridho Ananda and Ika Alfina, as the research project for Ridho's undergraduate thesis at Faculty of Computer Science, Universitas Indonesia in 2021. Aksara v1.1 uses a hybrid POS tagger method of Aksara and Hidden Markov Model (HMM) to do disambiguation.
* Aksara v1.2 was built by I Made Krisna Dwitama, Muhammad Salman Al Farisi, Ika Alfina, and Arawinda Dinakaramani as the research project for Krisna and Salman undergraduate thesis at Faculty of Computer Science, Universitas Indonesia in 2022. Aksara v1.2 improve the ability of the morphological analyzer in Aksara in order to be able to process informal Indonesian text.

## References
* I Made Krisna Dwitama, Muhammad Salman Al Farisi, Ika Alfina, dan Arawinda Dinakaramani. "Pengembangan _Morphological Analyzer_ Bahasa Indonesia Informal Menggunakan _Finite-State Transducer_ (FST)".
* M. Ridho Ananda, M. Yudistira Hanifmuti, and Ika Alfina. ["**A Hybrid of Rule-based and HMM-based POS Taggers for Indonesian**"](https://ieeexplore.ieee.org/abstract/document/9675180). In Proceeding of the 2021 International Conference of Asian Language Processing (IALP)   
* M. Yudistira Hanifmuti and Ika Alfina. ["**Aksara: An Indonesian Morphological Analyzer that Conforms to the UD v2 Annotation Guidelines**"](https://ieeexplore.ieee.org/document/9310490). In Proceeding of the 2020 International Conference of Asian Language Processing (IALP)  in Kuala Lumpur, Malaysia, 4-6 Desember 2020.
* Ika Alfina, Daniel Zeman, Arawinda Dinakaramani, Indra Budi, and Heru Suhartanto. ["**Selecting the UD v2 Morphological Features for Indonesian Dependency Treebank**"](https://ieeexplore.ieee.org/document/9310513). In Proceeding of the 2020 International Conference of Asian Language Processing (IALP)  in Kuala Lumpur, Malaysia, 4-6 Desember 2020.
* Ika Alfina, Arawinda Dinakaramani, Mohamad Ivan Fanany, and Heru Suhartanto. ["**A Gold Standard Dependency Treebank for Indonesian**"](https://waseda.repo.nii.ac.jp/?action=repository_action_common_download&item_id=48059&item_no=1&attribute_id=101&file_no=1). In  Proceeding of 33rd Pacific Asia Conference on Language, Information and Computation (PACLIC) 2019 in Hakodate, Japan, 13-15 September 2019. 


# Changelog
* 2022-08-30 v1.2
  * added gold standard in the form of informal Indonesian text
  * added informal lexicon, morphotactic rules, and morphophonemic rules
  * added feature Polite=Infm
  * improve tokenization evaluator
  * fixed bugs
* 2021-08-07 v1.1
  * added the disambiguation for POS tag, lemma, and morphological features
  * updated lexicon
  * removed features: Subcat, NumForm, AdpType, VerbType
  * added feature NumType
  * removed feature values: Degree=Pos
  * fixed bugs
* 2020-10-27 v1.0
  * Initial release.
    

# Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Contact
ika.alfina [at] cs.ui.ac.id
