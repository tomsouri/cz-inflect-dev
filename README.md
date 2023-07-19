# cz-inflect-dev

## Development directory of cz-inflect project
https://github.com/tomsouri/cz-inflect

The project was developed on Linux Mint system. Most of the scripts are
written in python3 or in bash (simple processing scripts and running cluster
jobs). The main python library used in the project is OpenNMT-py.

To prepare the whole development directory on a Linux system, you should
perform the following steps:

1. Create a python3 virtual environment in the root directory of the development repository (cz-inflect-dev/.venv) , e.g. by running mkdir -p .venv && python3 -m venv .venv.

2. Run make .venv to install the project and the requirements.
3. Run make build_data, if you want to build the data from scratch (not
needed to run the retrograde model).

The Makefile, present in the root directory, controls the installation of
dependencies (to be able to do it automatically it is needed that the name of
the virtual environment folder is specifically .venv) and data downloading
and processing.

After running make build_data it first installs all the dependencies.
Then it downloads MorfFlex, extracts nouns only, shuffles the data, performs
filtering and other processing of the data, removes duplicates, builds the
datasets and converts them to the format for neural network models. The
individual scripts providing the processing lie in src/morfflex.
To be able to run the skloňuj.cz baseline, you need to have installed PHP
7.3 and additionally package php7.3-mbstring.


## Run the models
In this section we briefly describe how to run the retrograde model and the
Transformer model TRM-11.

### Retrograde model 
To run the retrograde model, you also need to have
installed the requirements and the project. Then you can simply run the inter-
active script retrograde_model.py, which lies in src/czech_inflection/
/models/retrograde_model/. It will take some time to load the model, but
then it performs inflection relatively quickly. The script itself shows how to
use the retrograde model as a library.

### TRM-11 
The Transformer model lies in the development directory of the
inflection library: inflection_lib/cz-inflect/. To run the library script
with the TRM-11 instead of LSTM-44, you need to change the path to
the model in the script inflect.py (self-descriptive). If you have already
installed the requirements and the project by running make .venv, then you
can run it from the root development directory (cz-inflect-dev) by running
.venv/bin/python3 inflection_lib/cz-inflect/inflect.py.

### Run on GPU 
To run the inflection model from the inflection library on
GPU instead of CPU, you need to modify the script inflect.py, specifically
the definition of variable opt in method _inflect_file() (parameter gpu).


