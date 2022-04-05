from .Util.Util import extract_any, extract_all


class FormKeeper():
    def __init__(self):
        self.rooms = {}
        self.default_key = 'DEFAULT'

    def ask(self, word: str, path=()):
        print(path[0], end='')
        for dir in path[1:]:
            print(f', {dir}', end='')
        print(f' для слова "{word}": ', end='')
        return input()

    def accept(self, *args):
        for key, value in self.rooms.values():
            if key in args:
                if type(value) is str:
                    return value
                return value.accept(args)

        value = self.rooms[self.default_key]
        if type(value) is str:
            return value
        return value.accept(args)


class BaseFormKeeper(FormKeeper):
    def __init__(self, word: str, *args, path=()):
        super().__init__()
        
        if 'гл.' in args:
            if 'сов.' not in args and 'несов.' not in args:
                print('Пожалуйста, укажите завершённость глагола: совершенный "сов." или несовершённый "несов."')
                return

            self.rooms['инф.'] = word
            self.rooms['пов.'] = VerbImperativeFormKeeper(word, path=path + ('Повелительное наклонение', ))
            self.rooms[self.default_key] = VerbConjugableFormKeeper(word, args, path=path)
        elif 'сущ.' in args:
            if 'нескл.' in args:
                self.rooms[self.default_key] = word
            else:
                self.rooms[self.default_key] = NounDeclinedFormKeeper(word, args, path=path)
        elif 'пр.' in args:
            # self.default_key = 'ед.ч.'
            # self.rooms['ед.ч.'] = AdjSingularFormKeeper(word, args, path=path + ('Единственное число', ))
            # self.rooms['мн.ч.'] = AdjPluralFormKeeper(word, args, path=path + ('Множественное число', ))
            self.rooms[self.default_key] = NounDeclinedFormKeeper(word, args, path=path)
        else:
            self.rooms[self.default_key] = word


class VerbImperativeFormKeeper(FormKeeper):
    def __init__(self, word: str, *, path=()):
        super().__init__()
        
        imperative_form = self.ask(word, path, )
        self.rooms[self.default_key] = imperative_form
        self.rooms['мн.ч.'] = imperative_form + 'те'


class VerbConjugableFormKeeper(FormKeeper):
    def __init__(self, word: str, *args, path=()):
        super().__init__()

        self.rooms[self.default_key] = word

        self.rooms['п.в.'] = VerbPastTimeFormKeeper(word, path=path + ('Прошедшее время', ))
        self.rooms['б.в.'] = VerbTimeFormKeeper(word, args, path=path + ('Будущее время', ))
        if 'несов.' in args:
            self.rooms['н.в.'] = VerbTimeFormKeeper(word, args, path=path + ('Настоящее время', ))


class VerbPastTimeFormKeeper(FormKeeper):
    def __init__(self, word: str, *, path=()):
        super().__init__()

        standard_form = self.ask(word, path)

        self.rooms['м.р.'] = standard_form
        if standard_form[-1] != 'л':
            standard_form = standard_form + 'л'
        self.rooms['ж.р.'] = standard_form + 'а'
        self.rooms['с.р.'] = standard_form + 'о'
        self.rooms['мн.ч.'] = standard_form + 'и'


class VerbTimeFormKeeper(FormKeeper):
    def __init__(self, word: str, *args, path=()):
        super().__init__()

        self.rooms[self.default_key] = word
        
        self.rooms['1л'] = VerbPersonFormKeeper(word, args, path=path + ('первое лицо', ))
        self.rooms['2л'] = VerbPersonFormKeeper(word, args, path=path + ('второе лицо', ))
        self.rooms['3л'] = VerbPersonFormKeeper(word, args, path=path + ('третье лицо', ))


class VerbPersonFormKeeper(FormKeeper):
    def __init__(self, word: str, *args, path=()):
        super().__init__()

        self.rooms[self.default_key] = word

        if 'несов.' in args and 'Будущее время' in path:
            if 'первое лицо' in path:
                self.rooms['ед.ч.'] = 'буду ' + word
                self.rooms['мн.ч.'] = 'будем ' + word
                return
            if 'второе лицо' in path:
                self.rooms['ед.ч.'] = 'будешь ' + word
                self.rooms['мн.ч.'] = 'будете ' + word
                return
            if 'третье лицо' in path:
                self.rooms['ед.ч.'] = 'будет ' + word
                self.rooms['мн.ч.'] = 'будут ' + word
                return

        self.rooms['ед.ч.'] = self.ask(word, path + ('единственное число', ))
        self.rooms['мн.ч.'] = self.ask(word, path + ('множественное число', ))


class NounDeclinedFormKeeper(FormKeeper):
    def __init__(self, word: str, *args, path=()):
        super().__init__()

        self.default_key = 'и.п.'

        self.rooms['и.п.'] = NounCaseFormKeeper(word, args, path=path + ('Именительный падеж', ))
        self.rooms['р.п.'] = NounCaseFormKeeper(word, args, path=path + ('Родительный падеж', ))
        self.rooms['д.п.'] = NounCaseFormKeeper(word, args, path=path + ('Дательный падеж', ))
        self.rooms['в.п.'] = NounCaseFormKeeper(word, args, path=path + ('Винительный падеж', ))
        self.rooms['т.п.'] = NounCaseFormKeeper(word, args, path=path + ('Творительный падеж', ))
        self.rooms['п.п.'] = NounCaseFormKeeper(word, args, path=path + ('Предложный падеж', ))


class NounCaseFormKeeper(FormKeeper):
    def __init__(self, word: str, *args, path=()):
        super().__init__()

        self.default_key = 'ед.ч.' if 'мн.ч.' not in args else 'мн.ч.'

        if 'ед.ч.' in args:
            self.rooms['ед.ч.'] = word if 'Именительный падеж' in path else self.ask(word, path)
        elif 'мн.ч.' in args:
            self.rooms['мн.ч.'] = word if 'Именительный падеж' in path else self.ask(word, path)
        else:
            self.rooms['ед.ч.'] = word if 'Именительный падеж' in path else self.ask(word, path + ('единственное число', ))
            self.rooms['мн.ч.'] = self.ask(word, path + ('множественное число', ))