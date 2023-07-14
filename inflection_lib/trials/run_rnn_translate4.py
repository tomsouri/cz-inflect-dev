import torch
import onmt
import onmt.inputters
import onmt.translate

path = "model_released.pt"
src_sentence = "Č á s t k o v # P 7"

model_path = path
model_data = torch.load(model_path, map_location=lambda storage, loc: storage)

# Load the model parameters
model_opt = model_data['opt']
model_dict = model_data['model']
src_vocab = model_data['vocab']['src']
tgt_vocab = model_data['vocab']['tgt']

# Create the model
model = onmt.models.model.Model(model_opt, src_vocab, tgt_vocab)
model.load_state_dict(model_dict)

# Create the translator
translator = onmt.translate.Translator(model=model)

src_data = onmt.inputters.build_dataset(
    data_type='text', src_seq_length=100, src_raw=[src_sentence]
)
src_loader = onmt.inputters.OrderedIterator(
    dataset=src_data, device='cpu', batch_size=1,
    train=False, sort=False, shuffle=False
)

for batch in src_loader:
    src_seq, src_pos = batch.src
    src_seq = src_seq.to(translator.device)
    src_pos = src_pos.to(translator.device)

    _, tgt_seq = translator.translate_batch(src_seq, src_pos)
    translation = translator.translate(src_seq, src_pos, tgt_seq)
    print(translation[0])
