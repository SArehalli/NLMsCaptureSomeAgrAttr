import csv 

item_path ="items.txt"

out = []

conds = ["SP", "PS"]

with open(item_path) as item_f:
    for i, line in enumerate(item_f):
        for idx, cond in enumerate(conds):
            *sent, pred = line.split()
            pred = pred.split("/")

            idxs = [ix for ix, word in enumerate(sent) if "/" in word]
            assert len(idxs) == 2
            
            sent[idxs[0]] = sent[idxs[0]].split("/")[idx] 
            sent[idxs[1]] = sent[idxs[1]].split("/")[1-idx] 
            
            out.append({"sentence":" ".join(sent),
                        "condition": cond,
                        "item": "HaskellMacDonald_{}_{}".format(i, cond),
                        "target": pred[1],
                        "alternative": pred[0]})


with open("".join(item_path.split(".")[:-1]) + ".csv", "w") as out_f:
    csv_out = csv.DictWriter(out_f, fieldnames = ["item", "condition", "sentence", "target", "alternative"])
    csv_out.writeheader()
    csv_out.writerows(out)
