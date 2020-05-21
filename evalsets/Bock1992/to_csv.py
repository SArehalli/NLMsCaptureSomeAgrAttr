import csv
from pattern.en import pluralize

items_path = "items.txt"

subj_conds = ["s", "p"]
local_conds = ["s", "p"]
clauses = ["prop", "rc"]

out = []
with open(items_path) as items_f:
    for i, line in enumerate(items_f):
        for subj_cond in subj_conds:
            for local_cond in local_conds:
                for clause in clauses:             
                    pre, rest = line.split("[")
                    mid, later = rest.split("]")
                    prop, rc = mid.split("/")
                    
                    mid = prop if clause == "prop" else rc
                    sent = " ".join([pre, mid, later]).split()
                    
                    idxs = [i for i,w in enumerate(sent) if "(" in w]

                    assert(len(idxs) == 2)
                    subj_idx, local_idx = idxs

                    if subj_cond == "s":
                        sent[subj_idx] = sent[subj_idx].split("(")[0]
                    else:
                        sent[subj_idx] = pluralize(sent[subj_idx].split("(")[0])

                    if local_cond == "s":
                        sent[local_idx] = sent[local_idx].split("(")[0]
                    else:
                        sent[local_idx] = pluralize(sent[local_idx].split("(")[0])

                    out.append({"sentence": " ".join(sent),
                                "condition": subj_cond + local_cond + "_" + clause,
                                "item": "Bock1992_{}_{}_{}".format(i, subj_cond + local_cond, clause),
                                "target": "is" if subj_cond == "s" else "are",
                                "alternative": "is" if subj_cond == "p" else "are",
                                })

with open("".join(items_path.split(".")[:-1]) + ".csv", "w") as out_f:
    csv_out = csv.DictWriter(out_f, fieldnames = ["item", "condition", "sentence", "target", "alternative"])
    csv_out.writeheader()
    csv_out.writerows(out)





