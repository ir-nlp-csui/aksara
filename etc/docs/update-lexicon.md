# Updating Aksara Lexicon

These are some steps to do to update Aksara's lexicon.

- [Update lexicon rules on Foma files](update-lexicon-rules-on-Foma-files)
- [Compiling Foma files to binary file](compiling-foma-files-to-binary-file)
- [Configure Aksara](configure-aksara)
- [Testing Aksara](testing-aksara)

## Update lexicon rules on Foma files

To update lexicon rules, you must look for two files, `aksara@vX.Y.Z.foma` and `aksara@vX.Y.Z.lexc` in `etc/lexc/` folder.

1. Create a new copy from the latest version you want to update.

    For example, to create `v0.4.0` version, you can create a copy for each file from `aksara@v0.3.0.foma` and `aksara@v0.3.0.lexc`.
1. To update the lexicon list, look for the line with `LEXICON Stems` in `aksara@vX.Y.Z.lexc` file. You can add a new word to the corresponding POS tag group.

    For example, you want to add a `NOUN` word `meja`. Look for the line with `LEXICON NOUN`. Then, you can place the word `meja` into the list in __alphabetical__ order. Rewrite the word with spaces between the letter and inside the `<[...]>`. Finally, add the postag flag `POSFlagNOUN` at the end of the line.
    ```bash
    ...
    <[m e d i a s i]> POSFlagNOUN;
    <[m e d i t a s i]> POSFlagNOUN;
    # The rewrited example for word `meja`
    <[m e j a]> POSFlagNOUN;
    <[m e k a n i k a]> POSFlagNOUN;
    ...
    ```

1. To update lexicon rules, ... (To be added later)

1. Lastly, make sure you __update the `aksara@vX.Y.Z.foma`__ to __read the `aksara@vX.Y.Z.lexc`__ by updating the following line in `aksara@vX.Y.Z.foma`.

    ```bash
    ...
    # Edit this line to corresponding lexc file
    read lexc aksara@v0.4.0.lexc
    def Lexc;
    ...
    ```

## Compiling Foma files to binary file

1. Install [Foma](https://fomafst.github.io/) (you can skip this step if Foma is already installed). 

    For Debian/Ubuntu packaging, `apt-get install foma-bin`. Make sure you have the privilege to install the package or use `sudo`.
1. Change directory to `etc/lexc/` and open Foma console. In Ubuntu, you can execute `foma` on terminal.
     ```console
    foo@bar:~$ cd aksara/etc/lexc/
    foo@bar:~/aksara/etc/lexc$ foma
    Foma, version 0.9.18alpha
    Copyright © 2008-2014 Mans Hulden
    This is free software; see the source code for copying conditions.
    There is ABSOLUTELY NO WARRANTY; for details, type "help license"

    Type "help" to list all commands available.
    Type "help <topic>" or help "<operator>" for further help.

    foma[0]:
    ```

1. Before you start compiling foma files, make sure you set the `flag-is-epsilon` to `ON`.

    ```console
    foma[0]: set flag-is-epsilon ON
    variable flag-is-epsilon = ON
    ```

    If you skip this step, __you won't get the correct result for affixed words__. 

1. Compile Foma files with the version you want to use. Use `source` command. Make sure both `aksara@vX.Y.Z.foma` and `aksara@vX.Y.Z.lexc` do exist in `etc/lexc/` folder. If things go well, you won't find any errors here.
    ```console
    foma[0]: source aksara@v0.3.0.foma 
    Opening file 'aksara@v0.3.0.foma'.
    defined Cons: 1.1 kB. 2 states, 21 arcs, 21 paths.
    defined Vow: 413 bytes. 2 states, 5 arcs, 5 paths.
    ...
    ...
    defined Lexicon: 164.9 kB. 4558 states, 9976 arcs, Cyclic.
    defined Grammar: 164.9 kB. 4558 states, 9976 arcs, Cyclic.
    164.9 kB. 4558 states, 9976 arcs, Cyclic.
    foma[1]:
    ```
1. Save the stack into a file with the `save stack` command. Name it with format `aksara@vX.Y.Z.bin`.
    ```console
    foma[1]: save stack aksara@v0.3.0.bin
    Writing to file aksara@v0.3.0.bin.
    foma[1]: 
    ```
1. Exit from Foma console. You can see `aksara@vX.Y.Z.bin` is created inside `etc/lexc/` folder. Move `aksara@vX.Y.Z.bin` to `bin` folder in project root.
    ```console
    foma[1]: exit
    foo@bar:~/aksara/etc/lexc$ ls
    aksara@v0.3.0.bin   aksara@v0.3.0.lexc   aksara@v0.3.0.foma
    foo@bar:~/aksara/etc/lexc$ mv aksara@v0.3.0.bin ../../bin/aksara@v0.3.0.bin
    ```

## Configure Aksara

### Changing Binary used

1. Open `main.py` in the project root.
1. Update the `BIN_FILE` variable with binary you want to use (relative path from project root).

## Testing Aksara

TBD