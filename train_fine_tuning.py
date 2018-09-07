from model.data_utils import CoNLLDataset
from model.ner_model import NERModel
from model.config import Config


def main():
    # create instance of config，这里的config实现了load data的作用
    #拥有词表、glove训练好的embeddings矩阵、str->id的function
    config = Config()
    config.nepochs          = 200
    config.dropout          = 0.5
    config.batch_size       = 40
    config.lr_method        = "adam"
    config.lr               = 0.0003
    config.lr_decay         = 0.96
    config.clip             = -5.0 # if negative, no clipping
    config.nepoch_no_imprv  = 10
    
    # build model
    model = NERModel(config)
    model.build("fine_tuning")
    model.restore_session(config.dir_model)

    # model.restore_session("results/crf/model.weights/") # optional, restore weights
    # model.reinitialize_weights("proj")

    # create datasets [(char_ids), word_id]
    dev   = CoNLLDataset(config.filename_dev, config.processing_word,
                         config.processing_tag, config.max_iter)
    train = CoNLLDataset(config.filename_train, config.processing_word,
                         config.processing_tag, config.max_iter)

    # train model
    model.train(train, dev)

if __name__ == "__main__":
    main()
