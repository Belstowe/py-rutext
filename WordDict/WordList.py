from .Util.Util import extract_all
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
        tags = list(args)

        forms = extract_all(tags, 'ед.ч.', 'мн.ч.', 'и.п.', 'р.п.', 'д.п.', 'в.п.', 'т.п.', 'п.п.', 'п.в.', 'н.в.', 'б.в.', '1л', '2л', '3л', to_pop=True)

        if 'гл.' in args:
            forms.extend(extract_all(tags, 'инф.', 'пов.', 'м.р.', 'с.р.', 'ж.р.', to_pop=True))

        tag_correlations = tuple(filter(lambda word_tags: all(tag in word_tags[1] for tag in tags), self.tags.items())) if len(tags) > 0 else tuple(self.tags.items())

        if len(tag_correlations) == 0:
            return

        word = random.choice(tag_correlations)[0]

        return self.forms[word].accept(*forms)


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
                    tags.append('нескл.')
                case 'перс':
                    tags.append('ед.ч.')

        print(f'Базовая форма слова: "{name}".')
        print('Часть речи: ', end='')
        if 'гл.' in tags: print('глагол.')
        elif 'пр.' in tags: print('прилагательное/причастие.')
        elif 'сущ.' in tags: print('существительное.')
        else: print('другое (наречие/деепричастие/...)')
        print(f'Теги: {tags}.')
        print('Продолжить? (любой символ, чтобы отменить) ', end='')
        if len(input()) != 0:
            return
        print()

        self.forms[name] = FormKeepers.BaseFormKeeper(name, *tags)
        self.tags[name] = tags