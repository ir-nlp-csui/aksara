# Summary

Aksara is an Indonesian morphological analyzer that conforms to Universal Dependencies (UD) v2 annotation guidelines. Aksara can perform four tasks:
* Word segmentation (tokenization)
* Lemmatization
* POS tagging
* Morphological features analysis

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
foo@bar:~/aksara$ python3 main.py -s "sebuah kalimat contoh"
# sent_id = 1
# text = sebuah kalimat contoh
# text_en =
1       sebuah  sebuah  DET     _       _       _       _       _
2       kalimat kalimat NOUN    _       Number=Sing     _       _       _
3       contoh  contoh  NOUN    _       Number=Sing     _       _       _
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

* Aksara 1.0 was built by M. Yudistira Hanifmuti and Ika Alfina, as the reseach project for Yudistira's undergraduate thesis.
* Aksara 1.0 refers to the annotation guidelines for Indonesian dependency treebank proposed by Alfina et al. (2020)

## References
* M. Yudistira Hanifmuti and Ika Alfina. **"Aksara: An Indonesian Morphological Analyzer that Conforms to Universal Dependencies"**. In the Proceeding of the 2020 International Conference of Asian Language Processing (IALP)  in Kuala Lumpur, Malaysia, 4-6 Desember 2020. (_accepted_)
* Ika Alfina, Daniel Zeman, Arawinda Dinakaramani, Indra Budi, and Heru Suhartanto. "**Selecting the Universal Dependencies Morphological Features for Indonesian Dependency Treebank**". In the Proceeding of the 2020 International Conference of Asian Language Processing (IALP)  in Kuala Lumpur, Malaysia, 4-6 Desember 2020. (_accepted_)


# Changelog

* 2020-10-27 v1.0
  * Initial release.

# Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
