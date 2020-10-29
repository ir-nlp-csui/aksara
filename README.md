# Summary

Aksara is an Indonesian morphological analyzer that conforms to the Universal Dependencies (UD) v2 annotation guidelines. Aksara can perform four tasks:
* Word segmentation (tokenization)
* Lemmatization
* POS tagging
* Morphological features analysis
The output is in [ConLLU format](https://universaldependencies.org/format.html)
# Installation

1. Clone this [repository](https://github.com/bahasa-csui/aksara). `git clone https://github.com/bahasa-csui/aksara`

1. Install [Foma](https://fomafst.github.io/). For Debian/Ubuntu packaging, `apt-get install foma-bin`. Make sure you have the privilege to install package or use `sudo`.

1. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required packages.

    ```console
    foo@bar:~$ cd aksara
    foo@bar:~/aksara$ python3 -m pip install -r requirements.txt
    ```

    If [pip](https://pip.pypa.io/en/stable/) is not installed, please install pip first. `apt-get install python3-pip`

# Usage

Use console with `main.py`.

```console
foo@bar:~/aksara$ python3 main.py -s '“Meski kebanyakan transisi digital yang terjadi di Amerika Serikat belum pernah terjadi sebelumnya, transisi kekuasaan yang damai tidaklah begitu,” tulis asisten khusus Obama, Kori Schulman di sebuah postingan blog pada hari Senin.'
# sent_id = 1
# text = “Meski kebanyakan transisi digital yang terjadi di Amerika Serikat belum pernah terjadi sebelumnya, transisi kekuasaan yang damai tidaklah begitu,” tulis asisten khusus Obama, Kori Schulman di sebuah postingan blog pada hari Senin.
1       “       “       PUNCT   _       _       _       _       _       SpaceAfter=No
2       Meski   meski   SCONJ   _       _       _       _       _       _
3       kebanyakan      banyak  NOUN    _       Number=Sing     _       _       _       _
4       transisi        transisi        NOUN    _       Number=Sing     _       _       _       _
5       digital digital ADJ     _       Degree=Pos      _       _       _       _
6       yang    yang/yang       SCONJ/PRON      _       (PRON -> PronType=Rel)  _       _       _       _
7       terjadi jadi    VERB    _       Subcat=Tran|Voice=Pass  _       _       _       _
8       di      di      ADP     _       _       _       _       _       _
9       Amerika Amerika PROPN   _       _       _       _       _       _
10      Serikat Serikat PROPN   _       _       _       _       _       _
11      belum   belum   PART    _       Polarity=Neg    _       _       _       _
12      pernah  pernah  ADV     _       _       _       _       _       _
13      terjadi jadi    VERB    _       Subcat=Tran|Voice=Pass  _       _       _       _
14      sebelumnya      sebelumnya      ADV     _       _       _       _       _       SpaceAfter=No
15      ,       ,       PUNCT   _       _       _       _       _       _
16      transisi        transisi        NOUN    _       Number=Sing     _       _       _       _
17      kekuasaan       kuasa   NOUN    _       Number=Sing     _       _       _       _
18      yang    yang/yang       SCONJ/PRON      _       (PRON -> PronType=Rel)  _       _       _       _
19      damai   damai   ADJ     _       Degree=Pos      _       _       _       _
20-21   tidaklah        _       _       _       _       _       _       _       _
20      tidak   tidak   PART    _       Polarity=Neg    _       _       _       _
21      lah     lah     PART    _       PartType=Emp    _       _       _       _
22      begitu  begitu  DET     _       _       _       _       _       SpaceAfter=No
23      ,       ,       PUNCT   _       _       _       _       _       SpaceAfter=No
24      ”       ”       PUNCT   _       _       _       _       _       _
25      tulis   tulis   VERB    _       _       _       _       _       _
26      asisten asisten NOUN    _       Number=Sing     _       _       _       _
27      khusus  khusus  ADJ     _       Degree=Pos      _       _       _       _
28      Obama   Obama   PROPN   _       _       _       _       _       SpaceAfter=No
29      ,       ,       PUNCT   _       _       _       _       _       _
30      Kori    Kori    PROPN   _       _       _       _       _       _
31      Schulman        Schulman        PROPN   _       _       _       _       _       _
32      di      di      ADP     _       _       _       _       _       _
33      sebuah  buah    DET     _       Number=Sing|PronType=Ind        _       _       _       _
34      postingan       posting NOUN    _       Number=Sing     _       _       _       _
35      blog    blog    NOUN    _       Number=Sing     _       _       _       _
36      pada    pada    ADP     _       _       _       _       _       _
37      hari    hari    NOUN    _       Number=Sing     _       _       _       _
38      Senin   Senin   PROPN   _       _       _       _       _       SpaceAfter=No
39      .       .       PUNCT   _       _       _       _       _       _
foo@bar:~/aksara$
```

Accepting text file as input and write to file.

```console
foo@bar:~/aksara$ python3 main.py -f "input_example.txt" --output "output_example.conllu"
Processing inputs...
100%|██████████████████████████████████████████████████| 5/5 [00:32<00:00,  6.45s/it]
foo@bar:~/aksara$
```

# Documentation

* To be added. Please use option `--help` at the moment.

# Acknowledgments

* Aksara v1.0 was built by M. Yudistira Hanifmuti and Ika Alfina, as the reseach project for Yudistira's undergraduate thesis at Faculty of Computer Science, Universitas Indonesia.
* Aksara v1.0 refers to the annotation guidelines for Indonesian dependency treebank proposed by Alfina et al. (2019) and Alfina et al. (2020)

## References
* M. Yudistira Hanifmuti and Ika Alfina. **"Aksara: An Indonesian Morphological Analyzer that Conforms to the UD v2 Annotation Guidelines"**. In Proceeding of the 2020 International Conference of Asian Language Processing (IALP)  in Kuala Lumpur, Malaysia, 4-6 Desember 2020. (_accepted_)
* Ika Alfina, Daniel Zeman, Arawinda Dinakaramani, Indra Budi, and Heru Suhartanto. "**Selecting the UD v2 Morphological Features for Indonesian Dependency Treebank**". In Proceeding of the 2020 International Conference of Asian Language Processing (IALP)  in Kuala Lumpur, Malaysia, 4-6 Desember 2020. (_accepted_)
* Ika Alfina, Arawinda Dinakaramani, Mohamad Ivan Fanany, and Heru Suhartanto. ["**A Gold Standard Dependency Treebank for Indonesian**"](https://waseda.repo.nii.ac.jp/?action=repository_action_common_download&item_id=48059&item_no=1&attribute_id=101&file_no=1). In  Proceeding of 33rd Pacific Asia Conference on Language, Information and Computation (PACLIC) 2019 in Hakodate, Japan, 13-15 September 2019. 


# Changelog

* 2020-10-27 v1.0
  * Initial release.

# Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
