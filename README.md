# cz-inflect-dev

## Development directory of cz-inflect project


# RP Sourada
TODO
git@gitlab.mff.cuni.cz:teaching/nprg045/rosa/rp-sourada.git


# To start on a new server:
1) generate the ssh-keypair on the remote machine, based on the page
https://gitlab.mff.cuni.cz/help/user/ssh.md

Generate an SSH key pair
If you do not have an existing SSH key pair, generate a new one:


Open a terminal.


Run ssh-keygen -t followed by the key type and an optional comment.
This comment is included in the .pub file that's created.
You may want to use an email address for the comment.
For example, for ED25519:

ssh-keygen -t ed25519 -C "<comment>"

From github, run it with your github email in comment:
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

For 2048-bit RSA:

ssh-keygen -t rsa -b 2048 -C "<comment>"

Press Enter. Output similar to the following is displayed:

Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/user/.ssh/id_ed25519):

Accept the suggested filename and directory, unless you are generating a deploy key
or want to save in a specific directory where you store other keys.
You can also dedicate the SSH key pair to a specific host.


Specify a passphrase:

Enter passphrase (empty for no passphrase):
Enter same passphrase again:
A confirmation is displayed, including information about where your files are stored.


A public and private key are generated. Add the public SSH key to your GitLab account
and keep the private key secure.

2) git clone git@gitlab.mff.cuni.cz:teaching/nprg045/rosa/rp-sourada.git

If you are receiving error:
Cloning into...
git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.
Please make sure you have the correct access rights
and the repository exists.

... try running the ssh agent: 
> eval $(ssh-agent)
and possibly adding the ssh key:
> ssh-add ~/.ssh/id_rsa_specific_private_key_path


3) run new interactive job
qsub -l select=1:ncpus=1:mem=8gb:scratch_local=16gb -I
export TMPDIR=$SCRATCHDIR && \
module add python/3.8.0-gcc-rab6t cuda/cuda-11.2.0-intel-19.0.4-tn4edsz cudnn/cudnn-8.1.0.77-11.2-linux-x64-intel-19.0.4-wx22b5t && \
cd /storage/praha1/home/souradat

change dir to /.../rp-sourada/czech-automatic-inflection/

#4) run make build_data (creates the venv, downloads and builds the data)




4a) create the venv manually
mkdir -p .venv && \
python3 -m venv .venv && \
.venv/bin/pip install --no-cache-dir --upgrade pip setuptools && \
.venv/bin/python3 -m pip install -e .

4b) install requirements
.venv/bin/pip3 install --no-cache-dir -r requirements.txt

4c) build the data
run `make build_data`
