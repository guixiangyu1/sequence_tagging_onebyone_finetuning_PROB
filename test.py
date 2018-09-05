from model.data_utils import CoNLLDataset, get_vocabs, get_processing_word
from model.config import Config


if __name__ == '__main__':
    config = Config()

    with open(config.filename_test) as f:
        for line in f:
            if "$NUM$" in line:
                print(1)
            if "$UNK$" in line:
                print(2)






