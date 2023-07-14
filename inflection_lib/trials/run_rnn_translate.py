#!/usr/bin/env python3

import sys

import torch
import onmt
import onmt.inputters
import onmt.translate

path = "model_released.pt"
src_sentence = "Č á s t k o v # P 7"
model_path = path
#vocab_path = 'path_to_vocab.pt'

model = torch.load(model_path, map_location=lambda storage, loc: storage)

#out = model.translate(src_sentence)
print(model)
#src_vocab = torch.load(vocab_path)
#src_lang = 'source_language'  # The source language code used in training
#tgt_lang = 'target_language'  # The target language code used in training
#translator = onmt.translate.Translator(model, src_vocab, tgt_vocab, src_lang, tgt_lang)
translator = onmt.translate.Translator(model)

src_data = onmt.inputters.build_dataset(data_type='text', src_seq_length=100, src_raw=[src_sentence])
src_loader = onmt.inputters.OrderedIterator(dataset=src_data, device='cpu', batch_size=1, train=False, sort=False, shuffle=False)

for batch in src_loader:
    src_seq, src_pos = batch.src
    src_seq = src_seq.to(translator.device)
    src_pos = src_pos.to(translator.device)

    _, tgt_seq = translator.translate_batch(src_seq, src_pos)
    translation = translator.translate(src_seq, src_pos, tgt_seq)
    print(translation[0])
