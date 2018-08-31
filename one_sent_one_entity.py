



def file2list(filename):
    with open(filename) as f:
        all_tags = []
        tags = []
        words = []
        all_words = []
        for line in f:
            line = line.strip()
            if (len(line) == 0 or line.startswith("-DOCSTART-")):
                if len(words) != 0:
                    all_words += [words]
                    all_tags  += [tags]
                    words = []
                    tags  = []
            else:
                words += [line.split(' ')[0]]
                tags  += [line.split(' ')[-1]]
        if len(words) != 0:
            all_words += [words]
            words = []
            all_tags  += [tags]
            tags  = []
    return all_words, all_tags


def get_chunk(tags):
    """

    :param tags: [O,O,B-LOC,I-LOC,O]
    :return: [(2,4)]
    """
    chunk_start = None
    entity_chunk = []
    for i,tag in enumerate(tags):
        if tag.split('-')[0] == 'O' and chunk_start is not None:
            entity_chunk += [(chunk_start, i)]
            chunk_start = None
        elif tag.split('-')[0] == 'B':
            if chunk_start is not None:
                entity_chunk += [(chunk_start, i)]
            chunk_start = i
        else:
            pass
    if chunk_start is not None:
        entity_chunk += [(chunk_start, len(tags))]

    return entity_chunk



def one_entity_sent_write_file(all_words, all_tags, filename):
    with open(filename, "w") as f:
        for words, tags in zip(all_words, all_tags):

            for word, tag in zip(words, tags):
                entity_chunk = get_chunk(tags)
            for (entity_start, entity_end) in entity_chunk:
                for i, (word, tag) in enumerate(zip(words, tags)):
                    if i >= entity_start and i < entity_end:
                        f.write("{} {}\n".format(word, tag))
                    else:
                        f.write("{} O\n".format(word))
                f.write(("\n"))

def one_entity_file(filename_read, filename_write):
    all_words,all_tags = file2list(filename_read)
    one_entity_sent_write_file(all_words, all_tags, filename_write)
if __name__ == '__main__':
    one_entity_file("data/train.txt", "data/train1.txt")
    one_entity_file("data/test.txt", "data/test1.txt")
    one_entity_file("data/valid.txt", "data/valid1.txt")

