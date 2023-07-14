#!/bin/bash

export TMPDIR=$SCRATCHDIR
module add python/3.8.0-gcc-rab6t cuda/cuda-11.2.0-intel-19.0.4-tn4edsz cudnn/cudnn-8.1.0.77-11.2-linux-x64-intel-19.0.4-wx22b5t

# -e error_dir
# -o output_dir
# -m for email notifications
#qsub -m ea -q gpu -l select=1:ncpus=1:ngpus=1:mem=16gb:scratch_local=8gb:pbs_server=^cerit-pbs.cerit-sc.cz $1
#qsub -m ea -q gpu -l select=1:ncpus=1:ngpus=1:mem=16gb:pbs_server=^cerit-pbs.cerit-sc.cz $1

# PBS server cerit was not working, 
# host konos1 was offline.
#qsub -m ea -q gpu -l select=1:ncpus=1:ngpus=1:mem=16gb:pbs_server=^cerit-pbs.cerit-sc.cz:host=^konos1.fav.zcu.cz $1

qsub -m ea -q gpu -l select=1:ncpus=1:ngpus=1:mem=16gb:gpu_mem=20gb $1
