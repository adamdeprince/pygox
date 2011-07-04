class DictToAttrRecord:
    MAPPER = {}
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            func = self.MAPPER.get(key, lambda x:x)
            if func is not None:
                setattr(self, key, func(value))

    def __cmp__(self, other):
        if isinstance(other, type(self)):
            return cmp(tuple(self.__me__()), tuple(other.__me__()))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        return isinstance(other, type(self)) and not self.__cmp__(other)
    
    def __hash__(self):
        return hash(tuple(self.__me__()))

class DictToAttrRecordOnlyFields:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key not in self.FIELDS: continue 
            func = self.MAPPER.get(key, lambda x:x)
            if func is not None:
                setattr(self, key, func(value))


