SHELL=/bin/bash

###############################################################################
# Define filenames
morfflex-xz = data/raw/czech-morfflex-2.0.tsv.xz
morfflex = data/raw/czech-morfflex-2.0.tsv
nouns = data/processed/morfflex/morfflex-nouns.tsv
nouns-shuffled = data/processed/morfflex/morfflex-nouns-shuffled.tsv
filtered = data/processed/morfflex/filtered_data_full.txt
lemmata = data/processed/morfflex/morfflex-lemmata-only.txt
test-oov = data/cleaned/test_oov_data.txt
manually-checked = data/processed/dev_data_manual_check.txt

DATA_NO = \
		train \
		dev \
		test

DATA_WITH_DUPLICATES_NO = $(addprefix data/processed/morfflex/splits_with_duplicates/, $(DATA_NO))
DATA_WITH_DUPLICATES = $(addsuffix _data.txt, $(DATA_WITH_DUPLICATES_NO))


DATA_NOO = $(addprefix data/cleaned/, $(DATA_NO))
DATA = $(addsuffix _data.txt, $(DATA_NOO))

NEURAL_NO = \
        dev.src \
        dev.tgt \
        train.src \
        train.tgt \
        test.src \
        test.tgt \
		test-oov.src \
		test-oov.tgt

NEURAL := $(addprefix data/cleaned/neural/, $(NEURAL_NO))


a = tmpmake/a.tmp
b = tmpmake/b.tmp
c = tmpmake/c.tmp
d = tmpmake/d.tmp
e = tmpmake/e.tmp
###############################################################################

# Define paths to scripts for data processing

python = .venv/bin/python3
add_raw_lemma = src/czech_inflection/morfflex/add_raw_lemma.py
add_rand_col = src/czech_inflection/morfflex/add_rand_col.py
build_lemmata_only = src/czech_inflection/morfflex/build_lemmata_only.py
filter_forms_and_lemmata = src/czech_inflection/morfflex/filter_forms_and_lemmata.py
train_dev_test_split = src/czech_inflection/morfflex/train_dev_test_split.py
rm_duplicates = src/czech_inflection/morfflex/rm_duplicates.py
rm_dups_sh = src/czech_inflection/morfflex/rm_dups.sh
build_test_oov_data = src/czech_inflection/dev_testing/build_data/build_test_oov_data.py
convert2neural = src/czech_inflection/morfflex/convert2neural.py

###############################################################################

# delete all data not tracked by git (except for logs)
clear:
	rm -f $(DATA) $(NEURAL) $(morfflex) $(morfflex-xz) $(nouns) $(nouns-shuffled) $(lemmata) $(test-oov)
	rm -r .venv

# Create virtual environment manually:
venvcreation:
	echo "BEFORE AUTOMATICALLY INSTALLING THE PROJECT, CREATE MANUALLY THE VIRTUAL ENVIRONMENT FOR PYTHON3 BY RUNNING:"
	echo "mkdir -p .venv"
	echo "python3 -m venv .venv"
	echo ""
	echo "If you are in metacentrum, run:"
	echo "module add python/3.8.0-gcc-rab6t cuda/cuda-11.2.0-intel-19.0.4-tn4edsz cudnn/cudnn-8.1.0.77-11.2-linux-x64-intel-19.0.4-wx22b5t"
	echo ""
# Install dependencies and the project itself
.venv: venvcreation
	.venv/bin/pip install --no-cache-dir --upgrade pip setuptools
# install the project:
	$(python) -m pip install -e .
	.venv/bin/pip3 install --no-cache-dir -r requirements.txt


# Download morfflex
$(morfflex-xz):
	# Download morfflex 2.0 from the official repository
	curl -o $(morfflex-xz) --remote-name-all https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-3186{/czech-morfflex-2.0.tsv.xz}

# Unzip morfflex
# order-only-prerequisites: 
$(morfflex): $(morfflex-xz)
	unxz --keep $(morfflex-xz)

# extract nouns only:
$(nouns): | $(morfflex)
	cat $(morfflex) | egrep "^(\S*)\sN" > $(nouns)

# shuffle the data in the manner, that:
# 1) the rows containing the same lemma will be adjacent
# 2) otherwise the order is random
$(nouns-shuffled): .venv $(nouns) $(add_raw_lemma) $(add_rand_col)
	mkdir -p tmpmake


	cat $(nouns) | $(python) $(add_raw_lemma) 	> $(a) 
	cat $(a) | LC_ALL=C sort -k 1 --stable		> $(b)
	rm $(a)
	cat $(b) | cut -f2,3,4 						> $(c)
	rm $(b)
	cat $(c) | $(python) $(add_rand_col) 		> $(d)
	rm $(c)
	cat $(d) | sort -k 1 --stable				> $(e)
	rm $(d)
	cat $(e) | cut -f2,3,4 						> $(nouns-shuffled)
	rm $(e)
	rmdir tmpmake

$(lemmata): .venv $(morfflex) $(build_lemmata_only)
	$(python) $(build_lemmata_only)

$(filtered): .venv $(nouns-shuffled) $(filter_forms_and_lemmata)
	$(python) $(filter_forms_and_lemmata)

$(DATA_WITH_DUPLICATES): .venv $(filtered) $(train_dev_test_split)
	$(python) $(train_dev_test_split)

$(DATA): .venv $(DATA_WITH_DUPLICATES)
	bash $(rm_dups_sh) $(rm_duplicates) $@

$(test-oov): .venv $(manually-checked)
	$(python) $(build_test_oov_data)

# Convert data to neural format, and create smaller versions of the datasets.
$(NEURAL):  .venv $(DATA)
	$(python) $(convert2neural)
	head -n14000 data/cleaned/neural/dev.src > data/cleaned/neural/dev_small.src	
	head -n14000 data/cleaned/neural/dev.tgt > data/cleaned/neural/dev_small.tgt

	head -n14000 data/cleaned/neural/train.src > data/cleaned/neural/train_small.src
	head -n14000 data/cleaned/neural/train.tgt > data/cleaned/neural/train_small.tgt

	head -n140000 data/cleaned/neural/dev.src > data/cleaned/neural/dev_medium.src	
	head -n140000 data/cleaned/neural/dev.tgt > data/cleaned/neural/dev_medium.tgt

build_data: $(DATA) $(test-oov) $(lemmata) $(NEURAL)

# Print the running jobs
qstat:
	qstat -u souradat @elixir-pbs.elixir-czech.cz @meta-pbs.metacentrum.cz @cerit-pbs.cerit-sc.cz

# Print results of my model on sigmorphon22 dev data
sig:
	cat docs/hyperparams.txt | egrep -v "test" | egrep "dev" | egrep "DataSig"| egrep "warm4k"
