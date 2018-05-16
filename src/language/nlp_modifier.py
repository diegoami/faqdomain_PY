from .custom_words import remove_words
from .custom_stopwords import add_stop_words
from .custom_lemmas import CUSTOM_REMOVES, CUSTOM_LOOKUP
import spacy

class NlpWrapper():

    def __init__(self):
        self.nlp = spacy.load('de')
        self.modify()

    def __call__(self, text):
        return self.nlp(text)

    def modify(self):
        remove_words(self.nlp)
        map(self.nlp.Defaults.lemma_lookup.pop, CUSTOM_REMOVES)

        self.nlp.Defaults.lemma_lookup.update(CUSTOM_LOOKUP)
        add_stop_words(self.nlp)

    def retrieve_forms_for_lemma(self, lemma_to_find):
        all_forms = set()
        all_forms.add(lemma_to_find)
        for form, lemma in self.nlp.Defaults.lemma_lookup.items():
            if lemma.lower() == lemma_to_find.lower():
                all_forms.add(form)
                if (lemma != lemma.lower()):
                    all_forms.add(lemma)
        return all_forms