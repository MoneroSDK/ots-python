"""
OTS (Open Transaction Signing) Python Wrapper Library

This library provides a Python interface to the OTS library, enabling secure and offline transaction signing for Monero.

.. highlight:: python

To use this library via classes similar to the C++ API, you can import the necessary components as follows:

.. code-block::

    from ots import *
    print(f'OTS version: {Ots.version()}')
    SeedLanguage.setDefault(SeedLanguage.fromCode('en'), SeedType.POLYSEED)
    languages = SeedLanguage.list()
    for lang in languages:
        print(f"Language: {lang.name}, Code: {lang.code}, default: {'yes' if lang.isDefault(SeedType.POLYSEED) else 'no'}")


Or simply import only what is needed:

.. code-block::

    from ots import SeedLanguage, SeedType, Ots
    print(f'OTS version: {Ots.version()}')
    SeedLanguage.setDefault(SeedLanguage.fromCode('en'), SeedType.POLYSEED)
    languages = SeedLanguage.list()
    for lang in languages:
        print(f"Language: {lang.name}, Code: {lang.code}, default: {'yes' if lang.isDefault(SeedType.POLYSEED) else 'no'}")


To use the OTS library procedurally (not yet implemented):

.. code-block::

    from ots.procedural import *
    print(version())


Or better:

.. code-block::

    import procedural from ots as otsp
    print(otsp.version())


To use the OTS library almost raw like the C ABI:

.. code-block::

    from ots import raw as otsr
    result: ots_result_t = otsr.ots_version()
    if ots_is_error(result):
        print(f'Error: {otsr.ots_error_message(result)}')
    if ots_result_is_string(result):
        print(f'OTS version: {otsr.ots_result_string(result)}')
    del result  # Free the result


And to be completely raw:
.. code-block::

    from ots._ots import ffi, lib
    result: _CDataBase = ffi.new('ots_result_t **')
    result[0] = lib.ots_version()
    if lib.ots_is_error(result):
        print(f'Error: {ffi.string(lib.ots_error_message(result)).decode('utf-8')}')
    if lib.ots_result_is_string(result):
        print(f'OTS version: {ffi.string(lib.ots_result_string(result)).decode('utf-8')}')
    lib.ots_free_result(result)
    del result
"""
from os import environ
from hashlib import sha256
VERSION = '0.1.0'
environ['PYTHONHASHSEED'] = sha256(f'Monero OTS {VERSION}'.encode('utf-8')).hexdigest()
from .constants import *
from .enums import *
from .exceptions import OtsException
from .seed_indices import SeedIndices
from .seed_language import SeedLanguage
from .address import Address, AddressString
# from .seed import *
from .transaction import TxDescription, TxWarning
from .wallet import Wallet
from .seed_jar import SeedJar, SeedJarItem, Seed, MoneroSeed, Polyseed
from .ots import Ots
