import numpy as np

def get_label_chunk(seq):
    chunks = []
    chunk_type, chunk_start = None, None
    for i, tok in enumerate(seq):
        if tok == "O" and chunk_type != None:
            chunk = (chunk_type, chunk_start, i)
            chunks += [chunk]
            chunk_type, chunk_start =None, None
        elif tok != "O":
            tok_chunk_class, tok_chunk_type = get_chunk_type(tok)
            if chunk_type is None:
                chunk_type, chunk_start = tok_chunk_type, i
            elif tok_chunk_type != chunk_type or tok_chunk_class == "B":
                chunk = (chunk_type, chunk_start, i)
                chunks.append(chunk)
                chunk_type, chunk_start = tok_chunk_type, i
        else:
            pass
    if chunk_type is not None:
        chunk = (chunk_type, chunk_start, len(seq))
        chunks.append(chunk)
    return chunks



def get_chunk_type(tok):
    chunk_class = tok.split('-')[0]
    chunk_type  = tok.split('-')[-1]
    return  chunk_class, chunk_type


def main():
    tags = []
    whole_tag = []

    with open("data/transit.txt") as f:
        for line in f:
            line = line.strip()
            if len(line) != 0:
                tag = line.split(' ')[-1].split('-')[0]
                tags += [tag]
            else:
                if len(tags) != 0:
                    whole_tag += [tags]
                    tags = []
        if len(tags) != 0:
            whole_tag += [tags]
            tag = []

    category = []
    whole_category = []
    with open("data/result.txt") as g:
        for line in g:
            line = line.strip()
            if len(line) == 0:
                if len(category) != 0:
                    whole_category += [category]
                    category = []
            else:
                category += [line]
        if len(category) != 0:
            whole_category += [category]
            category = []
    print(len(whole_category),len(whole_tag))

    chunk = []
    tag_chunk = []
    tags_chunk =[]
    for tags in whole_tag:
        for tag in tags:
            if tag != "I":
                if len(tag_chunk) != 0:
                    chunk += [tag_chunk]
                    tag_chunk = [tag]
                else:
                    tag_chunk = [tag]
            else:
                tag_chunk += [tag]
        if len(tag_chunk) != 0:
            chunk += [tag_chunk]
            tag_chunk = []
        tags_chunk += [chunk]
        chunk = []

    tag_pred = []
    tags_pred = []

    for i,j in zip(tags_chunk, whole_category):
        for a,b in zip(i,j):
            for c in a:
                if c != "O":
                    tg = c + '-' + b
                    tag_pred += [tg]
                else:
                    tag_pred += ["O"]

        tags_pred += [tag_pred]
        tag_pred = []

    #print(tags_pred)

    tag, tags = [], []
    with open("data/test.txt") as f:
        words, tags = [], []
        for line in f:
            line = line.strip()  # 去掉前后的空格
            if (len(line) == 0 or line.startswith("-DOCSTART-")):
                if len(tag) != 0:
                    tags += [tag]
                    tag = []
            else:
                tag += [line.split(' ')[-1]]

        if len(tag) != 0:
            tags += [tag]
            tag = []
    #print(tags)

    correct_preds, total_preds, total_correct = 0., 0., 0.
    accs = []
    for label, label_pred in zip(tags, tags_pred):
        for i,j in zip(label, label_pred):
            accs += [i==j]
        #print(get_label_chunk(label))
        lab_chunks = set(get_label_chunk(label))
        lab_pred_chunks = set(get_label_chunk(label_pred))
        correct_preds += len(lab_chunks & lab_pred_chunks)
        total_preds   += len(lab_pred_chunks)

        total_correct += len(lab_chunks)
    print(correct_preds, total_preds,total_correct,)
    p = correct_preds / total_preds if correct_preds > 0 else 0
    r   = correct_preds / total_correct if correct_preds > 0 else 0
    f1  = 2 * p * r / (p + r) if correct_preds > 0 else 0
    acc = np.mean(accs)
    print("acc: ", acc)
    print("f1 : ", f1)
    print("r: ", r)
    print("p: ", p)








if __name__ == '__main__':
    main()








