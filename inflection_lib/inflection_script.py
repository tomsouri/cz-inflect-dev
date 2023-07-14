#!/usr/bin/env python3
"""
An inflection script working on the base of ctranslate2. It is able to work
with Transformer models only (from the OpenNMT)

Dependencies: 
ctranslate2==3.14.0
torch==2.0.1

A new model can be converted from OpenNMT format this way:

.venv/bin/ct2-opennmt-py-converter --model_path Transformer_v0.3_batchTypeSents_batch64_droupouts0.2_hidden256_wordvec256_step_100000.pt --output_dir models
"""

import ctranslate2
import sys

ct_model_path = sys.argv[1]

translator = ctranslate2.Translator(ct_model_path, device="cpu")

def inflect(lemma: str):
	# Convert to specific neural format
	line = " ".join(lemma)
	lines = [line + f" # S {i}" for i in range(1,7+1)] +  [line + f" # P {i}" for i in range(1,7+1)]
	lines = [line.split(" ") for line in lines]

	# Now there is one line for each expected wordform
	# Get the inflected forms
	translations = translator.translate_batch(lines, batch_type="tokens", max_batch_size=8)
	translations = [translation.hypotheses[0] for translation in translations]
	
	# Convert from neural format back to normal text 
	extracted = ["".join(translation) for translation in translations]
	return extracted


for line in sys.stdin:
	line = line.strip()
	print(inflect(line))
