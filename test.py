from model.data_utils import CoNLLDataset1, get_vocabs, get_processing_word
from model.config import Config


if __name__ == '__main__':
    config = Config()
    with open(config.filename_words) as f:
        for line in f:
            if "Peter$@&Blackburn" in line:
                print(True)






