from .Util.Util import extract_any, extract_all
from . import FormKeepers
import random


class WordList():

    word_types = ('безл.')

    word_traits = ('абр', 'пинг', 'перс')

    def __init__(self):
        self.forms = dict()
        self.tags = dict()

    def delete(self, *args):
        for name in args:
            del self.forms[name]
            del self.tags[name]
    
    def get(self, *args):
        tag_correlations = list(
            filter(lambda word_tags: all(tag in args for tag in word_tags[1]),
                   self.tags.items())
        )
        return random.choice(tag_correlations)

    def insert(self, name, tags):
        types = extract_all(tags, *self.word_types, to_pop=True)
        for word_type in types:
            match word_type:
                case 'безл.':
                    tags.extend('м.р.', 'ж.р.')

        traits = extract_all(tags, *self.word_traits, to_pop=False)
        for word_trait in traits:
            match word_trait:
                case 'абр' | 'пинг':
                    tags.extend('нескл.')
                case 'перс':
                    tags.extend('ед.ч.')

        self.forms[name] = FormKeepers.BaseFormKeeper(name, *tags)
        self.tags[name] = tags