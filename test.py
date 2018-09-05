from model.data_utils import CoNLLDataset, get_vocabs, get_processing_word
from model.config import Config


if __name__ == '__main__':
    config = Config()
    i, j = 0, 0
    with open(config.filename_train) as f:
        for line in f:
            if "$NUM$" in line:
                i += 1
            if "$UNK$" in line:

                j += 1
        print(i, j)






