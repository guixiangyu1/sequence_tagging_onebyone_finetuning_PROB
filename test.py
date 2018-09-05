from model.data_utils import CoNLLDataset, get_vocabs, get_processing_word
from model.config import Config


if __name__ == '__main__':
    config = Config()
    dev = CoNLLDataset(config.filename_dev, config.processing_word,
                       config.processing_tag, config.max_iter)
    i = 0
    for words,tags,masks in dev:
        pass
    print(1)
    for words,tags,masks in dev:
        pass
    print(2)
    for words,tags, masks in dev:
        if i < 20:
            print(words)
        i+=1





