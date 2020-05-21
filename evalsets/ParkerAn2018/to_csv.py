import csv


item_path = "items.txt"
out = []

out_comp = []
with open(item_path) as items_f:
    for i, sent_str in enumerate(items_f):

        idxs = [idx for idx, word in enumerate(sent_str.split()) if "/" in word]
        for num_idx, attr_num in enumerate(["S", "P"]):
            for env_idx, attr_env in enumerate(["OBLIQUE","CORE"]):
                sent = sent_str.split("|")[0].split()
                sent[idxs[0]] = sent[idxs[0]].split("/")[env_idx]
                sent[idxs[1]] = sent[idxs[1]].split("/")[num_idx]
                out.append({"sentence":" ".join(sent),
                            "condition": attr_env + "_" + attr_num,
                            "item": "ParkerAn_{}_{}_{}".format(i, attr_env, attr_num),
                            "target": "was",
                            "alternative": "were"})

        for num_idx, attr_num in enumerate(["S", "P"]):
            for env_idx, attr_env in enumerate(["OBLIQUE","CORE"]):
                for vi, verb in enumerate(["was", "were"]):
                    sent = sent_str.split()
                  
                    verb_idxs = [idx for idx, word in enumerate(sent) if word == "|"]
                    assert len(verb_idxs) == 1
                    verb_idx = verb_idxs[0]
                    
                    sent[idxs[0]] = sent[idxs[0]].split("/")[env_idx]
                    sent[idxs[1]] = sent[idxs[1]].split("/")[num_idx]
                    sent[verb_idx] = verb

                    gramm = "G" if num_idx == vi else "U"

                    out_comp.append({"sentence":" ".join(sent),
                                "condition": attr_env + "_" + attr_num + "_" + gramm,
                                "item": "ParkerAn_{}_{}_{}_{}".format(i, attr_env, attr_num, gramm),
                                "target": "",
                                "alternative": ""})




with open("".join(item_path.split(".")[:-1]) + ".csv", "w") as out_f:
    csv_out = csv.DictWriter(out_f, fieldnames = ["item", "condition", "sentence", "target", "alternative"])
    csv_out.writeheader()
    csv_out.writerows(out)

with open("".join(item_path.split(".")[:-1]) + ".comp.csv", "w") as out_f:
    csv_out = csv.DictWriter(out_f, fieldnames = ["item", "condition", "sentence", "target", "alternative"])
    csv_out.writeheader()
    csv_out.writerows(out_comp)
