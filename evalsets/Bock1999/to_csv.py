import csv
from pattern.en import pluralize

items_path = "items.txt"

subj_conds = ["s", "p", "c"]
local_conds = ["s", "p"]
target_conds = ["verb", "tag", "reflexive"]

out = []
with open(items_path) as items_f:
    for i, line in enumerate(items_f):
        for subj_cond in subj_conds:
            for local_cond in local_conds:
                for target_cond in target_conds:
                    condition = "{}{}({})".format(subj_cond, local_cond, target_cond)
                    sent = line.split()
                    
                    idx = [ix for ix, word in enumerate(sent) if ("/" in word or "(" in word)]
                    assert len(idx) == 3

                    if target_cond == "verb":
                        sent = sent[:-1]
                        target,alternative = "were", "was"
                    if target_cond == "reflexive":
                        sent[idx[2]] = sent[idx[2]][1:-1].split("/")[0]
                        target,alternative ="themselves","himself,herself,itself" 
                    if target_cond == "tag":
                        sent[idx[2]] = sent[idx[2]][1:-1].split("/")[1]
                        sent += ["did", "n't"]
                        target,alternative = "they", "he,she,it" 

                    if subj_cond == "s":
                        sent[idx[0]] = sent[idx[0]].split("(")[0]
                    elif subj_cond == "p":
                        sent[idx[0]] = pluralize(sent[idx[0]].split("(")[0])
                    else:
                        sent[idx[0]] = sent[idx[0]].split("/")[1]
                    
                    if local_cond == "s":
                        sent[idx[1]] = sent[idx[1]].split("(")[0]
                    else:
                        sent[idx[1]] = pluralize(sent[idx[1]].split("(")[0])

                    
                    out.append({"sentence": " ".join(sent),
                                "condition": condition,
                                "item": "Bock1999_{}_{}".format(i, condition),
                                "target": target,
                                "alternative": alternative
                                })

with open("".join(items_path.split(".")[:-1]) + ".csv", "w") as out_f:
    csv_out = csv.DictWriter(out_f, fieldnames = ["item", "condition", "sentence", "target", "alternative"])
    csv_out.writeheader()
    csv_out.writerows(out)





