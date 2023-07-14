import torch
from onmt.utils.misc import load_test_model
from onmt.translate.translator import Translator

# Load the model
model_path = "model_released.pt"
model, model_opt = load_test_model(model_path)

# Create a translator using the loaded model
translator = Translator(model, model_opt)

# Prepare the input
src_tokens = "k r k # S 1".split()

# Translate the input
translation = translator.translate(src_tokens)

# Get the translated tokens
tgt_tokens = translation[0]["tokens"]

# Detokenize the translated tokens
tgt_sentence = " ".join(tgt_tokens)

# Print the translated sentence
print(tgt_sentence)
