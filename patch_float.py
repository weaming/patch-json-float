import operator
from decimal import Decimal
from functools import wraps, partial
import json
import builtins

builtins_float = float
version = '0.4'


def to_decimal(fn):
    """
    parse to Decimal before every float operations
    """

    @wraps(fn)
    def _(self, other):
        op = getattr(operator, fn.__name__, None)
        if not op:
            # replace with lambda
            if '__r' in fn.__name__:
                _op = getattr(operator, fn.__name__.replace('__r', '__'), None)
                if _op:
                    op = lambda x, y: _op(y, x)
        if not op:
            raise NotImplementedError
        return Float(op(Decimal(str(self)), Decimal(str(other))))

    return _


class Float(builtins_float):
    """
    failed on following:
        builtins_float.__instancecheck__ = Float.__instancecheck__
        import builtins; builtins.__dict__.__getitem__ = something
    """

    __class__ = builtins_float

    for name in ['add', 'mul', 'mod', 'truediv', 'divmod', 'floordiv', 'pow', 'sub']:
        for x in ['', 'r', 'i']:
            real_name = f'__{x}{name}__'
            if hasattr(builtins_float, real_name):
                locals()[real_name] = to_decimal(getattr(builtins_float, real_name))


def patch_float():
    if builtins.__dict__['float'] == Float:
        return

    builtins.__dict__['float'] = Float
    print('==> WARNING: patched builtins float')


def patch_json_loads():
    json.loads = partial(json.loads, parse_float=Float)


def patch_float_all():
    patch_float()
    patch_json_loads()
