import torch
from onmt.translate import Translator

# Load the trained model checkpoint
model_checkpoint = "model_released.pt"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = torch.load(model_checkpoint, map_location=device)
model.eval()

# Initialize the translator
translator = Translator(model)

# Translate text
source_text = "j a b l k o # S 7"
translated_data = translator.translate(src_data=[source_text])
translated_text = translated_data[0]["tgt"]
print(translated_text)
