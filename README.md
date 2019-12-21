# Patch Python `float`

A wrapper `Float` for `float` which will convert `float` to `decimal.Decimal` for every math calculation operations. No more `0.1 + 0.2 != 0.3` :smile:

## Example

```python
>>> import json
>>> from decimal import Decimal
>>> from patch_float import builtins_float, Float, patch_json_loads, patch_float_all
>>> (builtins_float, float, Float)
(<class 'float'>, <class 'float'>, <class 'patch_float.Float'>)
>>> (type(0.1), type(float(0.1)), type(json.loads('{"a": 0.1}')['a']))
(<class 'float'>, <class 'float'>, <class 'float'>)
>>> patch_float_all()
==> WARNING: patched builtins float
>>> (type(0.1), type(float(0.1)), type(json.loads('{"a": 0.1}')['a']))
(<class 'float'>, <class 'patch_float.Float'>, <class 'patch_float.Float'>)
```
