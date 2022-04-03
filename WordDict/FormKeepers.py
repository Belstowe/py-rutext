from .Util.Util import extract_any, extract_all


class BaseFormKeeper():
    rooms = ('', )
    default = rooms[0]
    name = ''

    def __init__(self):
        self.rooms_dict = dict()
        self.is_settled = False

    def split(self, keeper):
        if not self.is_settled:
            self.is_settled = True
            for room in self.rooms:
                self.rooms_dict[room] = keeper()
            return
        
        for _, holder in self.rooms_dict.items():
            holder.split(keeper)
    
    def inhabit(self, path = (), rooms = rooms, *, key: str):
        for room in rooms:
            for node in path:
                print(f'{node}/', end='')
            print(f'{room}: ', end='')
            self.rooms_dict[room] = input()

    def settle(self, path = (), *, key: str):
        if not self.is_settled:
            self.inhabit(path, key=key)
            return

        for room, holder in self.rooms_dict.items():
            holder.settle(path + (room, ), key=key)

    def struct(self, path = ()):
        if not self.is_settled:
            return path + (self.name, )

        return self.struct(self.rooms_dict[self.default], path + (self.name, ))

    def accept(self, *args, key: str):
        room = extract_any(args, *self.rooms, if_none=self.default)

        if not self.is_settled:
            return room

        return room.accept(args, key)


class NumFormKeeper(BaseFormKeeper):
    rooms = ('ед.ч.', 'мн.ч.')
    default = rooms[0]
    name = 'Число'


class CaseFormKeeper(BaseFormKeeper):
    rooms = ('и.п.', 'р.п.', 'д.п.', 'в.п.', 'т.п.', 'п.п.')
    default = rooms[0]
    name = 'Падеж'


class TimeFormKeeper(BaseFormKeeper):
    rooms = ('п.в.', 'н.в.', 'б.в.')
    default = rooms[1]
    name = 'Время'

    def accept(self, *args, key: str):
        if 'инф' in args:
            return key

        return super().accept(*args, key)


class PerfectTimeFormKeeper(TimeFormKeeper):
    rooms = ('п.в.', 'б.в.')
    default = rooms[0]
    name = 'Время'


class ImperfectTimeFormKeeper(TimeFormKeeper):
    rooms = ('п.в.', 'н.в.', 'б.в.')
    default = rooms[1]
    name = 'Время'
    
    def inhabit(self, path=(), rooms=list(rooms), *, key: str):
        if 'б.в.' in rooms:
            rooms.remove('б.в.')
            person_num_pair = extract_all(path, 'ед.ч.', 'мн.ч.', '1л', '2л', '3л')
            match person_num_pair:
                case ('ед.ч.', '1л'): self.rooms_dict['б.в.'] = 'буду ' + key
                case ('мн.ч.', '1л'): self.rooms_dict['б.в.'] = 'будем ' + key
                case ('ед.ч.', '2л'): self.rooms_dict['б.в.'] = 'будешь ' + key
                case ('мн.ч.', '2л'): self.rooms_dict['б.в.'] = 'будете ' + key
                case ('ед.ч.', '3л'): self.rooms_dict['б.в.'] = 'будет ' + key
                case ('мн.ч.', '3л'): self.rooms_dict['б.в.'] = 'будут ' + key

        super().inhabit(path, rooms, key=key)


class PersonFormKeeper(BaseFormKeeper):
    rooms = ('1л', '2л', '3л')
    default = rooms[2]
    name = 'Лицо'


class GenderFormKeeper(BaseFormKeeper):
    rooms = ('м.р.', 'ж.р.', 'с.р.')
    default = rooms[0]
    name = 'Род'