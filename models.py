import spacy
from summarizer import Summarizer


class Models:

    def __init__(self):
        self.summarizer_model = None

    def get_summarizer_model(self):
        if self.summarizer_model is None:
            nlp = spacy.load('en_core_web_md', disable=['ner', 'parser', 'tagger'])
            nlp.add_pipe(nlp.create_pipe('sentencizer'))
            self.summarizer_model = Summarizer()
        return self.summarizer_model


m = Models()


def get_summarizer_model():
    return m.get_summarizer_model()