"""
OTS (Open Transaction Signing) Python Wrapper Library

This library provides a Python interface to the OTS library, enabling secure and offline transaction signing for Monero.

To use this library via classes similar to the C++ API, you can import the necessary components as follows:
```python
from ots import *
print(f'OTS version: {Ots.version()}')
SeedLanguage.setDefault(SeedLanguage.fromCode('en'), SeedType.POLYSEED)
languages = SeedLanguage.list()
for lang in languages:
    print(f"Language: {lang.name}, Code: {lang.code}, default: {'yes' if lang.isDefault(SeedType.POLYSEED) else 'no'}")
```

Or simply import only what is needed:
```
from ots import SeedLanguage, SeedType, Ots
print(f'OTS version: {Ots.version()}')
SeedLanguage.setDefault(SeedLanguage.fromCode('en'), SeedType.POLYSEED)
languages = SeedLanguage.list()
for lang in languages:
    print(f"Language: {lang.name}, Code: {lang.code}, default: {'yes' if lang.isDefault(SeedType.POLYSEED) else 'no'}")
```

To use the OTS library procedurally (not yet implemented):
```python
from ots.procedural import *
print(version())
```
Or better:
```Python
import procedural from ots as otsp
print(otsp.version())
```

To use the OTS library almost raw like the C ABI:
```python
from ots import raw as otsr
result: ots_result_t = otsr.ots_version()
if ots_is_error(result):
    print(f'Error: {otsr.ots_error_message(result)}')
if ots_result_is_string(result):
    print(f'OTS version: {otsr.ots_result_string(result)}')
del result  # Free the result
```

And to be completely raw:
```python
from ots._ots import ffi, lib
result: _CDataBase = ffi.new('ots_result_t **')
result[0] = lib.ots_version()
if lib.ots_is_error(result):
    print(f'Error: {ffi.string(lib.ots_error_message(result)).decode('utf-8')}')
if lib.ots_result_is_string(result):
    print(f'OTS version: {ffi.string(lib.ots_result_string(result)).decode('utf-8')}')
lib.ots_free_result(result)
del result
```
"""
from .constants import *
from .enums import *
from .exceptions import OtsException
from .seed_indices import SeedIndices
from .seed_language import SeedLanguage
from .address import Address, AddressString
from .seed import *
from .transaction import TxDescription, TxWarning
from .wallet import Wallet
from .seed_jar import SeedJar
from .ots import Ots
