#!/usr/bin/env python3
"""
Non-neural baseline system for the SIGMORPHON 2022 Shared Task 0.

Author: Mans Hulden
Modified by: Tiago Pimentel
Modified by: Jordan Kodner
Modified by: Tomas Sourada
Last Update: 12/07/2023
"""

import sys, os, getopt, re
from functools import wraps
from glob import glob

import datetime
import pickle

def hamming(s,t):
    return sum(1 for x,y in zip(s,t) if x != y)


def halign(s,t):
    """Align two strings by Hamming distance."""
    slen = len(s)
    tlen = len(t)
    minscore = len(s) + len(t) + 1
    for upad in range(0, len(t)+1):
        upper = '_' * upad + s + (len(t) - upad) * '_'
        lower = len(s) * '_' + t
        score = hamming(upper, lower)
        if score < minscore:
            bu = upper
            bl = lower
            minscore = score

    for lpad in range(0, len(s)+1):
        upper = len(t) * '_' + s
        lower = (len(s) - lpad) * '_' + t + '_' * lpad
        score = hamming(upper, lower)
        if score < minscore:
            bu = upper
            bl = lower
            minscore = score

    zipped = zip(bu,bl)
    newin  = ''.join(i for i,o in zipped if i != '_' or o != '_')
    newout = ''.join(o for i,o in zipped if i != '_' or o != '_')
    return newin, newout


def levenshtein(s, t, inscost = 1.0, delcost = 1.0, substcost = 1.0):
    """Recursive implementation of Levenshtein, with alignments returned."""
    @memolrec
    def lrec(spast, tpast, srem, trem, cost):
        if len(srem) == 0:
            return spast + len(trem) * '_', tpast + trem, '', '', cost + len(trem)
        if len(trem) == 0:
            return spast + srem, tpast + len(srem) * '_', '', '', cost + len(srem)

        addcost = 0
        if srem[0] != trem[0]:
            addcost = substcost

        return min((lrec(spast + srem[0], tpast + trem[0], srem[1:], trem[1:], cost + addcost),
                   lrec(spast + '_', tpast + trem[0], srem, trem[1:], cost + inscost),
                   lrec(spast + srem[0], tpast + '_', srem[1:], trem, cost + delcost)),
                   key = lambda x: x[4])

    answer = lrec('', '', s, t, 0)
    return answer[0],answer[1],answer[4]


def memolrec(func):
    """Memoizer for Levenshtein."""
    cache = {}
    @wraps(func)
    def wrap(sp, tp, sr, tr, cost):
        if (sr,tr) not in cache:
            res = func(sp, tp, sr, tr, cost)
            cache[(sr,tr)] = (res[0][len(sp):], res[1][len(tp):], res[4] - cost)
        return sp + cache[(sr,tr)][0], tp + cache[(sr,tr)][1], '', '', cost + cache[(sr,tr)][2]
    return wrap


def alignprs(lemma, form):
    """Break lemma/form into three parts:
    IN:  1 | 2 | 3
    OUT: 4 | 5 | 6
    1/4 are assumed to be prefixes, 2/5 the stem, and 3/6 a suffix.
    1/4 and 3/6 may be empty.
    """

    al = levenshtein(lemma, form, substcost = 1.1) # Force preference of 0:x or x:0 by 1.1 cost
    alemma, aform = al[0], al[1]
    # leading spaces
    lspace = max(len(alemma) - len(alemma.lstrip('_')), len(aform) - len(aform.lstrip('_')))
    # trailing spaces
    tspace = max(len(alemma[::-1]) - len(alemma[::-1].lstrip('_')), len(aform[::-1]) - len(aform[::-1].lstrip('_')))
    return alemma[0:lspace], alemma[lspace:len(alemma)-tspace], alemma[len(alemma)-tspace:], aform[0:lspace], aform[lspace:len(alemma)-tspace], aform[len(alemma)-tspace:]


def prefix_suffix_rules_get(lemma, form):
    """Extract a number of suffix-change and prefix-change rules
    based on a given example lemma+inflected form."""
    lp,lr,ls,fp,fr,fs = alignprs(lemma, form) # Get six parts, three for in three for out

    # Suffix rules
    ins  = lr + ls + ">"
    outs = fr + fs + ">"
    srules = set()
    for i in range(min(len(ins), len(outs))):
        srules.add((ins[i:], outs[i:]))
    srules = {(x[0].replace('_',''), x[1].replace('_','')) for x in srules}

    # Prefix rules
    prules = set()
    if len(lp) >= 0 or len(fp) >= 0:
        inp = "<" + lp
        outp = "<" + fp
        for i in range(0,len(fr)):
            prules.add((inp + fr[:i],outp + fr[:i]))
            prules = {(x[0].replace('_',''), x[1].replace('_','')) for x in prules}

    return prules, srules


def apply_best_rule(lemma, msd, allprules, allsrules):
    """Applies the longest-matching suffix-changing rule given an input
    form and the MSD. Length ties in suffix rules are broken by frequency.
    For prefix-changing rules, only the most frequent rule is chosen."""

    bestrulelen = 0
    base = "<" + lemma + ">"
    if msd not in allprules and msd not in allsrules:
        return lemma # Haven't seen this inflection, so bail out

    if msd in allsrules:
        applicablerules = [(x[0],x[1],y) for x,y in allsrules[msd].items() if x[0] in base]
        if applicablerules:
            bestrule = max(applicablerules, key = lambda x: (len(x[0]), x[2], len(x[1])))
            base = base.replace(bestrule[0], bestrule[1])

    if msd in allprules:
        applicablerules = [(x[0],x[1],y) for x,y in allprules[msd].items() if x[0] in base]
        if applicablerules:
            bestrule = max(applicablerules, key = lambda x: (x[2]))
            base = base.replace(bestrule[0], bestrule[1])

    base = base.replace('<', '')
    base = base.replace('>', '')
    return base


def numleadingsyms(s, symbol):
    return len(s) - len(s.lstrip(symbol))


def numtrailingsyms(s, symbol):
    return len(s) - len(s.rstrip(symbol))

###############################################################################
def ptime():
    print("CURRENT TIME")
    print(datetime.datetime.now())

class SaveData:
    def __init__(self, prules, srules, prefbias, suffbias):
        self.prules = prules
        self.srules = srules
        self.prefbias = prefbias
        self.suffbias = suffbias

def main(argv):
    ptime()
    options, remainder = getopt.gnu_getopt(argv[1:], 'dtvhpo:', ['dev','test', 'oov', 'help','path=','outpath='])
    DEV, OOV, TEST, OUTPUT, HELP, path, outpath = False, False, False,False, False, '../../part1/development_languages/', ''
    for opt, arg in options:
        #if opt in ('-o', '--output'):
        #    OUTPUT = True
        if opt in ('-d', '--dev'):
            DEV = True
        elif opt in ('-t', '--test'):
            TEST = True
        elif opt in ('-v', '--oov'):
            OOV = True
        elif opt in ('-h', '--help'):
            HELP = True
        elif opt in ('-p', '--path'):
            path = arg
        elif opt in ('-o', '--outpath'):
            OUTPUT = True
            outpath = arg
    if HELP:
            print("\n*** Baseline for the SIGMORPHON 2022 shared task ***\n")
            print("By default, the program runs all languages only evaluating accuracy.")
            print("To create output files, use -o")
            print("The training and dev-data are assumed to live in ./part1/development_languages/")
            print("Options:")
            print(" -d         evaluate on dev")
            print(" -t         evaluate on test instead of dev")
            print(" -oov       evaluate on test-oov instead of dev")
            #print(" -o         create output files with guesses (and don't just evaluate)")
            print(" -p [path]  data files path. Default is ./part1/development_languages/")
            print(" -o [path]  output path. If not set, do not create output files with guesses")
            quit()

    if not DEV and not TEST and not OOV:
        print("You have to choose either -d, -t, or -v")
        quit()

    totalavg, totalavg_seenlemma, totalavg_seenmsd, totalavg_seenneither = 0, 0, 0, 0
    numlang, numlang_seenlemma, numlang_seenmsd, numlang_seenneither = 0, 0, 0, 0

    print("Lang:\tAll\tLemmas\tMSD\tNeither")
    for lang in sorted(list({re.sub('\.train.*$','',d) for d in os.listdir(path) if '.train' in d})):

        SAVE_FILE="saveData.pickle"
        #PRULES_FILE="prules.pickle"
        #if not os.path.isfile(SRULES_FILE) or not os.path.isfile(PRULES_FILE):
        if not os.path.isfile(SAVE_FILE):
            allprules, allsrules = {}, {}
            if not os.path.isfile(path + lang +  ".train"):
                continue
            lines = [line.strip() for line in open(path + lang + ".train", "r") if line != '\n']

            trainlemmas = set()
            trainmsds = set()
            # First, test if language is predominantly suffixing or prefixing
            # If prefixing, work with reversed strings
            prefbias, suffbias = 0,0
            for l in lines:
                lemma, form, msd = l.split(u'\t')
                trainlemmas.add(lemma)
                trainmsds.add(msd)
                aligned = halign(lemma, form)
                if ' ' not in aligned[0] and ' ' not in aligned[1] and '-' not in aligned[0] and '-' not in aligned[1]:
                    prefbias += numleadingsyms(aligned[0],'_') + numleadingsyms(aligned[1],'_')
                    suffbias += numtrailingsyms(aligned[0],'_') + numtrailingsyms(aligned[1],'_')
            for l in lines: # Read in lines and extract transformation rules from pairs
                lemma, form, msd = l.split(u'\t')
                if prefbias > suffbias:
                    lemma = lemma[::-1]
                    form = form[::-1]
                prules, srules = prefix_suffix_rules_get(lemma, form)
    
                if msd not in allprules and len(prules) > 0:
                    allprules[msd] = {}
                if msd not in allsrules and len(srules) > 0:
                    allsrules[msd] = {}

                for r in prules:
                    if (r[0],r[1]) in allprules[msd]:
                        allprules[msd][(r[0],r[1])] = allprules[msd][(r[0],r[1])] + 1
                    else:
                        allprules[msd][(r[0],r[1])] = 1
    
                for r in srules:
                    if (r[0],r[1]) in allsrules[msd]:
                        allsrules[msd][(r[0],r[1])] = allsrules[msd][(r[0],r[1])] + 1
                    else:
                        allsrules[msd][(r[0],r[1])] = 1
            print("After extracting rules")
            ptime()
            saveData = SaveData(allprules,allsrules,prefbias,suffbias)
            
            with open(SAVE_FILE, 'wb') as save_file:
                # A new file will be created
                pickle.dump(saveData, save_file)
            #with open(SRULES_FILE, 'wb') as srules_file:
                # A new file will be created
            #    pickle.dump(allsrules, srules_file)
            #with open(PRULES_FILE, 'wb') as prules_file:
                # A new file will be created
            #    pickle.dump(allprules, prules_file)
            print("After pickling rules")

        else:
            with open(SAVE_FILE, 'rb') as save_file:
                saveData = pickle.load(save_file)
                allprules = saveData.prules
                allsrules = saveData.srules
                prefbias = saveData.prefbias
                suffbias = saveData.suffbias
            #with open(SRULES_FILE, 'rb') as srules_file:
            #    allsrules = pickle.load(srules_file)
            #with open(PRULES_FILE, 'rb') as prules_file:
            #    allprules = pickle.load(prules_file)
            print("After loading already pickled rules")
        ptime()
        # Run eval on dev
        if DEV:
            evallines = [line.strip() for line in open(path + lang.split("_")[0] + ".dev", "r") if line != '\n']
        elif TEST:
            evallines = [line.strip() for line in open(path + lang.split("_")[0] + ".gold", "r") if line != '\n']
        elif OOV:
            evallines = [line.strip() for line in open(path + lang.split("_")[0] + ".test-oov", "r") if line != '\n']
        
        num_seenlemma_correct, num_seenmsd_correct, num_seenneither_correct = 0, 0, 0
        num_seenlemma_guesses, num_seenmsd_guesses, num_seenneither_guesses = 0, 0, 0
        numcorrect, numguesses = 0, 0
        if OUTPUT:
            if DEV:
                outfile = open(outpath + lang + ".dev", "w")
            elif TEST:
                outfile = open(outpath + lang + ".test", "w")
            elif OOV:
                outfile = open(outpath + lang + ".test-oov", "w")

        # My counter
        supercounter = 0
        for l in evallines:
            supercounter += 1
            if supercounter % 1000 == 0:
                print(f"Translation: {supercounter}")
            lemma, correct, msd, = l.split(u'\t')
#                    lemma, msd, = l.split(u'\t')
            if prefbias > suffbias:
                lemma = lemma[::-1]
            outform = apply_best_rule(lemma, msd, allprules, allsrules)
            if prefbias > suffbias:
                outform = outform[::-1]
                lemma = lemma[::-1]
            # MAKE IT QUICKER BY REMOVING THE COUNTING
            #if lemma in trainlemmas:
            #    num_seenlemma_guesses += 1
            #    if outform == correct:
            #        num_seenlemma_correct += 1
            #elif msd in trainmsds:
            #    num_seenmsd_guesses += 1
            #    if outform == correct:
            #        num_seenmsd_correct += 1
            #else:
            #    num_seenneither_guesses += 1
            #    if outform == correct:
            #        num_seenneither_correct += 1
            if OUTPUT:
                outfile.write(lemma + "\t" + outform + "\t" + msd + "\n")

        if OUTPUT:
            outfile.close()
        print("after evaluation")
        ptime()
        numlang += 1
        
#        if num_seenlemma_guesses:
#            percentcorrect_seenlemma = num_seenlemma_correct/num_seenlemma_guesses
#            totalavg_seenlemma += percentcorrect_seenlemma
#            numlang_seenlemma += 1
#        else:
#            percentcorrect_seenlemma = 0
#        if num_seenmsd_guesses:
#            percentcorrect_seenmsd = num_seenmsd_correct/num_seenmsd_guesses
#            totalavg_seenmsd += percentcorrect_seenmsd
#            numlang_seenmsd += 1
#        else:
#            percentcorrect_seenmsd = 0
#        if num_seenneither_guesses:
#            percentcorrect_seenneither = num_seenneither_correct/num_seenneither_guesses
#            totalavg_seenneither += percentcorrect_seenneither
#            numlang_seenneither += 1
#        else:
#            percentcorrect_seenneither = 0
#        numcorrect = num_seenlemma_correct + num_seenmsd_correct + num_seenneither_correct
#        numguesses = num_seenlemma_guesses + num_seenmsd_guesses + num_seenneither_guesses
#        totalavg += numcorrect/numguesses

 #       print("%s:\t%s\t%s\t%s\t%s\t\t%s\t%s\t%s\t%s" % (lang, round(100*numcorrect/numguesses,3), round(100*percentcorrect_seenlemma,3), round(100*percentcorrect_seenmsd,3), round(100*percentcorrect_seenneither,3), numguesses, num_seenlemma_guesses, num_seenmsd_guesses, num_seenneither_guesses))

#    print("Average accuracy total\t\t", round(100*totalavg/numlang,3))
#    if numlang_seenlemma:
#        print("Average accuracy seen lemmas\t", round(100*totalavg_seenlemma/numlang_seenlemma,3))
#    if numlang_seenmsd:
#        print("Average accuracy seen msds\t", round(100*totalavg_seenmsd/numlang_seenmsd,3))
#    if numlang_seenneither:
#        print("Average accuracy seen neither\t", round(100*totalavg_seenneither/numlang_seenneither,3))


if __name__ == "__main__":
    main(sys.argv)
