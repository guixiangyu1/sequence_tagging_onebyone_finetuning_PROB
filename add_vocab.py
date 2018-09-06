from model.config import Config
from model.data_utils import CoNLLDataset1, get_vocabs, UNK, NUM, \
    get_glove_vocab, write_vocab, load_vocab, get_char_vocab, \
    export_trimmed_glove_vectors, get_processing_word, entity2vocab


def main():
    """Procedure to build data

    You MUST RUN this procedure. It iterates over the whole dataset (train,
    dev and test) and extract the vocabularies in terms of words, tags, and
    characters. Having built the vocabularies it writes them in a file. The
    writing of vocabulary in a file assigns an id (the line #) to each word.
    It then extract the relevant GloVe vectors and stores them in a np array
    such that the i-th entry corresponds to the i-th word in the vocabulary.


    Args:
        config: (instance of Config) has attributes like hyper-params...

    """
    # get config and processing of words
    config = Config(load=False)
    processing_word = get_processing_word(lowercase=True) # 把字符全部小写，数字替换成NUM

    # Generators

    to_be_add  = CoNLLDataset1(config.filename_test, processing_word) # 返回一句话（words），和标签tags


    # Build Word and Tag vocab

    vocab_words, _ = get_vocabs([to_be_add])
    vocab_glove = get_glove_vocab(config.filename_glove)  # glove词表

    words_have_vec = vocab_words & vocab_glove

    vocab_words_and_entity = entity2vocab(datasets=[to_be_add], vocab=words_have_vec)

    vocab_in_file = set(load_vocab(config.filename_words))

    vocab_words_to_be_add = vocab_words_and_entity - vocab_in_file

    if len(vocab_words_to_be_add) != 0:
        with open(config.filename_words, 'a') as f:
            for i, vocab_word in enumerate(vocab_words_to_be_add):
                f.write('\n{}'.format(vocab_word))


    # Trim GloVe Vectors
    vocab = load_vocab(config.filename_words)    # 得到dict类型的vocab：{word:index}
    # 针对vocab，生成numpy的embedding文件，包含一个矩阵，对应词嵌入
    export_trimmed_glove_vectors(vocab, config.filename_glove,
                                config.filename_trimmed, config.dim_word)



if __name__ == "__main__":
    main()
