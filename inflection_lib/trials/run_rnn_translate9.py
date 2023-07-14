import torch
from onmt import models
from onmt.translate import Translator

model_path = "model_released.pt"
device = torch.device("cpu")  # or "cuda"

model = torch.load(model_path, map_location=device)

model_data = model

model_opt = model_data['opt']
model_dict = model_data['model']
src_vocab = model_data['vocab']['src']
tgt_vocab = model_data['vocab']['tgt']

translator = Translator(model, beam_size=5, n_best=1, max_length=50, global_scorer=None, vocabs=[src_vocab,tgt_vocab])



def inflect(lemma: str):
    # Prepare input data
    src_data = [lemma + " S" + str(i) for i in range(1, 7 + 1)] + [lemma + " P" + str(i) for i in range(1, 7 + 1)]

    # Translate the input
    translations = translator.translate(src_data)

    # Extract the translations
    extracted = [translation.pred_sents[0] for translation in translations]

    return extracted

lemma = "pes"
inflected_forms = inflect(lemma)
print(inflected_forms)
