import csv
from pattern.en import pluralize

items_path = "items.txt"

numbers = ["S", "P"]
gramms = ["G", "U"]
out = []
with open(items_path) as items_f:
    for i, sent_str in enumerate(items_f):
        for number in numbers:
            for gramm in gramms:
                sent = sent_str.split()

                subj_idx = [idx for idx, w in enumerate(sent) if "(" in w]
                verb_idx = [idx for idx, w in enumerate(sent) if w == "was"]

                assert len(subj_idx) == 1
                subj_idx = subj_idx[0]
                verb_idx = verb_idx[0]

                if number == "S":
                    sent[subj_idx] = sent[subj_idx].split("(")[0]
                    if gramm == "U":
                        sent[verb_idx] = "were"

                else:
                    sent[subj_idx] = sent[subj_idx].replace("(", "").replace(")","")
                    if gramm == "G":
                        sent[verb_idx] = "were"

                condition = number + gramm
                out.append({"sentence": " ".join(sent),
                            "condition": condition,
                            "item": "WagersBaseline_{}_{}".format(i, condition),
                            "target": -1,
                            "alternative": -1
                            })

with open("".join(items_path.split(".")[:-1]) + ".csv", "w") as out_f:
    csv_out = csv.DictWriter(out_f, fieldnames = ["item", "condition", "sentence", "target", "alternative"])
    csv_out.writeheader()
    csv_out.writerows(out)

