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
        
        if 'гл.' in tags:
            if 'сов.' not in tags and 'несов.' not in tags:
                print('!! Пожалуйста, укажите завершённость глагола: совершённый "сов." или несовершённый "несов."')
                return
        if 'сущ.' in tags:
            if 'м.р.' not in tags and 'с.р.' not in tags and 'ж.р.' not in tags:
                print('! Вы не указали род существительного (м.р.|с.р.|ж.р.|безл.).\n  Выборка в тексте в основном требует род, что значит, ваше слово практически не будет показываться.')
        if len(name.split()) > 1:
            print('! Крайне не рекомендуем добавлять словосочетания.')
        if len(tags) == 0:
            print('! Теги добавляются при вводе. Например, "любить гл. несов."; "человек сущ. м.р."')

        print('Продолжить? (пустой ввод, если да) ', end='')
        if len(input()) != 0:
            return
        print()

        self.forms[name] = FormKeepers.BaseFormKeeper(name, *tags)
        self.tags[name] = tags