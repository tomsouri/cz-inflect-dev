import torch
from onmt.translate import TranslationService

# Load the trained model checkpoint
model_checkpoint = "model_released.pt"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = torch.load(model_checkpoint, map_location=device)
model.eval()

translator = TranslationService(model)

source_text = "j a b l k o # S 7"
translated_text = translator.translate_string(source_text)
print(translated_text)


