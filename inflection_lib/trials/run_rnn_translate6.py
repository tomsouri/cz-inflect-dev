from onmt.translate.translator import build_translator
from onmt.bin.translate import _get_parser
from argparse import Namespace

path = "model_released.pt"

parser = _get_parser()

opt = parser.parse_args()


#from onmt.translate.translator import build_translator
#from argparse import Namespace

#path = 'averaged-10-epoch.pt'
#opt = Namespace(alpha=0.0, batch_type='sents', beam_size=5, beta=-0.0, block_ngram_repeat=0, coverage_penalty='none', data_type='text', dump_beam='', fp32=False, gpu=-1, ignore_when_blocking=[], length_penalty='none', max_length=100, max_sent_length=None, min_length=0, models=['openmnt/averaged-10-epoch.pt'], n_best=1, output='/dev/null', phrase_table='', random_sampling_temp=1.0, random_sampling_topk=1, ratio=-0.0, replace_unk=False, report_align=False, report_time=False, seed=829, stepwise_penalty=False, tgt=None, verbose=False)
translator = build_translator(opt, report_score=False)


sentence = 'j a b l k o # S 7'

translated = translator.translate([sentence], batch_size=1)
print(translated[1][0][0])


#translator.translate(['it kinda works'], batch_size=1)


#opt = Namespace(models=[path], n_best=1, alpha=0.0, batch_type='sents', beam_size=5, beta=-0.0, block_ngram_repeat=0, coverage_penalty='none', data_type='text', dump_beam='', fp32=False, gpu=-1, ignore_when_blocking=[], length_penalty='none', max_length=100, max_sent_length=None, min_length=0, output='/dev/null', phrase_table='', random_sampling_temp=1.0, random_sampling_topk=1, ratio=-0.0, replace_unk=False, report_align=False, report_time=False, seed=829, stepwise_penalty=False, tgt=None, verbose=False, int8=False, random_sampling_topp=0, ban_unk_token=False, tgt_prefix=False, tgt_file_prefix=False, with_score=False)

#translator = build_translator(opt, report_score=False)

#sentence = 'j a b l k o # S 7'

#translated = translator._translate([sentence])
#print(translated[1][0][0])
