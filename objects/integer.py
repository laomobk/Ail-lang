# Integer
from core import aobjects as obj
from core.error import AILRuntimeError
from . import float as afloat, types
import objects.bool as abool

POOL_RANGE = (-1, 0)


def int_str(self :obj.AILObject):
    return '%d' % self['__value__']


def int_repr(self):
    return '< %d >' % self['__value__']


def int_init(self :obj.AILObject, value :obj.AILObject):
    if isinstance(value, int):
        self['__value__'] = value
    elif isinstance(value, float):
        o = obj.ObjectCreater.new_object(afloat.FLOAT_TYPE, value)
        self.reference = o.reference
        self.properties = o.properties
    elif obj.compare_type(value, INTEGER_TYPE):
        self['__value__'] = value['__value__']
    else:
        return AILRuntimeError('invalid number type \'%s\'' % type(value), 'TypeError')


def int_add(self :obj.AILObject, other :obj.AILObject) -> obj.AILObject:
    if other['__class__'] not in (INTEGER_TYPE, afloat.FLOAT_TYPE):   # do not have __value__ property
        return AILRuntimeError('Not support \'+\' with type %s' % other['__class__'].name, 'TypeError')

    sv = self['__value__']
    so = other['__value__']

    try:
        res = sv + so
    except Exception as e:
        return AILRuntimeError(str(e), 'PythonRuntimeError')

    if res in range(*POOL_RANGE):
        return INTEGER_POOL[int(abs(POOL_RANGE[0]) + res)]
    return obj.ObjectCreater.new_object(INTEGER_TYPE, res)


def int_sub(self :obj.AILObject, other :obj.AILObject) -> obj.AILObject:
    if other['__value__'] is None:   # do not have __value__ property
        return AILRuntimeError('Not support \'-\' with type %s' % str(other), 'TypeError')

    sv = self['__value__']
    so = other['__value__']

    try:
        res = sv - so
    except Exception as e:
        return AILRuntimeError(str(e), 'PythonRuntimeError')

    if res in range(*POOL_RANGE):
        return INTEGER_POOL[int(abs(POOL_RANGE[0]) + res)]
    return obj.ObjectCreater.new_object(INTEGER_TYPE, res)


def int_div(self :obj.AILObject, other :obj.AILObject) -> obj.AILObject:
    if other['__value__'] is None:   # do not have __value__ property
        return AILRuntimeError('Not support \'/\' with type %s' % str(other), 'TypeError')

    if other['__value__'] == 0:
        return AILRuntimeError('0 cannot be used as a divisor', 'ZeroDivisonError')

    sv = self['__value__']
    so = other['__value__']

    try:
        res = sv / so
    except Exception as e:
        return AILRuntimeError(str(e), 'PythonRuntimeError')

    return obj.ObjectCreater.new_object(afloat.FLOAT_TYPE, res)


def int_muit(self :obj.AILObject, other :obj.AILObject) -> obj.AILObject:
    if other['__value__'] is None:   # do not have __value__ property
        return AILRuntimeError('Not support \'*\' with type %s' % str(other), 'TypeError')

    sv = self['__value__']
    so = other['__value__']

    try:
        res = sv * so
    except Exception as e:
        return AILRuntimeError(str(e), 'PythonRuntimeError')

    if res in range(*POOL_RANGE):
        return INTEGER_POOL[int(abs(POOL_RANGE[0]) + res)]
    return obj.ObjectCreater.new_object(INTEGER_TYPE, res)


def int_mod(self :obj.AILObject, other :obj.AILObject) -> obj.AILObject:
    if other['__value__'] is None:   # do not have __value__ property
        return AILRuntimeError('Not support \'*\' with type %s' % str(other), 'TypeError')

    sv = self['__value__']
    so = other['__value__']

    try:
        res = sv % so
    except Exception as e:
        return AILRuntimeError(str(e), 'PythonRuntimeError')

    if res in range(*POOL_RANGE):
        return INTEGER_POOL[int(abs(POOL_RANGE[0]) + res)]
    return obj.ObjectCreater.new_object(INTEGER_TYPE, res)


def int_pow(self :obj.AILObject, other :obj.AILObject) -> obj.AILObject:
    if other['__value__'] is None:   # do not have __value__ property
        return AILRuntimeError('Not support \'*\' with type %s' % str(other), 'TypeError')

    sv = self['__value__']
    so = other['__value__']

    try:
        res = sv ** so
    except Exception as e:
        return AILRuntimeError(str(e), 'PythonRuntimeError')

    if res in range(*POOL_RANGE):
        return INTEGER_POOL[int(abs(POOL_RANGE[0]) + res)]
    return obj.ObjectCreater.new_object(INTEGER_TYPE, res)


def int_eq(self :obj.AILObject, o :obj.AILObject):
    if isinstance(o, obj.AILObject):
        return obj.ObjectCreater.new_object(abool.BOOL_TYPE, self['__value__'] == o['__value__'])
    return obj.ObjectCreater.new_object(abool.BOOL_TYPE, self['__value__'] == o)


def int_to_string(self):
   return str(self)


INTEGER_TYPE = obj.AILObjectType('<AIL integer type>', types.I_INT_TYPE,
                             methods={'to_string' : int_to_string},
                             __init__=int_init,
                             __add__=int_add,
                             __str__=int_str,
                             __div__=int_div,
                             __muit__=int_muit,
                             __sub__=int_sub,
                             __eq__=int_eq,
                             __repr__=int_repr,
                             __mod__=int_mod,
                             __pow__=int_pow
                             )


class _IntegerPool:
    def __init__(self):
        self.__pool = list()

        self.__init_pool()

    def __init_pool(self):
        mi, ma = POOL_RANGE

        for num in range(mi, ma):
            num = obj.ObjectCreater.new_object(INTEGER_TYPE, num)
            num.reference += 1
            self.__pool.append(num)

    @property
    def pool(self):
        return self.__pool


INTEGER_POOL = _IntegerPool().pool


def convert_to_integer(pyint :int):
    from objects import string

    try:
        if pyint['__class__'] in (
                INTEGER_TYPE, afloat.FLOAT_TYPE, string.STRING_TYPE):
                pyint['__value__'] = int(pyint['__value__'])
                return pyint

        elif type(pyint) in (int, float, str):
                return obj.ObjectCreater.new_object(INTEGER_TYPE, int(pyint))

    except ValueError as e:
        return AILRuntimeError(str(e), 'ValueError')

    return AILRuntimeError('argument must be a string or a number', 'TypeError')
