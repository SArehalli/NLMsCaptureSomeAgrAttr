import csv
from pattern.en import pluralize

items_path = "items.txt"

def get_var(s, idx):
    if "/" in s:
        return s.split("/")[idx]
    elif "(" in s:
        base = s.split("(")[0]
        affix = s.split("(")[1][:-1]
        return base + (affix if idx == 1 else "")

numbers = ["S", "P"]
gramms = ["U", "G"]
out = []
with open(items_path) as items_f:
    for i, sent_str in enumerate(items_f):
        for subj_number,subj_label in enumerate(numbers):
            for attr_number, attr_label in enumerate(numbers):
                for gramm, gramm_label in enumerate(gramms):
                    sent = sent_str.split()

                    idxs = [idx for idx, w in enumerate(sent) if ("(" in w) or ("/" in w)]
                    print(i, idxs)


                    sent[idxs[1]] = get_var(sent[idxs[1]], subj_number)
                    sent[idxs[2]] = get_var(sent[idxs[2]], subj_number ^ gramm)

                    sent[idxs[0]] = get_var(sent[idxs[0]], attr_number)
                    
                    for idx in idxs[3:]:
                        sent[idx] = get_var(sent[idx], 1 - attr_number)

                    condition = subj_label + attr_label + gramm_label
                    out.append({"sentence": " ".join(sent),
                                "condition": condition,
                                "item": "Wagers23_{}_{}".format(i, condition),
                                "target": -1,
                                "alternative": -1
                                })

with open("".join(items_path.split(".")[:-1]) + ".csv", "w") as out_f:
    csv_out = csv.DictWriter(out_f, fieldnames = ["item", "condition", "sentence", "target", "alternative"])
    csv_out.writeheader()
    csv_out.writerows(out)

