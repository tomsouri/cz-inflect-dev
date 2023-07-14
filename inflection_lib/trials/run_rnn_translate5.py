from onmt.translate.translator import build_translator
from argparse import Namespace

path = 'model_released.pt'

batch_size = 128
beam_size = 16  # the higher the beam size the longer the translation runs
max_length = 50
#opt = Namespace(
#	alpha=0.0, batch_type='sents', beam_size=5, beta=-0.0, block_ngram_repeat=0, coverage_penalty='none', 
#	data_type='text', dump_beam='', fp32=False, gpu=-1, ignore_when_blocking=[], length_penalty='none', 
#	max_length=100, max_sent_length=None, min_length=0, models=[path], n_best=1, output='/dev/null', 
#	phrase_table='', random_sampling_temp=1.0, random_sampling_topk=1, ratio=-0.0, replace_unk=False, 
#	report_align=False, report_time=False, seed=829, stepwise_penalty=False, tgt=None, verbose=False, 
#	int8=False, random_sampling_topp=False, ban_unk_token=False, tgt_file_prefix=None)
opt = Namespace(alpha=0.0, batch_type='sents', beam_size=beam_size, beta=-0.0, block_ngram_repeat=0,
                coverage_penalty='none',
                data_type='text', dump_beam='', fp32=False, gpu=0, ignore_when_blocking=[], length_penalty='none',
                max_length=max_length, max_sent_length=None, min_length=0,
                models=[path],
                n_best=1, output="currentoutput", phrase_table='', random_sampling_temp=1.0, random_sampling_topk=1, ratio=-0.0,
                replace_unk=False, report_align=False, report_time=False, seed=829, stepwise_penalty=False, tgt=None,
                verbose=False)

translator = build_translator(opt, report_score=False)
x = translator.translate(['Č á s t k o v # P 7'], batch_size=1)
print(x)
