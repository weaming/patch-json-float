import json
from decimal import Decimal
from patch_float import builtins_float, Float, patch_json_loads, patch_float_all
import pytest


def test_Float():
    a = 0.1
    b = 0.2
    c = 0.3
    assert a + b != c
    assert Float(a) + b == c
    assert a + Float(b) == c
    assert Decimal(a) + Float(b) == c


def test_cli_examples():
    estr_list = [
        '(builtins_float, float, Float)',
        '''(type(0.1), type(float(0.1)), type(json.loads('{"a": 0.1}')['a']))''',
        'patch_float_all()',
        '''(type(0.1), type(float(0.1)), type(json.loads('{"a": 0.1}')['a']))''',
    ]
    print()
    for estr in estr_list:
        print('>>>', estr)
        print(eval(estr))


def test_json_loads():
    data = {'a': 0.1, 'b': 0.2, 'c': 0.3}

    def test_data(data):
        ab = data['a'] + data['b']
        c = data['c']
        assert ab == c, (ab, c, type(data['a']))

    with pytest.raises(AssertionError):
        test_data(data)

    patch_json_loads()
    reloaded = json.loads(json.dumps(data))
    assert type(reloaded['a']) is Float
    test_data(reloaded)
