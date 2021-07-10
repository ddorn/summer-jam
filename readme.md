# XXX

This is the base template that we will use for
the [Pygame Community Summer Team Jam](https://itch.io/jam/pygame-community-summer-team-jam).

All the `XXX` will have to be replaced by the actual name of the game, which we don't know yet.

This repository contains all the source code and the assets for 
the game we made in one week for the jam.

### How to run it

The only two dependencies of the game are python 3.8 and pygame 2.0.1.
Once you have both installed, with your favourite tool, for instance
```shell script
python3 -m pip install pygame==2.0.1
```
or maybe
```shell script
poetry install
```
You will be able to run the game as
```shell script
python3.8 XXX.py
```

### Executables

In order to create executables for the game, we provide a makefile, that assumes 
that you have `python` and `poetry` installed, and takes care of the rest.
You can run the game with `make run` or build executables with `make linux`,`make windows`
and `make` builds the two executables along with the source as a zip.

