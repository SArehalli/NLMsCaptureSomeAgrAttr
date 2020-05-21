import csv

conditions = ["CPD", "CPC", "CSC", "PPD", "PPC", "PSC"]

item_path = "items.txt"

out = []

with open(item_path) as item_f:
    for i, line in enumerate(item_f):
        for condition in conditions:
            sent = line.split()
            subj, attr, prep = condition

            idx = [ix for ix, word in enumerate(sent) if "/" in word]
            assert len(idx) == 3

            print([sent[i] for i in idx])

            if subj == "C":
                sent[idx[0]] = sent[idx[0]].split("/")[0]
            else:
                sent[idx[0]] = sent[idx[0]].split("/")[1]
            
            if prep == "D":
                sent[idx[1]] = sent[idx[1]].split("/")[0]
            else:
                sent[idx[1]] = sent[idx[1]].split("/")[1]
            
            if attr == "S":
                sent[idx[2]] = sent[idx[2]].split("/")[0]
            else:
                sent[idx[2]] = "".join(sent[idx[2]].split("/"))

            out.append({"sentence":" ".join(sent),
                        "condition": condition,
                        "item": "HumphreysBock_{}_{}".format(i, condition),
                        "target": "are",
                        "alternative": "is"
                        })

with open("".join(item_path.split(".")[:-1]) + ".csv", "w") as out_f:
    csv_out = csv.DictWriter(out_f, fieldnames = ["item", "condition", "sentence", "target", "alternative"])
    csv_out.writeheader()
    csv_out.writerows(out)
