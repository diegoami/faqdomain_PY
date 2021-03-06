MIN_FREQUENCY = 3
DICTIONARY_FILENAME   = 'dictionary'
CORPUS_FILENAME       = 'corpus'
LSI_FILENAME          = 'lsi'
INDEX_FILENAME        = 'index'


from gensim import corpora, models, similarities
import numpy as np

import logging

from gensim import corpora, models, similarities
from gensim.corpora import MmCorpus

class TfidfFacade():

    def __init__(self, model_dir, no_below=5, no_above=0.78, num_topics=400, version=1):
        self.model_dir = model_dir
        self.no_below=no_below
        self.no_above=no_above
        self.num_topics= num_topics
        self.version = version

    def create_all_models(self, texts):
        corpus, dictionary =  self.create_dictionary(texts)
        lsi = self.create_model(corpus, dictionary)
        self.create_matrix(lsi, corpus)

    def create_dictionary(self, texts):
        dictionary = corpora.Dictionary(texts)
        logging.info("Initializing dictionary with {} texts".format(len(texts)))

        dictionary.filter_extremes(no_below=self.no_below, no_above=self.no_above, keep_n=150000)
        dictionary.save(self.model_dir+DICTIONARY_FILENAME)  # store the dictionary, for future reference
        corpus = [dictionary.doc2bow(text) for text in texts]
        logging.info("Created {} bags of words".format(len(corpus)))

        corpora.MmCorpus.serialize(self.model_dir+CORPUS_FILENAME, corpus)
        return corpus, dictionary

    def create_model(self, corpus, dictionary):

        tfidf = models.TfidfModel(corpus)  # step 1 -- initialize a model
        logging.info("Tfidf initialized with {} docs ".format(tfidf.num_docs))

        corpus_tfidf = tfidf[corpus]
        lsi = models.LsiModel(corpus_tfidf, num_topics=self.num_topics, id2word=dictionary, chunksize=70000)  # initialize an LSI transformation
        corpus_lsi = lsi[corpus_tfidf]  # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi

        lsi.save(self.model_dir+'/'+LSI_FILENAME)  # same for tfidf, lda, ...
        return lsi

    def create_matrix(self, lsi, corpus):
        index = similarities.MatrixSimilarity(lsi[corpus])  # transform corpus to LSI space and index it
        logging.info("Similarity Matrix Length : {} ".format(len(index)))

        index.save(self.model_dir+'/'+INDEX_FILENAME)

    def load_models(self):
        self.dictionary = corpora.Dictionary.load(self.model_dir + '/' + DICTIONARY_FILENAME)  # store the dictionary, for future reference
        self.corpus = MmCorpus(self.model_dir + '/' + CORPUS_FILENAME)
        self.tfidf = models.TfidfModel(self.corpus)
        self.lsi = models.LsiModel.load(self.model_dir + '/' + LSI_FILENAME)
        self.id2word = self.lsi.id2word
        self.index = similarities.MatrixSimilarity.load(self.model_dir + '/' + INDEX_FILENAME)

    def get_vec_from_tokenized(self, tokenized_doc):
        vec_bow = self.dictionary.doc2bow(tokenized_doc)
        vec_lsi = self.lsi[vec_bow]  # convert the query to LSI space
        return vec_lsi

    def get_doc_bow(self, tokenized_doc):
        vec_bow = self.dictionary.doc2bow(tokenized_doc)
        return vec_bow

    def get_vec_docid(self, id):
        vec_bow = self.corpus[id]
        vec_lsi = self.lsi[vec_bow]  # convert the query to LSI space
        return vec_lsi

    def get_scores_from_vec(self, vec_lsi):
        scores = self.index[vec_lsi]
        args_scores = np.argsort(-scores)

        return list(zip(args_scores, scores[args_scores]))