import onmt

path = "model_released.pt"
src_sentence = "Č á s t k o v # P 7"

# Load the released model
translator = onmt.translate.Translator.from_pretrained(path)

# Prepare the source sentence
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

    _, tgt_seq, _ = translator.translate_batch(
        src_seq, src_pos, tgt_seq=None
    )
    translation = translator.translate(
        src_seq, src_pos, tgt_seq=tgt_seq
    )
    print(translation[0])
