from .Util.Util import extract_any, extract_all, safe_remove
from . import FormKeepers
import random


class WordList():
    
    parts_of_speech = {
        'сущ': (FormKeepers.NumFormKeeper, FormKeepers.CaseFormKeeper),
        'пр': (FormKeepers.NumFormKeeper, FormKeepers.GenderFormKeeper),
        'гл': (FormKeepers.GenderFormKeeper, FormKeepers.NumFormKeeper, FormKeepers.PersonFormKeeper, FormKeepers.TimeFormKeeper),
        'нар': (),
        None: ()
    }

    word_types = ('безл.', 'нескл.')

    word_traits = ('абр', 'пинг', 'перс', 'сов.', 'несов.')

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
        keepers = list(self.parts_of_speech[extract_any(tags, *self.parts_of_speech.keys())])

        types = extract_all(tags, *self.word_types, to_pop=True)
        for word_type in types:
            match word_type:
                case 'безл.':
                    tags.extend('м.р.', 'ж.р.')
                case 'нескл.':
                    safe_remove(keepers, FormKeepers.CaseFormKeeper)
                    safe_remove(keepers, FormKeepers.NumFormKeeper)

        traits = extract_all(tags, *self.word_traits, to_pop=False)
        for trait in traits:
            match trait:
                case 'абр':
                    keepers.clear()
                case 'пинг':
                    keepers.clear()
                case 'перс':
                    safe_remove(keepers, FormKeepers.NumFormKeeper)
                case 'сов.':
                    safe_remove(keepers, FormKeepers.TimeFormKeeper)
                    keepers.append(FormKeepers.PerfectTimeFormKeeper)
                case 'несов.':
                    safe_remove(keepers, FormKeepers.TimeFormKeeper)
                    keepers.append(FormKeepers.ImperfectTimeFormKeeper)

        if len(keepers) == 0:
            self.forms[name] = name
        else:
            forms = keepers[0]()
            for keeper in keepers[1:]:
                forms.split(keeper)
            print('Введите для каждой формы корректное слово:')
            forms.settle(key=name)
            self.forms[name] = forms

        self.tags[name] = tags