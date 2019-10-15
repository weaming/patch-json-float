import operator
from decimal import Decimal
from functools import wraps, partial
import json
import builtins

builtins_float = float
version = '0.1'


def to_decimal(fn):
    """
    parse to Decimal before every float operations
    """

    @wraps(fn)
    def _(self, other):
        return float(
            getattr(operator, fn.__name__)(Decimal(str(self)), Decimal(str(other)))
        )

    return _


class Float(builtins_float):
    """
    failed on following:
        builtins_float.__instancecheck__ = Float.__instancecheck__
        import builtins; builtins.__dict__.__getitem__ = something
    """

    __class__ = builtins_float

    for name in ['add', 'mul', 'mod', 'truediv', 'divmod', 'floordiv', 'pow', 'sub']:
        for x in ['', 'r']:
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


def test_json_loads():
    data = {'a': 0.1, 'b': 0.2, 'c': 0.3}

    def test_data(data):
        ab = data['a'] + data['b']
        c = data['c']
        print(ab == c, ab, c, type(data['a']))

    test_data(data)
    test_data(json.loads(json.dumps(data)))


def test_float():
    estr_list = [
        '(builtins_float, float, Float)',
        (
            '(type(0.1), type(float(0.1)), isinstance(0.1, float), '
            'isinstance(float(0.1), float), isinstance(float(0.1), float), )'
        ),
    ]
    for estr in estr_list:
        print('==>', estr, '->', eval(estr))
