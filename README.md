# Aksara

## Description

Aksara is an Indonesian NLP tool that conforms to the [Universal Dependencies (UD) v2](https://universaldependencies.org/) annotation guidelines. Aksara can perform **five tasks**:
* Word segmentation (tokenization)
* Lemmatization
* POS tagging
* Morphological features analysis
* Dependency Parsing

The output is in the [CoNLL-U format](https://universaldependencies.org/format.html).

## Installation

1. Install [Foma](https://fomafst.github.io/). 
    
    a.  Linux <br>
    1. `apt-get install foma-bin`.
    
        Make sure you have the privilege to install package or  use `sudo`.
    
    b.  Windows
        
    1. Get precompiled foma binary from [foma-zip](https://bitbucket.org/mhulden/foma/downloads/)

    2. Unzip the precompiled foma binary
        
    3. Add the win32 folder path (from precompiled foma zip) to environment variable PATH

2. [OPTIONAL] It is strongly recommended to use virtual environment (see [venv](https://docs.python.org/3/library/venv.html) on how to create Python virtual environment using venv)

3. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Aksara library (it is recommended to use virtual environment to avoid dependency conflicts).

    ```console
    pip install -U aksara
    ```

## Usage

## Acknowledgments
* Aksara conforms to the annotation guidelines for Indonesian dependency treebank proposed by Alfina et al. (2019) and Alfina et al. (2020)
* Aksara v1.0 was built by M. Yudistira Hanifmuti and Ika Alfina, as the reseach project for Yudistira's undergraduate thesis at Faculty of Computer Science, Universitas Indonesia in 2020.
* Aksara v1.1 was built by Muhammad Ridho Ananda and Ika Alfina, as the research project for Ridho's undergraduate thesis at Faculty of Computer Science, Universitas Indonesia in 2021. Aksara v1.1 uses a hybrid POS tagger method of Aksara and Hidden Markov Model (HMM) to do disambiguation.
* Aksara v1.2 was built by I Made Krisna Dwitama, Muhammad Salman Al Farisi, Ika Alfina, and Arawinda Dinakaramani as the research project for Krisna and Salman undergraduate thesis at Faculty of Computer Science, Universitas Indonesia in 2022. Aksara v1.2 improve the ability of the morphological analyzer in Aksara in order to be able to process informal Indonesian text.
* Aksara v1.3 was built by Andhika Yusup Maulana, Ika Alfina, and Kurniawati Azizah as the research project for Maulana's undergraduate thesis at the Faculty of Computer Science, Universitas Indonesia, in August 2022. Aksara v1.3 introduces a machine-learning-based dependency parser to fill the 7-8th column that previously left empty.

## References
* Andhika Yusup Maulana, Ika Alfina, and Kurniawati Azizah. [**"Building Indonesian Dependency Parser Using Cross-lingual Transfer Learning"**](https://ieeexplore.ieee.org/abstract/document/9961296). In Proceeding of the 2022 International Conference of Asian Language Processing (IALP). 
* I Made Krisna Dwitama, Muhammad Salman Al Farisi, Ika Alfina, dan Arawinda Dinakaramani. [**"Building Morphological Analyzer for Informal Text in Indonesian"**](https://ieeexplore.ieee.org/abstract/document/9923494). In Proceeding of the ICACSIS 2022 (online).
* M. Ridho Ananda, M. Yudistira Hanifmuti, and Ika Alfina. ["**A Hybrid of Rule-based and HMM-based POS Taggers for Indonesian**"](https://ieeexplore.ieee.org/abstract/document/9675180). In Proceeding of the 2021 International Conference of Asian Language Processing (IALP)   
* M. Yudistira Hanifmuti and Ika Alfina. ["**Aksara: An Indonesian Morphological Analyzer that Conforms to the UD v2 Annotation Guidelines**"](https://ieeexplore.ieee.org/document/9310490). In Proceeding of the 2020 International Conference of Asian Language Processing (IALP)  in Kuala Lumpur, Malaysia, 4-6 Desember 2020.
* Ika Alfina, Daniel Zeman, Arawinda Dinakaramani, Indra Budi, and Heru Suhartanto. ["**Selecting the UD v2 Morphological Features for Indonesian Dependency Treebank**"](https://ieeexplore.ieee.org/document/9310513). In Proceeding of the 2020 International Conference of Asian Language Processing (IALP)  in Kuala Lumpur, Malaysia, 4-6 Desember 2020.
* Ika Alfina, Arawinda Dinakaramani, Mohamad Ivan Fanany, and Heru Suhartanto. ["**A Gold Standard Dependency Treebank for Indonesian**"](https://waseda.repo.nii.ac.jp/?action=repository_action_common_download&item_id=48059&item_no=1&attribute_id=101&file_no=1). In  Proceeding of 33rd Pacific Asia Conference on Language, Information and Computation (PACLIC) 2019 in Hakodate, Japan, 13-15 September 2019. 


## Changelog
* 2022-10-21 v1.3
  * added new flag `--model [MODEL_NAME]`
  * added dependency parser
  * integrated existing flow with dependency parsing task
* 2022-08-30 v1.2
  * added informal lexicon, morphotactic rules, and morphophonemic rules
  * added feature Polite=Infm
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
    

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Contact
ika.alfina [at] cs.ui.ac.id
