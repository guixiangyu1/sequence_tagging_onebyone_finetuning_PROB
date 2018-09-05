from model.data_utils import CoNLLDataset1, get_vocabs, get_processing_word
from model.config import Config
import numpy as np


if __name__ == '__main__':
    config = Config()
    embeddings = np.load(config.filename_trimmed)
    for i in embeddings:
        print(i)






