import inspect
from inspect import Parameter
import re
from typing import Union, List
from functools import partial

def _make_signature(fields: list):

    return inspect.Signature(
        Parameter(x, Parameter.POSITIONAL_OR_KEYWORD)
        for x in fields
        )


class Descriptor():
    ty = object


    def __init__(self, name=None):

        # Set in the metaclass and can be passed in __init__
        self.name = name
        self.value = None


    def __set__(self, instance, value):

        if not isinstance(value, self.ty):
            raise ValueError(f'Expected {self.ty}, got {type(value)}')

        instance.__dict__[self.name] = value


    @classmethod
    def gen_value(cls):

        if isinstance(cls.ty, tuple):
            ty = cls.ty[0]
            return ty()

        return cls.ty()


    def __repr__(self):

        return f'{self.__class__.__qualname__}()'


class Float(Descriptor):
    ty = (int, float)


class Integer(Descriptor):
    ty = int


class String(Descriptor):
    ty = str

    def __init__(self, *args, minsize: int=0, regex: str=None, maxsize: int=None, **kwargs):

        self.minsize = minsize
        self.maxsize = maxsize
        self.regex = regex
        super().__init__(*args, **kwargs)


    def __set__(self, instance, value: str):

        if self.maxsize is not None:

            if len(value) > self.maxsize:

                raise ValueError('Size is too big.')

        if len(value) < self.minsize:
            raise ValueError('Size is too small.')

        if self.regex is not None:
            if re.match(self.regex, value) is None:
                raise ValueError('Invalid string.')

        super().__set__(instance, value)


    def __repr__(self):

        return f'{self.__class__.__qualname__}(minsize={self.minsize}, maxsize={self.maxsize}, regex={self.regex!r})'


class Array(Descriptor):

    ty = (list, tuple)


    def __init__(self, type: Union[Descriptor, 'Schema'], minsize=0, maxsize=None):

        self.type = type
        self.minsize = minsize
        self.maxsize = maxsize


    def __set__(self, instance, value):

        if not isinstance(value, self.ty):
            raise TypeError(f'Expected {self.ty}, got {type(value)}.')

        if self.maxsize is not None:
            if len(value) > self.maxsize:
                raise ValueError('Value length is too long.')

        if len(value) < self.minsize:
            raise ValueError('Value is too small.')

        for val in value:

            if isinstance(val, dict):
                self.type(**val)
            else:
                self.type(val)


    def __repr__(self):

        return f'{self.__class__.__qualname__}(type={self.type.__qualname__}, minsize={self.minsize}, maxsize={self.maxsize})'


class Boolean(Descriptor):
    ty = bool


class MetaSchema(type):

    def __new__(cls, name: str, bases: tuple, clsdict: dict):

        _fields = []
        for name, value in clsdict.items():

            if not isinstance(value, Descriptor):
                continue

            value: Descriptor
            value.name = name
            clsdict[name] = value
            _fields.append(name)

        clsdict['_fields'] = _fields
        clsdict['__signature__'] = _make_signature(_fields)

        return super().__new__(cls, name, bases, clsdict)


    def __repr__(cls):

        fields: List[str] = cls._fields

        reprs = []
        for field in sorted(fields):

            value = getattr(cls, field)

            r = '\t'.expandtabs(4) + f'{field} : {value}'
            reprs.append(r)


        return '{\n' + ',\n'.join(reprs) + '\n}'


class Schema(metaclass=MetaSchema):
    """
    The `Schema` class is a base class that
    can be inherited to define class-based
    json validation schemes.
    """

    _fields: List[str]
    __signature__: inspect.Signature

    def __init__(self, *args, **kwargs):

        bound = self.__signature__.bind(*args, **kwargs)

        for name, value in bound.arguments.items():
            setattr(self, name, value)


    @classmethod
    def validate(cls, json: dict):

        try:
            cls(**json)
            return True

        except (ValueError, TypeError):
            return False


Date = partial(String, regex='\d{4}-\d{2}-\d{2}')
