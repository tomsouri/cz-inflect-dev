
from argparse import Namespace
from onmt.translate.translator import build_translator
from onmt.bin.translate import _get_parser
from argparse import Namespace

path = "model_released.pt"

parser = _get_parser()

opt = parser.parse_args()



beam_size = 16  # the higher the beam size the longer the translation runs
max_length = 50

#opt = Namespace(alpha=0.0, batch_type='sents', beam_size=beam_size, beta=-0.0, block_ngram_repeat=0,
#                coverage_penalty='none',
#                data_type='text', dump_beam='', fp32=False, gpu=0, ignore_when_blocking=[], length_penalty='none',
#                max_length=max_length, max_sent_length=None, min_length=0,
#                models=['model_released.pt'],
#                n_best=1, output="myoutput", phrase_table='', random_sampling_temp=1.0, random_sampling_topk=1, ratio=-0.0,
#                replace_unk=False, report_align=False, report_time=False, seed=829, stepwise_penalty=False, tgt=None,
#                verbose=False)
translator = build_translator(opt, report_score=False)

sent1 = "k r k # S 1".split(" ")
probs, sent1_trans = translator.translate(sent1, batch_size=len(sent1))
print(sent1_trans)
