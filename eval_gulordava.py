import torch
import torch.nn as nn
import torch.nn.functional as F

import numpy as np
import matplotlib.pyplot as plot

import argparse

import sys
sys.path.insert(0, "./colorlessgreenRNNs/src/language_models")
from dictionary_corpus import Dictionary

import pandas as pd
import seaborn as sns
import matplotlib as plt

def indexify(word):
    """ Convert word to an index into the embedding matrix """
    if word not in dictionary.word2idx:
        print("Warning: {} not in vocab".format(word))
    return dictionary.word2idx[word] if word in dictionary.word2idx else dictionary.word2idx["<unk>"]

def sample_prob_scoring(target, alternative):
    """ sampling linking hypothesis in log-space """
    denom = np.logaddexp(target.item(), alternative.item())
    correct = target.item() - denom
    
    return 100 * np.exp(correct)

def max_prob_scoring(target, alternative):
    """ max prob linking hypothesis in log-space """
    correct = 1 if target > alternative else 0 

    return 100 * correct

def surprisal_scoring(target, alternative):
    """ surprisal difference scoring """
    return -target + alternative

def get_score(targets, next_pred):
    """ Get a score for a set of target words """
    score = -np.inf
    for target in targets:
        target = indexify(target)
        score = np.logaddexp(score, next_pred[target].item())
    return score


parser = argparse.ArgumentParser()
parser.add_argument("--seed", type=int, default=1)
parser.add_argument("--model", type=str, required=True)
parser.add_argument("--data", type=str, required=True)
parser.add_argument("--input", type=str, required=True)
parser.add_argument("--scoring", type=str, default="max")
parser.add_argument("--paradigm", type=str, default="prod")
parser.add_argument("--out", type=str)
parser.add_argument("--latex", action="store_true")
parser.add_argument("--batch_size", type=int, default=1)
parser.add_argument("--cuda", action="store_true")
parser.add_argument("--flip", action="store_true")
parser.add_argument("--verbose", action="store_true")
parser.add_argument("--plot", action="store_true")

args = parser.parse_args()

# Make it reproduceable
torch.manual_seed(args.seed)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
np.random.seed(args.seed)

# Load models from comma-separated arg
model_fns = args.model.split(",")
models = []
for model_fn in model_fns:
    model = torch.load(model_fn)

    if args.cuda:
        model = model.cuda()
    else:
        model = model.cpu()

    model.eval()
    models.append(model)

# Load vocab
dictionary = Dictionary(args.data)

# Load experimental data csv
inp = pd.read_csv(args.input)

# Get scorers from comma-separated arg
scorers = []
args.scoring = set(args.scoring.split(","))
if "max" in args.scoring:
    scorers.append(("max", max_prob_scoring))
if "sample" in args.scoring:
    scorers.append(("sample", sample_prob_scoring))
if "surp" in args.scoring:
    scorers.append(("surprisal", surprisal_scoring))

for model_num, model in enumerate(models):
    corrects = {}
    target_s = []
    alt_s = []

    surpss = []
    total_surps = []

    with torch.no_grad():
        for sentence, target, alternative in zip(inp["sentence"], inp["target"], inp["alternative"]):
            input = torch.LongTensor([indexify(w) for w in sentence.split()])
            
            if args.cuda:
                input = input.cuda()

            out, _ = model(input.view(-1, 1), model.init_hidden(1))

            if args.paradigm == "comp":
                # Get surprisals for the first 10 words
                surps = []
                for i, word_idx in enumerate(input[1:11]):
                    surps.append(-F.log_softmax(out[i], dim=-1).view(-1)[word_idx].item())
                for i in range(10 - len(input[1:11])):
                    surps.append(-1)
                surpss.append(surps)
                # Get surprisals over the fill sentence
                total_surps.append(sum([-F.log_softmax(out[i], dim=-1).view(-1)[word_idx].item() 
                                        for i,word_idx in enumerate(input[1:])]))

            elif args.paradigm == "prod":
                next_pred = out[-1] 

                # use scorers/linking functions to eval on the target and alternative words' scores
                next_pred = F.log_softmax(next_pred, dim=-1).view(-1)
                target_scores = get_score(target.split(","), next_pred)
                alt_scores = get_score(alternative.split(","), next_pred)

                for scorer in scorers:
                    correct = scorer[1](target_scores, alt_scores)
                    corrects[scorer[0]] = corrects.get(scorer[0], []) + [correct]

                target_s.append(target_scores.item())
                alt_s.append(alt_scores.item())
    
# write out to csv
    if args.paradigm == "prod":
        for scorer_name, _ in scorers:
            inp["lstm {} correct ({})".format(model_num, scorer_name)] = corrects[scorer_name]

        inp["lstm {} target score".format(model_num)] = target_s
        inp["lstm {} alternative score".format(model_num)] = alt_s

    if args.paradigm == "comp":
        surpss = np.array(surpss)
        surpss = surpss.transpose()
        for i, position in enumerate(surpss):
            print(len(position))
            inp["(lstm {} at word {})".format(model_num, i + 1)] = position
        inp["lstm {} (surprisal)".format(model_num)] = total_surps


if args.out is None: args.out = args.input
inp.to_csv(args.out)
