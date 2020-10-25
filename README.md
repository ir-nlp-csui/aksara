# Umabi

Universal Morphological Analyzer for Bahasa Indonesia.

## Installation

1. Clone this [repository](https://github.com/shygnome/umabi.git). `git clone https://github.com/shygnome/umabi.git`

1. Install [Foma](https://fomafst.github.io/). For Debian/Ubuntu packaging, `apt-get install foma-bin`. Make sure you have the privilege to install package or use `sudo`.

1. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required packages.

    ```console
    foo@bar:~$ cd umabi
    foo@bar:~/umabi$ python3 -m pip install -r requirements.txt
    ```

    If [pip](https://pip.pypa.io/en/stable/) is not installed, please install pip first. `apt-get install python3-pip`

## Usage

Use console with `main.py`.

```console
foo@bar:~/umabi$ python3 main.py -s "sebuah kalimat contoh"
# sent_id = 1
# text = sebuah kalimat contoh
# text_en =
1       sebuah  sebuah  DET     _       _       _       _       _
2       kalimat kalimat NOUN    _       Number=Sing     _       _       _
3       contoh  contoh  NOUN    _       Number=Sing     _       _       _
```

Accepting text file as input and write to file.

```console
foo@bar:~/umabi$ python3 main.py -f "input_example.txt" --output "output_example.conllu"
Processing inputs...
100%|██████████████████████████████████████████████████| 5/5 [00:32<00:00,  6.45s/it]
foo@bar:~/umabi$
```

## Documentation

* To be added. Please use option `--help` at the moment.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[Apache License Version 2.0](https://choosealicense.com/licenses/apache-2.0/)
