# cz-inflect-dev: development repo for paper OOVs in the Spotlight: How to Inflect them?

This repository contains all scripts needed to run the experiments described in bachelor thesis [Automatic inflection in Czech language](http://hdl.handle.net/20.500.11956/184286) by Tomáš Sourada, and for experiments described in the paper [OOVs in the Spotlight: How to Inflect them?](https://aclanthology.org/2024.lrec-main.1091) by Tomáš Sourada, Jana Straková, Rudolf Rosa, presented at LREC-COLING 2024. 

Abstract of the paper: We focus on morphological inflection in out-of-vocabulary (OOV) conditions, an under-researched subtask in which state-of-the-art systems usually are less effective. We developed three systems: a retrograde model and two sequence-to-sequence (seq2seq) models based on LSTM and Transformer. For testing in OOV conditions, we automatically extracted a large dataset of nouns in the morphologically rich Czech language, with lemma-disjoint data splits, and we further manually annotated a real-world OOV dataset of neologisms. In the standard OOV conditions, Transformer achieves the best results, with increasing performance in ensemble with LSTM, the retrograde model and SIGMORPHON baselines. On the real-world OOV dataset of neologisms, the retrograde model outperforms all neural models. Finally, our seq2seq models achieve state-of-the-art results in 9 out of 16 languages from SIGMORPHON 2022 shared task data in the OOV evaluation (feature overlap) in the large data condition. We release the Czech OOV Inflection Dataset for rigorous evaluation in OOV conditions. Further, we release the inflection system with the seq2seq models as a ready-to-use Python library.

For the main results, see the [paper](https://aclanthology.org/2024.lrec-main.1091), for detailed description and implementation details, see the [thesis](http://hdl.handle.net/20.500.11956/184286).

Released ready-to-use library, together with presentation materials, can be found in [cz-inflect](https://github.com/tomsouri/cz-inflect).

[Czech OOV Inflection Dataset](http://hdl.handle.net/11234/1-5471), released with the paper, stored at LINDAT repository, aiming at rigorous evaluation of inflection in out-of-vocabulary conditions, used throughout the experiments.


## Development repository

The project was developed on Linux Mint system. Most of the scripts are
written in `python3` or in `bash` (simple processing scripts and running cluster
jobs). The main python library used in the project is `OpenNMT-py`.

To prepare the whole development directory on a Linux system, you should
perform the following steps:

1. Create a `python3` virtual environment in the root directory of the development repository (`cz-inflect-dev/.venv`) , e.g. by running `mkdir -p .venv && python3 -m venv .venv`.
2. Run `make .venv` to install the project and the requirements.
3. Run `make build_data`, if you want to build the data from scratch (not needed to run the retrograde model).

The Makefile, present in the root directory, controls the installation of
dependencies (to be able to do it automatically it is needed that the name of
the virtual environment folder is specifically `.venv`) and data downloading
and processing.

Running `make build_data` first installs all the dependencies.
Then it downloads MorfFlex, extracts nouns only, shuffles the data, performs
filtering and other processing of the data, removes duplicates, builds the
datasets and converts them to the format for neural network models. The
individual scripts providing the processing lie in `src/morfflex`.
To be able to run the skloňuj.cz baseline, you need to have installed `PHP
7.3` and additionally package `php7.3-mbstring`.


## Run the models
In this section we briefly describe how to run the retrograde model and the
Transformer model TRM-11 (for LSTM model, refer to the [original released library](https://github.com/tomsouri/cz-inflect)).

### Retrograde model 
To run the retrograde model, you also need to have
installed the requirements and the project. Then you can simply run the inter-
active script `retrograde_model.py`, which lies in `src/czech_inflection/
/models/retrograde_model/`. It will take some time to load the model, but
then it performs inflection relatively quickly. The script itself shows how to
use the retrograde model as a library.

### TRM-11 
The Transformer model lies in the development directory of the
inflection library: `inflection_lib/cz-inflect/`. To run the library script
with the TRM-11 instead of LSTM-44, you need to change the path to
the model in the script `inflect.py` (self-descriptive). If you have already
installed the requirements and the project by running `make .venv`, then you
can run it from the root development directory (cz-inflect-dev) by running
`.venv/bin/python3 inflection_lib/cz-inflect/inflect.py`.

### Run on GPU 
To run the inflection model from the inflection library on
GPU instead of CPU, you need to modify the script inflect.py, specifically
the definition of variable opt in method `_inflect_file()` (parameter `gpu`).


