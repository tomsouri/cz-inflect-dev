import torch
from onmt.translate.translator import Translator

# Load the model
model_path = "model_released.pt"
checkpoint = torch.load(model_path)
model = checkpoint['model']
model_opt = checkpoint['opt']

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
