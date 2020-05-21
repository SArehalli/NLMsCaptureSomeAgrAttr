import csv
from pattern.en import pluralize

items_path = "items.txt"
subj_idx = 1
attr_1_idx = 4
attr_2_idx = -1

labels = ["S", "P"]
out = []
with open(items_path) as items_f:
    for i, sent_str in enumerate(items_f):
        for subj_p in [0, 1]:
            for attr_1_p in [0, 1]:
                for attr_2_p in [0, 1]:
                    sent = sent_str.split()
                    condition = labels[subj_p] + labels[attr_1_p] + labels[attr_2_p] 
                    if subj_p: sent[subj_idx] = pluralize(sent[subj_idx])
                    if attr_1_p: sent[attr_1_idx] = pluralize(sent[attr_1_idx])
                    if attr_2_p: sent[attr_2_idx] = pluralize(sent[attr_2_idx])
                    out.append({"sentence": " ".join(sent),
                                "condition": condition,
                                "item": "Franck_{}_{}".format(i, condition),
                                "target": "is" if labels[subj_p] == "S" else "are",
                                "alternative": "is" if labels[1-subj_p] == "S" else "are"
                                })

with open("".join(items_path.split(".")[:-1]) + ".csv", "w") as out_f:
    csv_out = csv.DictWriter(out_f, fieldnames = ["item", "condition", "sentence", "target", "alternative"])
    csv_out.writeheader()
    csv_out.writerows(out)

