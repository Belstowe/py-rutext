from contextlib import suppress


def extract_any(self: list, *args, to_pop=False, if_none=None):
    for to_get in args:
        for from_list in self:
            if to_get == from_list:
                if to_pop:
                    self.remove(from_list)
                return to_get
    
    return if_none


def extract_all(self: list, *args, to_pop=False):
    to_return = []
    
    for to_get in args:
        for from_list in self:
            if to_get == from_list:
                if to_pop:
                    self.remove(from_list)
                to_return.append(to_get)
    
    return to_return


def visit(self: dict, visitor, path=() ):
    for key, value in self:
        if type(value) != self:
            visitor(path, self)
        else:
            visit(value, visitor, path + (key, ))


def safe_remove(self: list, elem):
    with suppress(ValueError, AttributeError):
        self.remove(elem)