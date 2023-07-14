# First convert your OpenNMT-py or OpenNMT-tf model to a CTranslate2 model.
# pip3 install ctranslate2
# • OpenNMT-py:
# ct2-opennmt-py-converter --model_path model.pt --output_dir enja_ctranslate2 --quantization int8
# • OpenNMT-tf:
# ct2-opennmt-tf-converter --model_path model --output_dir enja_ctranslate2 --src_vocab source.vocab --tgt_vocab target.vocab --model_type TransformerBase --quantization int8

# FROM: https://gist.github.com/ymoslem/60e1d1dc44fe006f67e130b6ad703c4b

# Uses sentence piece, which we probably do not need.


# Release the model: Try this command and see how it reduce the model size.
# onmt_release_model --model "model.pt" --output "model_released.pt



import ctranslate2
import sentencepiece as spm

# Set file paths
source_file_path = "test.en"
target_file_path = "test.ja"

sp_source_model_path = "spm_model.en"
sp_target_model_path = "spm_model.ja"

ct_model_path = "enja_ctranslate2/"


# Load the source SentecePiece model
sp = spm.SentencePieceProcessor()
sp.load(sp_source_model_path)

# Open the source file
with open(source_file_path, "r") as source:
  lines = source.readlines()

source_sents = [line.strip() for line in lines]

# Subword the source sentences
source_sents_subworded = sp.encode_as_pieces(source_sents)

# Translate the source sentences
translator = ctranslate2.Translator(ct_model_path, device="cpu")  # or "cuda" for GPU
translations = translator.translate_batch(source_sents_subworded, batch_type="tokens", max_batch_size=4096)
translations = [translation.hypotheses[0] for translation in translations]

# Load the target SentecePiece model
sp.load(sp_target_model_path)

# Desubword the target sentences
translations_desubword = sp.decode(translations)


# Save the translations to the a file
with open(target_file_path, "w+", encoding="utf-8") as target:
  for line in translations_desubword:
    target.write(line.strip() + "\n")

print("Done")
