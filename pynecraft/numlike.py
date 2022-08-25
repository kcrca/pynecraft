class numlike:
    def __init__(self, value: float = None):
        if value is not None:
            raise ValueError('Should not pass float to numlike.__init__')

    def extracter(self, *args, **kwargs):
        pass

    def factory(self, value: float):
        return self.__class__(value)

    def __float__(self):
        raise ValueError('Should not use numlike.__float__: provide your own')

    def __add__(self, other):
        other = float(other)
        return self.__class__(float(self) + float(other))

    def __neg__(self):
        return self.__class__(-float(self))

    def __sub__(self, other):
        return self + -other


class Foo(numlike):
    def __init__(self, v):
        super().__init__()
        self.v = float(v)

    def __float__(self):
        return self.v

    def __str__(self):
        return f'|{self.v}|'


print(Foo(1) + 2.5)
print(Foo(1) - 2.5)
